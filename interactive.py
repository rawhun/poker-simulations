"""
Interactive CLI for Texas Hold'em Poker.

Usage:
    python interactive.py
"""
from poker.engine import PokerGame
from poker.player import Player
from typing import Dict, Any, cast

def play_hand_cli():
    print("Welcome to Texas Hold'em Poker!")
    num_players = input("Enter number of players (2-9): ")
    try:
        num_players = int(num_players)
        if num_players < 2 or num_players > 9:
            print("Number of players must be between 2 and 9.")
            return
    except ValueError:
        print("Invalid number.")
        return
    player_names = []
    for i in range(num_players):
        if i == 0:
            name = input(f"Enter your name (Player {i+1}): ")
            player_names.append(name)
        else:
            player_names.append(f"AI {i+1}")
    players = [Player(name, stack=1000) for name in player_names]
    game = PokerGame(players, small_blind=10, big_blind=20)
    result = game.play_hand()
    print("\n--- Hand Result ---")
    print(result)
    print(f"Winners: {', '.join(result['winners'])}")
    print(f"Pot: {result['pot']}")
    print(f"Community Cards: {' '.join(result['community_cards'])}")
    print("Player Hands:")
    for pname, hand in result['player_hands'].items():
        print(f"  {pname}: {hand}")
    print("Hand History:")
    for action in result['hand_history']:
        print(f"  {action}")
    print("-------------------\n")

def quick_simulation():
    print("Running a quick simulation of 100 hands...")
    from simulate import run_monte_carlo
    results = run_monte_carlo(num_hands=100, players=2, starting_stack=1000)
    print(f"Simulated 100 hands. Example result:")
    result = cast(Dict[str, Any], results[0])
    print(f"Winners: {', '.join(result['winners'])}")
    print(f"Pot: {result['pot']}")
    print(f"Community Cards: {' '.join(result['community_cards'])}")
    print("Player Hands:")
    for pname, hand in result['player_hands'].items():
        print(f"  {pname}: {hand}")
    print("Hand History:")
    for action in result['hand_history']:
        print(f"  {action}")
    print("-------------------\n")

def main():
    print("1. Play a hand interactively")
    print("2. Run a quick simulation")
    choice = input("Choose an option (1/2): ")
    if choice == '1':
        play_hand_cli()
    elif choice == '2':
        quick_simulation()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main() 