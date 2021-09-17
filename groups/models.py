from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} / {self.name}"
        else:
            return f"ROOT / {self.name}"


class Group(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255, unique=True)
    desc = models.CharField(max_length=1024, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    bot_enabled = models.BooleanField(default=False)
    vacancy = models.BooleanField(default=True)
    flag = models.IntegerField(default=0, null=False)

    def __str__(self):
        return f"{self.category.name} / ({self.name}, {self.number})"


class Website(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    desc = models.CharField(max_length=1024, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} / ({self.name}, {self.url})"
