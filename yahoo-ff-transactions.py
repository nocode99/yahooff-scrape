import mechanize
from bs4 import BeautifulSoup
import urllib

username = 'username@yahoo.com'
password = 'password'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
br.open("https://football.fantasysports.yahoo.com/f1/313652/transactions")
br.select_form(nr=0)
br.form["username"] = username
br.form["passwd"] = password
response = br.submit()
html_scrape = response.read()
soup = BeautifulSoup(html_scrape, "lxml")
index = 1
dropped = {}

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

count = 1
for items in dropped:
	if (count % 2 == 0):
		player = dropped[items - 1]
		time = dropped[items]
		print "%s dropped on %s" %(player, time)
	count += 1