import quotes_guessing_methods as methods

print("WELCOME TO GUESS WHO SAID THAT?")

play = True
while play:
	quote = methods.Quote()
	print("Here's a quote: ")
	print(quote)
	print("Who said this quote?")
	attempts = 4
	while attempts > 0:
		guess = methods.guess(attempts, quote)	
		if guess.lower() == quote.author().lower():
			play = methods.play_again("win")
			break
		else:
			attempts -= 1
	else:
		play = methods.play_again(quote.author())



