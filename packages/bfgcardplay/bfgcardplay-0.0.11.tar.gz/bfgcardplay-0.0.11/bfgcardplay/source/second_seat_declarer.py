"""Second seat card play for declarer."""

import logging
log = logging.getLogger(__name__)

from typing import List, Dict, Tuple
from termcolor import colored

from bridgeobjects import SUITS, Card, RANKS
from bfgsupport import Board, Trick
from .player import Player
from .second_seat import SecondSeat
import bfgcardplay.source.global_variables as global_vars

manager = global_vars.manager

class SecondSeatDeclarer(SecondSeat):
    def __init__(self, player: Player):
        super().__init__(player)

    def selected_card(self) -> Card:
        """Return the card if the second seat."""
        player = self.player
        trick = player.board.tricks[-1]
        cards = player.cards_for_trick_suit(trick)
        if player.trump_suit:
            losers = self._get_declarers_losers(player)
        else:
            pass

        # When to duck - rule of 7
        opponents_unplayed_cards = player.opponents_unplayed_cards[trick.suit.name]
        if cards and opponents_unplayed_cards:
            can_win_trick = (cards[0].value > opponents_unplayed_cards[0].value and
                             cards[0].value > trick.cards[0].value)
            if self._rule_of_seven(player, trick) and can_win_trick:
                return cards[0]

        # Cover honour with honour
        # TODO see this web site http://www.rpbridge.net/4l00.htm

        suit_cards = player.suit_cards[trick.suit.name]
        if (len(suit_cards) > 1 and
                suit_cards[0].value == suit_cards[1].value + 1 and
                suit_cards[1].value >= 9):
            return suit_cards[1]

        if trick.cards[0].value >= 8: # nine or above
            if len(cards) >= 2:
                if cards[1].value >=9:
                    for card in cards[::-1]:
                        if card.value > trick.cards[0].value:
                            return card

        # Play lowest card
        if cards:
            return cards[-1]

        return self._select_card_if_void(player)

    @staticmethod
    def _rule_of_seven(player: Player, trick: Trick) -> bool:
        """Return True if rule of seven applies."""
        declarer_cards = player.board.hands[player.declarer].cards_by_suit[trick.suit.name]
        dummy_cards = player.board.hands[player.dummy].cards_by_suit[trick.suit.name]
        our_cards = declarer_cards + dummy_cards
        duck_count = 7 - len(our_cards) - len(player.board.tricks)
        return duck_count < 0

    @staticmethod
    def _get_declarers_losers(player: Player) -> Dict[str, Card]:
        """Return a dict of cards by suit that threaten declarers cards."""
        declarers_trumps = player.unplayed_cards_by_suit(player.trump_suit, player.declarer)
        dummys_trumps = player.unplayed_cards_by_suit(player.trump_suit, player.dummy)

        if len(declarers_trumps) > len(dummys_trumps):
            short_hand = player.board.hands[player.dummy]
            long_hand = player.board.hands[player.declarer]
        else:
            short_hand = player.board.hands[player.declarer]
            long_hand = player.board.hands[player.dummy]

        losers = {suit: [] for suit in SUITS}
        ranks = [rank for rank in RANKS]
        ranks.reverse()
        sorted_ranks = ranks[:-1]

        for suit in SUITS:
            long_cards = long_hand.cards_by_suit[suit]
            short_cards = short_hand.cards_by_suit[suit]
            cards = long_cards + short_cards
            missing = 13 - len(cards)
            winners = 0
            skip_card = False
            for index, rank in enumerate(sorted_ranks):
                ranking_card = Card(rank, suit)
                if ranking_card in cards:
                    if not skip_card:
                        winners += 1
                    skip_card = False

                    # No more cards to lose
                    if winners > missing:
                        break
                else:
                    losers[suit].append(ranking_card)
                    # skip card means that the next card in the suit is assumed to have been beaten
                    skip_card = True

                #losers only in long hand
                if index + 1 >= len(long_cards):
                    break
        return losers
