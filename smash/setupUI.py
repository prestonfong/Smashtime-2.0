from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt

class SetupUI(QWidget):
    def __init__(self,smashtime):
        super().__init__()
        
        # Create the input fields and labels
        name_label = QLabel("Tournament Name:")
        smashtime.name = QLineEdit()
        api_key_label = QLabel("Challonge API key:")
        smashtime.api = QLineEdit(smashtime.api)
        username_label = QLabel("Challone Username:")
        smashtime.username = QLineEdit(smashtime.username)
        setups_label = QLabel("Number of Setups:")
        smashtime.setups = QLineEdit()
        twilSID_label = QLabel("Twilio SID:")
        smashtime.twilSID = QLineEdit(smashtime.twilSID)
        twilAuth_label = QLabel("Twilio Auth Token:")
        smashtime.twilAuth = QLineEdit(smashtime.twilAuth)
        twilNum_label = QLabel("Twilio Number use:")
        smashtime.twilNum = QLineEdit(smashtime.twilNum)

        # Set the size policy of the input fields and labels to expanding
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        smashtime.name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        api_key_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        smashtime.api.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        username_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        smashtime.username.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        setups_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        smashtime.setups.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        twilSID_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        smashtime.twilSID.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        twilAuth_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        smashtime.twilAuth.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        twilNum_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        smashtime.twilNum.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the font size of the input fields to be proportional to the size of the input fields
        font = QFont()
        font.setPointSize(14)
        smashtime.name.setFont(font)
        smashtime.api.setFont(font)
        smashtime.username.setFont(font)
        smashtime.setups.setFont(font)
        smashtime.twilSID.setFont(font)
        smashtime.twilAuth.setFont(font)
        smashtime.twilSID.setFont(font)
        smashtime.twilNum.setFont(font)

        # Create the submit button and connect it to the submit_clicked function
        self.submit_button = QPushButton("Submit")
        self.submit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create a vertical layout for the input fields and labels
        layout = QVBoxLayout()

        # Create a horizontal layout for each input field and label
        name_layout = QVBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(smashtime.name)
        layout.addLayout(name_layout)

        setups_layout = QVBoxLayout()
        setups_layout.addWidget(setups_label)
        setups_layout.addWidget(smashtime.setups)
        layout.addLayout(setups_layout)

        api_key_layout = QVBoxLayout()
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(smashtime.api)
        layout.addLayout(api_key_layout)

        username_layout = QVBoxLayout()
        username_layout.addWidget(username_label)
        username_layout.addWidget(smashtime.username)
        layout.addLayout(username_layout)

        twilSID_layout = QVBoxLayout()
        twilSID_layout.addWidget(twilSID_label)
        twilSID_layout.addWidget(smashtime.twilSID)
        layout.addLayout(twilSID_layout)

        twilAuth_layout = QVBoxLayout()
        twilAuth_layout.addWidget(twilAuth_label)
        twilAuth_layout.addWidget(smashtime.twilAuth)
        layout.addLayout(twilAuth_layout)

        twilNum_layout = QVBoxLayout()
        twilNum_layout.addWidget(twilNum_label)
        twilNum_layout.addWidget(smashtime.twilNum)
        layout.addLayout(twilNum_layout)

        # Create a horizontal layout for the submit button
        submit_layout = QHBoxLayout()
        submit_layout.addStretch()
        submit_layout.addWidget(self.reset_button)
        submit_layout.addWidget(self.submit_button)
        layout.addLayout(submit_layout)

        self.setLayout(layout)

class ContinueUI(QWidget):
    def __init__(self,smashtime):
        super().__init__()
        self.cont_button = QPushButton(f"Continue {smashtime.name}?")
        self.reset_button = QPushButton(f"New Tournament?")

        # Set the size policy of the buttons to expanding
        self.cont_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.reset_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the font size of the buttons
        font = QFont()
        font.setPointSize(30)
        self.cont_button.setFont(font)
        self.reset_button.setFont(font)

        # Create a horizontal layout for the buttons
        layout = QHBoxLayout()
        layout.addWidget(self.cont_button)
        layout.addWidget(self.reset_button)

        # Set the form layout as the main layout of the window
        self.setLayout(layout)



