from PyQt5.QtWidgets import  QWidget, QGridLayout,QPushButton, QLabel,QSizePolicy
from PyQt5.QtCore import  Qt
import time
import challonge
import json
import functools

class MatchesUI(QWidget):
    def __init__(self,smashtime):
        super().__init__()
        self.smashtime = smashtime
        self.i = None
        if not self.smashtime.matches:
            self.smashtime.matches = [None for i in range(self.smashtime.setups)]

        # Create a grid layout with 11 columns
        self.row_num = -(self.smashtime.setups//-3)
        self.layout = QGridLayout()
        self.layout.setRowStretch(self.row_num*2+1, 1)
        self.layout.setColumnStretch(11, 1)
        for i in range(self.row_num):
            self.layout.setRowMinimumHeight(i*2 +1, self.height()//(self.row_num*2))
        for i in range(11):
            if i not in {1,5,9}:
                self.layout.setColumnMinimumWidth(i, self.width()//11)

        # Create Finish Button
        self.finish_button = QPushButton("Finish")

        # Connect to signal
        self.smashtime.sig.update.connect(self.decipher)
        
        self.update()

    def decipher(self,data):
        phonebook = self.smashtime.phonebook
        matches = self.smashtime.matches
        ids = self.smashtime.ids

        # Load data
        message = json.loads(data)
        sender = message["From"]
        body = message["Body"]

        # Process Messageself.
        body = body.lower().strip().replace(" ", "")

        if body[0] == "w" or body[0] == "l":
            # Check Valid
            try:
                scores = [int(body[1]),int(body[3])]
            except:
                return self.smashtime.respond(sender, f'Error reporting')

            # Report Match
            id = phonebook[sender]["id"]
            for i in range(len(matches)):
                if id == matches[i]["player1_id"]:
                    if body[0] == "w":
                        # Report
                        challonge.matches.update(self.smashtime.id,matches[i]["id"],scores_csv=str(max(scores)) + "-" + str(min(scores)),winner_id=matches[i]["player1_id"])
                        
                        # Message
                        self.smashtime.msg(ids[matches[i]["player2_id"]],f'Match reported {body[1:]} \nWinner: {ids[matches[i]["player1_id"]]["tag"]}')
                        self.smashtime.respond(sender, f'Match reported {body[1:]} \nWinner:  {ids[matches[i]["player1_id"]]["tag"]}')                 

                    elif body[0] == "l":
                        # Report
                        challonge.matches.update(self.smashtime.id,matches[i]["id"],scores_csv=str(min(scores)) + "-" + str(max(scores)),winner_id=matches[i]["player2_id"])
                        
                        # Message
                        self.smashtime.msg(ids[matches[i]["player2_id"]],f'Match reported {body[1:]} \nWinner:  {ids[matches[i]["player2_id"]]["tag"]}')
                        self.smashtime.respond(sender, f'Match reported {body[1:]} \nWinner:  {ids[matches[i]["player2_id"]]["tag"]}')
                    
                    # Clear and Update
                    self.smashtime.ids[matches[i]["player1_id"]]["time"] = time.time()
                    self.smashtime.ids[matches[i]["player2_id"]]["time"] = time.time()
                    matches[i] = None
                    return self.update()

                elif id == matches[i]["player2_id"]:
                    if body[0] == "w":
                        # Report
                        challonge.matches.update(self.smashtime.id,matches[i]["id"],scores_csv=str(min(scores)) + "-" + str(max(scores)),winner_id=matches[i]["player2_id"])
                        
                        # Message
                        self.smashtime.msg(ids[matches[i]["player1_id"]], f'Match reported {body[1:]} \nWinner:  {ids[matches[i]["player2_id"]]["tag"]}')
                        self.smashtime.respond(sender, f'Match reported {body[1:]} \nWinner:  {ids[matches[i]["player2_id"]]["tag"]}')


                    if body[0] == "l":
                        # Report
                        challonge.matches.update(self.smashtime.id,matches[i]["id"],scores_csv=str(max(scores)) + "-" + str(min(scores)),winner_id=matches[i]["player1_id"])
                        
                        # Message
                        self.smashtime.msg(ids[matches[i]["player1_id"]], f'Match reported {body[1:]} \nWinner:  {ids[matches[i]["player1_id"]]["tag"]}')
                        self.smashtime.respond(sender, f'Match reported {body[1:]} \nWinner:  {ids[matches[i]["player1_id"]]["tag"]}')

                    # Clear and Update
                    self.smashtime.ids[matches[i]["player1_id"]]["time"] = time.time()
                    self.smashtime.ids[matches[i]["player2_id"]]["time"] = time.time()
                    matches[i] = None

                    return self.update()

    def update(self):
        t = time.time()
        matches = self.smashtime.matches
        ids = self.smashtime.ids

        # Remove all Elements
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        
        # Grab all matches. Filter by not in progress
        all_matches = [match for match in challonge.matches.index(self.smashtime.id) if match["state"] == "open" and match["underway_at"] == None]
        
        # Sort by wait time
        all_matches.sort(key=lambda x: ids[x["player1_id"]]["time"] + ids[x["player1_id"]]["time"] - 2*t)

        # Sort by round. Negative are loser"s rounds in double elim
        all_matches.sort(key=lambda x: -x["round"]-.5 if x["round"] < 0 else (x["round"]-1)*2)

        # Assign matches
        for i in range(self.smashtime.setups):
            if matches[i] == None and all_matches:
                match_ = all_matches.pop(0)
                matches[i] = match_
                challonge.matches.mark_as_underway(self.smashtime.id,match_["id"])
                self.smashtime.msg(match_["player1_id"], f'You have a match against {ids[match_["player2_id"]]["tag"]} on setup {i+1}\nReport score using the format either w or l followed by the score\nw 3-2')
                self.smashtime.msg(match_["player2_id"], f'You have a match against {ids[match_["player1_id"]]["tag"]} on setup {i+1}\nReport score using the format either w or l followed by the score\nw 3-2')

        # Create layout
        for i in range(self.smashtime.setups):
            r = i//3
            c = i%3

            # Add Setup
            setup = QLabel(f"Setup {str(i+1)}")
            self.layout.addWidget(setup,r*2,c*4+1,alignment=Qt.AlignmentFlag.AlignHCenter)

            if matches[i]:
                # Add buttons
                win1_button = QPushButton(ids[matches[i]["player1_id"]]["tag"])
                win2_button = QPushButton(ids[matches[i]["player2_id"]]["tag"])
                win1_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                win2_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                win1_button.clicked.connect(functools.partial(self.report,i,1))
                win2_button.clicked.connect(functools.partial(self.report,i,2))
                self.layout.addWidget(win1_button,r*2+1,c*4,alignment=Qt.AlignmentFlag.AlignTop)
                self.layout.addWidget(win2_button,r*2+1,c*4+2,alignment=Qt.AlignmentFlag.AlignTop)
            else: 
                # Add Label
                empty1 = QLabel("Empty")
                self.layout.addWidget(empty1,r*2+1,c*4,alignment=Qt.AlignmentFlag.AlignTop)
                empty2 = QLabel("Empty")
                self.layout.addWidget(empty2,r*2+1,c*4+2,alignment=Qt.AlignmentFlag.AlignTop)

        # Add edit button
        self.edit_button = QPushButton("Edit")
        self.edit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.edit_button, self.row_num*2+1, 10)

        # Add Finish tournament button
        self.finish_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.finish_button, self.row_num*2+1, 11)

        # Set layout
        self.setLayout(self.layout)

        self.smashtime.save("data/smashtime.json")

    def report(self,i,winner):
        matches = self.smashtime.matches

        # Report
        if winner == 1:
            challonge.matches.update(self.smashtime.id, matches[i]["id"],scores_csv="1-0",winner_id=matches[i]["player1_id"])
        else:
            challonge.matches.update(self.smashtime.id, matches[i]["id"],scores_csv="0-1",winner_id=matches[i]["player2_id"])

        # Clear and Update
        self.smashtime.ids[matches[i]["player1_id"]]["time"] = time.time()
        self.smashtime.ids[matches[i]["player2_id"]]["time"] = time.time()
        matches[i] = None

        return self.update()

