import uuid
from django.db import models


class AwsBucket(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=20, unique=True)
    region = models.CharField(max_length=10)
    url = models.CharField(max_length=255, blank=False, null=False)
    access_browser = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.name
