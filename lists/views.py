from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):

    return render(request, "home.html")


def list_detail(request, list_id):
    _list = List.objects.get(pk=list_id)
    items = Item.objects.filter(list=_list)
    return render(request, "list.html", {"list": _list})

def list_list(request):
    if request.method == "POST":
        _list = List.objects.create()
        item = Item(text=request.POST["item_text"], list=_list)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            _list.delete()
            error = "You can't have an empty list item"
            return render(request, "home.html", {"error": error})
        return redirect(f"/lists/{_list.id}/")

def list_new_item(request, list_id):
    _list = List.objects.get(pk=list_id)
    Item.objects.create(text=request.POST["item_text"], list=_list)
    return redirect(f"/lists/{_list.id}/")