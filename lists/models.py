from django.db import models

class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey("lists.List", on_delete=models.SET_NULL, null=True)

class List(models.Model):
    pass