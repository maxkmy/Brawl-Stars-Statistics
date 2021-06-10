from django.db import models
import datetime

# models
class Player(models.Model):
	playerTag = models.CharField(max_length = 20)
	submissionDate = models.DateField(default = datetime.date.today)
	trophies = models.TextField()

	def __str__(self): 
		return self.playerTag

class Brawler(models.Model): 
	name = models.CharField(max_length = 20)
	submissionDate = models.DateField(default = datetime.date.today)
	trophies = models.TextField()
	Player = models.ForeignKey(Player, on_delete=models.CASCADE)

	def __str__(self): 
		return self.name