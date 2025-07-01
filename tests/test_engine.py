import unittest
from poker.player import Player, Action
from poker.deck import Card, Rank, Suit

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player('Test', stack=100)

    def test_receive_and_clear_hand(self):
        cards = [Card(Rank.ACE, Suit.SPADES), Card(Rank.KING, Suit.HEARTS)]
        self.player.receive_cards(cards)
        self.assertEqual(len(self.player.hand), 2)
        self.player.clear_hand()
        self.assertEqual(len(self.player.hand), 0)

    def test_fold_and_check(self):
        self.assertTrue(self.player.is_active)
        self.player.fold()
        self.assertFalse(self.player.is_active)
        self.player.is_active = True
        self.player.check()
        self.assertTrue(self.player.is_active)

    def test_bet_and_all_in(self):
        action = self.player.bet(50)
        self.assertEqual(self.player.stack, 50)
        action = self.player.all_in()
        self.assertEqual(self.player.stack, 0)
        self.assertTrue(self.player.is_all_in)

    def test_stats(self):
        self.player.record_hand_result(True, 50)
        stats = self.player.get_stats()
        self.assertIn('win_rate', stats)
        self.assertIn('vpip', stats)

if __name__ == '__main__':
    unittest.main() 