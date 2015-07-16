import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QGuiApplication, QIcon
from paramiko import SSHClient
from scp import SCPClient
import paramiko
from datetime import date
import time
import configparser

class Screenshoter:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('linux_screenshoter.cfg')
        self.ssh_hostname=config.get('ssh', 'hostname')
        self.ssh_port=int(config.get('ssh', 'port'))
        self.ssh_username=config.get('ssh', 'username')
        self.ssh_remote_path=config.get('ssh', 'remote_path')


    def handle_click(self, reason):
        if reason != QSystemTrayIcon.Trigger:
            return

        QGuiApplication.primaryScreen().grabWindow(0).save('scr.jpg', 'jpg')
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(hostname=self.ssh_hostname, port=self.ssh_port, username=self.ssh_username)
        scp = SCPClient(ssh.get_transport())
        dest_name = time.strftime("screenshot_%Y%m%d_%H%M%S.jpg", time.localtime())
        scp.put('scr.jpg', self.ssh_remote_path + '/' + dest_name)



app = QApplication(sys.argv)
icon = QIcon('icon.png')
tray = QSystemTrayIcon(icon)
tray.show()
trayMenu = QMenu()
quitAction = QAction("&Quit", trayMenu, triggered=QApplication.instance().quit)
trayMenu.addAction(quitAction)

tray.setContextMenu(trayMenu)
screenshoter = Screenshoter()
tray.activated.connect(screenshoter.handle_click)
app.exec()

