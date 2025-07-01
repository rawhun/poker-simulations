Texas Hold'em Poker Simulation & Analysis Engine

A comprehensive Python-based Texas Hold'em poker simulator designed for playing out hands, running tournaments, and analyzing strategy through Monte Carlo simulations.

Features

- Core Game Logic: Complete Texas Hold'em implementation with deck management, player actions, and round progression
- Monte Carlo Simulations: Run thousands of hands to analyze strategy and calculate equity
- Tournament Support: Multi-table tournament simulation with blind schedules
- Analytics: Track hand histories, compute metrics (VPIP, PFR, showdown frequency), and generate equity calculations
- Visualization: Plot bankroll curves, equity heatmaps, and strategy comparisons
- Modular Design: Clean, well-documented codebase with comprehensive unit tests

Installation

1. Clone the repository:
git clone <repository-url>
cd poker-simulations

2. Install dependencies:
pip install -r requirements.txt

Quick Start

Basic Hand Simulation
from poker.engine import PokerGame
from poker.player import Player

Create players
player1 = Player("Alice", stack=1000)
player2 = Player("Bob", stack=1000)

Create and run a game
game = PokerGame([player1, player2], small_blind=10, big_blind=20)
result = game.play_hand()
print(result)

Monte Carlo Simulation
from simulate import run_monte_carlo

Run 10,000 hands
results = run_monte_carlo(
    num_hands=10000,
    players=2,
    starting_stack=1000,
    small_blind=10
)
print(f"Average pot size: {results['avg_pot']}")

Equity Analysis
from poker.analysis import calculate_equity

Calculate equity for AKs vs QQ
equity = calculate_equity("AKs", "QQ", iterations=10000)
print(f"AKs vs QQ equity: {equity:.2%}")

Project Structure
poker/
├── deck.py      # Card and deck management
├── player.py    # Player classes and actions
├── engine.py    # Game engine and rules
└── analysis.py  # Analytics and equity calculations

simulate.py      # Batch simulation runner
interactive.py   # Interactive CLI/Jupyter interface
tests/           # Unit tests
demo_notebook.ipynb  # Jupyter demo


Usage Examples
Running a Tournament
from poker.engine import Tournament

tournament = Tournament(
    players=9,
    starting_stack=10000,
    blind_schedule=[(25, 50), (50, 100), (100, 200)]
)
winner = tournament.run()

Strategy Analysis
from poker.analysis import analyze_strategy

Analyze VPIP and PFR for a player
stats = analyze_strategy(player_hands, player_name="Alice")
print(f"VPIP: {stats['vpip']:.1%}, PFR: {stats['pfr']:.1%}")

Performance

- Hand Evaluation: ~1,000 hands/second on modern hardware
- **Equity Calculation: ~10,000 iterations/second for head-to-head matchups
- Tournament Simulation: ~100 hands/second for 9-player tournaments

Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

References

- [Treys Hand Evaluator](https://github.com/munvo/treys)
- [Poker Equity Basics](https://www.codingthewheel.com/archives/evaluate-texas-holdem-poker-hands/)
- [Texas Hold'em Rules](https://en.wikipedia.org/wiki/Texas_hold_%27em)