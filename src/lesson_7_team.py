# CRUD (Create Read Update Delete) operations
import csv
from typing import Optional

# Database representation


team: dict[int, dict] = {
    1: {"name": "John", "age": 20, "number": 1},
    3: {"name": "Mark", "age": 33, "number": 3},
    12: {"name": "Cavin", "age": 31, "number": 12},
}


# Application source code
def repr_players(players: dict[int, dict]):
    for player in players.values():
        print(f"\t[Player {player['number']}]: {player['name']},{player['age']}")


def player_add(name: str, age: int, number: int) -> Optional[dict]:
    if number in team:
        print(f"Player with number {number} already exists.")
        return None

    team[number] = {"name": name, "age": age, "number": number}
    return team[number]


def player_delete(number: int) -> None:
    if number in team:
        del team[number]


def save_to_csv_file() -> None:
    with open("players.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "age", "number"])
        for players in team.values():
            writer.writerow([players["name"], players["age"], players["number"]])


def main():
    operations = ("add", "del", "repr", "exit", "update")

    while True:
        operation = input("Please enter the operation: ")
        if operation not in operations:
            print(f"Operation: '{operation}' is not available\n")
            continue

        if operation == "exit":
            save_to_csv_file()
            print("Players saved to CSV successfully. Bye")

            break
        elif operation == "repr":
            repr_players(team)
        elif operation == "add":
            user_data = input("Enter new player information[name,age,number]: ")
            name, age, number = user_data.split(",")

            try:
                player_add(name=name, age=int(age), number=int(number))
            except ValueError:
                print("Age and number of player must be integers\n\n")
                continue
        elif operation == "update":
            try:
                number = int(input("Enter the number of the player to update: "))
            except ValueError:
                print("Number of player must be integers\n\n")
                continue

            player_update(number)
        else:
            raise NotImplementedError


def player_update(number: int) -> None:
    if number in team:
        print("Enter new information for the player (name,age): ")
        name, age = input().split(",")
        try:
            team[number]["name"] = name
            team[number]["age"] = int(age)
            print("Player updated successfully.")
        except ValueError:
            print("Invalid input. Age must be an integer.")
    else:
        print(f"Player with number {number} not found.")


if __name__ == "__main__":
    main()
