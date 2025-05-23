import sys,os
from typing import TextIO

if sys.version_info < (3, 8):
    print("only support python >= 3.8, but now is {}".format(sys.version_info))
    sys.exit(1)


try:
    import parameters,helpAbout,autoUpdate
    from Combobox import ComboBox
    import i18n
    from i18n import _
    import version
    import utils
    from conn.conn_serial import Serial
    from plugins import dbg
except ImportError:
    from COMTool import parameters,helpAbout,autoUpdate, utils
    from COMTool.Combobox import ComboBox
    from COMTool import i18n
    from COMTool.i18n import _
    from COMTool import version
    from COMTool.conn.conn_serial import Serial
    from COMTool.plugins import dbg

from PyQt5.QtCore import pyqtSignal,Qt, QRect, QMargins
from PyQt5.QtWidgets import (QApplication, QWidget,QPushButton,QMessageBox,QDesktopWidget,QMainWindow,
                             QVBoxLayout,QHBoxLayout,QGridLayout,QTextEdit,QLabel,QRadioButton,QCheckBox,
                             QLineEdit,QGroupBox,QSplitter,QFileDialog, QScrollArea)
from PyQt5.QtGui import QIcon,QFont,QTextCursor,QPixmap,QColor
import threading
import time
from datetime import datetime
import binascii,re
if sys.platform == "win32":
    import ctypes



class MainWindow(QMainWindow):
    hintSignal = pyqtSignal(str, str, str) # type(error, warning, info), title, msg
    statusBarSignal = pyqtSignal(str, str)
    updateSignal = pyqtSignal(object)
    countUpdateSignal = pyqtSignal(int, int)
    clearCountSignal = pyqtSignal()
    receiveCount = 0
    sendCount = 0
    DataPath = "./"
    app = None
    needRestart = False

    def __init__(self,app):
        super().__init__()
        self.app = app
        self.DataPath = parameters.dataPath
        self.config = self.loadParameters()
        i18n.set_locale(self.config.basic["locale"])
        self.initVar()
        self.initConn(self.config.basic["connId"], self.config.conns)
        self.initPlugins(self.config.basic["plugins"], self.config.basic["activePlugin"], self.config.plugins)
        self.initWindow()
        self.uiLoadConfigs(self.config)
        self.initEvent()
        self.uiInitDone()

    def __del__(self):
        pass

    def initConn(self, connId, configs):
        # get all conn info
        self.connections = [Serial()]
        # init connections
        for conn in self.connections:
            conn.onReceived = self.onReceived
            conn.configGlobal = self.config.basic
            conn.hintSignal = self.hintSignal
            config = {}
            if conn.id in configs:
                config = configs[conn.id]
            conn.onInit(config)
        # init last used one
        self.connection = None
        for conn in self.connections:
            if conn.id == connId:
                self.connection = conn
        if not self.connection:
            self.connection = self.connections[0]


    def initPlugins(self, enabled, activeId, configs):
        if not enabled:
            enabled = ["dbg"]
        self.connChilds = []
        self.plugins = [dbg.Plugin()]
        for plugin in self.plugins:
            plugin.hintSignal = self.hintSignal
            plugin.send = self.sendData
            plugin.clearCountSignal = self.clearCountSignal
            plugin.configGlobal = self.config.basic
            config = {}
            if plugin.id in configs:
                config = configs[plugin.id]
            plugin.onInit(config)
            if plugin.id in enabled:
                self.enablePlugin(plugin)
            if plugin.id == activeId:
                self.activePlugin(plugin)

    def enablePlugin(self, plugin):
        plugin.enabled = True
        if plugin.connParent == "main":
            self.connChilds.append(plugin)


    def activePlugin(self, plugin):
        plugin.active = True
        if plugin.connParent:
            for plugin in self.plugins:
                if plugin.id == plugin.connParent:
                    plugin.active = True
        

    
    def initVar(self):
        self.strings = parameters.Strings(self.config.basic["locale"])
        self.dataToSend = []
        self.fileToSend = []

    def uiInitDone(self):
        self.connection.onUiInitDone()
        for plugin in self.plugins:
            plugin.onUiInitDone()

    def initWindow(self):
        # main layout
        self.frameWidget = QWidget()
        frameLayout = QVBoxLayout()
        menuLayout = QHBoxLayout()
        contentWidget = QSplitter(Qt.Horizontal)
        frameLayout.addLayout(menuLayout)
        frameLayout.addWidget(contentWidget)
        self.frameWidget.setLayout(frameLayout)
        self.setCentralWidget(self.frameWidget)

        # option layout
        self.settingsButton = QPushButton()
        self.skinButton = QPushButton("")
        self.languageCombobox = ComboBox()
        self.languages = i18n.get_languages()
        for locale in self.languages:
            self.languageCombobox.addItem(self.languages[locale])
        self.aboutButton = QPushButton()
        self.functionalButton = QPushButton()
        self.encodingCombobox = ComboBox()
        self.supportedEncoding = parameters.encodings
        for encoding in self.supportedEncoding:
            self.encodingCombobox.addItem(encoding)
        self.settingsButton.setProperty("class", "menuItem1")
        self.skinButton.setProperty("class", "menuItem2")
        self.aboutButton.setProperty("class", "menuItem3")
        self.functionalButton.setProperty("class", "menuItem4")
        self.settingsButton.setObjectName("menuItem")
        self.skinButton.setObjectName("menuItem")
        self.aboutButton.setObjectName("menuItem")
        self.functionalButton.setObjectName("menuItem")
        menuLayout.addWidget(self.settingsButton)
        menuLayout.addWidget(self.skinButton)
        menuLayout.addWidget(self.aboutButton)
        menuLayout.addWidget(self.languageCombobox)
        menuLayout.addStretch(0)
        menuLayout.addWidget(self.encodingCombobox)
        menuLayout.addWidget(self.functionalButton)

        # widget main
        self.mainWidget = self.plugins[0].onWidgetMain()

        # widgets settings
        self.settingWidget = QWidget()
        self.settingWidget.setProperty("class","settingWidget")
        settingLayout = QVBoxLayout()
        self.settingWidget.setLayout(settingLayout)
        #  connection settings
        serialSettingsGroupBox = QGroupBox(self.strings.strSerialSettings)
        layout = QVBoxLayout()
        serialSettingsGroupBox.setLayout(layout)
        widget = self.connection.onWidget()
        layout.addWidget(widget)
        settingLayout.addWidget(serialSettingsGroupBox)
        #  other settings
        widget = self.plugins[0].onWidgetSettings()
        settingLayout.addWidget(widget)
        settingLayout.addStretch(1)
        # settingLayout.setContentsMargins(0,0,0,0)

        # right functional layout
        self.functionalWiget = self.plugins[0].onWidgetFunctional()
        self.hideFunctional()

        # main window
        self.statusBarStauts = QLabel()
        self.statusBarStauts.setMinimumWidth(80)
        self.onstatusBarText("info", self.strings.strReady)
        self.statusBarSendCount = QLabel('{}({}):0'.format(_("Sent"), _("bytes")))
        self.statusBarReceiveCount = QLabel('{}({}):0'.format(_("Received"), _("bytes")))
        self.statusBar().addWidget(self.statusBarStauts)
        self.statusBar().addWidget(self.statusBarSendCount,2)
        self.statusBar().addWidget(self.statusBarReceiveCount,3)

        contentWidget.addWidget(self.settingWidget)
        contentWidget.addWidget(self.mainWidget)
        contentWidget.addWidget(self.functionalWiget)
        contentWidget.setStretchFactor(0, 4)
        contentWidget.setStretchFactor(1, 7)
        contentWidget.setStretchFactor(2, 2)

        self.resize(800, 500)
        self.MoveToCenter()
        self.setWindowTitle(parameters.appName+" v"+version.__version__)
        icon = QIcon()
        print("icon path:"+self.DataPath+"/"+parameters.appIcon)
        icon.addPixmap(QPixmap(self.DataPath+"/"+parameters.appIcon), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("comtool")
        self.show()
        print("config file path:",parameters.configFilePath)

    def initEvent(self):
        # menu
        self.settingsButton.clicked.connect(self.toggleSettings)
        self.languageCombobox.currentIndexChanged.connect(self.onLanguageChanged)
        self.encodingCombobox.currentIndexChanged.connect(lambda: self.bindVar(self.encodingCombobox, self.config, "encoding"))
        self.functionalButton.clicked.connect(self.toggleFunctional)
        self.skinButton.clicked.connect(self.skinChange)
        self.aboutButton.clicked.connect(self.showAbout)
        # others
        self.updateSignal.connect(self.showUpdate)
        self.hintSignal.connect(self.showHint)
        self.statusBarSignal.connect(self.onstatusBarText)
        self.clearCountSignal.connect(self.onClearCount)
        self.countUpdateSignal.connect(self.onUpdateCountUi)

    def bindVar(self, uiObj, varObj, varName: str, vtype=None, vErrorMsg="", checkVar=lambda v:v, invert = False):
        objType = type(uiObj)
        if objType == QCheckBox:
            v = uiObj.isChecked()
            varObj.__setattr__(varName, v if not invert else not v)
            return
        elif objType == QLineEdit:
            v = uiObj.text()
        elif objType == ComboBox:
            varObj.__setattr__(varName, uiObj.currentText())
            return
        elif objType == QRadioButton:
            v = uiObj.isChecked()
            varObj.__setattr__(varName, v if not invert else not v)
            return
        else:
            raise Exception("not support this object")
        if vtype:
            try:
                v = vtype(v)
            except Exception:
                uiObj.setText(str(varObj.__getattribute__(varName)))
                self.hintSignal.emit("error", _("Error"), vErrorMsg)
                return
        try:
            v = checkVar(v)
        except Exception as e:
            self.hintSignal.emit("error", _("Error"), str(e))
            return
        varObj.__setattr__(varName, v)

    def sendData(self, data_bytes=None, file_path=None):
        if data_bytes:
            self.dataToSend.insert(0, data_bytes)
        if file_path:
            self.fileToSend.insert(0, file_path)

    def onSent(self, n_bytes):
        self.sendCount += n_bytes
        self.countUpdateSignal.emit(self.sendCount, self.receiveCount)

    def onReceived(self, data):
        self.receiveCount += len(data)
        self.countUpdateSignal.emit(self.sendCount, self.receiveCount)
        # invoke plugin onReceived
        for plugin in self.connChilds:
            if plugin.active:
                plugin.onReceived(data)


    def sendDataProcess(self):
        self.receiveProgressStop = False
        while(not self.receiveProgressStop):
            try:
                while len(self.dataToSend) > 0:
                    data = self.dataToSend.pop()
                    self.com.write(data)
                    self.onSent(len(data))
                while len(self.fileToSend) > 0:
                    file_path = self.fileToSend.pop()
                    ok = False
                    if file_path and os.path.exists(file_path):
                        data = None
                        try:
                            with open(file_path, "rb") as f:
                                data = f.read()
                        except Exception as e:
                            self.hintSignal.emit("error", _("Error"), _("Open file failed!") + "\n%s\n%s" %(file_path, str(e)))
                        if data:
                            self.com.write(data)
                            self.onSent(len(data))
                            ok = True
                    self.sendFileOkSignal.emit(ok, file_path)
                time.sleep(0.001)
            except Exception as e:
                if 'multiple access' in str(e):
                    self.hintSignal.emit("error", _("Error"), "device disconnected or multiple access on port?")
                break

    def onUpdateCountUi(self, send, receive):
        self.statusBarSendCount.setText('{}({}): {}'.format(_("Sent"), _("bytes"), send))
        self.statusBarReceiveCount.setText('{}({}): {}'.format(_("Received"), _("bytes"), receive))

    def onstatusBarText(self, msg_type, msg):
        if msg_type == "info":
            color = "#008200"
        elif msg_type == "warning":
            color = "#fb8c00"
        elif msg_type == "error":
            color = "#f44336"
        else:
            color = "#008200"
        text = '<font color={}>{}</font>'.format(color, msg)
        self.statusBarStauts.setText(text)        

    def updateStyle(self, widget):
        self.frameWidget.style().unpolish(widget)
        self.frameWidget.style().polish(widget)
        self.frameWidget.update()

    def onLanguageChanged(self):
        idx = self.languageCombobox.currentIndex()
        locale = list(self.languages.keys())[idx]
        self.config.basic["locale"] = locale
        i18n.set_locale(locale)
        reply = QMessageBox.question(self, _('Restart now?'),
                                     _("language changed to: ") + self.languages[self.config.basic["locale"]] + "\n" + _("Restart software to take effect now?"), QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.needRestart = True
            self.close()

    def onClearCount(self):
        self.receiveCount = 0
        self.sendCount = 0
        self.countUpdateSignal.emit(self.sendCount, self.receiveCount)

    def MoveToCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showHint(self, info_type: str, title: str, msg: str):
        if info_type == "info":
            QMessageBox.information(self, title, msg)
        elif info_type == "warning":
            QMessageBox.warning(self, title, msg)
        elif info_type == "error":
            QMessageBox.critical(self, title, msg)

    def closeEvent(self, event):
        print("----- close event")
        # reply = QMessageBox.question(self, 'Sure To Quit?',
        #                              "Are you sure to quit?", QMessageBox.Yes |
        #                              QMessageBox.No, QMessageBox.No)
        if 1: # reply == QMessageBox.Yes:
            self.receiveProgressStop = True
            self.programExitSaveParameters()
            event.accept()
        else:
            event.ignore()

    def programExitSaveParameters(self):
        paramObj = self.config
        # paramObj.skin = self.config.basic["skin"]
        # paramObj.sendHistoryList.clear()
        # for i in range(0,self.sendHistory.count()):
        #     paramObj.sendHistoryList.append(self.sendHistory.itemText(i))
        # send items
        # valid = []
        # for text in self.config.customSendItems:
        #     if text:
        #         valid.append(text)
        # self.config.customSendItems = valid
        paramObj.save(parameters.configFilePath)

    def loadParameters(self):
        paramObj = parameters.Parameters()
        paramObj.load(parameters.configFilePath)
        return paramObj

    def uiLoadConfigs(self, config):
        pass
        # for plugin in self.plugins:
        #     conf = {}
        #     if plugin.id in config.pluginsConfis:
        #         conf = config.pluginsConfis[plugin.id]
        #     plugin.updateConfig(conf)
        
        # self.receiveSettingsHex.setChecked(not paramObj.receiveAscii)
        # self.receiveSettingsAutoLinefeed.setChecked(paramObj.receiveAutoLinefeed)
        # try:
        #     interval = int(paramObj.receiveAutoLindefeedTime)
        #     paramObj.receiveAutoLindefeedTime = interval
        # except Exception:
        #     interval = parameters.Parameters.receiveAutoLindefeedTime
        # self.receiveSettingsAutoLinefeedTime.setText(str(interval) if interval > 0 else str(parameters.Parameters.receiveAutoLindefeedTime))
        # self.receiveSettingsTimestamp.setChecked(paramObj.showTimestamp)
        # self.sendSettingsHex.setChecked(not paramObj.sendAscii)
        # self.sendSettingsScheduledCheckBox.setChecked(paramObj.sendScheduled)
        # try:
        #     interval = int(paramObj.sendScheduledTime)
        #     paramObj.sendScheduledTime = interval
        # except Exception:
        #     interval = parameters.Parameters.sendScheduledTime
        # self.sendSettingsScheduled.setText(str(interval) if interval > 0 else str(parameters.Parameters.sendScheduledTime))
        # self.sendSettingsCRLF.setChecked(paramObj.useCRLF)
        # self.sendSettingsRecord.setChecked(paramObj.recordSend)
        # self.sendSettingsEscape.setChecked(paramObj.sendEscape)
        # for i in range(0, len(paramObj.sendHistoryList)):
        #     text = paramObj.sendHistoryList[i]
        #     self.sendHistory.addItem(text)
        # self.encodingCombobox.setCurrentIndex(self.supportedEncoding.index(paramObj.encoding))
        # try:
        #     idx = list(self.languages.keys()).index(paramObj.locale)
        # except Exception:
        #     idx = 0
        # self.languageCombobox.setCurrentIndex(idx)
        # self.logFilePath.setText(paramObj.saveLogPath)
        # self.logFilePath.setToolTip(paramObj.saveLogPath)
        # self.saveLogCheckbox.setChecked(paramObj.saveLog)
        # self.receiveSettingsColor.setChecked(paramObj.color)
        # # send items
        # self.toggleFunctional() # have to show then to get height
        # for text in self.config.customSendItems:
        #     self.insertSendItem(text, load=True)
        # self.toggleFunctional()

    def keyPressEvent(self, event):
        self.plugins[0].onKeyReleaseEvent(event)

    def keyReleaseEvent(self,event):
        # call active plugin
        self.plugins[0].onKeyReleaseEvent(event)

    def toggleSettings(self):
        if self.settingWidget.isVisible():
            self.hideSettings()
        else:
            self.showSettings()

    def showSettings(self):
        self.settingWidget.show()
        self.settingsButton.setStyleSheet(
            parameters.strStyleShowHideButtonLeft.replace("$DataPath",self.DataPath))

    def hideSettings(self):
        self.settingWidget.hide()
        self.settingsButton.setStyleSheet(
            parameters.strStyleShowHideButtonRight.replace("$DataPath", self.DataPath))

    def toggleFunctional(self):
        if self.functionalWiget.isVisible():
            self.hideFunctional()
        else:
            self.showFunctional()

    def showFunctional(self):
        self.functionalWiget.show()
        self.functionalButton.setStyleSheet(
            parameters.strStyleShowHideButtonRight.replace("$DataPath",self.DataPath))

    def hideFunctional(self):
        self.functionalWiget.hide()
        self.functionalButton.setStyleSheet(
            parameters.strStyleShowHideButtonLeft.replace("$DataPath", self.DataPath))

    def skinChange(self):
        if self.config.basic["skin"] == "light": # light
            file = open(self.DataPath + '/assets/qss/style-dark.qss', "r", encoding="utf-8")
            self.config.basic["skin"] = "dark"
        else: # elif self.config.basic["skin"] == 2: # dark
            file = open(self.DataPath + '/assets/qss/style.qss', "r", encoding="utf-8")
            self.config.basic["skin"] = "light"
        self.app.setStyleSheet(file.read().replace("$DataPath", self.DataPath))

    def showAbout(self):
        QMessageBox.information(self, _("About"), helpAbout.strAbout())

    def showUpdate(self, versionInfo):
        versionInt = versionInfo.int()
        if self.config.basic["skipVersion"] and self.config.basic["skipVersion"] >= versionInt:
            return
        msgBox = QMessageBox()
        desc = versionInfo.desc if len(versionInfo.desc) < 300 else versionInfo.desc[:300] + " ... "
        link = '<a href="https://github.com/Neutree/COMTool/releases">github.com/Neutree/COMTool/releases</a>'
        info = '{}<br>{}<br><br>v{}: {}<br><br>{}'.format(_("New versioin detected, please click learn more to download"), link, '{}.{}.{}'.format(versionInfo.major, versionInfo.minor, versionInfo.dev), versionInfo.name, desc)
        learn = msgBox.addButton(_("Learn More"), QMessageBox.YesRole)
        skip = msgBox.addButton(_("Skip this version"), QMessageBox.YesRole)
        nextTime = msgBox.addButton(_("Remind me next time"), QMessageBox.NoRole)
        msgBox.setWindowTitle(_("Need update"))
        msgBox.setText(info)
        result = msgBox.exec_()
        if result == 0:
            auto = autoUpdate.AutoUpdate()
            auto.OpenBrowser()
        elif result == 1:
            self.config.basic["skipVersion"] = versionInt

            

    def autoUpdateDetect(self):
        auto = autoUpdate.AutoUpdate()
        needUpdate, versionInfo = auto.detectNewVersion()
        if needUpdate:
            self.updateSignal.emit(versionInfo)

def gen_tranlate_files(curr_dir):
    try:
        import i18n
    except Exception:
        from COMTool import i18n
    cwd = os.getcwd()
    os.chdir(curr_dir)
    i18n.main("finish")
    os.chdir(cwd)

def load_fonts(paths):
    from PyQt5 import QtGui
    for path in paths:
        id = QtGui.QFontDatabase.addApplicationFont(path)
        fonts = QtGui.QFontDatabase.applicationFontFamilies(id)
        print("load fonts:", fonts)

def main():
    ret = 1
    try:
        while 1:
            # check translate
            curr_dir = os.path.abspath(os.path.dirname(__file__))
            print("curr_dir   ", curr_dir)
            mo_path = os.path.join(curr_dir, "locales", "en", "LC_MESSAGES", "messages.mo")
            if not os.path.exists(mo_path):
                gen_tranlate_files(curr_dir)
            app = QApplication(sys.argv)
            mainWindow = MainWindow(app)
            # path = os.path.join(mainWindow.DataPath, "assets", "fonts", "JosefinSans-Regular.ttf")
            # load_fonts([path])
            print("data path:"+mainWindow.DataPath)
            if(mainWindow.config.basic["skin"] == "light") :# light skin
                file = open(mainWindow.DataPath+'/assets/qss/style.qss',"r", encoding="utf-8")
            else: #elif mainWindow.config == "dark": # dark skin
                file = open(mainWindow.DataPath + '/assets/qss/style-dark.qss', "r", encoding="utf-8")
            qss = file.read().replace("$DataPath",mainWindow.DataPath)
            app.setStyleSheet(qss)
            t = threading.Thread(target=mainWindow.autoUpdateDetect)
            t.setDaemon(True)
            t.start()
            ret = app.exec_()
            if not mainWindow.needRestart:
                print("not mainWindow.needRestart")
                break
    except Exception as e:
        import traceback
        exc = traceback.format_exc()
        show_error(_("Error"), exc)
    return ret

def show_error(title, msg):
    print("error:", msg)
    app = QApplication(sys.argv)
    window = QMainWindow()
    QMessageBox.information(window, title, msg)

if __name__ == '__main__':
    sys.exit(main())

