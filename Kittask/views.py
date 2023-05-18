from typing import Optional

from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from Kittask.classes.auth import Auth
from Kittask.classes.session import Session
from Kittask.classes.sort import SortTasks
from Kittask.classes.task import Task
from Kittask.databases.database import Database
from Kittask.classes.date_time_module import DateTime
from Kittask.classes.verification import Verification

session: Optional[Session] = None
db = Database()


def home_page(request):
    if session is None:
        return redirect('login')

    tasks_today = db.get_tasks_today(session.u)
    for task in tasks_today:
        if task.completed:
            tasks_today.remove(task)
    if len(tasks_today) > 6:
        tasks_today = tasks_today[:6]

    context = {
        "date_today": DateTime.get_date_today(),
        "fullname": session.user.fullname,
        "tasks_today": tasks_today
    }
    return render(request, 'ui/home.html', context)


def login_page(request):
    global session
    session = None
    error_msg = ''

    if request.method == 'POST':
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if not Verification.is_phone_valid(phone):
            error_msg = "Phone Number is invalid."
            return render(request, 'ui/login.html', {"error_msg": error_msg})
        if not db.user_exists(phone):
            error_msg = "User with this phone number does not exist."
            return render(request, 'ui/login.html', {"error_msg": error_msg})
        if not db.password_matches(phone, password):
            error_msg = "Wrong password. Please try again."
            return render(request, 'ui/login.html', {"error_msg": error_msg})

        session = Auth.login(phone, password)
        if session is None:
            return render(request, 'ui/login.html', {"error_msg": error_msg})
        else:
            return redirect('home')

    else:
        return render(request, 'ui/login.html', {})


def signup_page(request):
    global session
    session = None

    if request.method == 'POST':
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")

        if not Verification.is_phone_valid(phone):
            error_msg = "Phone Number is invalid."
            return render(request, 'ui/signup.html', {'error_msg': error_msg})
        if db.user_exists(phone):
            error_msg = "User with this phone number already exists."
            return render(request, 'ui/signup.html', {'error_msg': error_msg})
        # '''
        if not Verification.is_password_valid(password):
            error_msg = mark_safe("""Password must match with all of the conditions below:
                   <br>&nbsp;  - At least 8 characters
                   <br>&nbsp;  - Lowercase and Uppercase character (a-z A-Z)
                   <br>&nbsp;  - Number (0-9)
                   <br>&nbsp;  - Special character (* @ ! ?)""")
            return render(request, 'ui/signup.html', {'error_msg': error_msg})
        # '''

        if password != repeat_password:
            error_msg = "Password mismatch."
            return render(request, 'ui/signup.html', {'error_msg': error_msg})

        db.add_user(fullname, phone, password)
        session = Auth.sign_up(phone, password)
        return redirect('home')

    else:
        return render(request, 'ui/signup.html', {})


def view_tasks(request):
    if session is None:
        return redirect('login')

    error_msg = ""
    sorted_tasks = db.get_owned_tasks(session.u)
    if request.method == 'POST':
        sort_prompt = str(request.POST.get('sort-prompt')).rstrip()
        if not Verification.is_prompt_valid(sort_prompt):
            error_msg = "Wrong Sort Prompt. Please try again."
            context = {
                "tasks": sorted_tasks,
                "fullname": session.user.fullname,
                "error": error_msg
            }
            return render(request, 'ui/view-tasks.html', context)
        tags = Verification.validate_tags_arr(request.POST.get('tags'))
        tags_str = ", ".join(tags)
        tasks = SortTasks(db.get_owned_tasks(session.u), sort_prompt, tags)
        sorted_tasks = tasks.sort_set()
        context = {
            "tasks": sorted_tasks,
            "fullname": session.user.fullname,
            "error": error_msg,
            "prompt": sort_prompt,
            "tags": tags_str
        }
        return render(request, 'ui/view-tasks.html', context)

    context = {
        "tasks": sorted_tasks,
        "fullname": session.user.fullname,
        "error": error_msg,
    }
    return render(request, 'ui/view-tasks.html', context)


def add_task(request):
    if session is None:
        return redirect('login')

    create_success = False

    if request.method == 'POST':
        task_title = request.POST.get('task-title')
        task_desc = request.POST.get('task-desc')
        created_at = DateTime.get_date_today()
        tags = Verification.validate_tags_str(request.POST.get('tags'))
        deadline = None
        has_deadline = request.POST.get('deadline')
        if has_deadline:
            year = request.POST.get('year')
            month = request.POST.get('month')
            day = request.POST.get('day')
            time = request.POST.get('time')
            deadline = f"{year}/{month}/{day} {time}"
            deadline = DateTime.change_format(deadline)
        session.create_task(Task(
            db.create_task_id(),
            session.u,
            task_title,
            task_desc,
            "",
            "",
            deadline,
            tags,
            False
        ))
        create_success = True

    context = {
        "date_today": DateTime.get_date_today(),
        "fullname": session.user.fullname,
        "create_success": create_success
    }
    return render(request, 'ui/add-task.html', context)

def edit_task(request, task_id: int):
    if session is None:
        return redirect('login')

    edit_success = False

    if request.method == 'POST':
        task_title = request.POST.get('task-title')
        task_desc = request.POST.get('task-desc')
        created_at = DateTime.get_date_today()
        tags = Verification.validate_tags_str(request.POST.get('tags'))
        deadline = None
        completed = request.POST.get('completed')
        has_deadline = request.POST.get('deadline')
        if has_deadline:
            year = request.POST.get('year')
            month = request.POST.get('month')
            day = request.POST.get('day')
            time = request.POST.get('time')
            deadline = f"{year}/{month}/{day} {time}"
            deadline = DateTime.change_format(deadline)
        session.edit_task(Task(
            task_id,
            session.u,
            task_title,
            task_desc,
            "",
            "",
            deadline,
            tags,
            completed
        ))
        edit_success = True

    context = {
        "date_today": DateTime.get_date_today(),
        "fullname": session.user.fullname,
        "task": db.get_task(task_id),
        "edit_success": edit_success
    }
    return render(request, 'ui/edit-task.html', context)

def view_tags(request):
    return render(request, 'ui/view-tags.html', {"tags": db.get_all_tags(), "fullname": session.user.fullname})
