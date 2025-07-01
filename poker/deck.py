"""
Deck and card management for Texas Hold'em poker.

This module provides Card and Deck classes for representing poker cards,
shuffling, dealing, and managing the deck during gameplay.
"""

import random
from typing import List, Optional
from enum import Enum


class Suit(Enum):
    """Poker card suits."""
    HEARTS = "h"
    DIAMONDS = "d"
    CLUBS = "c"
    SPADES = "s"


class Rank(Enum):
    """Poker card ranks."""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Card:
    """
    Represents a single poker card.
    
    Attributes:
        rank (Rank): The card's rank (2-14, where 14 is Ace)
        suit (Suit): The card's suit (hearts, diamonds, clubs, spades)
        treys_value (int): Integer representation for treys hand evaluator
    """
    
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
        self.treys_value = self._calculate_treys_value()
    
    def _calculate_treys_value(self) -> int:
        """Calculate the integer value used by treys hand evaluator."""
        # Treys uses: rank + (suit * 13)
        suit_values = {Suit.CLUBS: 0, Suit.DIAMONDS: 1, Suit.HEARTS: 2, Suit.SPADES: 3}
        return self.rank.value + (suit_values[self.suit] * 13)
    
    @classmethod
    def from_string(cls, card_str: str) -> 'Card':
        """
        Create a Card from a string representation.
        
        Args:
            card_str: String like "Ah" (Ace of hearts) or "Kd" (King of diamonds)
            
        Returns:
            Card object
            
        Raises:
            ValueError: If card string is invalid
        """
        if len(card_str) != 2:
            raise ValueError(f"Invalid card string: {card_str}")
        
        rank_char = card_str[0].upper()
        suit_char = card_str[1].lower()
        
        # Parse rank
        rank_map = {
            '2': Rank.TWO, '3': Rank.THREE, '4': Rank.FOUR, '5': Rank.FIVE,
            '6': Rank.SIX, '7': Rank.SEVEN, '8': Rank.EIGHT, '9': Rank.NINE,
            'T': Rank.TEN, 'J': Rank.JACK, 'Q': Rank.QUEEN, 'K': Rank.KING, 'A': Rank.ACE
        }
        
        if rank_char not in rank_map:
            raise ValueError(f"Invalid rank: {rank_char}")
        
        # Parse suit
        suit_map = {
            'h': Suit.HEARTS, 'd': Suit.DIAMONDS, 'c': Suit.CLUBS, 's': Suit.SPADES
        }
        
        if suit_char not in suit_map:
            raise ValueError(f"Invalid suit: {suit_char}")
        
        return cls(rank_map[rank_char], suit_map[suit_char])
    
    def __str__(self) -> str:
        """String representation like 'Ah' for Ace of hearts."""
        rank_chars = {
            Rank.TWO: '2', Rank.THREE: '3', Rank.FOUR: '4', Rank.FIVE: '5',
            Rank.SIX: '6', Rank.SEVEN: '7', Rank.EIGHT: '8', Rank.NINE: '9',
            Rank.TEN: 'T', Rank.JACK: 'J', Rank.QUEEN: 'Q', Rank.KING: 'K', Rank.ACE: 'A'
        }
        return f"{rank_chars[self.rank]}{self.suit.value}"
    
    def __repr__(self) -> str:
        return f"Card({self.rank.name}, {self.suit.name})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self) -> int:
        return hash((self.rank, self.suit))


class Deck:
    """
    Represents a standard 52-card poker deck.
    
    Provides methods for shuffling, dealing, and managing the deck during gameplay.
    """
    
    def __init__(self):
        """Initialize a fresh deck with all 52 cards."""
        self.cards = []
        self.reset()
    
    def reset(self):
        """Reset the deck to a fresh 52-card deck."""
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))
    
    def shuffle(self):
        """Shuffle the deck using Fisher-Yates algorithm."""
        random.shuffle(self.cards)
    
    def deal(self, num_cards: int = 1) -> List[Card]:
        """
        Deal cards from the top of the deck.
        
        Args:
            num_cards: Number of cards to deal
            
        Returns:
            List of dealt cards
            
        Raises:
            ValueError: If trying to deal more cards than available
        """
        if num_cards > len(self.cards):
            raise ValueError(f"Cannot deal {num_cards} cards, only {len(self.cards)} remaining")
        
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards
    
    def deal_one(self) -> Optional[Card]:
        """
        Deal a single card from the top of the deck.
        
        Returns:
            Card object or None if deck is empty
        """
        if not self.cards:
            return None
        return self.cards.pop(0)
    
    def burn_card(self):
        """Burn a card (remove from deck without dealing it)."""
        if self.cards:
            self.cards.pop(0)
    
    def remaining_cards(self) -> int:
        """Return the number of cards remaining in the deck."""
        return len(self.cards)
    
    def is_empty(self) -> bool:
        """Check if the deck is empty."""
        return len(self.cards) == 0
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __str__(self) -> str:
        return f"Deck({len(self.cards)} cards remaining)"
    
    def __repr__(self) -> str:
        return f"Deck(cards={len(self.cards)})"