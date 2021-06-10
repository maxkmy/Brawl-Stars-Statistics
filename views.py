from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import PlayerForm
from .models import Player, Brawler
import requests, datetime

# Brawl Stars API Calling
headers = {
	"Accept": "application/json",
	"authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjM5ZDVhZjRkLWE4ZWItNDE0ZC1hMDZhLTUxZWZhOWRhOWU2YyIsImlhdCI6MTYxODE3NDcyNywic3ViIjoiZGV2ZWxvcGVyL2YzMDI3MGQwLWZiMmQtOThhNS0zZmE5LTMxYTM4OWNmMjIzMyIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiOTkuMjQ3LjMzLjIwMyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.EhQPQ8hrl-qlMi5yhsDBkCA8b4c5WLF7OQgeUoKhQETtyZprPXfqZj-F4oSGPVfP4Gu3OVwQb3KPlgZZ3UYI3A",
}

def findUser(query): 
	urlRequest = "https://api.brawlstars.com/v1/players/%23" + query
	response = requests.get(urlRequest, headers)
	userJson = response.json()
	
	try: 
		name = userJson['name']
		trophies = userJson['trophies']
		experience = userJson['expLevel']

		brawlerList = []
		for brawler in userJson['brawlers']: 
			brawlerName = brawler['name']
			brawlerPower = brawler['power']
			brawlerRank = brawler['rank']
			brawlerTrophies = brawler['trophies']
			brawlerList.append([brawlerName, brawlerPower, brawlerRank, brawlerTrophies])

		# returning player and brawler information
		return query, name, trophies, experience, brawlerList

	except LookupError: # some changes need to be made
		return None, None, None, None, None

def home(request): 
	if request.method == 'POST': 
		form = PlayerForm(request.POST) 
		if form.is_valid(): 
			obj = PlayerForm() 
			obj.playerTag = form.cleaned_data['playerTag']
			newUrl = 'display/' + str(obj.playerTag) + '/'
			return HttpResponseRedirect(newUrl)
		else: 
			return HttpResponse('<p>The form is not valid</p>')
	else: 
		form = PlayerForm()
		return render(request, 'home.html', {'playerForm':form})

def playerDetail(request, playerTag):
	# getting player and brawler information
	playerTag, name, trophies, experience, brawlerList = findUser(playerTag) 

	# check if playerTag exists
	if name is None: 
		raise HttpResponse("<p>The player tag does not exist. Player tags are case sensitive. Make sure to NOT include # in front of your player tag.</p>")

	playerSet = Player.objects.filter(playerTag=playerTag)
	if len(playerSet) == 1: 
		# get existing player
		player = playerSet[0]
		trophiesWithDate = " " + str(datetime.date.today) + ":" + str(trophies) 
	elif len(playerSet) == 0: 
		# create a new player
		player = Player(playerTag=playerTag, trophies=trophies)
		trophiesWithDate = str(datetime.date.today) + ":" + str(trophies)

	# updating player's trophies (with date)
	player.trophies = str(player.trophies) + trophiesWithDate
	player.save()

	# getting the player's brawlers
	brawlerSet = Brawler.objects.filter(Player=player.id)

	for brawler in brawlerList: 
		brawlerName = brawler[0]
		for brawlerObj in brawlerSet: 
			if brawlerName == brawlerObj.name: 
				trophies = " " + str(datetime.date.today) + ":" + str(brawler[3]) 
				brawlerObj.trophies += trohpies 
				brawlerObj.save()
			else: 
				trophies = str(datetime.date.today) + ":" + str(brawler[3])
				brawlerObj = Brawler(name=brawlerName,trophies=trophies, Player=player.id)
				brawlerObj.save()
			
	return render(request, 'playerDetail.html', {'playerTag':playerTag, 
												'playerName':name,
												'playerTrophies':trophies,
												'playerExperience':experience,
												'brawlerList': brawlerList})