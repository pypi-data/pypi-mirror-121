import os
import sys
import tempfile
import wasmtime
import platform
import click
import pathlib
import hashlib
import appdirs
import lzma
from importlib import resources as importlib_resources
try:
    importlib_resources.files # py3.9+ stdlib
except AttributeError:
    import importlib_resources # py3.8- shim


# ==============================
# Note on wasmtime path handling
# ==============================
#
# Hack: Right now, wasmtime's preopen_dir / --map functionality is completely borked. AFAICT only the first mapping is
# even considered, and preopening both / and . simply does not work: Either all paths open'ed by the executable must be
# absolute, or all paths must be relative. I spent some hours trying to track down where exactly this borkage originates
# from, but I found the code confusing and did not succeed.
# 
# FOR NOW we work around this issue the dumb way: We simply have click parse enough of the command line to transform any
# paths given on the command line to absolute paths. The actual path resolution is done by click because of
# resolve_path=True.
#
# This is not as ugly as it sounds since we have to do some command-line fuckery anyway: resvg/usvg's fontdb dependency
# bakes in the target OS'es system font paths (like /usr/share/fonts) at compile time, but we need to decide at runtime
# which paths to use.
# 


def _run_wasm_app(wasm_filename, argv, cachedir="resvg-wasi"):

    module_binary = importlib_resources.read_binary(__package__, wasm_filename)

    module_path_digest = hashlib.sha256(__file__.encode()).hexdigest()
    module_digest = hashlib.sha256(module_binary).hexdigest()
    cache_path = pathlib.Path(os.getenv("RESVG_WASI_CACHE_DIR", appdirs.user_cache_dir(cachedir)))
    cache_path.mkdir(parents=True, exist_ok=True)
    cache_filename = (cache_path / f'{wasm_filename}-{module_path_digest[:8]}-{module_digest[:16]}')
    
    wasi_cfg = wasmtime.WasiConfig()
    wasi_cfg.argv = argv
    wasi_cfg.preopen_dir('/', '/')
    wasi_cfg.inherit_stdin()
    wasi_cfg.inherit_stdout()
    wasi_cfg.inherit_stderr()
    engine = wasmtime.Engine()

    import time
    try:
        with cache_filename.open("rb") as cache_file:
            module = wasmtime.Module.deserialize(engine, lzma.decompress(cache_file.read()))
    except:
        print("Preparing to run {}. This might take a while...".format(argv[0]), file=sys.stderr)
        module = wasmtime.Module(engine, module_binary)
        with cache_filename.open("wb") as cache_file:
            cache_file.write(lzma.compress(module.serialize(), preset=0))

    linker = wasmtime.Linker(engine)
    linker.define_wasi()
    store = wasmtime.Store(engine)
    store.set_wasi(wasi_cfg)
    app = linker.instantiate(store, module)
    linker.define_instance(store, "app", app)

    try:
        app.exports(store)["_start"](store)
        return 0
    except wasmtime.ExitTrap as trap:
        return trap.code


def system_font_dirs():
    """ Generator yielding absolute paths of system font directories.

    Logic copied from fontdb/src/lib.rs where platforms are resolved at compile time.
    """

    sys = platform.system() 
    if sys == 'Windows':
        yield 'C:\\Windows\\Fonts\\'

    elif sys == 'Darwin':
        yield '/Library/Fonts'
        yield '/System/Library/Fonts'
        yield '/System/Library/AssetsV2/com_apple_MobileAsset_Font6'
        yield '/Network/Library/Fonts'
        if 'HOME' in os.environ:
            yield os.path.abspath(os.path.join(os.environ['HOME'], 'Library/Fonts'))

    else: # assume unix
        yield '/usr/share/fonts/'
        yield '/local/share/fonts/'
        if 'HOME' in os.environ:
            yield os.path.abspath(os.path.join(os.environ['HOME'], '.fonts'))
            yield os.path.abspath(os.path.join(os.environ['HOME'], '.local/share/fonts'))


@click.command(context_settings={'ignore_unknown_options': True})
@click.option('--resources-dir',                type=click.Path(resolve_path=True, file_okay=False))
@click.option('--use-font-file', multiple=True, type=click.Path(resolve_path=True, dir_okay=False))
@click.option('--use-fonts-dir', multiple=True, type=click.Path(resolve_path=True, file_okay=False))
@click.option('--skip-system-fonts', is_flag=True)
@click.argument('in_svg',                       type=click.Path(resolve_path=True, dir_okay=False))
@click.argument('out_svg',                      type=click.Path(resolve_path=True, dir_okay=False, writable=True))
@click.argument('usvg_args', nargs=-1, type=click.UNPROCESSED)
def run_usvg(resources_dir, use_font_file, use_fonts_dir, in_svg, skip_system_fonts, out_svg, usvg_args):

    cmdline = ['usvg', *usvg_args]

    for val in use_font_file:
        cmdline += ['--use-font-file', val]
    for val in use_fonts_dir:
        cmdline += ['--use-fonts-dir', val]
    if resources_dir:
        cmdline += ['--resources-dir', resources_dir]

    if not skip_system_fonts:
        for val in system_font_dirs():
            cmdline += ['--use-fonts-dir', val]

    cmdline += [in_svg, out_svg]
    sys.exit(_run_wasm_app("usvg.wasm", cmdline))

@click.command(context_settings={'ignore_unknown_options': True})
@click.option('--resources-dir',                type=click.Path(resolve_path=True, file_okay=False))
@click.option('--use-font-file', multiple=True, type=click.Path(resolve_path=True, dir_okay=False))
@click.option('--use-fonts-dir', multiple=True, type=click.Path(resolve_path=True, file_okay=False))
@click.option('--dump-svg',                     type=click.Path(resolve_path=True, dir_okay=False, writable=True))
@click.argument('in_svg',                       type=click.Path(resolve_path=True, dir_okay=False))
@click.argument('out_png',                      type=click.Path(resolve_path=True, dir_okay=False, writable=True))
@click.argument('resvg_args', nargs=-1, type=click.UNPROCESSED)
def run_resvg(resources_dir, use_font_file, use_fonts_dir, dump_svg, in_svg, out_png, resvg_args):

    cmdline = ['resvg', *resvg_args]

    for val in use_font_file:
        cmdline += ['--use-font-file', val]
    for val in use_fonts_dir:
        cmdline += ['--use-fonts-dir', val]
    if resources_dir:
        cmdline += ['--resources-dir', resources_dir]
    if dump_svg:
        cmdline += ['--dump-svg', dump_svg]

    if not skip_system_fonts:
        for val in system_font_dirs():
            cmdline += ['--use-fonts-dir', val]

    cmdline += [in_svg, out_png]
    sys.exit(_run_wasm_app("resvg.wasm", cmdline))

