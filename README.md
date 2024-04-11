# 5gLa-QGIS
## Description
This QGIS plugin provides the visualization of sensor data from the 5gLA platform. It is part of the 5GLA project, which is funded by the German Federal Ministry of Transport and Digital Infrastructure ( BMVI).The website of the project is https://www.5gla.de/, you can find all additional information there.

If you want to create you own QGIS Plugin you can follow along. If you just want to use the plugin you can start straight with the Section "Install the plugin". 

## QGIS Plugin Creation
For the creation of the QGIS plugin we use the Plugin Builder 3 which itself is a QGIS plugin. The Plugin can be installed directly over the QGIS UI. 

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/ae974bdd-67e0-49ac-9afb-45e81a1f7f6b)

The "Class name" must be an allowed name for a python class. The "Module name" must be an allowd name for python module. 

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/a2a70c94-5edf-4b50-bb98-1f152bda301c)

The Plugin will be "Tool button with dialog" in the plugin section.

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/9fb9a322-083b-4297-ac9e-0fbf6e113d10)

Extra components couldb be added but currently they are not necessary. 

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/7a522356-8b3b-467b-837c-9440e41381af)

The URLs to the github repo, the 5gla website and our author contact details will be added. 

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/5519ce3b-350b-48a6-9a65-8a1fd89203e1)

The plugin folder will be exported to a directory of our choice. 

## Change the icon and compile the plugin

Before we can install the plugin we need to compile the plugin. To change the icon later, it is necessary to recompile the plugin. The icon will be stored in the resources.py. 
To compile the plugin we use the OSGeo4W Shell which comes with the QGIS installation. 
![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/54ef01bd-8c26-4440-9dbe-abe2024b74b2)

We cd into the plugin folder and use the pyrcc5 comand to compile the plugin.

## Install the plugin

First we need to copy our plugin folder (sensor_data_viewer) to the Qgis python plugin directory. 

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/0aba3dd6-8954-4893-8b58-fc7fba7bd2e4)

The easiest way is to go to settings --> Userprofiles --> open current profile directory. In the explorer you cd to /python/plugins. Copy the plugin folder to this directory. 

The Folder will be initialized with the start of qgis so you to restart qgis after you copying the folder to the plugin directory. 

To install the plugin you go to Plugins -> manage and install plugins.

![image](https://github.com/vitrum-connect/5gla-qgis/assets/86096399/c3080940-c68b-42c0-93a3-fb4f5687b576)

You should find the 5gLa sensor data viewer in the UI. If you check the checkbox left to the plugin you install it. if you uncheck it you deactivate it. By clicking Uninstall plugin on the bottom you remove (delete) the plugin folder from your plugins directory.

