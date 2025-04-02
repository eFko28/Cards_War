"""Modul card.py - Trida Card pro hru Vojna."""

# Barvy karet
SUITS = ["♠", "♥", "♦", "♣"]

class Card:


    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        if self.value == 11:
            val = "J"
        elif self.value == 12:
            val = "Q"
        elif self.value == 13:
            val = "K"
        elif self.value == 14:
            val = "A"
        else:
            val = str(self.value)
        return f"{val}{self.suit}"

    def __lt__(self, other):
        if self.value < other.value:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.value == other.value:
            return True
        else:
            return False


# Testovací kód (pokud se soubor spustí samostatně)
if __name__ == "__main__":
    card1 = Card(14, "♠")  # Eso pikové
    card2 = Card(10, "♥")  # Desítka srdcová
    print(card1)  # Očekávaný výstup: A♠
    print(card2)  # Očekávaný výstup: 10♥
    print(card1 > card2)  # True, protože eso (14) je větší než desítka (10)
    print(card1 == Card(14, "♦"))  # True, protože obě karty mají hodnotu 14
