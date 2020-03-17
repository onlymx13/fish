import random

"""
0: 2 of Clubs
6: 9 of Clubs
12: 2 of Hearts
18: 9 of Hearts
24: 2 of Spades
30: 9 of Spades
36: 2 of Diamonds
42: 9 of Diamonds
48-51: 8s of Clubs, Hearts, Spades, Diamonds
52-53: Black and Red Jokers
"""

currTurn = random.randrange(0,6)
playerCount = 6
playerHands = [[0 for j in range (0,9)] for i in range (0,6)] # initialize hands to empty
goodPoints = 0
badPoints = 0
playerNames = ["" for i in range (0, 6)]

def nameCard(card):
    cardNames = ["2", "3", "4", "5", "6", "7", "9", "10", "Jack", "Queen", "King", "Ace"];
    suitNames = ["Clubs", "Hearts", "Spades", "Diamonds"]
    if card >= 52:
        return ["Black", "Red"][card - 52] + " Joker"
    elif card >= 48:
        return "8 of " + suitNames[card - 48]
    else:
        return cardNames[card % 12] + " of " + suitNames[card // 12]

def printPlayerHand():
    playerHands[0].sort()
    print("Your hand:\n")
    cardNum = 0
    for card in playerHands[0]:
        print(str(cardNum + 1) + ". " + nameCard(card))
        cardNum += 1

def takeTurn():
    global currTurn
    if currTurn == 0:
        humanTakeTurn()
    elif currTurn < 3:
        allyTakeTurn()
    else:
        enemyTakeTurn()

def listCardsInHalfSuitOf(card, player):
    cardNum = 0
    cards = []
    for otherCard in range(card // 6 * 6, card // 6 * 6 + 6):
        if not otherCard in playerHands[player]: # If the player chose the 2 of Clubs and has the 3 of Clubs, don't list it
            cards.append(otherCard)
            if currTurn == 0: # On the player's turn, print them
                print(str(cardNum + 1) + ". " + nameCard(otherCard))
            cardNum += 1
    return cards

def askForCardInHalfSuitOf(card):
    print("Cards in half-suit:\n")
    cards = listCardsInHalfSuitOf(card, 0) # Assume the player is the human, since why else would you print it?
    if len(cards) == 0:
        print("You have all the cards in that half-suit! You can't ask for any cards in that half-suit!\n")
        return -1
    while True:
        try:
            cardAskedFor = cards[int(input("Ask about which card? ")) - 1] # -1 because prompt is 1-indexed
        except Exception as err:
            print("Bad input: " + str(err))
        else:
            break
    print("You will ask for the " + nameCard(cardAskedFor) + ".")
    return cardAskedFor

def humanTakeTurn():
    global currTurn
    print("It's your turn!")
    if len(playerHands[0]) == 0: # Need testing
        currTurn = int(input("Your hand is empty.\n1. " + playerNames[1] + "\n2. " + playerNames[2] + "\nGive your turn to which teammate?"))
        return
    printPlayerHand()
    while True:
        try:
            cardChosen = int(input("\nAsk about which card's half-suit? ")) - 1 # because the prompt was 1-indexed
            cardAskedFor = askForCardInHalfSuitOf(playerHands[0][cardChosen])
        except Exception as err:
            print("Problem occurred: " + str(err))
        else:
            break
    if cardAskedFor == -1:
        humanTakeTurn()
        return
    else:
        while True:
            try:
               playerAsked = int(input("\n1. " + playerNames[3] + " (hand size " + str(len(playerHands[3])) + ")\n2. " + playerNames[4] + " (hand size " + str(len(playerHands[4])) + ")\n3. " + playerNames[5] + " (hand size " + str(len(playerHands[5])) + ")\n\nAsk which player? ")) + 2 # if you put 1, the number is 3
            except Exception as err:
                print("Problem occurred: " + str(err))
            else:
                break
        playerAskPlayerFor(0, playerAsked, cardAskedFor)
        

def enemyTakeTurn(): #TODO: Enemy AI. Currently, a very basic random choice.
    global currTurn
    if len(playerHands[currTurn]) == 0: # Needs testing
        print(playerNames[currTurn] + "'s hand is empty.")
        while len(playerHands[currTurn]) == 0: # Don't give your turn to someone else with an empty hand
            currTurn = random.randrange(3, 6) # random bad guy
        print("Turn given to " + playerNames[currTurn] + ".")
        return
    cardAskedFor = random.choice(listCardsInHalfSuitOf(random.choice(playerHands[currTurn]), currTurn)) # Pick a random card in this player's hand and find a card in its half-suit that that player doesn't have.
    while True:
        playerAsked = random.randrange(0, 3) # random good guy
        if len(playerHands[playerAsked]): # Don't ask someone whose hand is empty
            break
    playerAskPlayerFor(currTurn, playerAsked, cardAskedFor) 

def allyTakeTurn(): #TODO: Ally AI. Currently, a very basic random choice.
    global currTurn
    print("Length of " + str(len(playerHands[currTurn])))
    if len(playerHands[currTurn]) == 0: # Needs testing
        print(playerNames[currTurn] + "'s hand is empty.")
        while len(playerHands[currTurn]) == 0: # Don't give your turn to someone else with an empty hand
            currTurn = random.randrange(0, 3) # random good guy
        print("Turn given to " + playerNames[currTurn] + ".")
        return
    cardAskedFor = random.choice(listCardsInHalfSuitOf(random.choice(playerHands[currTurn]), currTurn)) # Pick a random card in this player's hand and find a card in its half-suit that that player doesn't have.
    while True:
        playerAsked = random.randrange(3, 6) # random bad guy
        if len(playerHands[playerAsked]): # Don't ask someone whose hand is empty
            break
    playerAskPlayerFor(currTurn, playerAsked, cardAskedFor) 

def printPoints():
    global goodPoints
    global badPoints
    print("You: " + str(goodPoints) + " | Them: " + str(badPoints) + "\n")

def playerAskPlayerFor(asking, giving, card):
    global currTurn
    print(playerNames[asking] + " asked " + playerNames[giving] + " for the " + nameCard(card) + ".")
    if card in playerHands[giving]:
        print(playerNames[giving] + " had it.")
        playerHands[giving].remove(card)
        playerHands[asking].append(card)
    else:
        print(playerNames[giving] + " did not have it.")
        currTurn = giving

def promptClaim(): # Currently, this is only for the human. Parts of this should be reused for enemies and allies.
    global goodPoints
    global badPoints

    if input("\nDo you want to make a claim (y/N)? ").upper() == "Y":
        halfSuitTuple = halfSuitsLeft[int(input("Half-suits:\n\n" + '\n'.join(list(str(n + 1) + ". " + halfSuitsLeft[n][0] for n in range(len(halfSuitsLeft)))) + "\nMake a claim about which half-suit? ")) - 1]
        halfSuit = halfSuitTuple[1]
        claimGood = True # claims default to good
        print("1. You (hand size " + str(len(playerHands[0])) + ")\n2. " + playerNames[1] + " (hand size " + str(len(playerHands[1])) + ")\n3. " + playerNames[2] + " (hand size " + str(len(playerHands[2])) + ")")
        oof = ""
        for card in range(6 * halfSuit, 6 * halfSuit + 6): # for all cards in that half-suit
            player = int(input("Who has the " + nameCard(card) + "? ")) - 1
            if not card in playerHands[player]: # If at any point part of the claim is wrong, label it wrong, but don't stop it
                claimGood = False
            for player in range(6):
                if card in playerHands[player]:
                    playerHands[player].remove(card) # Eventually the cards will be placed aside regardless of whether the claim is good. May as well do that now.
                    oof += playerNames[player] + " had the " + nameCard(card) + ".\n"
        if claimGood:
            print("\nThe claim was good! Your team gets 1 point.")
            goodPoints += 1
        else:
            print("\nThe claim was bad. The other team gets 1 point.\n" + oof)
            badPoints += 1
        halfSuitsLeft.remove(halfSuitTuple)

def promptPlayerNames():
    playerNames[0] = "You" # input("What is your name? ")
    for i in range(1,3):
        playerNames[i] = input("What will you name ally " + str(i) + "? ") + " (A)"
    for i in range(3,6):
        playerNames[i] = input("What will you name enemy " + str(i - 2) + "? ") + " (E)"

deck = list(range(0, 54))
random.shuffle(deck)
cardNumber = 0
for card in deck: # place shuffled cards in hands
    playerHands[cardNumber // 9][cardNumber % 9] = card
    cardNumber += 1

halfSuitsLeft = [("Low Clubs", 0), ("High Clubs", 1), ("Low Hearts", 2), ("High Hearts", 3), ("Low Spades", 4), ("High Spades", 5), ("Low Diamonds", 6), ("High Diamonds", 7), ("8s and Jokers", 8)]
promptPlayerNames()
printPlayerHand()
while True:
    printPoints()
    takeTurn()
    printPlayerHand()
    promptClaim()
    if len(halfSuitsLeft) == 0:
        print("The game is over!")
        if goodPoints > badPoints:
            print("The good guys won!")
        else:
            print("The bad guys won!")

