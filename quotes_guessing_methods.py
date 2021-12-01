# http://quotes.toscrape.com/

from random import choice
import requests
from bs4 import BeautifulSoup
import pickle
from time import sleep

class Quote:

	def __init__(self):
		self.quote = self.get_random_quote()

	def __repr__(self):
		return self.quote[0]

	def scrape_quotes(self):
		quotes_list = []
		
		response = requests.get("http://quotes.toscrape.com/")
		soup = BeautifulSoup(response.text, "html.parser")

		i = 1
		while soup.find(class_= "next"):
			response = requests.get(f"https://quotes.toscrape.com/page/{i}/")
			soup = BeautifulSoup(response.text, "html.parser")
			quotes = soup.find_all(class_="quote")
			print("Please wait...")
			print("o..")
			print(".o.")
			print("..o")
		
			for quote in quotes:
				text = quote.find(class_="text").get_text()
				author = quote.find(class_="author").get_text()
				url = quote.find("a")["href"] # a single atribute
				quotes_list.append([text, author, url])
				sleep(2)
			i += 1
		return quotes_list

	def pickle_quotes(self):
		quotes = self.scrape_quotes()
		with open("quotes.pickle", "wb") as file:
			pickle.dump(quotes, file)

	def unpickle_quotes(self):
		with open("quotes.pickle", "rb") as file:
			quotes_list = pickle.load(file)
		return quotes_list

	def get_random_quote(self):
		try:
			quotes_list = self.unpickle_quotes()
		except:
			self.pickle_quotes()
			quotes_list = self.unpickle_quotes()
		return choice(quotes_list)

	def scrape_author(self, quote):
		print("Please wait...")
		response = requests.get(f"http://quotes.toscrape.com{self.quote[2]}")
		soup = BeautifulSoup(response.text, "html.parser")
		born_date = soup.find(class_="author-born-date").get_text()
		born_place = soup.find(class_="author-born-location").get_text()
		long_bio = soup.find(class_="author-description").get_text()
		return [born_date, born_place, long_bio]

	def author(self):
		return self.quote[1]

	def author_initials(self):
		name = self.quote[1].split(" ")
		initials = [n[0] for n in name]
		init = " .".join(initials)
		return f"The author initials are {init}"

	def author_short_bio(self):
		return f"The author was born {self.scrape_author(self.quote)[0]} {self.scrape_author(self.quote)[1]}"

	def author_long_bio(self):
		name = self.quote[1].split(" ")
		text = self.scrape_author(self.quote)[2]
		for n in name:
			text = text.replace(n, " $$$ ")
		return text


def play_again(outcome):
	if outcome == "win":
		print("GOOD JOB YOU WIN!!")
	else:
		print("No more attempts")
		print(f"The author is {outcome}")

	answer = ''
	while answer not in ["y", "yes", "n", "no"]:
		answer = input("Do you want to play again? (y/n) ")
	
	if answer in ["y", "yes"]:
		return True
	elif answer in ["n", "no"]:
		print("Thanks for playing \nGoodbye!")
		return False
	else:
		print("Please choose yes or no (y/n)")

def guess(i, quote):
	if i == 1:
		print("Here's a big hint: ")
		print(quote.author_long_bio())
	elif i == 2:
		print("Here's another hint: ")
		print(quote.author_short_bio())
	elif i == 3 :
		print("Here's a small hint: ")
		print(quote.author_initials())

	guess = input(f"Number of attempts {i}: ")

	return guess


