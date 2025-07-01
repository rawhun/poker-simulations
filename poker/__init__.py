"""
Texas Hold'em Poker Simulation & Analysis Engine

A comprehensive Python-based poker simulator for playing hands, running tournaments,
and analyzing strategy through Monte Carlo simulations.
"""

__version__ = "1.0.0"
__author__ = "Poker Simulations Team"

from .deck import Card, Deck
from .player import Player, Action
from .engine import PokerGame, Tournament
from .analysis import calculate_equity, analyze_strategy, plot_results

__all__ = [
    'Card', 'Deck', 'Player', 'Action', 'PokerGame', 'Tournament',
    'calculate_equity', 'analyze_strategy', 'plot_results'
]