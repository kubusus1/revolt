import random
from dataclasses import dataclass, field

@dataclass
class District:
    name: str
    loyalty: int = 80
    activism: int = 10
    resources: int = 50
    repression: int = 20

    def summary(self) -> str:
        return f"{self.name}: Lojalnosc={self.loyalty} Aktywizm={self.activism} Zasoby={self.resources} Represja={self.repression}"

@dataclass
class Game:
    districts: list = field(default_factory=list)
    influence: int = 0
    turn: int = 0
    revolution_threshold: int = 60

    def __post_init__(self):
        if not self.districts:
            self.districts = [
                District("Centrum"),
                District("Industrial"),
                District("Stare Miasto"),
                District("Zoliborz"),
                District("Port"),
            ]

    def print_board(self):
        print(f"\nTura: {self.turn}, Wplyw: {self.influence}\n")
        for d in self.districts:
            print(d.summary())
        print()

    def choose_action(self):
        print("Akcje:")
        actions = [
            "1. Agitacja",
            "2. Sabotaz",
            "3. Zamieszki",
            "4. Przejecie Mediów",
            "5. Skonc z tura",
        ]
        for a in actions:
            print(a)
        choice = input("Wybierz akcje: ")
        return choice.strip()

    def action_agitate(self, district: District):
        success = random.random() < 0.7
        if success:
            district.activism += 10
            self.influence += 2
            print(f"Agitacja w {district.name} powiodla sie.")
        else:
            district.repression += 5
            print(f"Agitacja w {district.name} nieudana, represja wzrasta.")

    def action_sabotage(self, district: District):
        success = random.random() < 0.5
        if success:
            district.loyalty -= 15
            self.influence += 3
            print(f"Sabotaz w {district.name} udany.")
        else:
            district.repression += 10
            print(f"Sabotaz w {district.name} nieudany, represja wzrasta.")

    def action_riots(self, district: District):
        success = random.random() < 0.4
        if success:
            district.loyalty -= 10
            district.repression += 15
            self.influence += 5
            print(f"Zamieszki w {district.name} rozprzestrzeniaja sie!")
        else:
            district.repression += 20
            print(f"Zamieszki w {district.name} stlumione.")

    def action_media(self, district: District):
        success = random.random() < 0.3
        if success:
            district.loyalty -= 20
            self.influence += 10
            print(f"Udalo sie przejac media w {district.name}!")
        else:
            district.repression += 25
            print(f"Proba przejecia mediow w {district.name} nieudana.")

    def government_reaction(self):
        total_activism = sum(d.activism for d in self.districts)
        if total_activism > 200:
            for d in self.districts:
                d.repression += 5
            print("Rzad zwieksza represje w odpowiedzi na wzrost aktywizmu.")

    def check_revolution(self):
        controlled = sum(1 for d in self.districts if d.activism > d.loyalty)
        percent = controlled / len(self.districts) * 100
        return percent >= self.revolution_threshold

    def turn_loop(self):
        self.turn += 1
        self.print_board()
        choice = self.choose_action()
        if choice == '1':
            d = self.select_district()
            self.action_agitate(d)
        elif choice == '2':
            d = self.select_district()
            self.action_sabotage(d)
        elif choice == '3':
            d = self.select_district()
            self.action_riots(d)
        elif choice == '4':
            d = self.select_district()
            self.action_media(d)
        elif choice == '5':
            print("Koniec tury")
        else:
            print("Nieznana akcja")

        self.government_reaction()

    def select_district(self) -> District:
        for idx, d in enumerate(self.districts, 1):
            print(f"{idx}. {d.name}")
        while True:
            try:
                idx = int(input("Wybierz dzielnice: "))
                if 1 <= idx <= len(self.districts):
                    return self.districts[idx-1]
            except ValueError:
                pass
            print("Zly wybor. Sprobuj ponownie.")

    def play(self):
        print("=== Rewolt - Symulator Wzniecania Rewolucji ===")
        while True:
            self.turn_loop()
            if self.check_revolution():
                print("\nTwoje dzialania przechylily szale! Ogolnokrajowe powstanie wybucha!")
                print("*** Zwyciestwo! ***")
                break
            if any(d.repression > 100 for d in self.districts):
                print("\nRepresja przekroczyla granice. Twoj ruch zostal zduszony.")
                print("*** Porażka ***")
                break

if __name__ == "__main__":
    game = Game()
    game.play()
