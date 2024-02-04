from typing import Generator


class Player:
    def __init__(self, first_name: str, last_name: str):
        self.first_name: str = first_name
        self.last_name: str = last_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


team: list[Player] = [
    Player("John", "Smith"),
    Player("Marry", "Smith"),
    Player("Jack", "Hill"),
    Player("Nick", "Doe"),
    Player("John", "Doe"),
    Player("Marry", "Doe"),
]

for player in team:
    print(player)


# Output:
# John Smith
# Marry Smith
# Jack Hill
# Nick Doe
# John Doe


def dedup(collection) -> Generator[str, None, None]:
    see_all_component = set()
    for i in collection:
        if i.first_name not in see_all_component:
            see_all_component.add(i.first_name)
            yield str(i)


print("___________")
for player_names in dedup(team):
    print(player_names)

# Expected Output:
# John Smith
# Marry Smith
# Jack Hill
# Nick Doe

# Explaination:
# The dedup function should return a generator that yields the unique players in the team.
# The uniqueness of a player is determined by its first name only
