from django.shortcuts import redirect, render
from django.http import HttpResponse

from books.src.config import DEFAULTS as D
from books.src import entities as ents

# Create your views here.

def entity_created(entity_name):
    if ents.create_entity(entity_name, D) == entity_name:
        return True

def deal_with_invalid_entity(invalid_entity):
    """Inform user that entry wasn't accepted"""
    pass

def home_page(request):
    if request.method == "POST":
        new_entity = request.POST["new_entity"]
        ret = ents.create_entity(new_entity, D)
        if ret is None:
            print("Didn't create an entity.")
            new_entity = ''
            deal_with_invalid_entity(new_entity)
            pass
        else:
            return redirect('/')

    return render(request, "home.html")

