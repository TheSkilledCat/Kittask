from .session import Session


class Session_CLI:
    def __init__(self, session: Session):
        self.s = session
        self.run()

    def run(self):
        while True:
            cmd = int(input("\n"
                            "+-------------------------+\n"
                            "1. Create a new poll\n"
                            "2. List of polls\n"
                            "3. Participate in a poll\n"
                            "4. Delete your poll\n"
                            "5. Activate or deactivate your poll\n"
                            "6. Poll results\n"
                            "7. List of your polls\n"
                            "8. Exit\n"
                            "+-------------------------+\n"
                            "\n"
                            ">>> "))

            if cmd == 1:
                self.s.create_poll()
            elif cmd == 2:
                self.s.show_polls()
            elif cmd == 3:
                self.s.participate()
            elif cmd == 4:
                self.s.delete_poll()
            elif cmd == 5:
                self.s.change_poll_status()
            elif cmd == 6:
                self.s.show_results()
            elif cmd == 7:
                self.s.show_owned_polls()
            elif cmd == 8:
                self.s.db.db.close()
                quit()
            else:
                print("\033[0;31m(!) Wrong command. Please try again.\033[0m")
