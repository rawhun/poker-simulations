"""
Game engine for Texas Hold'em poker.

This module provides PokerGame and Tournament classes for managing game state,
round progression, pot management, and tournament simulation.
"""

from typing import List, Dict, Optional, Any
from .deck import Deck, Card
from .player import Player, Action, PlayerAction, AIPokerPlayer

class PokerGame:
    """
    Manages a single hand of Texas Hold'em poker.
    Handles round progression, betting, pot management, and showdown.
    """
    def __init__(self, players: List[Player], small_blind: int = 10, big_blind: int = 20, ante: int = 0):
        self.players = players
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.ante = ante
        self.deck = Deck()
        self.community_cards: List[Card] = []
        self.pot = 0
        self.side_pots: List[Dict[str, Any]] = []
        self.hand_history: List[PlayerAction] = []
        self.button_position = 0
        self.current_bet = 0
        self.street = "preflop"

    def play_hand(self) -> Dict[str, Any]:
        """
        Play a full hand of Texas Hold'em.
        Returns a dictionary with hand results and history.
        """
        self.reset_hand()
        self.deal_hole_cards()
        self.post_blinds_and_antes()
        self.betting_round("preflop")
        self.deal_community_cards(3)  # Flop
        self.betting_round("flop")
        self.deal_community_cards(1)  # Turn
        self.betting_round("turn")
        self.deal_community_cards(1)  # River
        self.betting_round("river")
        winners = self.showdown()
        pot_amount = self.pot  # Save pot before distributing
        self.distribute_pot(winners)
        # AI learning: update aggression based on outcome
        for player in self.players:
            if isinstance(player, AIPokerPlayer):
                last_action = player.last_action.action.value if player.last_action else 'check'
                player.learn_from_hand(player.name in [w.name for w in winners], last_action)
        result = {
            "winners": [p.name for p in winners] if winners else [],
            "pot": pot_amount,
            "community_cards": [str(card) for card in self.community_cards],
            "hand_history": [str(a) for a in self.hand_history],
            "player_hands": {p.name: p.get_hand_string() for p in self.players},
        }
        return result

    def deal_hole_cards(self):
        self.deck.shuffle()
        for player in self.players:
            player.receive_cards(self.deck.deal(2))

    def post_blinds_and_antes(self):
        # Simple: SB = player 0, BB = player 1
        if self.ante > 0:
            for player in self.players:
                player.stack -= self.ante
                self.pot += self.ante
        if len(self.players) > 1:
            sb_player = self.players[0]
            bb_player = self.players[1]
            sb_amt = min(self.small_blind, sb_player.stack)
            bb_amt = min(self.big_blind, bb_player.stack)
            sb_player.stack -= sb_amt
            bb_player.stack -= bb_amt
            sb_player.total_bet += sb_amt
            bb_player.total_bet += bb_amt
            self.pot += sb_amt + bb_amt
            self.current_bet = bb_amt
            self.hand_history.append(PlayerAction(sb_player, Action.BET, sb_amt, "preflop"))
            self.hand_history.append(PlayerAction(bb_player, Action.BET, bb_amt, "preflop"))

    def betting_round(self, street: str):
        # Smarter AI: fold weak, call/check medium, bet/raise strong
        from treys import Evaluator, Card as TreysCard
        evaluator = Evaluator()
        import random
        for player in self.players:
            if not player.is_active or player.is_all_in:
                continue
            to_call = self.current_bet - player.total_bet
            is_ai = isinstance(player, AIPokerPlayer)
            # Evaluate hand strength for AI
            hand_strength = 0.5
            if is_ai:
                aggression = player.aggression if hasattr(player, 'aggression') else 0.5
                if street == "preflop":
                    ranks = [c.rank.value for c in player.hand]
                    if ranks[0] == ranks[1] and ranks[0] >= 10:
                        hand_strength = 0.9
                    elif max(ranks) >= 12 and min(ranks) >= 11:
                        hand_strength = 0.8
                    elif max(ranks) >= 11:
                        hand_strength = 0.6
                    else:
                        hand_strength = 0.3
                else:
                    board = [TreysCard.new(str(card)) for card in self.community_cards]
                    hand = [TreysCard.new(str(card)) for card in player.hand]
                    score = evaluator.evaluate(board, hand)
                    hand_strength = 1 - evaluator.get_five_card_rank_percentage(score)
                # AI decision: use aggression to randomize betting/raising
                rand_val = random.random()
                if hand_strength + aggression * 0.5 >= 1.0 and to_call == 0 and player.stack > 0 and rand_val < aggression:
                    bet_amt = min(self.pot // 2 if self.pot > 0 else self.big_blind, player.stack)
                    player.stack -= bet_amt
                    player.total_bet += bet_amt
                    self.pot += bet_amt
                    self.current_bet = max(self.current_bet, player.total_bet)
                    action = PlayerAction(player, Action.BET, bet_amt, street)
                elif hand_strength + aggression * 0.5 >= 0.7 and player.stack >= to_call:
                    player.stack -= to_call
                    player.total_bet += to_call
                    self.pot += to_call
                    action = PlayerAction(player, Action.CALL, to_call, street)
                elif hand_strength + aggression * 0.5 < 0.5 and to_call > 0 and rand_val > aggression:
                    player.is_active = False
                    action = PlayerAction(player, Action.FOLD, 0, street)
                else:
                    action = PlayerAction(player, Action.CHECK, 0, street)
            else:
                if to_call > 0:
                    if player.stack >= to_call:
                        player.stack -= to_call
                        player.total_bet += to_call
                        self.pot += to_call
                        action = PlayerAction(player, Action.CALL, to_call, street)
                    else:
                        player.is_active = False
                        action = PlayerAction(player, Action.FOLD, 0, street)
                else:
                    action = PlayerAction(player, Action.CHECK, 0, street)
            self.hand_history.append(action)

    def deal_community_cards(self, num_cards: int):
        self.deck.burn_card()
        self.community_cards.extend(self.deck.deal(num_cards))

    def showdown(self):
        # Use treys to evaluate hands
        from treys import Evaluator, Card as TreysCard
        evaluator = Evaluator()
        best_score = None
        winners = []
        board = [TreysCard.new(str(card)) for card in self.community_cards]
        for player in self.players:
            if not player.is_active:
                continue
            hand = [TreysCard.new(str(card)) for card in player.hand]
            score = evaluator.evaluate(board, hand)
            if best_score is None or score < best_score:
                best_score = score
                winners = [player]
            elif score == best_score:
                winners.append(player)
        return winners

    def distribute_pot(self, winners):
        # Simple: split pot equally among winners
        if not winners:
            return
        share = self.pot // len(winners)
        for player in winners:
            player.stack += share
        self.pot = 0

    def reset_hand(self):
        self.deck.reset()
        self.community_cards = []
        self.pot = 0
        self.side_pots = []
        self.hand_history = []
        self.current_bet = 0
        self.street = "preflop"
        for player in self.players:
            player.clear_hand()
            player.total_bet = 0
            player.is_active = True
            player.is_all_in = False

class Tournament:
    """
    Manages a multi-table Texas Hold'em tournament.
    Handles blind schedule, player elimination, and table balancing.
    """
    def __init__(self, players: int, starting_stack: int, blind_schedule: List[tuple]):
        self.players = [Player(f"Player {i+1}", stack=starting_stack) for i in range(players)]
        self.blind_schedule = blind_schedule
        self.current_level = 0
        self.hands_played = 0
        self.active_players = self.players.copy()

    def run(self) -> Player:
        """
        Run the tournament until one player remains.
        Returns the winning Player.
        """
        blind_level = 0
        hands_per_level = 20
        self.hands_played = 0
        self.active_players = self.players.copy()
        while len([p for p in self.active_players if p.stack > 0]) > 1:
            # Set blinds for this level
            sb, bb = self.blind_schedule[min(blind_level, len(self.blind_schedule)-1)]
            # Remove busted players
            self.active_players = [p for p in self.active_players if p.stack > 0]
            # Play a hand
            game = PokerGame(self.active_players, small_blind=sb, big_blind=bb)
            game.play_hand()
            self.hands_played += 1
            # Advance blinds every N hands
            if self.hands_played % hands_per_level == 0:
                blind_level += 1
        # Return the last player with chips
        winner = [p for p in self.active_players if p.stack > 0][0]
        return winner

    def advance_blinds(self):
        """Advance to the next blind level."""
        # TODO: Implement blind advancement
        pass

    def eliminate_players(self):
        """Eliminate players with zero chips."""
        # TODO: Implement elimination logic
        pass 