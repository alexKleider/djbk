from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def entity_created(entity_name):
    return True

def announce_failure(bad_entry):
    """Inform user that entry wasn't accepted"""
    pass

def home_page(request):
    new_entity = request.POST.get("new_entity", "")
    if new_entity:
        if not entity_created(new_entity):
            announce_failure(new_entity)
            new_entity = ''
    return render(request, "home.html", {
        "new_entity_text": new_entity,
        })

