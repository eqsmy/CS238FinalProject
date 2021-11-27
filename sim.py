import sys
from deck_of_cards import deck_of_cards
from queue import Queue
from queue import LifoQueue
# import set
from collections import OrderedDict
import random as rand

# Play around with random and slightly better than random polices (greedy) which uses heuristics
# slightly better is if a card on discard pile will make a meld, then take it. 
# knock right away if you can....
# prioritize laying down the lowest card versus a random card. 
# improve this by basing it on the status of the game. 
# 3. local search with hooke jeeves in like 5 lines 
# 4.cross entropy method
# 5.look ahead with rollouts
# 6.monte carlo tree search

def play_gin():
    # scoreboard = [0,0,0]
    points = [0,0]
    # gins = [0,0]
    #one wins, two wins, no one wins
    for _ in range(1000):
        player_one_hand, player_two_hand, deck, discard_pile, max_deadwood = deal()
        greedy_vs_random(player_one_hand, player_two_hand, deck, discard_pile, max_deadwood, points)
    # print(scoreboard)
    # print(gins)
    print('greedy: ', points[0], ' points')
    print('random: ', points[1], ' points')

    # remaining_hand = find_melds(dummy_hand)

def deal():
    suits = {0:'spades', 1:'hearts', 2:'diamonds', 3:'clubs'}
    deck_obj = deck_of_cards.DeckOfCards()
    
    for _ in range(6): deck_obj.shuffle_deck()

    deck = Queue(maxsize = 52)
    for _ in range(52):
        card = deck_obj.give_random_card() 
        deck.put({'suit': card.suit, 'rank': card.rank}) #make sure face cards are 10, 11, 12
    
    player_one_hand = []
    player_two_hand = []
    for _ in range(10): player_one_hand.append(deck.get())
    for _ in range(10): player_two_hand.append(deck.get())

    #sort the hands
    
    # print(player_one_hand)
    discard_pile = LifoQueue(maxsize=30) #discard_pile.qsize(), stack.put() and stack.get

    first_card = deck.get()
    discard_pile.put(first_card) #first card
    max_deadwood = min(first_card['rank'], 10)
    
    dummy_hand = [{'suit': 1, 'rank': 10}, 
    {'suit': 3, 'rank': 10}, 
    {'suit': 0, 'rank': 10}, 
    {'suit': 1, 'rank': 10}, 
    {'suit': 1, 'rank': 9}, 
    {'suit': 1, 'rank': 8}, 
    {'suit': 0, 'rank': 12}, 
    {'suit': 0, 'rank': 13}, 
    {'suit': 1, 'rank': 13}, 
    {'suit': 1, 'rank': 4}]

    return player_one_hand, player_two_hand, deck, discard_pile, max_deadwood

    

def greedy_vs_random(player_one_hand, player_two_hand, deck, discard_pile, max_deadwood, points):
    #player one is random
    #player two is greedy
    rand.seed(a=None,version=2)
    while (deck.qsize() > 3):
        # print('iter')
        #random goes first
        #draw card from either discard or deck
        #lay card down 
        #call mind melds
        #return gin if remaining hand is empty
        #knock if deadwood less than max_deadwood
        #repeat. 
        
        #player one draws first
        player_one_hand.append(deck.get()) if rand.randint(0,1) == 0 else player_one_hand.append(discard_pile.get())        
        index_to_discard = rand.randint(0, len(player_one_hand) - 1)
        discard_pile.put(player_one_hand[index_to_discard])
        del player_one_hand[index_to_discard]
        player_one_hand = find_melds(player_one_hand)

        #check player one gin check
        if (len(player_one_hand)) == 0:
            # print("Player One Gins and WINS the game!")
            points[0] += (25 + calculate_deadwood(player_two_hand))
            return

        #check player one knock
        knocking_outcome = check_knock_player_one(player_one_hand, player_two_hand, max_deadwood)
        if (knocking_outcome[0] == 1 or knocking_outcome[0] == 2): 
            # scoreboard[knocking_outcome[0] - 1] += 1
            points[knocking_outcome[0] - 1] += abs(calculate_deadwood(player_one_hand) - calculate_deadwood(player_two_hand))
            return 

        #player two draws second
        #player two (greedy) always draws from the deck, for now
        player_two_hand.append(deck.get()) 
        index_to_discard = rand.randint(0, len(player_two_hand) - 1)
        discard_pile.put(player_two_hand[index_to_discard])
        del player_two_hand[index_to_discard]

        player_two_hand = find_melds(player_two_hand)

        #check player two gin
        if (len(player_two_hand)) == 0:
            # scoreboard[1] += 1
            # gins[1] += 1
            points[1] += (25 + calculate_deadwood(player_one_hand))
            # print("Player two Gins and WINS the game!")
            return

        #check player one knock
        knocking_outcome = check_knock_player_two(player_one_hand, player_two_hand, max_deadwood)
        if (knocking_outcome[0] == 1 or knocking_outcome[0] == 2): 
            # scoreboard[knocking_outcome[0] - 1] += 1
            points[knocking_outcome[0] - 1] += abs(calculate_deadwood(player_one_hand) - calculate_deadwood(player_two_hand))
            return 
    
    # print('no one wins :(')
    # scoreboard[2] += 1
 

#e.g. [{'suit': 'hearts', 'rank': 10}, {'suit': 'hearts', 'rank': 1}, {'suit': 'spades', 'rank': 2}, 
def find_melds(hand):
    #there are possible melds: (4, 4), (3, 3, 4), (3, 3), (3), (4), (4, 3), ()
    #further, for each of these (except empty) there are could be multiple options. 
    #check out https://stackoverflow.com/questions/62707039/gin-rummy-algorithm-for-determining-optimal-melding
    
    melds = []
    # melds = set()
    # print(type(melds))
    if len(hand) < 3: return melds 

    hand_copy = hand
    #find a four meld 
    three_meld = find_three_meld(hand_copy)
    if (len(three_meld) > 2): hand_copy = remove(three_meld, hand_copy)
    #find up to two three melds 
    
    four_meld = find_four_meld(hand_copy)
    if (len(four_meld) > 3): hand_copy = remove(four_meld, hand_copy)

    four_meld2 = find_four_meld(hand_copy)
    if (len(four_meld2) > 3): hand_copy = remove(four_meld2, hand_copy)

    return hand_copy
    #four melds 

    
    # melds = unique(melds)
    print("melds = ", melds)
    return melds

def find_three_meld(hand):
    #all three melds 
    for i in range(len(hand)):
        for j in range(i + 1, len(hand)):
            for k in range(j + 1, len(hand)):
                meld = [hand[i], hand[j], hand[k]]
                if is_meld(meld): 
                    return meld
    return []


def find_four_meld(hand):
    for i in range(len(hand)):
        for j in range(i + 1, len(hand)):
            for k in range(j + 1, len(hand)):
                for l in range(k + 1, len(hand)):
                    meld = [hand[i], hand[j], hand[k], hand[l]]
                    if is_meld(meld): 
                        return meld
    return []

def is_meld(cards):
    if len(cards) < 3 or len(cards) > 4: return False
    return is_run(cards) or is_set(cards)

def is_set(cards):
    rank = cards[0]['rank']
    for card in cards:
        if card['rank'] != rank: return False
    return True

def is_run(cards):
    cards = sorted(cards, key=lambda card: card['rank'])
    prev_rank = cards[0]['rank']
    suit = cards[0]['suit']
    for i in range(1, len(cards)):
        # print('cards[i][\'suit\'] = ', cards[i]['suit'], 'suit = ', suit)
        if cards[i]['suit'] != suit or cards[i]['rank'] - 1 != prev_rank: return False
        prev_rank = cards[i]['rank']
    return True

def remove(meld, hand):
    for item in meld:
        hand.remove(item)
    return hand

def calculate_deadwood(hand):
    hand = find_melds(hand) #for redundancy
    deadwood = 0
    for card in hand: deadwood += card['rank']
    return deadwood

#player one is random and player 2 is greedy
#only player one is alowed to knock here 
def check_knock_player_one(hand1, hand2, max_deadwood):
    one_deadwood = calculate_deadwood(hand1)
    two_deadwood = calculate_deadwood(hand2)
    if (one_deadwood <= max_deadwood) and rand.randint(0,1) == 1: 
        if (one_deadwood < two_deadwood): 
            # print ('player one knocks with deadwood of ', one_deadwood, ' and BEATs player two with deadwood of ', two_deadwood)
            return (1, one_deadwood - two_deadwood)
        else: 
            # print ('player one knocks with deadwood of ', one_deadwood, ' and LOSES to player two with deadwood of ', two_deadwood)
            return (2, two_deadwood - one_deadwood)
    #if both players don't knock, no one wins and we keep going
    return (0,0)

#only player two is allowed to knock here
def check_knock_player_two(hand1, hand2, max_deadwood):
    # print(max_deadwood)
    one_deadwood = calculate_deadwood(hand1)
    two_deadwood = calculate_deadwood(hand2)
    #player two (greedy) will always knock if able 
    if (two_deadwood <= max_deadwood):
        if(two_deadwood < one_deadwood):
            # print ('player two knocks with deadwood of ', two_deadwood, ' and BEATs player one with deadwood of ', one_deadwood)
            return (2, two_deadwood - one_deadwood)
        else: 
            # print ('player two knocks with deadwood of ', two_deadwood, ' and LOSES to player one with deadwood of ', one_deadwood)
            return (1, one_deadwood - two_deadwood)
    return (0,0)
    
def unique(melds):
    list(OrderedDict.fromkeys(melds))


def main():
    play_gin()

if __name__ == '__main__':
    main()


