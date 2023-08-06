Geode-GEM
=========

Geode-GEM (former GEM) is a GTK+ Graphical User Interface (GUI) for GNU/Linux
which allows you to easily manage your emulators and games collection. This
software aims to stay the simplest.

![Geode-GEM main interface](preview.jpg)

Licenses
--------

The Geode-GEM application is a free software redistribute under the term of the
[GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html) version
3.0 or later.

The Geode-GEM logo was made with the [Inkscape](https://inkscape.org/) software
and redistribute under the term of the [Free Art License](http://artlibre.org/licence/lal/en/).

The consoles icons used by Geode-GEM come from the [Evan-Amos](https://commons.wikimedia.org/wiki/User:Evan-Amos)
gallery and are [Public Domain](https://en.wikipedia.org/wiki/Public_domain).

Emulators
---------

Default configuration files allow you to use the following emulators out of the
box:

* [Mednafen](https://mednafen.github.io/)
* [Stella](https://stella-emu.github.io/) (Atari 2600)
* [Hatari](https://hatari.tuxfamily.org/) (Atari ST)
* [Fceux](https://fceux.com/web/home.html) (Nintendo NES)
* [Nestopia](http://0ldsk00l.ca/nestopia/) (Nintendo NES)
* [Mupen64plus](https://mupen64plus.org/) (Nintendo 64)
* [Desmume](https://desmume.org/) (Nintendo DS)
* [Dolphin](https://dolphin-emu.org/) (Nintendo GameCube et Nintendo Wii)
* [Gens](http://www.gens.me/index.shtml) (Sega Genesis)
* [DosBOX](https://dosbox-staging.github.io/)

The emulator licenses information have been stored into the [LICENSE.emulators.md](geode_gem/data/docs/LICENSE.emulators.md)
file.

Authors
-------

### Developpers

* [PacMiam](https://pacmiam.tuxfamily.org) (Ellena Lubert)

### Translators

* Pingax (Anthony Jorion) - French
* DarkNekros (José Luis Lopez Castillo) - Spanish

### Testers

* atralfalgar (Bruno Visse)
* Herlief (Jérôme Vigneron)

Packages
--------

### Pypi

This application is available on [Pypi](https://pypi.org/project/Geode-GEM) and
can be installed with the `pip` command:

```
pip install Geode-GEM
```

### Distribution

* [Frugalware](https://frugalware.org/packages/219539) - Thanks to Pingax !
* [Solus](https://dev.getsol.us/source/gem/) - Thanks to Devil505 !

Dependencies
------------

### Python

* python3 >= 3.8
* python3-gobject
* python3-setuptools
* python3-xdg

### System

* file
* gnome-icon-theme
* gnome-icon-theme-symbolic
* gobject-introspection
* gtk+3
* gtksourceview
* libgirepository
* libgirepository-devel
* librsvg
* xdg-utils

Retrieve source code
--------------------

To retrieve source code, you just need to use [git](https://git-scm.com/) and
run the following command:

```
git clone https://framagit.org/geode/gem.git
```

You can also retrieve an archive from the [Geode-GEM download repository](https://download.tuxfamily.org/gem/releases/).

### Testing Geode-GEM

Go to the Geode-GEM source code root folder and launch the following command:

```
python3 -m geode_gem
```

It's possible to set the configuration folders with `--cache`, `--config` and
`--local` arguments:

```
python3 -m geode_gem --cache ~/.cache --config ~/.config --local ~/.local/share
```

### System installation

An installation script is available to help you to install Geode-GEM. You just
need to launch the following command with root privilege:

```
./tools/install.sh
```

This script install Geode-GEM with [setuptools](https://setuptools.readthedocs.io/en/latest/)
and add the `geode-gem` script under `/usr/bin` by default.

You can specify the default prefix by using the `PREFIX` environment variable
with the previous script:

```
PREFIX="/usr/local" ./tools/install.sh
```

Geode-GEM will be available in your desktop environment menu under the **Games**
category.

### User installation

You can also use `pip` to install the code source. You just need to go under the
root directory of Geode-GEM, and launch the following command:

```
pip install .
```

After that, you can install the desktop file with these commands:

```
mkdir -p ~/.local/share/applications/
cp -v geode_gem/data/desktop/gem.desktop ~/.local/share/applications/
```

And the Geode-GEM icon files with the following commands:

```
mkdir -p ~/.local/share/icons/hicolor/scalable/apps/
cp -v geode_gem/data/desktop/gem.svg ~/.local/share/icons/hicolor/scalable/apps/
mkdir -p ~/.local/share/pixmaps/
cp -v geode_gem/data/desktop/gem.svg ~/.local/share/pixmaps/
```
