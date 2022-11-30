from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import WorkerCreationForm, WorkerSearchForm
from manager.models import Task, Position, Worker, TaskType


def index(request):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    num_workers = get_user_model().objects.count()
    num_completed_task = Task.objects.filter(is_completed=True).count()
    num_not_completed_task = Task.objects.filter(is_completed=False).count()

    important_tasks = Task.objects.filter(is_completed=False).order_by("deadline")[:3]

    context = {
        "num_visits": num_visits + 1,
        "num_workers": num_workers,
        "num_completed_task": num_completed_task,
        "num_not_completed_task": num_not_completed_task,
        "important_tasks": important_tasks,
    }

    return render(request, "manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10
    queryset = Task.objects.all().select_related("task_type")


@login_required
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)

    context = {
        "task": task,
    }

    return render(request, "manager/task_detail.html", context=context)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ["name", "description", "priority", "deadline", "task_type", "assignees"]
    success_url = reverse_lazy("manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    success_url = reverse_lazy("manager:task-list")
    fields = "__all__"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("manager:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5
    queryset = Worker.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_worker"] = WorkerSearchForm(
            initial={"title": username})

        return context

    def get_queryset(self):
        username = self.request.GET.get("username")

        if username:
            return self.queryset.filter(username__icontains=username)
        return self.queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().select_related("position")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "position"]
    success_url = reverse_lazy("manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")
