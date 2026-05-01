#My notes/python code for this class was highly disorganized and so I made one file with all the information

# Sessions 1-5

import random


# session 1

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"p<{self.x}, {self.y}>"

    def __repr__(self):
        return self.__str__()

    def distance_origin(self):
        return (self.x**2 + self.y**2) ** 0.5

    def __lt__(self, other):
        if isinstance(other, int):
            return self.x < other
        return self.distance_origin() < other.distance_origin()

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return self.x == other

    def __mul__(self, other):
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        raise TypeError("Can only multiply by integers")


# session 2

class ColorPoint(Point):
    def __init__(self, x, y, color):
        if not isinstance(x, (int, float)):
            raise TypeError
        if not isinstance(y, (int, float)):
            raise TypeError

        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        return f"{self.color}: cp<{self.x},{self.y}>"


# session 3

class AdvancedPoint(ColorPoint):
    COLORS = ["red", "green", "blue", "black", "white", "yellow"]

    def __init__(self, x, y, color):
        if not isinstance(x, (int, float)):
            raise TypeError("x must be int or float")
        if not isinstance(y, (int, float)):
            raise TypeError("y must be int or float")
        if color not in self.COLORS:
            raise TypeError(f"Color must be one of {self.COLORS}")

        self._x = x
        self._y = y
        self._color = color

    def __str__(self):
        return f"p<{self.x}, {self.y}, {self.color}>"

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("x must be int or float")
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("y must be int or float")
        self._y = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value not in self.COLORS:
            raise TypeError(f"Color must be one of {self.COLORS}")
        self._color = value

    @classmethod
    def add_color(cls, color):
        cls.COLORS.append(color)

    @staticmethod
    def distance_2_points(p1, p2):
        return p1.distance_origin() + p2.distance_origin()

    @staticmethod
    def from_string(text):
        color, x, y = text.split()
        if color not in AdvancedPoint.COLORS:
            raise TypeError(f"Color must be one of {AdvancedPoint.COLORS}")
        return AdvancedPoint(float(x), float(y), color)


# session 4

class PlayingCard:
    SUITS = ["♦", "♣", "♥", "♠"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, suit, rank):
        if suit not in self.SUITS:
            raise ValueError(f"suit must be in {self.SUITS}")
        if rank not in self.RANKS:
            raise ValueError(f"rank must be in {self.RANKS}")

        self._suit = suit
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return self.__str__()


class Deck:
    def __init__(self):
        self._cards = []
        for suit in PlayingCard.SUITS:
            for rank in PlayingCard.RANKS:
                self._cards.append(PlayingCard(suit, rank))

    @property
    def cards(self):
        return tuple(self._cards)

    def __str__(self):
        return str(self.cards)

    def shuffle(self):
        random.shuffle(self._cards)

    def deal(self):
        return self._cards.pop()


# session 5

class PokerHand:
    def __init__(self):
        deck = Deck()
        deck.shuffle()
        self._cards = []

        for _ in range(5):
            self._cards.append(deck.deal())

    @property
    def cards(self):
        return tuple(self._cards)

    @property
    def num_matches(self):
        count = 0
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                if self._cards[i].rank == self._cards[j].rank:
                    count += 1
        return count

    @property
    def is_pair(self):
        return self.num_matches == 2

    @property
    def is_2_pair(self):
        return self.num_matches == 4

    @property
    def is_trips(self):
        return self.num_matches == 6

    @property
    def is_full_house(self):
        return self.num_matches == 8

    @property
    def is_4_kind(self):
        return self.num_matches == 12

    @property
    def is_straight(self):
        if self.num_matches != 0:
            return False

        cards = list(self._cards)
        cards.sort(key=lambda card: PlayingCard.RANKS.index(card.rank))

        first_card_index = PlayingCard.RANKS.index(cards[0].rank)
        last_card_index = PlayingCard.RANKS.index(cards[-1].rank)

        if first_card_index + 4 == last_card_index:
            return True

        if cards[-1].rank == "A" and cards[-2].rank == "5":
            return True

        return False

    @property
    def is_flush(self):
        for card in self._cards[1:]:
            if self._cards[0].suit != card.suit:
                return False

        if self.is_straight:
            return False

        return True

    @property
    def is_straight_flush(self):
        return self.is_flush and self.is_straight

    @property
    def is_normal_flush(self):
        return self.is_flush and not self.is_straight

    def __str__(self):
        return str(self.cards)


# quick checks

p1 = Point(1, 2)
p2 = Point(3, 4)
print(p1)
print(p2.distance_origin())

cp = ColorPoint(1, 2, "red")
print(cp)

ap = AdvancedPoint(1, 2, "blue")
print(ap)

deck = Deck()
deck.shuffle()
print(deck.deal())

hand = PokerHand()
print(hand)
print(hand.is_pair, hand.is_flush, hand.is_straight)
