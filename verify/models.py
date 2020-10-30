from django.db import models


class ApiKey(models.Model):
    key = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_enabled = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description}：{self.key} - {self.last_modified}"
