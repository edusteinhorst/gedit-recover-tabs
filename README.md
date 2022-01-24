## gedit Recover Tabs

This is a plugin for [gedit][1], the official text editor of the GNOME desktop
environment. 

It will reopen all previously open tabs across all gedit windows, in case they were not intentionally closed. 

Perfect for when you simply need to restart the computer or things crash. 

Inspired on [restore-tabs plugin](https://github.com/Quixotix/gedit-restore-tabs), originally written by Micah Carrick. 

This plugin is for gedit versions 3.36 and above (included in Ubuntu 20.04).

**This plugin is NOT compatible with gedit 2.x**.

Installation
------------

1. Download the source code from this repository, and extract the contents: 

       wget https://github.com/edusteinhorst/gedit-recover-tabs/archive/main.zip -O gedit-recover-tabs.zip
       unzip gedit-recover-tabs.zip

2. After extraction, copy all the files that begin with `recovertabs.*` to your local `gedit` plugins directory, located at `~/.local/share/gedit/plugins/`:

       cd gedit-recover-tabs-main
       mkdir -p ~/.local/share/gedit/plugins
       cp recovertabs.* ~/.local/share/gedit/plugins/   
     
3. Copy and compile the settings schema as **sudo/root**. We need to add a `glib` schema, and gedit looks for such schema in the `/usr/` directory in the file system. Thus, we will need to root privileges, in order to put the newly compiled schemas database in that location.

       sudo cp org.gnome.gedit.plugins.recovertabs.gschema.xml /usr/share/glib-2.0/schemas/
       sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

4. Restart gedit, and activate the plugin by going to `Edit` > `Preferences`, selecting the `Plugins` tab and marking the checkbox by the `Recover Tabs` entry.

[1]: http://www.gedit.org
