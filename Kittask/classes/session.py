import datetime

from .database import Database
from .task import Task


class Session:
    def __init__(self, username: str, password: str):
        self.u = username
        self.p = password
        self.db = Database()

    def create_task(self):
        print("Add your task credentials:")
        task_id = self.db.create_task_id()
        title = input('  Title: ')
        desc = input('  Description: ')
        date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_modified = date_created
        deadline = input("  Deadline(Default: None): ")
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
        tags = input("  Tags(Split with comma for multiple): ")



        created_task = Task(task_id, self.u, title, desc, date_created, date_modified, deadline, tags)
        self.db.add_task(created_task)
        print("\033[0;32m(✓) Task was successfully created.\033[0m")

    def show_polls(self):
        poll_list = self.db.get_active_polls()
        for i in range(len(poll_list)):
            print(f"{poll_list[i][0]}. {poll_list[i][1]}")

    def participate(self):
        poll_id = int(input('Enter poll id: '))
        poll = self.db.get_poll(poll_id)
        if poll is None:
            return
        if poll.is_active is False:
            print("\033[0;31m(!) You can only vote for active polls.\033[0m")
        if self.db.has_voted(poll_id, self.u):
            return print("\033[0;31m(!) You can only vote 1 time for each poll.\033[0m")



        print(poll.title)
        for i in range(len(poll.options)):
            if len(poll.options[i]) != 0:
                print(f"{i + 1}. {poll.options[i]}")

        vote = int(input('Your vote: '))
        while vote > 5 or poll.options[vote - 1] == "":
            print("\033[0;31m[ERROR] Invalid vote. Please re-enter your vote.\033[0m")
            vote = int(input('Your vote: ')[1:-1])

        self.db.add_vote(poll_id, self.u, vote)
        print(f'\033[0;32m(✓) Submitted vote "{vote}".\033[0m')

    def delete_poll(self):
        poll_id = int(input('Enter your poll id: '))
        poll = self.db.get_poll(poll_id)
        if poll.owned_by != self.u:
            return print("\033[0;31m[ERROR] Sorry. You can only delete polls you own.\033[0m")

        confirmation = input(f"\033[93mAre you sure you want to delete this poll? '{poll_id}'\n"
                             f" 1. Yes\n"
                             f" 2. No\n\033[0m"
                             f" >>> ")
        if confirmation == '1' or confirmation.lower() == 'yes':
            self.db.delete_poll(poll_id)
            print(f"\033[0;32m(✓) Successfully deleted poll '{poll.title}'.\033[0m")

    def change_poll_status(self):
        poll_id = int(input('Enter your poll id: '))
        poll = self.db.get_poll(poll_id)
        if poll.owned_by != self.u:
            return print("\033[0;31m[ERROR] Sorry. You can only change polls you own.\033[0m")

        self.db.change_status(poll_id)
        print(f"\033[0;32m(✓) Successfully changed status of poll '{poll.title}'.\033[0m")

    def show_results(self):
        poll_id = int(input('Enter poll id: '))
        poll = self.db.get_poll(poll_id)
        results = self.db.get_results(poll_id)
        percentages = []
        for num in results:
            percentage = (num / sum(results)) * 100
            percentages.append(percentage)
        print(poll.title)
        for i in range(len(poll.options)):
            if len(poll.options[i]) != 0:
                print(f"{i + 1}. {poll.options[i]} --> {results[i]} votes ({percentages[i]}%)")

    def show_owned_polls(self):
        poll_list = self.db.get_owned_polls(self.u)
        for i in range(len(poll_list)):
            if poll_list[i].is_active:
                status = "Active"
            else:
                status = "Deactivated"
            print(f"{poll_list[i].poll_id}. {poll_list[i].title} ({status})")


class Admin_Session(Session):
    pass
