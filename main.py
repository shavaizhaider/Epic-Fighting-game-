import random
import time

game_data = {
    "player": {
        "name": "Warrior Hero",
        "health": 100,
        "max_health": 100,
        "attack": 20,
        "defense": 10,
        "potions": 3,
        "gold": 0
    },
    "enemies": {
        "Goblin 1": {"name": "Goblin 1", "health": 40,  "attack": 12, "defense": 3, "gold_reward": 20},
        "Goblin 2": {"name": "Goblin 2", "health": 45,  "attack": 14, "defense": 4, "gold_reward": 25},
        "Orc 1": {"name": "Orc 1", "health": 70,  "attack": 18, "defense": 6, "gold_reward": 40},
        "Orc 2": {"name": "Orc 2", "health": 80,  "attack": 20, "defense": 8, "gold_reward": 50},
        "Dragon": {"name": "The Dragon (Boss)", "attack": 30, "defense": 12,
                   "gold_reward": 100}
    }
}

game_stats = {
    "enemies_defeated": 0,
    "potions_used": 0,
    "gold_earned": 0,
    "total_damage_dealt": 0
}


def calculate_damage(attacker, defender):
    base_dmg = attacker["attack"] - defender["defense"]
    if base_dmg < 1:
        base_dmg = 1

    roll = random.randint(0, 10)

    if roll >= 9:
        final_dmg = base_dmg * 2
        return final_dmg, "CRITICAL HIT! (2x Damage)"
    elif roll <= 1:
        return 0, "MISSED!"
    else:
        final_dmg = base_dmg + roll
        return final_dmg, "Normal Hit"


def attack_enemy(player, enemy):
    print(f"\nYou slash at {enemy['name']}!")
    time.sleep(0.5)

    dmg, hit_type = calculate_damage(player, enemy)
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0

    game_stats["total_damage_dealt"] += dmg
    print 

    print(f"-> {hit_type} | Dealt {dmg} damage to {enemy['name']}.")
    print(f"-> {enemy['name']} HP: {enemy['health']}/{enemy['max_health']}")


def enemy_turn(enemy, player):
    print(f"\n{enemy['name']} attacks you!")
    time.sleep(0.5)

    dmg, hit_type = calculate_damage(enemy, player)
    player["health"] -= dmg
    if player["health"] < 0:
        player["health"] = 0

    print(f"-> {hit_type} | Received {dmg} damage from {enemy['name']}.")
    print(f"-> Your HP: {player['health']}/{player['max_health']}")


def use_potion(player):
    if player["potions"] > 0:
        if player["health"] == player["max_health"]:
            print("Your health is already full!")
            return False

        player["potions"] -= 1
        game_stats["potions_used"] += 1

        old_hp = player["health"]
        player["health"] = min(player["max_health"], player["health"] + 30)
        healed_amount = player["health"] - old_hp

        print(f"\nYou drank a health potion! Healed for {healed_amount} HP.")
        print(f"Current HP: {player['health']}/{player['max_health']} | Potions left: {player['potions']}")
        return True
    else:
        print("\nOut of potions! Buy more from the shop between waves.")
        return False


def shop_menu(player):
    while True:
        print("\n" + "=" * 35)
        print("WELCOME TO THE MERCHANTS SHOP")
        print("=" * 35)
        print(f"Your Gold: {player['gold']} | Attack: {player['attack']} | Potions: {player['potions']}")
        print("-" * 35)
        print("1. Buy Health Potion (+30 HP healing)   | Cost: 15 Gold")
        print("2. Upgrade Weapon (+5 Attack Power)      | Cost: 30 Gold")
        print("3. Buy Armor Kit (+3 Defense Power)      | Cost: 25 Gold")
        print("4. Exit Shop (Proceed to Next Wave)")
        print("-" * 35)

        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            if player["gold"] >= 15:
                player["gold"] -= 15
                player["potions"] += 1
                print("\nPurchased 1 Health Potion!")
            else:
                print("\nNot enough gold!")
        elif choice == '2':
            if player["gold"] >= 30:
                player["gold"] -= 30
                player["attack"] += 5
                print("\nWeapon upgraded! Your Attack Power is now:", player["attack"])
            else:
                print("\nNot enough gold!")
        elif choice == '3':
            if player["gold"] >= 25:
                player["gold"] -= 25
                player["defense"] += 3
                print("\nArmor upgraded! Your Defense Power is now:", player["defense"])
            else:
                print("\nNot enough gold!")
        elif choice == '4':
            print("\nLeaving the shop. Get ready for the next battle!")
            break
        else:
            print("\nInvalid choice! Please select 1, 2, 3, or 4.")


def print_final_report(player, won):
    status = "VICTORY!" if won else "DEFEAT"

    print("\n" + "x" + "=" * 48 + "x")
    print(f"|               GAME OVER - {status}               |")
    print("x" + "=" * 48 + "x")
    print(f"|  Stat Metric                           Value   |")
    print("x" + "=" * 48 + "x")
    print(f"|  Player Name                          {player['name']:<8} |")
    print(f"|  Enemies Defeated                     {game_stats['enemies_defeated']:<8} |")
    print(f"|  Potions Consumed                     {game_stats['potions_used']:<8} |")
    print(f"|  Total Gold Earned                    {game_stats['gold_earned']:<8} |")
    print(f"|  Remaining Gold                       {player['gold']:<8} |")
    print(f"|  Total Damage Dealt                   {game_stats['total_damage_dealt']:<8} |")
    print(f"|  Final Attack Power                   {player['attack']:<8} |")
    print(f"|  Final Defense Power                  {player['defense']:<8} |")
    print("x" + "=" * 48 + "x")
    print("\nThank you for playing!\n")


def combat_loop(player, enemy):
    print(f"\nA wild {enemy['name']} appears! (HP: {enemy['health']})")

    while enemy["health"] > 0 and player["health"] > 0:
        print("\n" + "-" * 30)
        print(f"YOUR TURN: HP {player['health']}/{player['max_health']} | Potion: {player['potions']}")
        print(f"ENEMY: {enemy['name']} HP {enemy['health']}/{enemy['max_health']}")
        print("-" * 30)
        print("1. Attack")
        print("2. Heal")
        print("3. Run Away")

        choice = input("What will you do? (1-3): ").strip()

        if choice == '1':
            attack_enemy(player, enemy)

            if enemy["health"] > 0:
                enemy_turn(enemy, player)

        elif choice == '2':
            healed = use_potion(player)
            if healed and enemy["health"] > 0:
                enemy_turn(enemy, player)

        elif choice == '3':
            print("\nYou fled from the battle.")
            print("Running away forfeits the wave rewards.")
            return "run"
        else:
            print("\nInvalid Input! Please enter 1, 2, or 3.")
            continue

    if player["health"] <= 0:
        return "lost"
    elif enemy["health"] <= 0:
        player["gold"] += enemy["gold_reward"]
        game_stats["gold_earned"] += enemy["gold_reward"]
        game_stats["enemies_defeated"] += 1
        print(f"\nYou defeated {enemy['name']}!")
        print(f"Loot found: +{enemy['gold_reward']} Gold Coins!")
        return "won"


def start_game():
    player = game_data["player"]
    enemies = game_data["enemies"]

    print("  WELCOME TO WARRIOR'S QUEST      ")
    player_name = input("Enter your hero's name: ").strip()
    if player_name:
        player["name"] = player_name

    print(f"\nGreetings, {player['name']}! Your journey starts now.")

    waves = [
        {"name": "Wave 1: Goblin Outpost", "enemies": ["Goblin 1", "Goblin 2"]},
        {"name": "Wave 2: Orc Stronghold", "enemies": ["Orc 1", "Orc 2"]},
        {"name": "Wave 3: The Dragon's Lair", "enemies": ["Dragon"]}
    ]

    game_won = True

    for i, wave in enumerate(waves):
        print(f"\n=========================================")
        print(f" STARTING {wave['name'].upper()} ")
        print(f"=========================================")
        time.sleep(1)

        for enemy_key in wave["enemies"]:
            enemy = enemies[enemy_key]
            result = combat_loop(player, enemy)

            if result == "lost":
                print(f"\nYou died! {enemy['name']} proved to be too strong.")
                game_won = False
                break
            elif result == "run":
                print("\nGame Over because you ran away!")
                game_won = False
                break

        if not game_won:
            break

        print(f"\nWave cleared successfully!")

        if i < len(waves) - 1:
            shop_menu(player)

    print_final_report(player, game_won)


if __name__ == "__main__":
    start_game()