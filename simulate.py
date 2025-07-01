"""
Batch simulation runner for Texas Hold'em Poker.

Usage:
    python simulate.py --hands 10000 --players 2 --stack 1000
"""
import argparse
from poker.engine import PokerGame, Tournament
from poker.player import Player
import pandas as pd
import matplotlib.pyplot as plt

def run_monte_carlo(num_hands=10000, players=2, starting_stack=1000, small_blind=10, big_blind=20):
    results = []
    player_stacks = [[starting_stack] for _ in range(players)]
    player_wins = [0 for _ in range(players)]
    player_showdowns = [0 for _ in range(players)]
    player_names = [f"Player {i+1}" for i in range(players)]
    for i in range(num_hands):
        player_objs = [Player(name, stack=player_stacks[j][-1]) for j, name in enumerate(player_names)]
        game = PokerGame(player_objs, small_blind=small_blind, big_blind=big_blind)
        hand_result = game.play_hand()
        results.append(hand_result)
        # Track stacks
        for j, p in enumerate(player_objs):
            player_stacks[j].append(p.stack)
        # Track wins
        for j, p in enumerate(player_objs):
            if p.name in hand_result['winners']:
                player_wins[j] += 1
        # Track showdowns
        for j, p in enumerate(player_objs):
            if p.name in hand_result['winners'] or p.name in [a.split()[0] for a in hand_result['hand_history'] if 'all-in' in a or 'calls' in a]:
                player_showdowns[j] += 1
    return results, player_stacks, player_wins, player_showdowns, player_names

def main():
    parser = argparse.ArgumentParser(description="Texas Hold'em Poker Monte Carlo Simulator")
    parser.add_argument('--hands', type=int, default=10000, help='Number of hands to simulate')
    parser.add_argument('--players', type=int, default=2, help='Number of players')
    parser.add_argument('--stack', type=int, default=1000, help='Starting stack size')
    parser.add_argument('--sb', type=int, default=10, help='Small blind')
    parser.add_argument('--bb', type=int, default=20, help='Big blind')
    parser.add_argument('--plot', action='store_true', help='Plot Player 1 bankroll over time')
    parser.add_argument('--plot-winrate', action='store_true', help='Plot win rate over time')
    parser.add_argument('--plot-stacks', action='store_true', help='Plot stack distribution at end')
    parser.add_argument('--tournament', action='store_true', help='Run a tournament simulation')
    parser.add_argument('--export-csv', type=str, default='', help='Export hand results to CSV file')
    parser.add_argument('--export-json', type=str, default='', help='Export hand results to JSON file')
    args = parser.parse_args()

    if args.tournament:
        blind_schedule = [(args.sb, args.bb), (args.sb*2, args.bb*2), (args.sb*4, args.bb*4)]
        tournament = Tournament(players=args.players, starting_stack=args.stack, blind_schedule=blind_schedule)
        winner = tournament.run()
        print(f"Tournament winner: {winner.name}")
        print(f"Total hands played: {tournament.hands_played}")
        return

    results, player_stacks, player_wins, player_showdowns, player_names = run_monte_carlo(
        num_hands=args.hands, players=args.players, starting_stack=args.stack, small_blind=args.sb, big_blind=args.bb)
    df = pd.DataFrame(results)
    print(df.describe())
    # Showdown frequency
    print("Showdown frequency:")
    for i, name in enumerate(player_names):
        print(f"{name}: {player_showdowns[i]} showdowns, {player_wins[i]} wins")
    # Export analytics
    if args.export_csv:
        df.to_csv(args.export_csv, index=False)
        print(f"Exported hand results to {args.export_csv}")
    if args.export_json:
        df.to_json(args.export_json, orient='records', lines=True)
        print(f"Exported hand results to {args.export_json}")
    # Plotting
    if args.plot:
        plt.plot(player_stacks[0])
        plt.title("Player 1 Bankroll Over Time")
        plt.xlabel("Hand Number")
        plt.ylabel("Stack Size")
        plt.show()
    if args.plot_winrate:
        win_rates = [w / args.hands for w in player_wins]
        plt.bar(player_names, win_rates)
        plt.title("Win Rate by Player")
        plt.ylabel("Win Rate")
        plt.show()
    if args.plot_stacks:
        final_stacks = [stacks[-1] for stacks in player_stacks]
        plt.bar(player_names, final_stacks)
        plt.title("Final Stack Distribution")
        plt.ylabel("Stack Size")
        plt.show()

if __name__ == "__main__":
    main() 