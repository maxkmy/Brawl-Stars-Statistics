from django.contrib import admin
from .models import Player, Brawler

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin): 
	list_display = ['playerTag', 'submissionDate', 'trophies'] 

@admin.register(Brawler)
class BrawlerAdmin(admin.ModelAdmin):
	list_display = ['name', 'submissionDate', 'trophies', 'Player']