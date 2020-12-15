from django.contrib.postgres.indexes import HashIndex
from django.db import models

# Create your models here.
from accounts.models import Profile


class Report(models.Model):
    """
        Model to store reports about cheaters
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    last = models.ForeignKey("Entry", on_delete=models.CASCADE, blank=True, null=True, related_name="rprt")

    def __str__(self):
        return self.text[:50]


class Entry(models.Model):
    """
        Model is used to store data about user.
        This model creates a tree/trees and a DSU.
        All vertexes in one connected component describe one person.
    """
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    # Graph
    neighbours = models.ManyToManyField("self", blank=True)

    # DSU
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    rate = models.IntegerField(blank=True, default=0)

    indexes = (
        HashIndex(fields=('key', 'value')),
    )

    def get_parent(self):
        if self.parent == self:
            return self
        parent = self.parent.get_parent()
        self.parent = parent
        self.save()
        return parent

    def merge(self, other):
        a, b = self.get_parent(), other.get_parent()
        if a.rate < b.rate:
            a, b = b, a
        b.parent = a
        if a.rate == b.rate:
            a.rate += 1
        a.save()
        b.save()

    def save(self, *args, **kwargs):
        # Any changes here should be also applied in admin.py
        super(Entry, self).save(*args, **kwargs)
        if self._state.adding:
            self.parent = self
            self.save()
            if self.report.last is not None and self.report.last.get_parent() != self.get_parent():
                self.merge(self.report.last)
                self.neighbours.add(self.report.last)

            neighbours = Entry.objects.filter(key=self.key, value=self.value)
            for neighbour in neighbours.all():
                if self.get_parent() != neighbour.get_parent() and self != neighbour:
                    self.merge(neighbour)
                    self.neighbours.add(neighbour)

            self.report.last = self
            self.report.save()
            self.save()

    def __str__(self):
        return "{} : {}".format(self.key, self.value)
