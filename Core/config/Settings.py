from PyQt4.QtGui import *
from xml.dom import minidom
from PyQt4.QtCore import *
from re import search

"""
Description:
    This program is a module for wifi-pumpkin.py.

Copyright:
    Copyright (C) 2015 Marcos Nesster P0cl4bs Team
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

class frm_Settings(QDialog):
    def __init__(self, parent = None):
        super(frm_Settings, self).__init__(parent)
        self.setWindowTitle('Settings WiFi-Pompkin')
        self.Main = QVBoxLayout()
        self.frm = QFormLayout()
        self.setGeometry(0, 0, 420, 300)
        self.center()
        self.loadtheme(self.XmlThemeSelected())
        self.Qui()

    def loadtheme(self,theme):
        sshFile=("Core/%s.qss"%(theme))
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

    def XmlThemeSelected(self):
        theme = self.xmlSettings('themes', 'selected',None,False)
        return theme
    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def xmlSettings(self,id,data,bool,show=False):
        xmldoc = minidom.parse('Core/config/Settings.xml')
        country = xmldoc.getElementsByTagName(id)
        firstchild = country[0]
        if bool != None:
            firstchild.attributes[data].value = bool
        xmldoc.writexml( open('Core/config/Settings.xml', 'w'))

        return firstchild.attributes[data].value

    def save_settings(self):
        if self.AP_0.isChecked():
            self.xmlSettings('accesspoint','actived','hostapd',False)
        elif self.AP_1.isChecked():
            self.xmlSettings('accesspoint','actived','airbase-ng',False)
        if self.d_scapy.isChecked():
            self.xmlSettings('deauth','select','packets_scapy',False)
        elif self.d_mdk.isChecked():
            self.xmlSettings('deauth','select','packets_mdk3',False)

        if self.scan_scapy.isChecked():
            self.xmlSettings('scanner_AP', 'select', 'scan_scapy',False)
        elif self.scan_airodump.isChecked():
            self.xmlSettings('scanner_AP', 'select', 'scan_airodump', False)

        if self.dhcp1.isChecked():
            self.xmlSettings('dhcp','dhcp_server','iscdhcpserver',False)
        elif self.dhcp2.isChecked():
            self.xmlSettings('dhcp','dhcp_server','dnsmasq',False)
        if self.theme1.isChecked():
            self.xmlSettings('themes','selected','themes/theme1',False)
        elif self.theme2.isChecked():
            self.xmlSettings('themes','selected','themes/theme2',False)
        if self.scan1.isChecked():
            self.xmlSettings('advanced','Function_scan','Ping',False)
        elif self.scan2.isChecked():
            self.xmlSettings('advanced','Function_scan','Nmap',False)
        self.txt_arguments.setText(self.xmlSettings('mdk3', 'arguments', str(self.txt_arguments.text()), False))
        self.txt_ranger.setText(self.xmlSettings('scan','rangeIP',str(self.txt_ranger.text()),False))
        self.interface.setText(self.xmlSettings('interface', 'monitor_mode', str(self.interface.text()), False))
        self.Apname.setText(self.xmlSettings('AP', 'name', str(self.Apname.text()), False))
        self.xmlSettings('channel', 'mchannel', str(self.channel.value()), False)
        self.xmlSettings('redirect', 'port', str(self.redirectport.text()), False)
        self.xmlSettings('netcreds', 'interface', str(self.InterfaceNetCreds.text()), False)
        with open('Core/config/hostapd/hostapd+.conf','w') as apconf:
            apconf.write(self.ListHostapd.toPlainText())
        self.close()


    def listItemclicked(self,pos):
        item = self.ListRules.selectedItems()
        self.listMenu= QMenu()
        menu = QMenu()
        additem = menu.addAction('Add')
        editem = menu.addAction('Edit')
        removeitem = menu.addAction('Remove ')
        clearitem = menu.addAction('clear')
        action = menu.exec_(self.ListRules.viewport().mapToGlobal(pos))
        if action == removeitem:
            if item != []:
                self.ListRules.takeItem(self.ListRules.currentRow())
        elif action == additem:
            text, resp = QInputDialog.getText(self, 'Add rules iptables',
            'Enter the rules iptables:')
            if resp:
                try:
                    itemsexits = []
                    for index in xrange(self.ListRules.count()):
                        itemsexits.append(str(self.ListRules.item(index).text()))
                    for i in itemsexits:
                        if search(str(text),i):
                            QMessageBox.information(self,'Rules exist','this rules already exist!')
                            return
                    item = QListWidgetItem()
                    item.setText(text)
                    item.setSizeHint(QSize(30,30))
                    self.ListRules.addItem(item)
                except Exception as e:
                    QMessageBox.information(self,'error',str(e))
                    return
        elif action == editem:
            text, resp = QInputDialog.getText(self, 'Add rules iptables',
            'Enter the rules iptables:',text=self.ListRules.item(self.ListRules.currentRow()).text())
            if resp:
                try:
                    itemsexits = []
                    for index in xrange(self.ListRules.count()):
                        itemsexits.append(str(self.ListRules.item(index).text()))
                    for i in itemsexits:
                        if search(str(text),i):
                            QMessageBox.information(self,'Rules exist','this rules already exist!')
                            return
                    item = QListWidgetItem()
                    item.setText(text)
                    item.setSizeHint(QSize(30,30))
                    self.ListRules.insertItem(self.ListRules.currentRow(),item)
                except Exception as e:
                    QMessageBox.information(self,'error',str(e))
                    return
        elif action == clearitem:
            self.ListRules.clear()

    def redirectAP(self):
        item = QListWidgetItem()
        if self.check_redirect.isChecked():
            item.setText('iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1:80')
            item.setSizeHint(QSize(30,30))
            self.ListRules.addItem(item)
            return
        rules = []
        for index in xrange(self.ListRules.count()):
            rules.append(str(self.ListRules.item(index).text()))
        for i,j in enumerate(rules):
            if search('--to-destination 10.0.0.1:80',j):
                self.ListRules.takeItem(i)
    def Qui(self):
        self.form = QFormLayout(self)
        self.tabcontrol = QTabWidget(self)

        # tabs
        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)
        self.tab4 = QWidget(self)

        self.page_1 = QFormLayout(self.tab1)
        self.page_2 = QFormLayout(self.tab2)
        self.page_3 = QFormLayout(self.tab3)
        self.page_4 = QFormLayout(self.tab4)

        self.tabcontrol.addTab(self.tab1, 'General')
        self.tabcontrol.addTab(self.tab2, 'Advanced')
        self.tabcontrol.addTab(self.tab3,'Iptables')
        self.tabcontrol.addTab(self.tab4,'hostpad')

        self.btn_save = QPushButton('Save')
        self.btn_save.clicked.connect(self.save_settings)
        self.btn_save.setFixedWidth(80)
        self.btn_save.setIcon(QIcon('Icons/Save.png'))

        self.GruPag0=QButtonGroup()
        self.GruPag1=QButtonGroup()
        self.GruPag2=QButtonGroup()
        self.GruPag3=QButtonGroup()
        self.GruPag4=QButtonGroup()

        self.gruButtonPag2 = QButtonGroup()
        #page general

        self.AP_0 = QRadioButton('hostapd')
        self.AP_1 = QRadioButton('airbase-ng')
        self.AP_1.setEnabled(False)
        self.d_scapy = QRadioButton('Scapy Deauth')
        self.d_mdk = QRadioButton('mdk3 Deauth')
        self.scan_scapy = QRadioButton('Scan from scapy')
        self.scan_airodump = QRadioButton('Scan from airodump-ng')
        self.dhcp1 = QRadioButton('iscdhcpserver')
        self.dhcp2 = QRadioButton('dnsmasq')
        self.dhcp2.setDisabled(True)
        self.theme1 = QRadioButton('theme Dark Orange')
        self.theme2 = QRadioButton('theme Dark blur')

        #page Adavanced
        self.txt_ranger = QLineEdit(self)
        self.txt_arguments = QLineEdit(self)
        self.scan1 = QRadioButton('Ping Scan:: Very fast scan IP')
        self.scan2 = QRadioButton('Python-Nmap:: Get hostname from IP')
        self.interface = QLineEdit(self)
        self.Apname =  QLineEdit(self)
        self.channel = QSpinBox(self)
        self.redirectport = QLineEdit(self)
        self.InterfaceNetCreds = QLineEdit(self)

        # page Iptables
        self.ListRules = QListWidget(self)
        self.ListRules.setFixedHeight(300)
        self.ListRules.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ListRules.setMinimumWidth(self.ListRules.sizeHintForColumn(100))
        self.ListRules.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ListRules.connect(self.ListRules,
        SIGNAL('customContextMenuRequested(QPoint)'),
        self.listItemclicked)
        for i in range(4):
            j = self.xmlSettings('rules'+str(i),'value',None,False)
            item = QListWidgetItem()
            item.setText(j)
            item.setSizeHint(QSize(30,30))
            self.ListRules.addItem(item)
        self.check_redirect = QCheckBox('add Redirect all Port 80 to ipaddress::10.0.0.1')
        self.check_redirect.clicked.connect(self.redirectAP)

        # page hostpad
        self.ListHostapd = QTextEdit(self)
        self.ListHostapd.setFixedHeight(300)
        with open('Core/config/hostapd/hostapd+.conf','r') as apconf:
            self.ListHostapd.setText(apconf.read())

        #grup page 1
        self.GruPag0.addButton(self.AP_0)
        self.GruPag0.addButton(self.AP_1)
        self.GruPag1.addButton(self.d_scapy)
        self.GruPag1.addButton(self.d_mdk)
        self.GruPag2.addButton(self.dhcp1)
        self.GruPag2.addButton(self.dhcp2)
        self.GruPag3.addButton(self.scan_scapy)
        self.GruPag3.addButton(self.scan_airodump)
        self.GruPag4.addButton(self.theme1)
        self.GruPag4.addButton(self.theme2)

        # grup page 2
        self.gruButtonPag2.addButton(self.scan1)
        self.gruButtonPag2.addButton(self.scan2)

        #page 1
        self.AP_check = self.xmlSettings('accesspoint','actived',None,False)
        self.deauth_check = self.xmlSettings('deauth','select',None,False)
        self.scan_AP_check = self.xmlSettings('scanner_AP', 'select', None, False)
        self.dhcp_check = self.xmlSettings('dhcp', 'dhcp_server', None, False)
        self.txt_ranger.setText(self.xmlSettings('scan', 'rangeIP', None, False))
        self.txt_arguments.setText(self.xmlSettings('mdk3', 'arguments', None, False))

        # setting page 1
        self.scanIP_selected  = self.xmlSettings('advanced','Function_scan',None,False)
        if self.scanIP_selected == 'Ping':
            self.scan1.setChecked(True)
            self.scan2.setChecked(False)
        elif self.scanIP_selected == 'Nmap':
            self.scan2.setChecked(True)
            self.scan1.setChecked(False)
        if self.AP_check == "hostapd":self.AP_0.setChecked(True)
        elif self.AP_check == "airbase-ng":self.AP_1.setChecked(True)

        if self.deauth_check == 'packets_mdk3':self.d_mdk.setChecked(True)
        else:self.d_scapy.setChecked(True)

        if self.dhcp_check == 'iscdhcpserver':self.dhcp1.setChecked(True)
        else:self.dhcp2.setChecked(True)

        if self.scan_AP_check == 'scan_scapy': self.scan_scapy.setChecked(True)
        else:self.scan_airodump.setChecked(True)

        self.theme_selected = self.xmlSettings('themes', 'selected', None, False)
        if self.theme_selected == 'themes/theme1':
            self.theme1.setChecked(True)
        else:
            self.theme2.setChecked(True)

        # tab general
        self.page_1.addRow(QLabel('AccessPoint:'))
        self.page_1.addRow(self.AP_0)
        self.page_1.addRow(self.AP_1)
        self.page_1.addRow(QLabel('Deauth Options:'))
        self.page_1.addRow(self.d_scapy)
        self.page_1.addRow(self.d_mdk)
        self.page_1.addRow(QLabel('Scan diveces:'))
        self.page_1.addRow(self.scan_scapy)
        self.page_1.addRow(self.scan_airodump)
        self.page_1.addRow(QLabel('DHCP:'))
        self.page_1.addRow(self.dhcp1)
        self.page_1.addRow(self.dhcp2)
        self.page_1.addRow(QLabel('Pumpkin Themes:'))
        self.page_1.addRow(self.theme1)
        self.page_1.addRow(self.theme2)

        #settings tab Advanced
        self.interface.setText(self.xmlSettings('interface', 'monitor_mode', None, False))
        self.Apname.setText(self.xmlSettings('AP', 'name', None, False))
        self.channel.setValue(int(self.xmlSettings('channel', 'mchannel', None, False)))
        self.redirectport.setText(self.xmlSettings('redirect', 'port', None, False))
        self.InterfaceNetCreds.setText(self.xmlSettings('netcreds', 'interface', None, False))
        #add tab Advanced
        self.page_2.addRow(QLabel('Thread ScanIP:'))
        self.page_2.addRow(self.scan1)
        self.page_2.addRow(self.scan2)
        self.page_2.addRow('Interface Monitor:',self.interface)
        self.page_2.addRow('AP Name:',self.Apname)
        self.page_2.addRow('Channel:',self.channel)
        self.page_2.addRow('Port sslstrip:',self.redirectport)
        self.page_2.addRow('NetCreds Interface:',self.InterfaceNetCreds)
        self.page_2.addRow(QLabel('mdk3 Args:'),self.txt_arguments)
        self.page_2.addRow(QLabel('Range ARP Posion:'),self.txt_ranger)

        #add tab iptables
        self.page_3.addWidget(QLabel('Iptables:'))
        self.page_3.addRow(self.ListRules)
        self.page_3.addRow(self.check_redirect)

        #add tab hostpad
        self.page_4.addWidget(QLabel('Settings hostapd:'))
        self.page_4.addRow(self.ListHostapd)

        self.form.addRow(self.tabcontrol)
        self.form.addRow(self.btn_save)
        self.Main.addLayout(self.form)
        self.setLayout(self.Main)
