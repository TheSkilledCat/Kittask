# THIS FILE IS NOT USED


#####################################################################################
# Project "Kittask Task Manager"
#####################################################################################

from Kittask.databases.database import Database


# from kavenegar import *


class CLI:

    def __init__(self):
        self.session = None
        self.db = Database()


def main():
    cli = CLI()


if __name__ == '__main__':
    main()
