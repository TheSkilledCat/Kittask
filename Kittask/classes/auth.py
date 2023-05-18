from Kittask.databases.database import Database
from .session import Session


class Auth:
    db = Database()

    @classmethod
    def login(cls, phone, password):
        cls.session = cls.start_session(phone, password)
        return Session(phone, password)

    @classmethod
    def sign_up(cls, phone, password):
        # Phone number verification
        """
        try:
            verification_code = f"{random.randint(0, 99999):05d}"
            api = KavenegarAPI('50515750512F7A46766D4B6874706F4972664E396F636F6A6972574748774D654969564974687A6730726F3D')
            params = {
                'sender': '1000596446',
                'receptor': f'{phone}',
                'message': f'This is your phone number verification email. Please enter the code below to confirm your sign up.\n'
                           f'Code: {verification_code}',
            }
            response = api.sms_send(params)
            print("We sent a verification code to your phone number. Please enter the code in order to verify.")
            input_code = input("Enter code: ")
            if verification_code != input_code:
                print('\033[0;31m(!) The code you entered is wrong. Please try again later.\033[0m')
                return self.run()
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)
        """

        return Session(phone, password)

    @classmethod
    def start_session(cls, phone, password):
        return Session(phone, password)
