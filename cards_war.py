"""_summary_
**Cards_war.py** je hlavní skript, který řídí simulaci karetní hry **Vojna** pro **2 až 4 hráče**.  
Využívá objektově orientovaný přístup a pracuje s třídami **`Card`**, **`Deck`** a **`Player`**.  

## ✨ Klíčové vlastnosti:
- **Podpora více hráčů** (2–4).
- **Automatická herní smyčka**, která pokračuje, dokud nezůstane jen jeden hráč s kartami.
- **Správná logika vojny** – pokud dojde k remíze, hráči pokládají karty lícem dolů i nahoru.
- **Logování do souboru `cards_war.log`** – zaznamenává průběh hry, vítěze kol i vojny.
- **Čistá a modulární OOP struktura** – jednotlivé třídy jsou uloženy ve vlastních souborech.

### Možné rozšíření:
- **Použití dekorátoru `@log_action`**, který automaticky zapisuje důležité události hry.

## 🚀 Jak hra funguje?
1. Vytvoří se **balíček karet** a **hráči**.
2. Hráči **postupně hrají karty**, nejvyšší karta vyhrává kolo.
3. Při **remíze nastává vojna**, kde hráči pokládají karty lícem dolů i nahoru.
4. **Hra končí**, když **zbude pouze jeden hráč s kartami** nebo po 1000 kolech.

"""

from modules.deck import Deck
from modules.player import Player
import os
import sys

# Nastavení relativní cesty k logu
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log")  # Relativní cesta k adresáři /log
LOG_FILE = os.path.join(LOG_DIR, "cards_war.log")  # Plná cesta k logovacímu souboru
LOG_ENABLED = True  # Lze zapnout/vypnout voláním enable_logging() / disable_logging()


# Pokud složka log neexistuje, vytvoříme ji
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def log_message(message: str):
    from datetime import datetime

    if LOG_ENABLED:
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

'''
def log_action(func):
    """Dekorátor pro automatické logování volání funkcí.
    Args:
        func (function): Funkce, jejíž volání chceme zaznamenat.
    Returns:
        function: Ozdobená funkce s logováním.
    """

    def wrapper(*args, **kwargs):
        self = args[0]  # První argument je vždy `self` (instance WarGame)
        func_name = func.__name__  # Název funkce
        result = func(*args, **kwargs)  # Zavoláme původní funkci

        if func_name == "play_round":
            # Zaznamenáme průběh kola
            log_message(
                f"Kolo {self.round_count}: {self.player1.name} zahrál {self.player1_last_card}, "
                f"{self.player2.name} zahrál {self.player2_last_card} → {self.round_winner}"
            )
        elif func_name == "war":
            # Zaznamenáme průběh vojny
            log_message(
                f"VOJNA! {self.player1.name} vs. {self.player2.name} → vítěz: {self.war_winner}"
            )

        return result  # Vrátíme výsledek původní funkce
    return wrapper
'''

class WarGame:
    """Třída reprezentující hru Vojna pro 2 až 4 hráče."""

    def __init__(self, player_names):
        """Inicializuje hru, vytvoří balíček a rozdělí karty mezi hráče."""
        if len(player_names) < 2 or len(player_names) > 4:
            raise ValueError("Hra může mít pouze 2 až 4 hráče.")

        deck = Deck()
        hands = self.split_deck_for_players(deck, len(player_names))

        self.players = []
        i = 0
        while i < len(player_names):
            self.players.append(Player(player_names[i], hands[i]))
            i = i + 1

        self.round_count = 0

        # Build up the string exactly like the original print output
        names_str = ""
        j = 0
        while j < len(player_names):
            names_str = names_str + player_names[j]
            if j != len(player_names) - 1:
                names_str = names_str + ", "
            j = j + 1

        log_message("Hra zahájena: " + names_str)

    def split_deck_for_players(self, deck, num_players):
        """Rozdělí balíček mezi hráče."""
        deck.shuffle_cards()
        result = []
        i = 0
        while i < num_players:
            hand = []
            j = i
            while j < len(deck.cards):
                hand.append(deck.cards[j])
                j = j + num_players
            result.append(hand)
            i = i + 1
        return result

    def play_round(self):
        """Odehraje jedno kolo hry."""
        self.round_count = self.round_count + 1

        if self.round_count > 1000:
            log_message("\nHra se zacyklila! Je to nuda. Remíza.\n\n\n")
            import sys
            sys.exit("Hra se zacyklila! Je to nuda. Remíza.\n\n\n")

        # Print round header (the output remains the same)
        print("\n=== Kolo " + str(self.round_count) + " ===")

        # Each player plays a card; build the dictionary manually
        played_cards = {}
        index = 0
        while index < len(self.players):
            if self.players[index].has_cards():
                card = self.players[index].play_card()
                played_cards[self.players[index]] = card
            index = index + 1

        # Print played cards
        for player in played_cards:
            print(player.name + " zahrál: " + str(played_cards[player]))

        # Determine the maximum card value played
        max_value = -1
        for key in played_cards:
            if played_cards[key].value > max_value:
                max_value = played_cards[key].value

        winners = []
        for key in played_cards:
            if played_cards[key].value == max_value:
                winners.append(key)

        if len(winners) == 1:
            winner = winners[0]
            print(winner.name + " vyhrává kolo!")
            all_cards = []
            for key in played_cards:
                all_cards.append(played_cards[key])
            winner.collect_cards(all_cards)
            log_text = "Kolo " + str(self.round_count) + ": "
            for key in played_cards:
                log_text = log_text + key.name + " " + str(played_cards[key]) + ", "
            log_text = log_text + "→ Vítěz: " + winner.name
            log_message(log_text)
        else:
            names = ""
            k = 0
            while k < len(winners):
                names = names + winners[k].name
                if k != len(winners) - 1:
                    names = names + ", "
                k = k + 1
            print("Remíza mezi " + names + "! VOJNA!")
            temp_cards = []
            for key in played_cards:
                temp_cards.append(played_cards[key])
            self.war(winners, temp_cards)

        # Print players' status
        status = ""
        m = 0
        while m < len(self.players):
            status = status + str(self.players[m])
            if m != len(self.players) - 1:
                status = status + " | "
            m = m + 1
        print(status)

    def war(self, tied_players, war_pile):
        """Řeší vojnu mezi více hráči."""
        i = 0
        while i < len(tied_players):
            if len(tied_players[i].hand) < 2:
                print(tied_players[i].name + " nemá dost karet na vojnu a prohrává!")
                self.players.remove(tied_players[i])
                return
            i = i + 1

        print("Každý hráč přidává jednu kartu lícem dolů...")
        i = 0
        while i < len(tied_players):
            war_pile.append(tied_players[i].play_card())
            i = i + 1

        print("Každý hráč přidává jednu kartu lícem nahoru...")
        new_played_cards = {}
        i = 0
        while i < len(tied_players):
            new_played_cards[tied_players[i]] = tied_players[i].play_card()
            i = i + 1

        for player in new_played_cards:
            print(player.name + " zahrál: " + str(new_played_cards[player]))

        max_value = -1
        for key in new_played_cards:
            if new_played_cards[key].value > max_value:
                max_value = new_played_cards[key].value

        winners = []
        for key in new_played_cards:
            if new_played_cards[key].value == max_value:
                winners.append(key)

        for key in new_played_cards:
            war_pile.append(new_played_cards[key])

        if len(winners) == 1:
            winner = winners[0]
            print(winner.name + " vyhrává VOJNU!")
            winner.collect_cards(war_pile)
            log_message("VOJNA mezi " + ", ".join(p.name for p in tied_players) + " → Vítěz: " + winner.name)
        else:
            print("Další remíza! VOJNA pokračuje!")
            self.war(winners, war_pile)

    def play_game(self):
        """Spustí hru a pokračuje, dokud nezůstane jeden hráč s kartami."""
        print("\n=== Začíná hra Vojna! ===")
        names_str = ""
        i = 0
        while i < len(self.players):
            names_str = names_str + self.players[i].name
            if i != len(self.players) - 1:
                names_str = names_str + ", "
            i = i + 1
        print("Hrají: " + names_str)

        while True:
            active = []
            i = 0
            while i < len(self.players):
                if self.players[i].has_cards():
                    active.append(self.players[i])
                i = i + 1
            if len(active) <= 1:
                break
            self.play_round()

        winner = None
        i = 0
        while i < len(self.players):
            if self.players[i].has_cards():
                winner = self.players[i]
                break
            i = i + 1

        if winner is not None:
            print("\n=== Konec hry! Vítěz: " + winner.name + " ===\n\n\n")
            log_message("Hra skončila! Vítěz: " + winner.name)
            log_message("\n\n ============================================= \n\n\n")


############## MAIN ##############
if __name__ == "__main__":
    game = WarGame(["Válek", "Hrnčiřík", "Metelka", "Urubek"])
    game.play_game()



