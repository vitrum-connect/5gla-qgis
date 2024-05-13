# 5gLa-QGIS

## Description

This QGIS plugin provides the visualization of data from the 5gLA platform. It is part of the 5GLa project, which is
funded by the German Federal Ministry of Transport and Digital Infrastructure (BMVI). The website of the project
is https://www.5gla.de/, you can find all additional information there.
If you want to create your own QGIS Plugin, you can follow along. If you just want to use the plugin, you can start
straight with the Section "Install the plugin".

## QGIS Plugin Creation

For the creation of the QGIS plugin, we use the Plugin Builder 3, which itself is a QGIS plugin. The Plugin can be
installed directly over the QGIS UI.

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/ae974bdd-67e0-49ac-9afb-45e81a1f7f6b)

The "Class name" must be an allowed name for a python class. The "Module name" must be an allowed name for python
module.

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/934743a6-27a9-4777-a00b-1b5481ad2430)

The Plugin will be "Tool button with dialog" in the plugin section.

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/2c970a2a-bb3e-4a2f-8bac-ea576dc4ee85)

Extra components could be added, but currently they are not necessary.

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/8c00fbb7-e1a3-4c40-a9b1-2edcb1291288)

The URLs to the GitHub repository, the 5GLa Website and our author contact details will be added.

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/9a0e7c51-b6cc-4ee2-8be9-fae85d54e60d)

The plugin folder will be exported to a directory of our choice.

## Change the icon and compile the plugin

Before we can install the plugin, we need to compile the plugin. To change the icon later, it is necessary to recompile
the plugin. The icon will be stored in the resources.py. To compile the plugin, we use the OSGeo4W Shell which comes
with the QGIS installation.

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/20ceb028-cdc8-47b6-9c32-650e0ef01c50)

We navigate into the plugin folder and use the pyrcc5 command to compile the plugin.

## Install the plugin

First, we need to copy our plugin folder `fivegla_visualization` to the Qgis python plugin directory.

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/651d9cd2-6b21-4075-b91f-8df3f43cb7a0)

The easiest way is to go to `Settings` --> `Userprofiles` --> `Open current profile directory`. In the explorer you
navigate to `/python/plugins`. Copy the plugin folder to this directory. The folder will be initialized with the start
of qgis so you to restart qgis after you copy the folder to the plugin directory. To install the plugin, you go to
`Plugins` -> `Manage and install plugins`.

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/1a4f070f-f8a5-4f7a-80be-2811286c20e5)

You should find the `fivegla_visualization` plugin in the UI. If you check the checkbox left to the plugin, you install it. If
you uncheck it, you deactivate it. By clicking Uninstall plugin on the bottom, you remove (delete) the plugin folder
from your plugins' directory.
