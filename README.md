# Output Pro
An extension to export print-ready documents from Inkscape

## Introduction
With this extension you will be able to export your Inkscape documents into a variety of formats and colormodes. As it initial and main goal,Inkscape Output Pro export into the CMYK colormode, compatible with the press and graphic industry standards.

It is possible to use specific ICC profiles, set other colormodes than RGB and CMYK, like Grayscale and Lab, set specific JPEG configurations, insert pre-press marks and even more.

## Installation

### Linux
First, make sure you have Libcanberra and PyQt4 installed

```
sudo apt install libcanberra-gtk-module libcanberra-gtk3-module
sudo apt install python-qt4
```

The copy `outputpro.inx`, `outputpro.py` and the `outputpro` directory to:

```
/usr/share/inkscape/extensions
```

If you don't have root access or only want the files to be available to the current user:

```
<YOUR HOME DIR>/.config/inkscape/extensions
```

**Note**:

I'm on elementary OS Juno and I had to install `gtk2-engines-pixbuf` to get rid of an error message after exporting:

```
sudo apt install gtk2-engines-pixbuf
```

This might be true for all Ubuntu based distros as well.


### Windows
This might work, but has not been tested yet. To-do.

### macOS
To-do.

## Important
As the orignal author abandoned the project. It is my intention to keep it working in recent versions of Inkscape.

## Credits
The [Output Pro](http://jonata.org/inkscape/outputpro/) extension was originally written by Jonatã Bolzan.

## License
Output Pro is licensed under the terms of the GNU License.
