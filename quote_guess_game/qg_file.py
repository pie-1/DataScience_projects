import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep

all_quotes = []


def scrape_quotes(page_num):
    base_url = "http://quotes.toscrape.com/"
    url = f"/page/{page_num}"
    
    res = requests.get(f'{base_url}{url}')
    soup = BeautifulSoup(res.text, "html.parser")
    quotes = soup.find_all(class_="quote")

    for quote in quotes:
        all_quotes.append({
            "text": quote.find(class_="text").get_text(),
            "author": quote.find(class_="author").get_text(),
            "bio-link": quote.find("a")["href"]
        })


def start_game():
    print("\nWelcome to the Quote Guessing Game!")
    print("You will be shown a quote, and you need to guess the author.")
    print("You have 4 guesses, and hints will be provided after incorrect guesses.")
    print("Type 'exit' anytime to quit the game.")

    remaining_guesses = 4
    quote = choice(all_quotes)
    print("\nHere's a quote:\n")
    print(quote["text"])

    guess = ''
    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}\nYour guess: ")
        
        if guess.lower() == 'exit':
            print("Thanks for playing!")
            return
        
        if guess.lower() == quote["author"].lower():
            print("Congrats! You got it right!")
            break

        remaining_guesses -= 1

        if remaining_guesses == 3:
            res = requests.get(f"http://quotes.toscrape.com{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(f"Hint 1: The author was born on {birth_date} {birth_place}")
        
        elif remaining_guesses == 2:
            print(f"Hint 2: The author's first name starts with: {quote['author'][0]}")
        
        elif remaining_guesses == 1:
            last_initial = quote["author"].split(" ")[1][0]
            print(f"Hint 3: The author's last name starts with: {last_initial}")

    if remaining_guesses == 0:
        print(f"Sorry, you're out of guesses. The correct answer was {quote['author']}.")

    again = input("\nWould you like to play again? (y/n): ")
    if again.lower() == 'y':
        start_game()
    else:
        print("Thanks for playing!")


def main():
    page_num = 1
    while len(all_quotes) < 5: 
        scrape_quotes(page_num)
        page_num += 1

    start_game()

if __name__ == "__main__":
    main()
