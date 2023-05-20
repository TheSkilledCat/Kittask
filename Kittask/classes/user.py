######################################
#   Basic model of the User object   #
######################################

class User:
    def __init__(self, fullname: str, phone: str, password: str, email: str = None):
        self.fullname = fullname
        self.phone = phone
        self.password = password
        self.email = email

    def __str__(self):
        return f"""
                Full name: {self.fullname} 
                Phone: {self.phone}
                Email: {self.email}
                """
