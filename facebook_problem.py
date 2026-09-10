from __future__ import annotations

import unittest
from dataclasses import dataclass
from enum import Enum
from random import Random
from typing import Optional


# ============================================================
# Task 1: Validate a numeric literal
# ============================================================


def is_valid_number(s: str) -> bool:
    """
    Return whether `s`, after trimming leading and trailing whitespace,
    matches this grammar:

        number   := sign? (digits '.' digits? | '.' digits | digits) exponent?
        exponent := ('e' | 'E') sign? digits
        sign     := '+' | '-'
        digits   := one or more ASCII characters from '0' through '9'

    Important:
    - The entire trimmed string must match.
    - Internal whitespace is invalid.
    - Only ASCII digits 0-9 count as digits.
    - Do not use float(), decimal.Decimal, or regular expressions.

    Examples:
        "0"       -> True
        "-3.14"   -> True
        "+.8"     -> True
        "2e10"    -> True
        "-1.2E-3" -> True
        "abc"     -> False
        "."       -> False
        "1e"      -> False

    Target complexity:
        Time:  O(n)
        Space: O(1)
    """
    raise NotImplementedError


# ============================================================
# Task 2: Maximize profit from one trade
# ============================================================


def max_trade_profit(prices: list[int]) -> int:
    """
    Choose at most one buy day and one strictly later sell day.

    Return the maximum possible profit. Return 0 if no profitable trade
    exists.

    Constraints:
    - prices may be empty.
    - Prices are non-negative integers.
    - You must buy before you sell.
    - Implement this in a single pass.

    Examples:
        [7, 1, 5, 3, 6, 4] -> 5  (buy at 1, sell at 6)
        [7, 6, 4, 3, 1]    -> 0
        [2, 4, 1, 8]       -> 7  (buy at 1, sell at 8)

    Target complexity:
        Time:  O(n)
        Space: O(1)
    """
    raise NotImplementedError


# ============================================================
# Task 3: Right side view of a binary tree
# ============================================================


@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def right_side_view(root: Optional[TreeNode]) -> list[int]:
    """
    Return the rightmost visible node value at each tree depth.

    Example:

              1
             / \\
            2   3
             \\   \\
              5   4

        Result: [1, 3, 4]

    You may use either breadth-first search or depth-first search.

    Target complexity:
        Time:  O(n)
        Space: O(w) for BFS, where w is maximum tree width,
               or O(h) for DFS, where h is tree height.
    """
    raise NotImplementedError


# ============================================================
# Task 4: Standard card deck
# ============================================================


class Suit(Enum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"


class Rank(Enum):
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


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank


class Deck:
    """
    A mutable standard 52-card deck.

    Required behavior:
    - A new deck contains every suit/rank combination exactly once.
    - reset() restores all 52 cards in deterministic order.
    - shuffle() randomizes only the currently remaining cards.
    - draw(n) removes and returns exactly n cards.
    - draw(0) returns an empty list.
    - draw(n) raises ValueError when n is negative.
    - draw(n) raises ValueError when fewer than n cards remain.
    - A failed draw must not modify the deck.
    - remaining() returns the number of undrawn cards.
    - No card may be returned twice unless reset() is called.

    Testability:
    - Accept an optional Random instance so tests can use a fixed seed.
    """

    def __init__(self, rng: Optional[Random] = None) -> None:
        raise NotImplementedError

    def reset(self) -> None:
        """Restore all 52 cards in deterministic suit/rank order."""
        raise NotImplementedError

    def shuffle(self) -> None:
        """Shuffle the cards that have not yet been drawn."""
        raise NotImplementedError

    def draw(self, n: int = 1) -> list[Card]:
        """Remove and return n cards according to the rules above."""
        raise NotImplementedError

    def remaining(self) -> int:
        """Return the number of cards still available."""
        raise NotImplementedError


# ============================================================
# Tests
# ============================================================


class NumberValidationTests(unittest.TestCase):
    def test_valid_numbers(self) -> None:
        valid = [
            "0",
            "-3.14",
            "+.8",
            "2e10",
            "-1.2E-3",
            "3.",
            ".1",
            "+6",
            "  42  ",
            "005",
            "46.e3",
        ]

        for value in valid:
            with self.subTest(value=value):
                self.assertTrue(is_valid_number(value))

    def test_invalid_numbers(self) -> None:
        invalid = [
            "",
            "   ",
            "abc",
            "1a",
            "e9",
            ".",
            "+",
            "1e",
            "--6",
            "1 2",
            "6e-",
            "1.2.3",
            "NaN",
            "Infinity",
            "１２",  # Unicode digits, not ASCII digits
        ]

        for value in invalid:
            with self.subTest(value=value):
                self.assertFalse(is_valid_number(value))


class TradeProfitTests(unittest.TestCase):
    def test_typical_profit(self) -> None:
        self.assertEqual(max_trade_profit([7, 1, 5, 3, 6, 4]), 5)

    def test_declining_prices(self) -> None:
        self.assertEqual(max_trade_profit([7, 6, 4, 3, 1]), 0)

    def test_empty_prices(self) -> None:
        self.assertEqual(max_trade_profit([]), 0)

    def test_single_price(self) -> None:
        self.assertEqual(max_trade_profit([10]), 0)

    def test_later_minimum(self) -> None:
        self.assertEqual(max_trade_profit([2, 4, 1, 8]), 7)

    def test_equal_prices(self) -> None:
        self.assertEqual(max_trade_profit([5, 5, 5]), 0)


class RightSideViewTests(unittest.TestCase):
    def test_empty_tree(self) -> None:
        self.assertEqual(right_side_view(None), [])

    def test_single_node(self) -> None:
        self.assertEqual(right_side_view(TreeNode(1)), [1])

    def test_balanced_example(self) -> None:
        root = TreeNode(
            1,
            left=TreeNode(2, right=TreeNode(5)),
            right=TreeNode(3, right=TreeNode(4)),
        )
        self.assertEqual(right_side_view(root), [1, 3, 4])

    def test_left_node_visible_when_right_is_missing(self) -> None:
        root = TreeNode(
            1,
            left=TreeNode(
                2,
                right=TreeNode(5),
            ),
            right=TreeNode(3),
        )
        self.assertEqual(right_side_view(root), [1, 3, 5])

    def test_left_only_tree(self) -> None:
        root = TreeNode(1, left=TreeNode(2, left=TreeNode(3)))
        self.assertEqual(right_side_view(root), [1, 2, 3])


class DeckTests(unittest.TestCase):
    def test_new_deck_has_52_unique_cards(self) -> None:
        deck = Deck()
        cards = deck.draw(52)

        self.assertEqual(len(cards), 52)
        self.assertEqual(len(set(cards)), 52)
        self.assertEqual(deck.remaining(), 0)

    def test_draw_reduces_remaining_count(self) -> None:
        deck = Deck()

        drawn = deck.draw(5)

        self.assertEqual(len(drawn), 5)
        self.assertEqual(deck.remaining(), 47)

    def test_separate_draws_never_duplicate_cards(self) -> None:
        deck = Deck()

        first = deck.draw(20)
        second = deck.draw(20)

        self.assertTrue(set(first).isdisjoint(second))

    def test_draw_zero(self) -> None:
        deck = Deck()

        self.assertEqual(deck.draw(0), [])
        self.assertEqual(deck.remaining(), 52)

    def test_negative_draw_is_rejected(self) -> None:
        deck = Deck()

        with self.assertRaises(ValueError):
            deck.draw(-1)

        self.assertEqual(deck.remaining(), 52)

    def test_drawing_too_many_is_atomic(self) -> None:
        deck = Deck()
        deck.draw(50)

        with self.assertRaises(ValueError):
            deck.draw(3)

        self.assertEqual(deck.remaining(), 2)

    def test_reset_restores_the_deck(self) -> None:
        deck = Deck()
        deck.draw(15)

        deck.reset()

        self.assertEqual(deck.remaining(), 52)
        self.assertEqual(len(set(deck.draw(52))), 52)

    def test_seeded_shuffle_is_reproducible(self) -> None:
        first = Deck(Random(1234))
        second = Deck(Random(1234))

        first.shuffle()
        second.shuffle()

        self.assertEqual(first.draw(52), second.draw(52))

    def test_shuffle_only_affects_remaining_cards(self) -> None:
        deck = Deck(Random(42))
        already_drawn = set(deck.draw(10))

        deck.shuffle()
        remaining_cards = deck.draw(42)

        self.assertEqual(len(set(remaining_cards)), 42)
        self.assertTrue(already_drawn.isdisjoint(remaining_cards))


if __name__ == "__main__":
    unittest.main()
