from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"



class Questions(models.Model):

    content = models.CharField(max_length=280, default=None)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster", null=True, default=None)
    randomPoster = models.CharField(max_length=64, null=True, default=None)
    askedFor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="askedFor", null=True, default=None)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return f"Question: {self.poster}: {self.content}"

class Answers(models.Model):

    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="question")
    content = models.CharField(max_length=280, default=None)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
    answerPoster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answerPoster", null=True, default=None)
    randomPoster = models.CharField(max_length=64, null=True, default=None)

    def __str__(self):
        return f"Answer: {self.poster}: {self.content}"