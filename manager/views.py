from django.contrib.auth import get_user_model
from django.shortcuts import render

from manager.models import Task


def index(request):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    num_workers = get_user_model().objects.count()
    num_completed_task = Task.objects.filter(is_completed=True).count()
    num_not_completed_task = Task.objects.filter(is_completed=False).count()

    context = {
        "num_visits": num_visits,
        "num_workers": num_workers,
        "num_completed_task": num_completed_task,
        "num_not_completed_task": num_not_completed_task,
    }

    return render(request, "manager/index.html", context=context)
