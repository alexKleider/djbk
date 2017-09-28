from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    if request.method == "POST":
        return HttpResponse(request.POST["new_entity"])
        # ^ Returns just what the user enters.
        # <input name="new_entity ....
        # Doesn't return the whole page with new item in its proper
        # place so tests => error.
    return render(request,"home.html")
