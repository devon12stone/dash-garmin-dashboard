class User(object):

    def __init__(self,username,password,data):
        self.username = username
        self.password = password
        self.data = data

    def update_username(self,username):
        self.username = username

    def update_password(self,password):
        self.password = password
    
    def update_data(self,data):
        self.data = data