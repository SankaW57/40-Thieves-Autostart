'''
*********************REMINDER*********************
The cards are labelled from 1 to 13 for the value and a letter for the suit.
    D = Diamonds, C = Clovers, H = Hearts, S = Spades
    1 = Ace, 2 - 10 = values 2 - 10, 11 = Jack, 12 = Queen, 13 = King
    Jokers are not included
'''

# Required modules
import random, time, csv, re
import matplotlib.pyplot as plt


flag = True
count2 = 0
start = time.time() # start timer to check how long program runs
playingStack = 10   # number of stacks with 4 cards each
playingSize = 4   # size of the playing stack
deckNum = 2  # number of decks inserted
finalPiles = 8  # number of piles
suitsOfFinal = int(finalPiles/4)  # piles per suit(8 piles/4 suits)

# Lists/Dictionaries
initialDeck = []  # cards taken from csv
deck = []  # all cards for both decks
countingList = []  # list to hold number of loop iterations
tempList = []   # list to hold temporary deck
stackDict = {}  # dictionary that has every stack
pileDict = {}  # dictionary that has every pile


def openDeckCsv(filename, deck):   # Import csv file and adds each line in as an element
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            deck.append(line[0])
        file.close()

def autoStartFunc(sDict, stackNum, numSuitP, pDict, pCount):

    c = 0   # counter for iterations
    while c < stackNum:     # check top of playing stack till the last playing stack is checked
        topOfStack = []     # local list for top stack
        for i in (sDict.keys()):
            try:
                topOfStack.append(sDict[i][-1])     # check
            except IndexError:
                topOfStack.append('0D')

        current = topOfStack[c]  # set top of card to current card
        cardNum = int(re.search(r'\d+', current).group())

        # if (cardNum is int):    # check for type
        #     return True

        setSuit = current[len(current) - 1:len(current)]  # set suit of card
        lastCard = str(cardNum - 1) + setSuit  # set last card
        stack = sDict.get('stack' + str(c + 1))  # set stack to stack of card on top

        for i in range(numSuitP):
            pile = pDict.get('pile' + setSuit + str(i + 1))
            pLength = len(pile)
            pTop = pile[-1:]
            p = [lastCard]

            # if the pile is empty AND current card is 1, place card into the pile
            if pLength == 0 and cardNum == 1:
                pile.append(current)
                stack.remove(stack[-1])
                pCount += 1
                c = 0
                break

            # if the top card on stack is equal to previous, place card into the stack
            elif pTop == p:
                pile.append(current)
                stack.remove(stack[-1])
                pCount += 1
                c = 0
                break

            # otherwise all cards in the piles have been gone through
            elif (i + 1) == numSuitP:
                c += 1
                break

    return pCount   # total cards moved during autostart


# ====================================================================================
openDeckCsv('sollitaire.csv', initialDeck)   # imports deck from csv into deckinput
print(initialDeck)

for x in range(deckNum):    # place the initial deck as seperate elements, shuffle the deck
    deck.extend(initialDeck)
    random.shuffle(deck)    # deck contains second deck into first and randomly shuffled

# make stack
for i in range(1, playingStack + 1):    # for i in range (1, 11)
    stackDict['stack' + str(i)] = []
    s = stackDict.get('stack' + str(i))
    for x in range(playingSize):    # for x in range (4)
        s.append(deck[0])   # add first value in deck into tempDeck
        deck.remove(deck[0])    # remove value that was added from deck
        # print('This is s:' + str(s))
        # print('This is deck' + str(deck))

for i in range(suitsOfFinal):            # for i in range(2), creates the 8 piles
    pileDict['pileS' + str(i + 1)] = []  # create 4 piles per iteration for final piles
    pileDict['pileH' + str(i + 1)] = []
    pileDict['pileD' + str(i + 1)] = []
    pileDict['pileC' + str(i + 1)] = []

# ==================================== AUTOSTART FUNCTION EXAMPLE==============================================
# count = 0
# autoStartFunc(stackDict, playingStack, suitsOfFinal, pileDict, count)
# print('\n')
# print(stackDict)
# print('\n')
# print(pileDict)
# print('\n')

# ================================= AUTOSTART FUNCTION FOR MIN OF 15 MOVES ====================================
while flag == True:
    # Makes deck an empty array every iteration
    deck = []
    for x in range(deckNum):
        deck.extend(initialDeck)
        random.shuffle(deck)

    for i in range(1,playingStack+1):
        stackDict['stack'+str(i)] = []
        s = stackDict.get('stack'+str(i))
        for x in range(playingSize):
            s.append(deck[0])
            deck.remove(deck[0])

    for i in range(suitsOfFinal):
        pileDict['pileS'+str(i+1)] = []
        pileDict['pileH'+str(i+1)] = []
        pileDict['pileD'+str(i+1)] = []
        pileDict['pileC'+str(i+1)] = []

    pileCount = autoStartFunc(stackDict, playingStack, suitsOfFinal, pileDict, count2)

    countingList.append(pileCount)
    print(pileCount)

    if pileCount >= 15:
        flag = False


x = countingList
y = 20
n, bins, patches = plt.hist(x, y, density=0, facecolor='red', alpha=0.5)
plt.subplots_adjust(left=0.15)
finish = time.time()-start  # time program finishes computation

print(finish)
print(len(countingList))

plt.title("Forty Thieves AutoStart")
plt.xlabel("Number of cards moved")
plt.ylabel("Frequency of moves")
plt.show()