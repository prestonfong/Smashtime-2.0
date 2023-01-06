import json

class Smashtime(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def save(self,file):
        # Save progress
        with open(file, 'w') as f:
            json.dump(self, f,default=lambda o: False)
        f.close()

    def load(self,file):
        try:
            # Open File
            with open(file, 'r') as f:
                data = json.load(f)
            s = Smashtime(data)
            f.close()

            # Reconnect Pointers
            if s.reg:
                if s.ids:
                    s.ids = {s.tags[tag]['id']: s.tags[tag] for tag in s.reg}
                s.phonebook = {s.tags[tag]['phone']: s.tags[tag] for tag in s.reg if s.tags[tag].get('phone',0)}

            return s
        except:
            return Smashtime({"username":"",
                    "api":"",
                    "twilSID":"",
                    "twilAuth":"",
                    "twilNum":"",
                    "TO": ""})

    def respond(self,num,message):
        # Respond to Message
        return self.client.messages.create(to=num,from_=self.twilNum,body=message)

    def msg(self,id,message):

        # Look up Phone number
        try:
            num = self.ids[id]['phone']
        except:
            try:
                num = self.tags[id]['phone']
            except:
                return

        # Create Message
        return self.client.messages.create(to=num,from_=self.twilNum,body=message)
