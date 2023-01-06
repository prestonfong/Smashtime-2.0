import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMessageBox, QMainWindow
import json
from smash.smashtime import Smashtime
import challonge
from twilio.rest import Client
from smash.setupUI import SetupUI, ContinueUI
from smash.signupsUI import SignupsUI
from smash.matchesUI import MatchesUI
import time
import subprocess
import socket
import threading

class Signal(QObject):
    update = pyqtSignal(str)

class MainWindow(QMainWindow):
    def __init__(self,):
        super().__init__()

        # Set Window Title
        self.setWindowTitle("Smashtime 2.0")

        # Load Smashtime
        self.smashtime = Smashtime().load("data/smashtime.json")

        # Resize
        desktop = QDesktopWidget().screenGeometry()
        width, height = desktop.width(), desktop.height()
        self.resize(width // 2, height // 2)
        self.move((width - self.width()) // 2, (height - self.height()) // 2)

        # Set stylesheet
        with open("StyleSheets/MacOS.qss", "r") as f:
            style = f.read()
        app.setStyleSheet(style)

        # Close programs
        self.p = None
        self.closeEvent = self.close

        # Begin GUI
        if self.smashtime.id:
            self.startContinueUI()
        else:
            self.startSetupUI()

    def startContinueUI(self):
        # Open continue option
        self.continueTab = ContinueUI(self.smashtime)
        self.setCentralWidget(self.continueTab)

        # Connect buttons
        self.continueTab.reset_button.clicked.connect(self.reset_clicked)
        self.continueTab.cont_button.clicked.connect(self.continue_clicked)
        self.show()

    def startSetupUI(self):

        # Open setup page
        self.setupTab = SetupUI(self.smashtime)
        self.setCentralWidget(self.setupTab)

        # Connect Buttons
        self.setupTab.reset_button.clicked.connect(self.reset_clicked)
        self.setupTab.submit_button.clicked.connect(self.submit_clicked)
        self.show()

    def startSignupsUI(self):
        # Start Coms
        self.startComs()

        # Open Signup page
        self.signupTab = SignupsUI(self.smashtime)
        self.setCentralWidget(self.signupTab)

        # Connect Buttons
        self.signupTab.startTournament.clicked.connect(self.startTournament_clicked)
        self.show()

    def startTournamentUI(self):
        # Open Matches page
        self.matchesTab = MatchesUI(self.smashtime)
        self.setCentralWidget(self.matchesTab)

        # Connect Buttons
        self.matchesTab.finish_button.clicked.connect(self.finish_clicked)
        self.show()
        
    def reset_clicked(self):
        # New tournament
        with open("data/default.json","r") as f:
            data = json.load(f)
        self.smashtime = Smashtime(data)

        # Reload setup page
        self.startSetupUI()

    def continue_clicked(self):
        # If continue, 
        challonge.set_credentials(self.smashtime.username,self.smashtime.api)
        self.smashtime.client = Client(self.smashtime.twilSID,self.smashtime.twilAuth)

        if self.smashtime.started:
            self.startComs()
            self.startTournamentUI()
        else:
            self.startSignupsUI()
    
    def submit_clicked(self):
        name = self.smashtime.name.text()
        api_key = self.smashtime.api.text()
        username = self.smashtime.username.text()
        twilSID = self.smashtime.twilSID.text()
        twilAuth = self.smashtime.twilAuth.text()
        twilNum = self.smashtime.twilNum.text()

        # Test Input Fields
        try:
            setups = int(self.smashtime.setups.text())
            if not name or not api_key or not username or not setups or not twilSID or not twilAuth or not twilNum:
                raise ValueError

            # Test Twilio credentials
            try:
                self.smashtime.client = Client(twilSID,twilAuth)
                self.smashtime.client.messages.create(to="+15005550006",from_=twilNum,body="test")

            except:
                QMessageBox.warning(self, "Error", "Twilio Credentials incorrect")
                return

            # Test Challonge Credentials
            try:
                challonge.set_credentials(username,api_key)
                tournament = challonge.tournaments.create(name,tournament_type="double elimination",url=None)
                self.smashtime.name = name
                self.smashtime.api = api_key
                self.smashtime.username = username
                self.smashtime.twilSID = twilSID
                self.smashtime.twilAuth = twilAuth
                self.smashtime.twilNum = twilNum
                self.smashtime.setups = setups
                self.smashtime.id = tournament["id"]
                self.smashtime.url = tournament["url"]
                self.smashtime.save("data/smashtime.json")

                return self.startSignupsUI()

            except:
                QMessageBox.warning(self, "Error", "Challonge Credentials incorrect")
                return

        except:
            QMessageBox.warning(self, "Error", "Fields are not filled out correctly")
            return

    def finish_clicked(self):
        challonge.tournaments.finalize(self.smashtime.id)
        self.startSetupUI()

    def startTournament_clicked(self):
        # Check for all Participants
        if len(challonge.participants.index(self.smashtime.id)) != len(self.smashtime.reg):
            print("error")
            QMessageBox.warning(self, "Error", "Not all participants have been added")
            return

        # Check for paid
        for k,v in self.smashtime.paid.items():
            if not v:
                QMessageBox.warning(self, "Error", "Everyone has not paid")
                return
        
        # Start Tournament
        challonge.tournaments.start(self.smashtime.id)
        self.smashtime.started = True
        for tag in self.smashtime.reg:
            if self.smashtime.tags[tag].get("phone",0):
                self.smashtime.msg(tag,f"The tournament has started. Please end friendlies and wait for your match. Good luck!")
        
        # Disconnect the socket listener
        self.smashtime.sig.disconnect()

        # Populate the participants info
        participants = challonge.participants.index(self.smashtime.id)

        # Create lookup for ids
        self.smashtime.ids = {}
        for i in range(len(participants)):
            self.smashtime.tags[participants[i]["name"]]["id"] = participants[i]["id"]
            self.smashtime.tags[participants[i]["name"]]["time"] = time.time()
            self.smashtime.ids[int(participants[i]["id"])] = self.smashtime.tags[participants[i]["name"]]
        self.smashtime.save("data/smashtime.json")

        self.startTournamentUI()

    def startComs(self):
        # Set up communications for flask api post
        self.p = subprocess.Popen(r"python twilioServer.py",shell = False)
        self.smashtime.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.smashtime.sock.bind(("127.0.0.1", 5001))

        # Open signal to read data
        self.smashtime.sig = Signal()
        self.thread = threading.Thread(target=self.recieve)
        self.thread.daemon = True
        self.thread.start()

    def recieve(self):              
        while True:
            data, _ = self.smashtime.sock.recvfrom(1024)
            data = data.decode()
            self.smashtime.sig.update.emit(data)   

    def close(self,event):
        if self.p:
            subprocess.Popen.kill(self.p)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())