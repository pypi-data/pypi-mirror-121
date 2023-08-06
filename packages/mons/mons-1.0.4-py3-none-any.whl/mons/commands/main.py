import click
from click import echo

import os
import subprocess
import io

from ..mons import cli, UserInfo, pass_userinfo
from ..utils import *
from ..clickExt import *


@cli.command(no_args_is_help=True)
@click.argument('name', type=Install(exist=False))
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
@click.option('--set-primary', is_flag=True, help='Set as default install for commands.')
@pass_userinfo
def add(userInfo: UserInfo, name, path, set_primary):
    '''Add a Celeste Install'''
    if os.path.basename(path) == 'Celeste.app':
        path = os.path.join(path, 'Resources')
    installPath = fileExistsInFolder(path, 'Celeste.exe', forceName=False, log=True)

    if installPath:
        userInfo.installs[name] = {
            'Path': installPath,
        }
        echo(f'Found Celeste.exe: {installPath}')
        echo('Caching install info...')
        echo(buildVersionString(getInstallInfo(userInfo, name)))
        if set_primary:
            userInfo.config['user']['PrimaryInstall'] = name
            echo(f'Primary install is now `{name}`.')


@cli.command()
@click.argument('name', type=Install())
@pass_userinfo
def set_primary(userInfo: UserInfo, name):
    '''Set the primary install used by commands'''
    userInfo.config['user']['PrimaryInstall'] = name
    echo(f'Primary install is now `{name}`.')


@cli.command(no_args_is_help=True)
@click.argument('old', type=Install(exist=True))
@click.argument('new', type=Install(exist=False))
@pass_userinfo
def rename(userInfo: UserInfo, old, new):
    '''Rename a Celeste install'''
    userInfo.installs[new] = userInfo.installs.pop(old)


@cli.command(no_args_is_help=True)
@click.argument('name', type=Install(check_path=False))
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
@pass_userinfo
def set_path(userInfo: UserInfo, name, path):
    '''Change the path of an existing install'''
    installPath = fileExistsInFolder(path, 'Celeste.exe', forceName=False, log=True)
    if installPath:
        userInfo.installs[name]['Path'] = installPath
        echo(f'Found Celeste.exe: {installPath}')
        echo(buildVersionString(getInstallInfo(userInfo, name)))


@cli.command(no_args_is_help=True, )
@click.argument('name', type=Install())
@pass_userinfo
def remove(userInfo: UserInfo, name):
    '''Remove an existing install'''
    if click.confirm('Are you sure?', abort=True):
        userInfo.installs.remove_section(name)
        userInfo.cache.remove_section(name)
        if userInfo.config.has_option('user', 'PrimaryInstall'):
            echo(f'Un-setting primary install (was {name}).')
            userInfo.config.remove_option('user', 'PrimaryInstall')


@cli.command(no_args_is_help=True)
@click.argument('name', type=Install(resolve_install=True))
@click.argument('branch')
def set_branch(name, branch):
    '''Set the preferred branch name for an existing install'''
    name['PreferredBranch'] = branch
    echo(f'Preferred branch for `{name.name}` is now `{branch}`.')


@cli.command()
@pass_userinfo
def list(userInfo: UserInfo):
    '''List existing installs'''
    primary = userInfo.config['user'].get('PrimaryInstall', fallback='')
    for install in userInfo.installs.sections():
        info = buildVersionString(getInstallInfo(userInfo, install))
        name = install + (' (primary)' if install == primary else '')
        echo('{}:\t{}'.format(name, info))


@cli.command()
@click.argument('name', type=Install(), required=False, callback=default_primary)
@click.option('-v', '--verbose', is_flag=True)
@pass_userinfo
def info(userInfo: UserInfo, name, verbose):
    '''Get information for a specific install'''
    info = getInstallInfo(userInfo, name)
    primary = name == userInfo.config['user'].get('PrimaryInstall', fallback='')
    if verbose:
        if primary:
            echo('--Primary install--')
        echo('\n'.join('{}:\t{}'.format(k, v) for k, v in info.items()))
    else:
        if primary:
            name = name + ' (primary)'
        echo('{}:\t{}'.format(name, buildVersionString(info)))


@cli.command(no_args_is_help=True, cls=CommandWithDefaultOptions)
@click.argument('name', type=Install(), required=False, callback=default_primary)
@click.argument('versionSpec', required=False)
@click.option('-v', '--verbose', is_flag=True, help='Be verbose.')
@click.option('--latest', is_flag=True, help='Install latest available build, branch-ignorant.')
@click.option('--zip', 
    type=click.Path(exists=True, dir_okay=False, resolve_path=True), 
    help='Install from local zip artifact.')
@click.option('--src',
    cls=ExplicitOption,
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help='Build and install from source folder.')
@click.option('--src', cls=DefaultOption, is_flag=True)
@click.option('--no-build', is_flag=True, help='Use with --src to install without building.')
@click.option('--launch', is_flag=True, help='Launch Celeste after installing.')
@pass_userinfo
def install(userinfo: UserInfo, name, versionspec, verbose, latest, zip, src, src_default, no_build, launch):
    '''Install Everest

    VERSIONSPEC can be a branch name, build number, or version number.'''
    path = userinfo.installs[name]['Path']
    installDir = os.path.dirname(path)
    success = False

    artifactPath = None
    build = None

    if src_default:
        src = userinfo.config.get('user', 'SourceDirectory', fallback=None)
        if not src:
            raise click.BadOptionUsage(
                '--src',
                '--src option passed with no path and no SourceDirectory set'
            )

    if src:
        build_success = 0 if no_build else 1
        if not no_build:
            if shutil.which('dotnet'):
                build_success = subprocess.run(
                    [
                        'dotnet', 'build',
                        '--verbosity', 'normal' if verbose else 'minimal'
                    ],
                    cwd=src
                ).returncode
            elif shutil.which('msbuild'):
                build_success = subprocess.run(
                    [
                        'msbuild',
                        '-verbosity:' + ('normal' if verbose else 'minimal')
                    ],
                    cwd=src
                ).returncode
            else:
                raise click.ClickException('Unable to build project: could not find `dotnet` or `msbuild` on PATH.\n' +
                'Include the --no-build switch to skip build step.')

        if build_success == 0:
            echo('Copying files...')
            copy_recursive_force(os.path.join(src, 'Celeste.Mod.mm', 'bin', 'Debug', 'net452'),
                installDir,
                ignore=lambda path, names : [name for name in names if isUnchanged(path, installDir, name)]
            )
            copy_recursive_force(os.path.join(src, 'MiniInstaller', 'bin', 'Debug', 'net452'),
                installDir,
                ignore=lambda path, names : [name for name in names if isUnchanged(path, installDir, name)]
            )
            success = True

    elif zip:
        artifactPath = zip
    elif versionspec and versionspec.startswith('file://'):
        artifactPath = versionspec[len('file://'):]

    if artifactPath:
        label = f'Unzipping {os.path.basename(artifactPath)}'
        with zipfile.ZipFile(artifactPath) as wrapper:
            try:
                entry = wrapper.open('olympus-build/build.zip') # Throws KeyError if not present
                with zipfile.ZipFile(entry) as artifact:
                    unpack(artifact, installDir, label=label)
                    success = True
            except KeyError:
                unpack(wrapper, installDir, 'main/', label=label)
                success = True

    elif not src:
        versionspec = '' if latest else (versionspec or userinfo.installs.get(name, 'PreferredBranch'))
        build = parseVersionSpec(versionspec)
        if not build:
            raise click.ClickException(f'Build number could not be retrieved for `{versionspec}`.')

        echo(f'Installing Everest build {build}')
        echo('Downloading build metadata...')
        try:
            meta = getBuildDownload(build, 'olympus-meta')
            with zipfile.ZipFile(io.BytesIO(meta.read())) as file:
                size = int(file.read('olympus-meta/size.txt').decode('utf-16'))
        except:
            size = 0

        if size > 0:
            echo('Downloading olympus-build.zip', nl=False)
            response = getBuildDownload(build, 'olympus-build')
            artifactPath = os.path.join(installDir, 'olympus-build.zip')
            echo(f' to file {artifactPath}')
            blocksize = max(4096, size//100)
            with open(artifactPath, 'wb') as file:
                with progressbar(length=size, label='Downloading') as bar:
                    while True:
                        buf = response.read(blocksize)
                        if not buf:
                            break
                        file.write(buf)
                        bar.update(len(buf))
                    bar.update(bar.length - bar.pos)
            with zipfile.ZipFile(artifactPath) as wrapper:
                with zipfile.ZipFile(wrapper.open('olympus-build/build.zip')) as artifact:
                    unpack(artifact, installDir, label='Extracting')
                    success = True

        else:
            echo('Downloading main.zip', nl=False)
            response = getBuildDownload(build, 'main')
            artifactPath = os.path.join(installDir, 'main.zip')
            echo(f' to file {artifactPath}')
            with open(artifactPath, 'wb') as file:
                file.write(response.read())
            echo('Unzipping main.zip')
            with zipfile.ZipFile(artifactPath) as artifact:
                unpack(artifact, installDir, 'main/', label='Extracting')
                success = True

    if success:
        echo('Running MiniInstaller...')
        stdout = None if verbose else subprocess.DEVNULL
        if os.name == 'nt':
            installer_ret = subprocess.run(os.path.join(installDir, 'MiniInstaller.exe'), stdout=stdout, stderr=None, cwd=installDir)
        else:
            uname = os.uname()
            if uname.sysname == 'Darwin':
                kickstart_dir = os.path.join(installDir, '..', 'MacOS')
                with copied_file(
                    os.path.join(kickstart_dir, 'Celeste'),
                    os.path.join(kickstart_dir, 'MiniInstaller')
                ) as miniinstaller:
                    installer_ret = subprocess.run(miniinstaller, stdout=stdout, stderr=None, cwd=installDir)
            else:
                suffix = 'x86_64' if uname.machine == 'x86_64' else 'x86'
                with copied_file(
                    os.path.join(os.path.join(installDir, f'Celeste.bin.{suffix}')),
                    os.path.join(installDir, f'MiniInstaller.bin.{suffix}')
                ) as miniinstaller:
                    installer_ret = subprocess.run(miniinstaller, stdout=stdout, stderr=None, cwd=installDir)

        if installer_ret.returncode == 0:
            echo('Install success')
            if build:
                peHash = getMD5Hash(path)
                userinfo.cache[name].update({
                    'Hash': peHash,
                    'Everest': str(True),
                    'EverestBuild': str(build),
                })
            else:
                getInstallInfo(userinfo, name)
                echo('Install info cached')
            if launch:
                echo('Launching Celeste...')
                subprocess.Popen(path)
            return

    # If we got this far, something went wrong
    click.get_current_context().exit(1)


@cli.command(
    cls=DefaultArgsCommand,
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ))
@click.argument('name', type=Install(), required=False, callback=default_primary)
@click.pass_context
def launch(ctx, name):
    '''Launch the game associated with an install'''
    path = ctx.obj.installs[name]['Path']
    if os.name != 'nt':
        if os.uname().sysname == 'Darwin':
            path = os.path.normpath(os.path.join(os.path.dirname(path), '..', 'MacOS', 'Celeste'))
        else:
            path = os.path.splitext(path)[0] # drop the .exe
    subprocess.Popen([path] + ctx.args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


@cli.command()
@click.option('-e', '--edit', is_flag=True)
@click.option('--open', is_flag=True, hidden=True)
@pass_userinfo
def config(userinfo, edit, open):
    '''Manage the global config'''
    if edit:
        userinfo.config = editConfig(userinfo.config, CONFIG_FILE)
    elif open:
        click.launch(os.path.join(config_dir, CONFIG_FILE), locate=True)
    else:
        echo('''Managing config directly via commandline is not currently supported.
Use --edit to edit the config the default editor.''')
