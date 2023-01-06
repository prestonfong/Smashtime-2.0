from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QPushButton, QLabel, QSizePolicy, QLineEdit
import functools
import challonge
import json
from PyQt5.QtCore import Qt

class SignupsUI(QWidget):
    def __init__(self,smashtime):
        super().__init__()
        self.smashtime = smashtime
        self.i = None

        # Create a list of tags
        if not self.smashtime.reg:
            self.smashtime.reg = []

        # Create a dict for phonenumbers
        if not self.smashtime.phonebook:
            self.smashtime.phonebook = {}

        # Create a dict for tags
        if not self.smashtime.tags:
            self.smashtime.tags = {}

        if not self.smashtime.paid:
            self.smashtime.paid = {}
        
        # Create a grid layout with 14 rows and 3 columns
        self.layout = QGridLayout()
        self.layout.setRowStretch(15, 1)
        self.layout.setColumnStretch(9, 1) 
        for i in range(15):
            self.layout.setRowMinimumHeight(i, self.height()//15)
        for i in range(9):
            self.layout.setColumnMinimumWidth(i, self.width()//9)

        # Add start button
        self.startTournament = QPushButton("Start")

        # Connect to signal
        self.smashtime.sig.update.connect(self.decipher)
        
        self.update()

    def decipher(self,data):
        # Load data
        message = json.loads(data)
        sender = message["From"]
        body = message["Body"]

        # Process Message
        if body.lower().strip() == "hello":
            if not self.smashtime.phonebook.get(sender,0):
                self.smashtime.phonebook[sender] = {"phone":sender}
            return self.smashtime.respond(sender, f"Welcome to {self.smashtime.name}\nWhat is your tag?")
        else:
            if not self.smashtime.phonebook.get(sender,0):
                return self.smashtime.respond(sender, f"Message 'hello' to enter the tournament")
            else:
                if not self.smashtime.phonebook[sender].get("tag",0):
                    self.smashtime.phonebook[sender]["tag"] = body
                    self.smashtime.tags[body] = self.smashtime.phonebook[sender]

                    # Add and update
                    self.smashtime.reg.append(body)
                    self.update()

                    return self.smashtime.respond(sender, f'Thanks {self.smashtime.phonebook[sender]["tag"]}, you are registered!')
                else:
                    return self.smashtime.respond(sender, f"You are already registered. Report to TO for problems.")

    def update(self):
        # Remove all Elements
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)

        # Add labels to the first row
        for i in range(-(len(self.smashtime.reg)//-13)):
            paid_label = QLabel("Paid")
            tag_label = QLabel("Tag")
            remove_label = QLabel("Remove")
            self.layout.addWidget(paid_label, 0, i*3)
            self.layout.addWidget(tag_label, 0, i*3+1)
            self.layout.addWidget(remove_label, 0, i*3+2)

        # Iterate over the list of tags
        for i, tag in enumerate(self.smashtime.reg):
            # Add a checkbox to the first column
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(functools.partial(self.paid,tag))
            checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            if tag in self.smashtime.paid:
                checkbox.setChecked(True)
            self.layout.addWidget(checkbox, i%13+1, (i//13)*3)  # add the checkbox to the row i+1 (since the first row is occupied by the labels)
            
            # Add a label with the tag name to the second column
            swap_button = QPushButton(tag)
            swap_button.clicked.connect(functools.partial(self.swap,i))
            if i == self.i:
                swap_button.setEnabled(False)
            self.layout.addWidget(swap_button, i%13+1, (i//13)*3+1)
            
            # Add a button to the third column
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(functools.partial(self.remove,tag)) 
            self.layout.addWidget(remove_button, i%13+1, (i//13)*3+2) 

        # Add name field
        self.new_tag = QLineEdit()
        self.layout.addWidget(self.new_tag, 15, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignBottom)

        # Add adding button
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add)
        self.layout.addWidget(self.add_button, 15, 4,alignment=Qt.AlignmentFlag.AlignBottom)

        # Add seeding button
        self.seed_button = QPushButton("Seed")
        self.seed_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.seed_button.clicked.connect(self.seed)
        self.layout.addWidget(self.seed_button, 15, 8,alignment=Qt.AlignmentFlag.AlignBottom)

        # Add start tournament button
        self.startTournament.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.startTournament, 15, 9,alignment=Qt.AlignmentFlag.AlignBottom)
        self.startTournament.setEnabled(False)

        # Set the layout for the main window
        self.setLayout(self.layout)

        # Save changes
        self.smashtime.save("data/smashtime.json")

    def seed(self):
        # Clear Tournament
        challonge.participants.clear(self.smashtime.id)

        # Add participants
        # participants = [{'name':tag,'seed':i} for i,tag in enumerate(self.smashtime.reg)]
        challonge.participants.bulk_add(self.smashtime.id,names=self.smashtime.reg)

        # Message
        for tag in self.smashtime.reg:
            if self.smashtime.tags[tag].get("phone",0):
                self.smashtime.msg(tag,f"Please check seedings at \nhttps://challonge.com/{self.smashtime.url}")

        self.startTournament.setEnabled(True)

    def add(self):
        # Add new Tag
        if self.new_tag.text():
            self.smashtime.reg.append(self.new_tag.text())
            self.smashtime.tags[self.new_tag.text()] = {"tag": self.new_tag.text()}

            self.update()

    def remove(self,tag):
        # Remove person
        self.smashtime.reg.remove(tag)
        try:
            del self.smashtime.phonebook[self.smashtime.tags[tag]['phone']]
        except:
            pass
        try:
            del self.smashtime.paid[tag]
        except:
            pass
        del self.smashtime.tags[tag]

        # Update
        self.i = None
        self.update()

    def swap(self,i):
        # Set marker
        if self.i == None:
            self.i = i

        # Swap
        else:
            temp = self.smashtime.reg[i]
            self.smashtime.reg[i] = self.smashtime.reg[self.i]
            self.smashtime.reg[self.i] = temp
            self.i = None
        self.update()

    def paid(self,tag,state):
        self.smashtime.paid[tag] = state
