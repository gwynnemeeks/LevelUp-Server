"""Game model module"""
from django.db import models


class Game(models.Model):
    """Game database model"""
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
    title = models.CharField(max_length=75)
    gametype = models.ForeignKey("GameType", on_delete=models.CASCADE)