"""
Player management for Texas Hold'em poker.

This module provides Player class and Action enum for representing players,
their actions, and managing player state during gameplay.
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
from .deck import Card


class Action(Enum):
    """Player actions in poker."""
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all_in"


@dataclass
class PlayerAction:
    """Represents a player's action in a hand."""
    player: 'Player'
    action: Action
    amount: int = 0
    street: str = ""  # preflop, flop, turn, river
    
    def __str__(self) -> str:
        if self.action == Action.FOLD:
            return f"{self.player.name} folds"
        elif self.action == Action.CHECK:
            return f"{self.player.name} checks"
        elif self.action == Action.CALL:
            return f"{self.player.name} calls {self.amount}"
        elif self.action == Action.BET:
            return f"{self.player.name} bets {self.amount}"
        elif self.action == Action.RAISE:
            return f"{self.player.name} raises to {self.amount}"
        elif self.action == Action.ALL_IN:
            return f"{self.player.name} all-in {self.amount}"
        return f"{self.player.name} {self.action.value}"


class Player:
    """
    Represents a poker player.
    
    Attributes:
        name (str): Player's name
        stack (int): Current chip stack
        hand (List[Card]): Player's hole cards
        position (str): Player's position (UTG, MP, CO, BTN, SB, BB)
        is_active (bool): Whether player is still in the current hand
        is_all_in (bool): Whether player is all-in
        total_bet (int): Total amount bet in current hand
        last_action (Optional[PlayerAction]): Player's last action
    """
    
    def __init__(self, name: str, stack: int = 1000):
        self.name = name
        self.stack = stack
        self.hand: List[Card] = []
        self.position = ""
        self.is_active = True
        self.is_all_in = False
        self.total_bet = 0
        self.last_action: Optional[PlayerAction] = None
        
        # Statistics tracking
        self.stats = {
            'hands_played': 0,
            'hands_won': 0,
            'total_profit': 0,
            'vpip_count': 0,  # Voluntarily Put Money In Pot
            'pfr_count': 0,   # Pre-Flop Raise
            'showdown_count': 0,
            'fold_count': 0,
            'total_bets': 0,
            'total_raises': 0,
            'win_rate': 0.0,
            'vpip': 0.0,
            'pfr': 0.0,
            'fold_rate': 0.0
        }
    
    def receive_cards(self, cards: List[Card]):
        """Receive hole cards."""
        self.hand = cards.copy()
    
    def clear_hand(self):
        """Clear the player's hand."""
        self.hand = []
        self.is_active = True
        self.is_all_in = False
        self.total_bet = 0
        self.last_action = None
    
    def fold(self) -> PlayerAction:
        """Player folds."""
        self.is_active = False
        action = PlayerAction(self, Action.FOLD)
        self.last_action = action
        self.stats['fold_count'] += 1
        return action
    
    def check(self) -> PlayerAction:
        """Player checks (only if no bet to call)."""
        action = PlayerAction(self, Action.CHECK)
        self.last_action = action
        return action
    
    def call(self, amount: int) -> PlayerAction:
        """Player calls a bet."""
        if amount > self.stack:
            return self.all_in()
        
        self.stack -= amount
        self.total_bet += amount
        action = PlayerAction(self, Action.CALL, amount)
        self.last_action = action
        self.stats['vpip_count'] += 1
        return action
    
    def bet(self, amount: int) -> PlayerAction:
        """Player makes a bet."""
        if amount >= self.stack:
            return self.all_in()
        
        self.stack -= amount
        self.total_bet += amount
        action = PlayerAction(self, Action.BET, amount)
        self.last_action = action
        self.stats['vpip_count'] += 1
        self.stats['total_bets'] += 1
        return action
    
    def raise_to(self, amount: int) -> PlayerAction:
        """Player raises to a specific amount."""
        if amount >= self.stack:
            return self.all_in()
        
        call_amount = amount - self.total_bet
        self.stack -= call_amount
        self.total_bet += call_amount
        action = PlayerAction(self, Action.RAISE, amount)
        self.last_action = action
        self.stats['vpip_count'] += 1
        self.stats['pfr_count'] += 1
        self.stats['total_raises'] += 1
        return action
    
    def all_in(self) -> PlayerAction:
        """Player goes all-in."""
        amount = self.stack
        self.stack = 0
        self.total_bet += amount
        self.is_all_in = True
        action = PlayerAction(self, Action.ALL_IN, amount)
        self.last_action = action
        self.stats['vpip_count'] += 1
        return action
    
    def can_afford(self, amount: int) -> bool:
        """Check if player can afford a bet."""
        return self.stack >= amount
    
    def get_call_amount(self, current_bet: int) -> int:
        """Get the amount needed to call the current bet."""
        return max(0, current_bet - self.total_bet)
    
    def get_min_raise_amount(self, current_bet: int, min_raise: int) -> int:
        """Get the minimum raise amount."""
        return current_bet + min_raise
    
    def is_in_hand(self) -> bool:
        """Check if player is still in the current hand."""
        return self.is_active and not self.is_all_in
    
    def has_folded(self) -> bool:
        """Check if player has folded."""
        return not self.is_active
    
    def get_hand_string(self) -> str:
        """Get string representation of player's hand."""
        if not self.hand:
            return "No cards"
        return " ".join(str(card) for card in self.hand)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get player statistics."""
        stats = self.stats.copy()
        if stats['hands_played'] > 0:
            stats['win_rate'] = stats['hands_won'] / stats['hands_played']
            stats['vpip'] = stats['vpip_count'] / stats['hands_played']
            stats['pfr'] = stats['pfr_count'] / stats['hands_played']
            stats['fold_rate'] = stats['fold_count'] / stats['hands_played']
        else:
            stats['win_rate'] = 0.0
            stats['vpip'] = 0.0
            stats['pfr'] = 0.0
            stats['fold_rate'] = 0.0
        
        return stats
    
    def record_hand_result(self, won: bool, profit: int):
        """Record the result of a hand."""
        self.stats['hands_played'] += 1
        if won:
            self.stats['hands_won'] += 1
        self.stats['total_profit'] += profit
    
    def record_showdown(self):
        """Record that player reached showdown."""
        self.stats['showdown_count'] += 1
    
    def __str__(self) -> str:
        return f"{self.name} (${self.stack})"
    
    def __repr__(self) -> str:
        return f"Player('{self.name}', stack={self.stack})"


class AIPokerPlayer(Player):
    """
    AI Poker Player with simple learning (adjusts aggression based on outcomes).
    """
    def __init__(self, name: str, stack: int = 1000):
        super().__init__(name, stack)
        self.aggression = 0.5  # 0 = passive, 1 = aggressive
        self.memory = []  # List of (action, result) tuples

    def learn_from_hand(self, won: bool, last_action: str):
        """Adjust aggression based on outcome of last hand."""
        self.memory.append((last_action, won))
        # Simple: if lost after aggressive action, be less aggressive; if won, be more aggressive
        if last_action in ('bet', 'raise', 'all_in'):
            if won:
                self.aggression = min(1.0, self.aggression + 0.05)
            else:
                self.aggression = max(0.0, self.aggression - 0.05)
        elif last_action in ('fold', 'check', 'call'):
            if won:
                self.aggression = max(0.0, self.aggression - 0.02)
            else:
                self.aggression = min(1.0, self.aggression + 0.02) 