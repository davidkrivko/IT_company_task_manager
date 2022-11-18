from django.urls import path

from manager.views import index, TaskListView

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", TaskListView.as_view(), name="task-list")
]


app_name = "manager"
