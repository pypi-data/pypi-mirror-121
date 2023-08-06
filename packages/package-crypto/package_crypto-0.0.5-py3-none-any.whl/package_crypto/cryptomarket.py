import requests
from bs4 import BeautifulSoup
class Pars:
	def getInfo(self, name):
		url_test = "https://coinmarketcap.com/currencies/%s"
		url = url_test %name
		result = requests.get(url)
		soup = BeautifulSoup(result.content, 'html5lib')
		lst = soup.find_all('p')
		for i in lst:
			print(i.get_text())
			print()
