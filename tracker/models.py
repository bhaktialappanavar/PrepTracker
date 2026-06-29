# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Skill Model
class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# Topic Model
class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


# Daily Task Model
class DailyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Study Log Model
class StudyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=1)
    notes = models.TextField()

    def __str__(self):
        return str(self.date)