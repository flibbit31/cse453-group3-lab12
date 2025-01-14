########################################################################
# COMPONENT:
#    INTERACT
# Author:
#    Br. Helfrich, Kyle Mueller, <your name here if you made a change>
# Summary: 
#    This class allows one user to interact with the system
########################################################################

import messages, control

###############################################################
# USER
# User has a name and a password
###############################################################
class User:
    def __init__(self, name, password, subject_control):
        self.name = name
        self.password = password
        self.subject_control = subject_control

userlist = [
   [ "AdmiralAbe",     "password", control.SecurityLevel.Secret ],  
   [ "CaptainCharlie", "password", control.SecurityLevel.Privileged ], 
   [ "SeamanSam",      "password", control.SecurityLevel.Confidential ],
   [ "SeamanSue",      "password", control.SecurityLevel.Confidential ],
   [ "SeamanSly",      "password", control.SecurityLevel.Confidential ]
]

###############################################################
# USERS
# All the users currently in the system
###############################################################
users = [*map(lambda u: User(*u), userlist)]

ID_INVALID = -1

######################################################
# INTERACT
# One user interacting with the system
######################################################
class Interact:

    ##################################################
    # INTERACT CONSTRUCTOR
    # Authenticate the user and get him/her all set up
    ##################################################
    def __init__(self, username, password, messages):
        if self._authenticate(username, password) != -1:
            self._username = username
            self._subject_control = self._subject_control_from_user(username)
            self._p_messages = messages
            self._valid = True
        else:
            print("Incorrect username or password.")  
            self._valid = False

    ##################################################
    # INTERACT :: SHOW
    # Show a single message
    ##################################################
    def show(self):
        id_ = self._prompt_for_id("display")
        message = self._p_messages.find_by_id(id_)
        if not(message and control.securityConditionRead(self._p_messages.find_by_id(id_).text_control, self._subject_control) and self._p_messages.show(id_)):
            print(f"ERROR! Message ID \'{id_}\' could not be read.")
         
        print()

    ##################################################
    # INTERACT :: DISPLAY
    # Display the set of messages
    ################################################## 
    def display(self):
        print("Messages:")
        for m in self._p_messages._messages:
            if control.securityConditionRead(m.text_control, self._subject_control):
                m.display_properties()
        print()

    ##################################################
    # INTERACT :: ADD
    # Add a single message
    ################################################## 
    def add(self):
        print(f"Security levels: Public, Confidential, Privileged, or Secret")
        try:
            self._p_messages.add(control.SecurityLevel[self._prompt_for_line("Security Level")],
                             self._prompt_for_line("message"),
                             self._username,
                             self._prompt_for_line("date"))
        except:
            print(f"ERROR! invalid security level. Must be: Public, Confidential, Privileged, or Secret")

    ##################################################
    # INTERACT :: UPDATE
    # Update a single message
    ################################################## 
    def update(self):
        id_ = self._prompt_for_id("update")
        if control.securityConditionWrite(self._p_messages.find_by_id(id_).text_control, self._subject_control) and not self._p_messages.show(id_):
            print(f"ERROR! Message ID \'{id_}\' does not exist\n")
            return
        self._p_messages.update(id_, self._prompt_for_line("message"))
        print()
            
    ##################################################
    # INTERACT :: REMOVE
    # Remove one message from the list
    ################################################## 
    def remove(self):
        id_ = self._prompt_for_id("delete")
        if control.securityConditionRead(self._p_messages.find_by_id(id_).text_control, self._subject_control):
            self._p_messages.remove(id_)

    ##################################################
    # INTERACT :: PROMPT FOR LINE
    # Prompt for a line of input
    ################################################## 
    def _prompt_for_line(self, verb):
        return input(f"Please provide a {verb}: ")

    ##################################################
    # INTERACT :: PROMPT FOR ID
    # Prompt for a message ID
    ################################################## 
    def _prompt_for_id(self, verb):
        return int(input(f"Select the message ID to {verb}: "))

    ##################################################
    # INTERACT :: AUTHENTICATE
    # Authenticate the user: find their control level
    ################################################## 
    def _authenticate(self, username, password):
        id_ = self._id_from_user(username)
        return ID_INVALID != id_ and password == users[id_].password
        
    ##################################################
    # INTERACT :: SUBJECT CONTROL FROM USER
    # Find the subject control of a given user
    ##################################################
    def _subject_control_from_user(self, username):
        for id_user in range(len(users)):
            if username == users[id_user].name:
                return users[id_user].subject_control
        return ID_INVALID #Should we be returning ID_INVALID here?
        
    ##################################################
    # INTERACT :: ID FROM USER
    # Find the ID of a given user
    ################################################## 
    def _id_from_user(self, username):
        for id_user in range(len(users)):
            if username == users[id_user].name:
                return id_user
        return ID_INVALID

#####################################################
# INTERACT :: DISPLAY USERS
# Display the set of users in the system
#####################################################
def display_users():
    for user in users:
        print(f"\t{user.name}")
