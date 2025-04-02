"""Modul deck.py - Definice třídy Deck pro správu balíčku karet ve hře Vojna."""

import random
from modules.card import Card, SUITS  # Importujeme třídu Card a konstantu SUITS

# Konstanty pro hodnoty karet v balíčku
CARD_VALUES = list(range(2, 15))

class Deck:

    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for value in range(2, 15):
                self.cards.append(Card(value, suit))
        self.shuffle_cards()

    def shuffle_cards(self):
        random.shuffle(self.cards)


    def deal_card(self):
        if len(self.cards) == 0:
            print("Balíček je prázdný! Nelze rozdat další karty.")
            return None
        return self.cards.pop()

    def split_deck(self):
        half1 = []
        half2 = []
        for i in range(len(self.cards)):
            if i < len(self.cards) / 2:
                half1.append(self.cards[i])
            else:
                half2.append(self.cards[i])
        return half1, half2
    

# Testovací kód (pokud se soubor spustí samostatně)
if __name__ == "__main__":
    deck = Deck()
    print(f"Počet karet v balíčku: {len(deck.cards)}")  # Očekávaný výstup: 52
    card = deck.deal_card()
    print(f"Rozdaná karta: {card}")  # Náhodná karta
    print(f"Počet karet po rozdání: {len(deck.cards)}")  # Očekávaný výstup: 51
    half1, half2 = deck.split_deck()
    print(f"Rozdělené balíčky: {len(half1)}, {len(half2)}")  # Očekávaný výstup: 26, 26
