import re


class Verification:
    @staticmethod
    def is_password_valid(password):
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        return bool(re.match(pattern, password))

    @staticmethod
    def is_phone_valid(phone):
        pattern = r"^(00989|\+989|09)[0-9]{9}$"
        return bool(re.match(pattern, phone))

    @staticmethod
    def is_email_valid(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def is_username_valid(username):
        pattern = r"^[A-Za-z0-9_]{6,16}$"
        return bool(re.match(pattern, username))
