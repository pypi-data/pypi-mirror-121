# ------------------------------------------------------------------------------
#  Copyleft 2015-2021  PacMiam
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
# ------------------------------------------------------------------------------

# Filesystem
from pathlib import Path
from shutil import rmtree

# GEM
from geode_gem.engine.api import GEM
from geode_gem.engine.utils import copy, get_data
from geode_gem.engine.lib.configuration import Configuration

from geode_gem.ui.data import Icons, Columns, Folders, Metadata
from geode_gem.ui.utils import magic_from_file

# Logging
from logging import getLogger

# System
from argparse import ArgumentParser
from os import environ

# Translation
from gettext import textdomain, bindtextdomain
from gettext import gettext as _

# XDG
from xdg.BaseDirectory import (save_cache_path, save_config_path,
                               save_data_path, xdg_cache_home,
                               xdg_config_home, xdg_data_home)


# ------------------------------------------------------------------------------
#   Launcher
# ------------------------------------------------------------------------------

def copy_file(path, new_path):
    """

    Parameters
    ----------
    path : pathlib.Path
        Original file path to copy
    new_path : pathlib.Path
        Destination path

    Returns
    -------
    bool
        True is copy is successful, False, otherwise
    """

    if path.exists() and not new_path.exists():
        copy(path, new_path)
        return True

    return False


def make_directory(path, mode=0o755, make_parents=True):
    """ Generate a directory

    Parameters
    ----------
    path : pathlib.Path
        Directory path
    mode : octal integer, optional
        Directory access permissions
    make_parents : bool, optional
        Ensure to create all the directories from path if missing

    Returns
    -------
    bool
        True is creation is successful, False, otherwise
    """

    if not path.exists():
        path.mkdir(mode=mode, parents=make_parents)
        return True

    return False


def make_user_directory(directory, xdg_method):
    """ Generate an user directory

    Parameters
    ----------
    directory : str
        User directory path to generate
    xdg_method : func
        Specific xdg.BaseDirectory method to use when directory is null

    Returns
    -------
    pathlib.Path
        Generated directory path
    """

    if directory is None:
        return Path(xdg_method(GEM.Instance)).expanduser()

    path = Path(directory).expanduser().joinpath(GEM.Instance)
    path.mkdir(mode=0o755, parents=True, exist_ok=True)

    return path


def init_localization(egg_name):
    """ Initialize application localization

    Parameters
    ----------
    egg_name : str
        Python egg name
    """

    bindtextdomain(egg_name, localedir=str(get_data("data", "i18n")))
    textdomain(egg_name)


def init_environment():
    """ Initialize main environment

    Returns
    -------
    geode_gem.engine.lib.configuration.Configuration
        Metadata configuration file instance for testing purpose
    """

    # Initialize metadata
    metadata = Configuration(get_data("data", "config", "metadata.conf"))

    # Retrieve metadata informations
    if metadata.has_section("metadata"):
        for key, value in metadata.items("metadata"):
            setattr(Metadata, key.upper(), value)

    # Retrieve icons informations
    if metadata.has_section("icons"):
        for key, value in metadata.items("icons"):
            setattr(Icons, key.upper(), value)
            setattr(Icons.Symbolic, key.upper(), f"{value}-symbolic")

    if metadata.has_section("icon-sizes"):
        for key, value in metadata.items("icon-sizes"):
            setattr(Icons.Size, key.upper(), value.split())

    # Retrieve columns informations
    if metadata.has_section("misc"):
        setattr(Columns, "ORDER",
                metadata.get("misc", "columns_order", fallback=str()))

    if metadata.has_section("list"):
        for key, value in metadata.items("list"):
            setattr(Columns.List, key.upper(), int(value))

    if metadata.has_section("grid"):
        for key, value in metadata.items("grid"):
            setattr(Columns.Grid, key.upper(), int(value))

    return metadata


def init_configuration(gem):
    """ Initialize user configuration

    Parameters
    ----------
    gem : gem.engine.api.GEM
        GEM API instance
    """

    move_collection = False

    # Configuration
    for filename in ("gem.conf", "consoles.conf", "emulators.conf"):
        path = get_data("data", "config", filename)
        new_path = gem.get_config(filename)

        if copy_file(path, new_path):
            gem.logger.debug(f"Copy {path} to {new_path}")

    # Local
    for folder in ("logs", "notes"):
        if make_directory(gem.get_local(folder)):
            gem.logger.debug(f"Generate {folder} directory")

    # Cache
    for name in ("consoles", "emulators", "games"):
        for size in getattr(Icons.Size, name.upper(), list()):
            path = Folders.CACHE.joinpath(name, f"{size}x{size}")

            if make_directory(path):
                gem.logger.debug(f"Generate {path} directory")

    # Icons
    icons_path = gem.get_local("icons")

    if not icons_path.exists():
        if make_directory(icons_path):
            gem.logger.debug(f"Generate {icons_path} directory")

        move_collection = True

    # Remove older icons collections folders (GEM < 1.0)
    else:
        for folder in ("consoles", "emulators"):
            path = icons_path.joinpath(folder)

            if not path.exists():
                continue

            if path.is_dir():
                rmtree(path)

            elif path.is_symlink():
                path.unlink()

            move_collection = True

    # Copy default icons
    if move_collection:
        gem.logger.debug("Generate consoles icons folder")

        for filename in get_data("data", "icons").glob("*.png"):

            if not filename.is_file():
                continue

            # Check the file mime-type to avoid non-image file
            mime = magic_from_file(filename, mime=True)
            if mime.startswith("image/"):
                new_path = icons_path.joinpath(filename.name)

                if copy_file(filename, new_path):
                    gem.logger.debug(f"Copy {filename} to {new_path}")


def init_cache_directory(directory, clean_cache):
    """ Initialize Geode-GEM dedicated user cache directory

    Parameters
    ----------
    directory : str
        Cache directory path
    clean_cache : bool
        Remove files from cache if directory exists

    Notes
    -----
    By default, this directory if often ~/.cache/gem
    """

    setattr(Folders, "CACHE", directory)

    if Folders.CACHE.exists() and clean_cache:

        if Folders.CACHE.is_dir():
            rmtree(Folders.CACHE)

        Folders.CACHE.mkdir(mode=0o755, parents=True, exist_ok=True)


def launch_interface(gem, cache):
    """ Start main interface

    Parameters
    ----------
    gem : geode_gem.engine.api.GEM
        GEM API instance
    cache : pathlib.Path
        Cache directory path

    Returns
    -------
    bool
        False if the interface was launched successfully, True otherwise
    """

    if "DISPLAY" not in environ or len(environ.get("DISPLAY")) == 0:
        getLogger(gem.Instance).critical(
            "Cannot launch GEM without display")

        return True

    if not gem.is_locked():
        # Initialize main configuration files
        init_configuration(gem)

        getLogger(gem.Instance).info(f"Start GEM with PID {gem.pid}")

        # Start splash
        from geode_gem.ui.splash import Splash
        Splash(gem)

        # Start interface
        from geode_gem.ui.interface import MainWindow
        MainWindow(gem, cache)

        # Remove lock
        gem.free_lock()

    else:
        getLogger(gem.Instance).critical(
            f"GEM is already running with PID {gem.pid}")

        from geode_gem.ui.splash import Message
        message = Message(
            _("An instance already exists"),
            _("GEM is already running with PID %s") % gem.pid)
        message.run()

    return False


def start_geode_gem(cache=None, config=None, local=None,
                    clean_cache=False, debug=False):
    """ Generate Geode-GEM API object and launch main interface

    Parameters
    ----------
    cache : None
        Geode-GEM cache directory path (Default: None)
    config : None
        Geode-GEM config directory path (Default: None)
    local : None
        Geode-GEM data directory path (Default: None)
    clean_cache : bool
        Ensure to clean Geode-GEM directory cache (Default: False)
    debug : bool
        Activate debug flag (Default: False)

    Returns
    -------
    bool
        False if the process was launched successfully, True otherwise
    """

    process_status = False

    # Initialize localization
    init_localization("geode_gem")

    # Initialize user application directories
    cache = make_user_directory(cache, save_cache_path)
    config = make_user_directory(config, save_config_path)
    local = make_user_directory(local, save_data_path)

    # Manage cache directory
    init_cache_directory(cache, clean_cache)

    try:
        gem = GEM(config, local, debug)

        process_status = launch_interface(gem, cache)

    except ImportError:
        getLogger("gem").exception("An error occur during modules importation")
        process_status = True

    except KeyboardInterrupt:
        getLogger("gem").warning("Terminate by keyboard interrupt")
        process_status = True

    except Exception:
        getLogger("gem").exception("An error occur during execution")
        process_status = True

    # Remove lock when an error occurs
    if process_status:
        gem.free_lock()

    return process_status


def main():
    """ Main launcher
    """

    # Initialize environment
    init_environment()

    # ----------------------------------------
    #   Generate arguments
    # ----------------------------------------

    parser = ArgumentParser(
        epilog=Metadata.COPYLEFT,
        description=f"{Metadata.NAME} - {Metadata.VERSION}",
        conflict_handler="resolve")

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{Metadata.NAME} {Metadata.VERSION} "
                f"({Metadata.CODE_NAME}) - {Metadata.LICENSE}",
        help="show the current version")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="launch gem with debug flag")

    parser_api = parser.add_argument_group("api arguments")
    parser_api.add_argument(
        "--cache",
        action="store",
        metavar="DIR",
        default=None,
        help=f"set cache folder (default: {xdg_cache_home})")
    parser_api.add_argument(
        "--config",
        action="store",
        metavar="DIR",
        default=None,
        help=f"set configuration folder (default: {xdg_config_home})")
    parser_api.add_argument(
        "--local",
        action="store",
        metavar="DIR",
        default=None,
        help=f"set data folder (default: {xdg_data_home})")

    parser_maintenance = parser.add_argument_group("maintenance arguments")
    parser_maintenance.add_argument(
        "--clean-cache",
        action="store_true",
        help="clean icons cache directory")

    return start_geode_gem(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
