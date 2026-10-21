# topics/models.py
from django.db import models
from notes.models import Tag


class TopicNote(models.Model):
    tag            = models.OneToOneField(Tag, on_delete=models.CASCADE, related_name='topic_note')
    core_statement = models.TextField(blank=True)
    key_tricks     = models.JSONField(default=list, blank=True)
    when_to_use    = models.TextField(blank=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Topic: {self.tag.name}"