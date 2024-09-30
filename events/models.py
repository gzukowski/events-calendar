from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    duration = models.PositiveIntegerField()
    image_url = models.URLField(max_length=200, blank=True, null=True)
    short_description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name="events")

    def __str__(self):
        return self.name
