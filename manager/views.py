from django.shortcuts import render


def index(request):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_visits": num_visits
    }

    return render(request, "manager/index.html", context=context)
