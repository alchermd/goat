from django.db import models
from django.urls import reverse


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey("lists.List", on_delete=models.SET_NULL, null=True)

class List(models.Model):
    def get_absolute_url(self):
        return reverse("list_detail", args=[self.id])