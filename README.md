# Description
I am in a keeper league where we have a deadline for players that need to remain on the roster for the remainder of the year.  I wanted to find a way to script this process and have it mail me the data or possibly store in Google docs.  As of now, this will just print the data on the terminal

# Requirements
* Python 2.7
  * mechanize
  * BeautifulSoup4
  
command:

```
pip install mechanize beautifulsoup4
```

# Self-Use
There will be some changes need to be made.  Obviously the Yahoo login and this line:

```
br.open("https://football.fantasysports.yahoo.com/f1/313652/transactions")
```

I've only tested this with my Yahoo Football league and plan on testing with my Basketball league.  My guess is any Yahoo transaction page will work, but that has not been tested yet.

# Code
The code uses mechanize to simulate Yahoo's login through a browser.  Upon my research, this is the only method I have found available for authenticating against Yahoo, but I am open to suggestions!

Once the page is loaded, we use BeautifulSoup's functions to parse through and extract the data.  There are two For loops.

#### First Loop

```
for players in soup.select("table > tr > td > div"):
	player = players.find('a').get_text()
	try:
		if (players.find('h6').get_text() == ' To Waivers' ):
			dropped[index] = player
	except AttributeError:
		pass

	time = players.find('span',{'class':"Block F-timestamp Fz-xxs Nowrap"})
	if (time != None):
		try:
			nullplayer = dropped[index - 1]
			time = time.get_text()
			dropped[index] = time
		except KeyError:
			pass
	index += 1
```

1. We use BeautifulSoup's css selector to find the table we want to get data from.  I created an index that grows through the iteration and will explain later on
2. We use a try/catch block to see if the Player has the ' To Waivers' attribute.  If so, then we add Player to a dictionary using the index as the key.
3. As we iterate over the table, I also want to grab the date/time when the player transaction was made.  I use another try/catch statement here to verify that the item in the previous index had valid Player.  This is because the transaction page can have trades, players only added, trades with multiple players, etc so it's not always going to be the same set.  
4. Once the loop finishes, we should have a dictionary where the dictionary key's are in sequential order and the values should be Player, Date, Player, Date, etc

#### Second Loop

```
count = 1
for items in dropped:
	if (count % 2 == 0):
		player = dropped[items - 1]
		time = dropped[items]
		print "%s dropped on %s" %(player, time)
	count += 1
```

1. The second loop is much simpler and I use another index to iterate over the dictionary.  The purpose of this is to output the text so I can read cleanly the Player and the date/time they were dropped.  I used a modulus operator to get the Date value and print out the previous iteration value together.

### Suggestions/Comments
Please feel free to leave and suggestions/comments!