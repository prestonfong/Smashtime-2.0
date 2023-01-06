# Smashtime 2.0
Project expansion from [Chris Pak's smashtime](https://github.com/jpak1996/smashtime)

Fully automates double elimination bracket through text messages

GUI for setup, signups, match assignments, and reporting

## Getting Started

### Requirements
```
Flask==2.2.2
pychallonge==1.11.5
PyQt5==5.15.7
twilio==7.16.0
```

Need to add the following code into pychallonge challonge.participants
```
def clear(tournament):
    """Deletes all participants in a tournament. (Only allowed if tournament hasn't started yet)"""

    api.fetch("DELETE", "tournaments/%s/participants/clear" % (tournament))
```
### Challonge
Need Challonge Account and API key
* https://api.challonge.com/v1

### Twilio
Need Twilio Account for SID, Auth
Need to buy a phone number
* https://www.twilio.com/

### Hosting
Need to be able to host webhook for Twilio
* https://ngrok.com/

### Data
You can fill out all these fields in the default.json file so you do not have to add info everytime. Smashtime.json is there to save progress if program crashes. You can restart from any part in tournament.

## Executing
* Start Webhook
```
$ Ngrok http 5000
```
* Copy Forwarding Address
* Connect with Twilio phone number 

![twilio](https://github.com/prestonfong/smashtime-2.0/blob/main/tutorial_img/Twilio.png?raw=true)
* Run main.py
```
python main.py
```
* Reset to load default.json

![setup](https://github.com/prestonfong/smashtime-2.0/blob/main/tutorial_img/setup.png?raw=true)

* Text hello to enter tournament or enter manually
* Can swap seeds by clicking the tags

![signins](https://github.com/prestonfong/smashtime-2.0/blob/main/tutorial_img/signups.png?raw=true)

* Report using text messages or manually by clicking button

![matches](https://github.com/prestonfong/smashtime-2.0/blob/main/tutorial_img/matches.png?raw=true)

![matches](https://github.com/prestonfong/smashtime-2.0/blob/main/tutorial_img/msg.png?raw=true)



