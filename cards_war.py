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
        if not 2 <= len(player_names) <= 4:
            raise ValueError("Hra může mít pouze 2 až 4 hráče.")

        deck = Deck()
        hands = self.split_deck_for_players(deck, len(player_names))

        self.players = [Player(name, hand) for name, hand in zip(player_names, hands)]
        self.round_count = 0

        log_message(f"Hra zahájena: {', '.join(player_names)}")


    def split_deck_for_players(self, deck, num_players):
        """Rozdělí balíček mezi hráče."""
        deck.shuffle()
        return [deck.cards[i::num_players] for i in range(num_players)]


    def play_round(self):
        """Odehraje jedno kolo hry."""
        self.round_count += 1
        
        # pseudoošetření pro případ, že se hra zacyklila a nevede k výsledku
        if self.round_count > 1000:
            log_message("\nHra se zacyklila! Je to nuda. Remíza.\n\n\n")
            sys.exit("Hra se zacyklila! Je to nuda. Remíza.\n\n\n")
        
        print(f"\n=== Kolo {self.round_count} ===")

        # Každý hráč zahraje kartu
        played_cards = {player: player.play_card() for player in self.players if player.has_cards()}

        """ Čitelnější varianta předchozího řádku:
        played_cards = {}  # Vytvoříme prázdný slovník

        for player in self.players:  # Procházíme seznam hráčů
            if player.has_cards():  # Pokud hráč má karty
                played_cards[player] = player.play_card()  # Zahraje kartu a uložíme ji do slovníku
        """

        # Výpis odehraných karet
        for player, card in played_cards.items():
            print(f"{player.name} zahrál: {card}")

        # Určíme vítěze kola
        max_value = max(card.value for card in played_cards.values())
        winners = [player for player, card in played_cards.items() if card.value == max_value]

        if len(winners) == 1:
            winner = winners[0]
            print(f"{winner.name} vyhrává kolo!")
            winner.collect_cards(list(played_cards.values()))
            log_message(f"Kolo {self.round_count}: {', '.join(f'{p.name} {c}' for p, c in played_cards.items())} → Vítěz: {winner.name}")
        else:
            print(f"Remíza mezi {', '.join(player.name for player in winners)}! VOJNA!")
            self.war(winners, list(played_cards.values()))

        # Výpis stavu hráčů
        print(" | ".join(str(player) for player in self.players))
        # time.sleep(1)


    def war(self, tied_players, war_pile):
        """Řeší vojnu mezi více hráči."""
        for player in tied_players:
            if len(player.hand) < 2:
                print(f"{player.name} nemá dost karet na vojnu a prohrává!")
                self.players.remove(player)
                return
        
        print("Každý hráč přidává jednu kartu lícem dolů...")
        for player in tied_players:
            war_pile.append(player.play_card())

        print("Každý hráč přidává jednu kartu lícem nahoru...")
        new_played_cards = {player: player.play_card() for player in tied_players}
        war_pile.extend(new_played_cards.values())

        for player, card in new_played_cards.items():
            print(f"{player.name} zahrál: {card}")

        # Určíme vítěze vojny
        max_value = max(card.value for card in new_played_cards.values())
        winners = [player for player, card in new_played_cards.items() if card.value == max_value]

        if len(winners) == 1:
            winner = winners[0]
            print(f"{winner.name} vyhrává VOJNU!")
            winner.collect_cards(war_pile)
            log_message(f"VOJNA mezi {', '.join(p.name for p in tied_players)} → Vítěz: {winner.name}")
        else:
            print("Další remíza! VOJNA pokračuje!")
            self.war(winners, war_pile)


    def play_game(self):
        """Spustí hru a pokračuje, dokud nezůstane jeden hráč s kartami."""
        print("\n=== Začíná hra Vojna! ===")
        print(f"Hrají: {', '.join(player.name for player in self.players)}")

        while len([player for player in self.players if player.has_cards()]) > 1:
            self.play_round()

        winner = next(player for player in self.players if player.has_cards())
        print(f"\n=== Konec hry! Vítěz: {winner.name} ===\n\n\n")
        log_message(f"Hra skončila! Vítěz: {winner.name}")
        log_message(f"\n\n ============================================= \n\n\n")

############## MAIN ##############
if __name__ == "__main__":
    game = WarGame(["Válek", "Hrnčiřík", "Metelka", "Urubek"])
    game.play_game()



