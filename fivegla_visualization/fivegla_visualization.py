  # -*- coding: utf-8 -*-

import os.path

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .constants import Constants
from .device_measurement import FiveGLaVisualizationDeviceMeasurement
from .device_position import FiveGLaVisualizationDevicePosition
from .resources import *
from .settings import FiveGLaVisualizationSettings


class FiveGLaVisualization:
    """ QGIS Plugin Implementation.

    This class is responsible for setting up the plugin and the GUI
    """

    def __init__(self, iface):
        """ Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            Constants.PLUGIN_DIR,
            'i18n',
            'fivegla_visualization_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&5GLa Visualization')
        self.first_start = None

        # change the initial qgis working dir to plugin file
        plugin_directory = os.path.dirname(os.path.abspath(__file__))
        os.chdir(plugin_directory)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """ Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """

        return QCoreApplication.translate('fivegla_visualization', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """ Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        # Adds a tooltip info
        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """ Create the menu entries and toolbar icons inside the QGIS GUI.

        :return: None
        """
        self.first_start = True

        icon_settings = ':/plugins/fivegla_visualization/icons/settings.png'
        settings_action_text = u'Settings'
        fivegla_visualization_settings = FiveGLaVisualizationSettings(self.iface, self.handle_first_start)
        self.add_action(
            icon_settings,
            text=self.tr(settings_action_text),
            callback=lambda: fivegla_visualization_settings.run(),
            add_to_toolbar=False,
            parent=self.iface.mainWindow())

        fivegla_visualization_device_position = FiveGLaVisualizationDevicePosition(self.iface, self.handle_first_start)
        icon_device_position = ':/plugins/fivegla_visualization/icons/drone.png'
        device_position_action_text = u'Device Position'
        self.add_action(
            icon_device_position,
            text=self.tr(device_position_action_text),
            callback=lambda: fivegla_visualization_device_position.run(),
            add_to_toolbar=True,
            parent=self.iface.mainWindow())

        fivegla_visualization_device_measurement = FiveGLaVisualizationDeviceMeasurement(self.iface,
                                                                                         self.handle_first_start)
        icon_device_measurement = ':/plugins/fivegla_visualization/icons/sensor.png'
        device_measurement_action_text = u'Device Measurement'
        self.add_action(
            icon_device_measurement,
            text=self.tr(device_measurement_action_text),
            callback=lambda: fivegla_visualization_device_measurement.run(),
            add_to_toolbar=True,
            parent=self.iface.mainWindow())

    def unload(self):
        """ Removes the plugin menu item and icon from QGIS GUI.

        :return: None
        """
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&5GLa Visualization'),
                action)
            self.iface.removeToolBarIcon(action)

    def handle_first_start(self):
        """ The method ensures that all dependencies are correctly initialized and declared

        :return: None
        """
        if self.first_start:
            self.first_start = False
