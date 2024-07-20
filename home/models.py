from django.db import models

# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return f"{self.team_name}"
    

class Person(models.Model):
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE, related_name="members", default=None, to_field="team_name")
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    location = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
    