from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from manager.models import Task


@login_required
def index(request):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    num_workers = get_user_model().objects.count()
    num_completed_task = Task.objects.filter(is_completed=True).count()
    num_not_completed_task = Task.objects.filter(is_completed=False).count()

    context = {
        "num_visits": num_visits + 1,
        "num_workers": num_workers,
        "num_completed_task": num_completed_task,
        "num_not_completed_task": num_not_completed_task,
    }

    return render(request, "manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    queryset = Task.objects.all().select_related("task_type")


