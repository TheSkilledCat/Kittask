#####################################################################################
# Project "Task Manager/To Do List" Level B
# Parsa Sheikh Ansari - 10/6
#####################################################################################
import random

from classes.database import Database as db, Database
from classes.session import Session, Admin_Session
from classes.session_cli import Session_CLI
from classes.verification import Verification


from kavenegar import *
import re


class CLI:

    
    def __init__(self):
        self.session = None
        self.db = Database()

    def run(self):
        while True:
            commands = ['Login', 'Sign up', 'Quit']
            print("+-------------------------+")
            for i in range(len(commands)):
                print(f"{i+1}. {commands[i]}")
            print("+-------------------------+")

            inp = input(">>> ")
            cmd = inp.split(" ")[0].lower()
            args = inp.split(" ")[1:]

            if cmd == "login" or cmd == "1":
                self.login()
                return Session_CLI(self.session)
            elif cmd == "sign_up" or cmd == "2":
                self.sign_up()
                return Session_CLI(self.session)
            elif cmd == "quit" or cmd == str(len(commands)):
                self.db.db.close()
                quit()
            else:
                print("\033[0;31m(!) Wrong command. Please try again.\033[0m")

    def login(self):
        username = input("Enter username or email: ")
        if not db.user_exists(username):
            print(f"\033[0;31m(!) Username '{username}' doesn't exist.\033[0m")
            self.run()
        password = input("Enter Password: ")
        if not db.password_matches(username, password):
            print("\033[0;31m(!) Wrong password. Please try again.\033[0m")
            self.run()
        self.session = self.start_session(username, password)
        return print("\033[0;32m(✓) Successfully logged-in to your account. Welcome!\033[0m")

    def sign_up(self):
        username = input("Enter username: ")
        if not Verification.is_username_valid(username):
            print('\033[0;31m(!) The username you entered is not in the correct format.\033[0m')
            self.run()
        if db.user_exists(username):
            print(f"\033[0;31m(!) Username '{username}' already exists.\033[0m")
            self.run()

        phone = input("Enter your phone number: ")
        if not Verification.is_phone_valid(phone):
            print('\033[0;31m(!) The phone you entered is not in the correct format.\033[0m')
            self.run()

        password = input("Enter Password: ")
        if not Verification.is_password_valid(password):
            print("\033[0;31m(!) Password must match with all of the conditions below:\n"
                  " - At least 8 characters"
                  " - Lowercase and Uppercase character (a-z A-Z)\n"
                  " - Number (0-9)\n"
                  " - Special character (* @ ! ?)\033[0m")
            return self.sign_up()

        repeat_password = input("Repeat Password: ")
        if password != repeat_password:
            print("\033[0;31m(!) Password mismatch.\033[0m")
            return self.sign_up()

        # Phone number verification
        '''
        try:
            verificiation_code = f"{random.randint(0, 99999):05d}"
            api = KavenegarAPI('50515750512F7A46766D4B6874706F4972664E396F636F6A6972574748774D654969564974687A6730726F3D')
            params = {
                'sender': '1000596446',
                'receptor': f'{phone}',
                'message': f'This is your phone number verification email. Please enter the code below to confirm your sign up.\n'
                           f'Code: {verificiation_code}',
            }
            response = api.sms_send(params)
            print("We sent a verification code to your phone number. Please enter the code in order to verify.")
            input_code = input("Enter code: ")
            if verificiation_code != input_code:
                print('\033[0;31m(!) The code you entered is wrong. Please try again later.\033[0m')
                return self.run()
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)
        '''

        db.add_user(username, password, phone)
        print("\033[0;32m(✓) Successfully created your account. Welcome!\033[0m")
        return Session(username, password)


def main():
    cli = CLI()
    cli.run()

    


if __name__ == '__main__':
    main()
