import unittest
from poker.deck import Card, Deck, Suit, Rank

class TestDeck(unittest.TestCase):
    def test_deck_has_52_cards(self):
        deck = Deck()
        self.assertEqual(len(deck), 52)

    def test_shuffle_changes_order(self):
        deck1 = Deck()
        deck2 = Deck()
        deck2.shuffle()
        self.assertNotEqual([str(c) for c in deck1.cards], [str(c) for c in deck2.cards])

    def test_deal_and_burn(self):
        deck = Deck()
        card = deck.deal_one()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck), 51)
        deck.burn_card()
        self.assertEqual(len(deck), 50)

    def test_card_from_string(self):
        card = Card.from_string('Ah')
        self.assertEqual(str(card), 'Ah')
        with self.assertRaises(ValueError):
            Card.from_string('ZZ')

if __name__ == '__main__':
    unittest.main() 