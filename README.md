# Freshest

**Freshest** is a minimalist graphic customizable application menu with a simple-but-effective automatic reordering mechanism. It is written in Python with GTK+.

How does it work? When you launch an application, it is moved to the head of the list. This way the most heavily used applications are concentrated in one end, and the least used ones in the other. This has two-way benefit, as most of the time you’ll want to use an application which you use frequently (duh!…), but sometimes you’d rather choose to launch one which gathers dust (e.g. that game you’ve downloaded months ago but haven’t got the chance to play and now you find it awesome).



## Features

* Automatic **reordering** of items according to your changing habits and needs.
* Everything is done in open human-readable, computer-manipulatable **standard formats** ([freedesktop.org](http://www.freedesktop.org/)’s [desktop entries](http://www.freedesktop.org/wiki/Specifications/desktop-entry-spec/) and [JSON](http://www.json.org/)). Desktop entries can be copied (or symlinked) from your system’s appropriate directory (e.g. `/usr/share/applications` in [http://archlinux.org](Arch Linux)).
* Native support for **localization** ([POSIX locale](https://en.wikipedia.org/wiki/Locale#POSIX_platforms)). If a desktop entry file doesn’t contain a name suitable for your language, you can [add it manually](http://standards.freedesktop.org/desktop-entry-spec/latest/ar01s04.html).
* While manipulating the menu requires some technical skills, using the menu is dead **simple**, making it perfect for children (my kids use it for launching games).



## Usage

One can have several independent profiles; they are located by default each at `~/.config/freshest/PROFILENAME`, where the default `PROFILENAME` is `default`. The latter is used by running `freshest`, while other profiles can be used by running `freshest PROFILENAME` (this will create a new profile in case it doesn't exist yet).

Each profile has:
* `applications/`: a subdirectory which you should populate with `.desktop` files
* `list.json`: an automatically managed file which contains data about which applications was used most recently
* `config.json`: a configuration file

Desktop entry files can be easily edited with any text editor. If you want a specialized tool, give [this](https://github.com/MicahCarrick/desktop-entry-editor) a try.



## Contribution

Feel free to contribute to this software ☺. Just fork it, make the changes you want and send a pull request.

I’m just a novice Python programmer. I’m aware the code isn’t elegant; if you have suggestions for making it more readable, efficient, neat or Pythonic, don’t hesitate.



## Dependencies

* [PyGObject](https://live.gnome.org/PyGObject) 3, for GUI (Arch `pygobject-devel`; Fedora `pygobject3`; Ubuntu `python-gobject`)
* [PyXDG](http://freedesktop.org/wiki/Software/pyxdg/), for parsing `.desktop` files (Arch and Ubuntu `python-xdg`; Fedora `pyxdg`)



## License

[Abolish intellectual property](https://en.wikipedia.org/wiki/Anti-copyright_movement)! ☠
