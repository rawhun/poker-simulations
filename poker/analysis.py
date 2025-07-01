"""
Analysis and equity calculation for Texas Hold'em poker.

This module provides functions for equity calculation, strategy analysis,
metrics computation, and plotting utilities.
"""

from typing import List, Dict, Any, cast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# For hand evaluation, use treys
from treys import Evaluator, Card as TreysCard

def calculate_equity(hand1: str, hand2: str, iterations: int = 10000) -> float:
    """
    Monte Carlo equity calculation for two hands.
    Args:
        hand1: e.g. 'AKs' or 'AhKh'
        hand2: e.g. 'QQ' or 'QdQc'
        iterations: Number of simulations
    Returns:
        Equity (win probability) for hand1 vs hand2
    """
    import random
    from treys import Deck as TreysDeck

    def parse_hand(hand_str):
        # Accepts 'AhKh' or 'AKs' or 'QQ' style
        ranks = '23456789TJQKA'
        suits = 'cdhs'
        if len(hand_str) == 4:  # e.g. AhKh
            return [TreysCard.new(hand_str[:2]), TreysCard.new(hand_str[2:])]
        elif len(hand_str) == 2:  # e.g. QQ
            r = hand_str[0]
            s = hand_str[1]
            if s == 's':  # suited
                # Return all suited combos
                return [[TreysCard.new(r + suit1), TreysCard.new(r + suit2)]
                        for suit1 in suits for suit2 in suits if suit1 != suit2]
            else:
                # Pair, return all combos
                return [[TreysCard.new(r + s1), TreysCard.new(r + s2)]
                        for s1 in suits for s2 in suits if s1 != s2]
        elif len(hand_str) == 3:  # e.g. AKs
            r1, r2, suited = hand_str[0], hand_str[1], hand_str[2]
            if suited == 's':
                return [[TreysCard.new(r1 + s), TreysCard.new(r2 + s)] for s in suits]
            else:
                return [[TreysCard.new(r1 + s1), TreysCard.new(r2 + s2)]
                        for s1 in suits for s2 in suits if s1 != s2]
        else:
            raise ValueError(f"Invalid hand string: {hand_str}")

    evaluator = Evaluator()
    wins = 0
    ties = 0
    for _ in range(iterations):
        deck = TreysDeck()
        # Parse hands
        h1 = parse_hand(hand1)
        h2 = parse_hand(hand2)
        # If multiple combos, pick one at random
        if isinstance(h1[0], list):
            h1 = random.choice(h1)
        if isinstance(h2[0], list):
            h2 = random.choice(h2)
        # Ensure h1 and h2 are lists of two ints
        if not (isinstance(h1, list) and len(h1) == 2 and all(isinstance(x, int) for x in h1)):
            continue
        if not (isinstance(h2, list) and len(h2) == 2 and all(isinstance(x, int) for x in h2)):
            continue
        # Remove hole cards from deck
        for c in h1:
            if c in deck.cards:
                deck.cards.remove(c)
        for c in h2:
            if c in deck.cards:
                deck.cards.remove(c)
        # Deal 5 community cards
        board = [deck.draw(1)[0] for _ in range(5)]
        if not (len(board) == 5 and all(isinstance(x, int) for x in board)):
            continue
        # Now h1, h2, and board are all lists of ints
        h1 = cast(list[int], h1)
        h2 = cast(list[int], h2)
        board = cast(list[int], board)
        score1 = evaluator.evaluate(board, h1)
        score2 = evaluator.evaluate(board, h2)
        if score1 < score2:
            wins += 1
        elif score1 == score2:
            ties += 1
    return (wins + 0.5 * ties) / iterations

def analyze_strategy(hand_histories: List[Dict[str, Any]], player_name: str) -> Dict[str, float]:
    """
    Analyze a player's strategy from hand histories.
    Args:
        hand_histories: List of hand history dicts
        player_name: Name of player to analyze
    Returns:
        Dict of metrics: VPIP, PFR, showdown frequency, etc.
    """
    # TODO: Implement strategy analysis
    return {}

def plot_results(data: pd.DataFrame, metric: str = 'bankroll'):
    """
    Plot results (e.g., bankroll over time) using matplotlib.
    Args:
        data: DataFrame with results
        metric: Column to plot
    """
    # TODO: Implement plotting
    pass 