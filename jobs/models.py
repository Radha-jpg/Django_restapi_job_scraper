from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    publish_date = models.CharField(max_length=100, blank=True, null=True)
    detail_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title
