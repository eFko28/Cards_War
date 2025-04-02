"""Modul player.py - Definice třídy Player pro hru Vojna."""

from typing import List
from modules.card import Card


class Player:

    def __init__(self, name, cards):
        self.name = name
        self.hand = []
        for card in cards:
            self.hand.append(card)

    def has_cards(self):
        if len(self.hand) > 0:
            return True
        else:
            return False

    def play_card(self):
        if len(self.hand) == 0:
            print(f"{self.name} nemá už žádné karty!")
            return None
        first_card = self.hand[0]
        new_hand = []
        for i in range(1, len(self.hand)):
            new_hand.append(self.hand[i])
        self.hand = new_hand
        return first_card

    def collect_cards(self, won_cards):
        for card in won_cards:
            self.hand.append(card)

    def __str__(self):
        return f"{self.name} má {len(self.hand)} karet."


# Testovací kód (pokud se soubor spustí samostatně)
if __name__ == "__main__":
    from deck import Deck

    deck = Deck()
    half1, half2 = deck.split_deck()
    
    player1 = Player("Alice", half1)
    player2 = Player("Bob", half2)

    print(player1)  # Očekávaný výstup: Alice (karet: 26)
    print(player2)  # Očekávaný výstup: Bob (karet: 26)

    card1 = player1.play_card()
    card2 = player2.play_card()

    print(f"{player1.name} zahrál: {card1}")  # Očekávaný výstup: První karta hráče Alice
    print(f"{player2.name} zahrál: {card2}")  # Očekávaný výstup: První karta hráče Boba

    player1.collect_cards([card1, card2])  # Alice vyhrála obě karty
    print(f"{player1.name} nyní má {len(player1.hand)} karet.")  # Očekávaný výstup: 27
