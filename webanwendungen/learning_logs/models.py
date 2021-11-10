from django.db import models
from django.db.models.aggregates import Max


class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Retrun a string representation of the model."""
        return self.text


class Entry(models.Model):
    """Something specific learnd about a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a string representation of the model."""
        return f'{self.text[:50]}...' if len(self.text) > 50 else self.text
