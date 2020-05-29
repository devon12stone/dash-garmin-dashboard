class User(object):

    def __init__(self,username,password,data,status):
        self.username = username
        self.password = password
        self.data = data
        self.status = status

    # functions to be used to edit the current user at login in and log out
    def update_username(self,username):
        self.username = username

    def update_password(self,password):
        self.password = password
    
    def update_data(self,data):
        self.data = data
    
    def update_status(self,status):
        self.status = status