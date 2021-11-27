# CS238FinalProject

## Progress

### Remaining Things for Hooke Jeeves Implementation

[x] Rollout
[] Step Function (converts state and action into state prime) -> pretty much complete
[] Reward Function (calculates reward for state) -> will need this to complete the step function
[] Pi function (turns parameter and state into actions) -> right now implemented as random action, will need to determine our parameters and figure out calculation
[x] Make it so it actually plays a player 2 -> right now implemented as random

## State Space

0. Stock pile
1. Player 1 card
2. Player 2 card
3. Top discard
4. Non-top discard

## Example Action Space

(21 possible actions -- from sample on AA228 website)

1. Draw from deck, discard card 1 from hand
2. Draw from deck, discard card 2 from hand
   .
   .
   .
3. Draw from deck, discard card 10 from hand
4. Draw from deck, discard drawn card
5. Pick up top discard card, discard card 1 from hand
6. Pick up top discard card, discard card 2 from hand
   .
   .
   .
7. Pick up top discard card, discard card 10 from hand

## Potential Parameters

(Parameters are denoted by uppercase letters)

1. when to knock
   - irrelevant if we can't knock
   - if we can knock
     - wait until deadwood value is below A
     - knock B percent of the time if we have a partial meld
2. which cards to lay down
   - order deadwood in decreasing value
   - look at first card:
     - if there is another card with the same suit or number, keep the card C percent of the time
     - if there is not another card with the same suit or number
       - if value is 8 or lower, keep according to parameter specified below
       - if value is 8 or higher, keep according to parameter specified below
3. whether to keep higher or lower cards in your hand based on the status of the game
   - if stock pile has more than 15 cards left
     - keep cards with value greater than 8 D% of the time
     - keep cards with value less than 8 E% of the time
   - if stock pile has 15 or fewer cards left
     - keep cards with value greater than 8 F% of the time
     - keep cards with value less than 8 G% of the time
4. whether to take a card from the discard pile or the stock pile
   - if discard pile has card with the same number or suit within 4 numbers
     - take from discard pile H percent of the time
   * else
     - always take from stock pile (?)
