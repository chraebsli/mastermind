import random
import sys


class Game:
    class Colourvalues:
        red = "\033[31m"
        magenta = "\033[35m"
        green = "\033[32m"
        yellow = "\033[33m"
        white = "\033[97m"
        black = "\033[30m"
        normal = '\033[0m'

    def __init__(self, maxPasses, numberOfColours):
        'Start new game\nmaxpasses: int\nnumberOfColours: int'
        self.maxPasses = maxPasses
        self.numOfColours = numberOfColours
        self.colours = [['red', 'r', '1'], ['magenta', 'm', '2'], ['green', 'g', '3'], [
            'yellow', 'y', '4'], ['white', 'w', '5'], ['black', 'b', '6']]
        self.computerGuess = Game.getRandom(self)
        self.black = 0
        self.white = 0

    def getRandom(self):
        'get random colour values'
        l = [e[0] for e in self.colours]
        return random.choices(k=self.numOfColours, population=l)

    def startGame(self):
        'start the game'
        start = input('Are you ready?\ny/n: ').lower()

        if start in ('y', 'yes'):
            Game.loopGame(self)
        else:
            sys.exit()

    def loopGame(self):
        computerGuess = self.computerGuess
        print(computerGuess)
        running = True
        PASS = 1

        while running:
            userGuess = Game.getInput(self, PASS)
            Game.getMatching(self, userGuess)

            if self.black == 4:
                print(
                    f'\nYou won!\nYou got the same guesses like the computer in {PASS} ', end='')
                match PASS:
                    case 1:
                        print('try')
                    case 2:
                        print('tries')

                Game.printColored(self, computerGuess, pre='Solution: ')

                again = input('\nDo you want to play again?\ny/n: ').lower()
                if again in ('y', 'yes'):
                    gameInitializer()
                else:
                    sys.exit()
            else:
                print(
                    f'\nYou have {self.black} positions right.\nYou have {self.white}x the right colour but on the wrong position\n')

            PASS += 1

    def getMatching(self, userGuess):
        self.white = 0
        self.black = 0
        for element in range(4):
            curUser = userGuess[element]
            curComputer = self.computerGuess[element]

            # get matching positions
            if curUser == curComputer:
                self.black += 1

            # get matching colours
            elif curUser in self.computerGuess:
                self.white += 1
            element += 1

    def getInput(self, PASS):
        'gets a validated input'
        colours = self.colours

        while self.maxPasses >= PASS or self.maxPasses == 0:
            if self.maxPasses == 0:
                print(f'Write your {PASS}./∞ guess')
            else:
                print(f'Write your {PASS}./{self.maxPasses} guess')
            userInput = input().lower()

            if userInput in ('q', 'quit', 'e', 'exit'):
                sys.exit()
            if userInput in ('r', 'restart'):
                Game.startGame(self)

            userInput = Game.splitInput(self, userInput)
            breaker = Game.validateInput1(self, userInput)
            if breaker:
                break

        return Game.validateInput(self, userInput)

    def validateInput1(self, userInput):
        if len(userInput) == 4:
            return Game.checkColours(self, userInput)
        UILen = len(userInput)
        if UILen > 4:
            print(
                f'\nYou entered too much values. You can only input 4 values but you entered {UILen}.')
        if UILen < 4:
            print(
                f'\nYou entered too few values. You have to input 4 values but you entered only {UILen}.')

    def splitInput(self, userInput):
        if len(userInput) == 4:
            userInput = [userInput[0], userInput[1],
                         userInput[2], userInput[3]]
        else:
            userInput = userInput.split(' ')
        return userInput

    def checkColours(self, userInput):
        colours = self.colours
        c = 0
        o = [False, False, False, False]
        for element in userInput:
            f = 0
            for pair in colours:
                if element not in pair:
                    f += 1
                if element in pair:
                    o[c] = True
            if f == 6:
                print(
                    f'\nYou entered a wrong value ("{element}"). Please try again.')
                break
            c += 1
        if o == [True, True, True, True]:
            return True

    def validateInput(self, userInput):
        'validate input\n\n--> input in colour names'
        userGuess = []
        colours = self.colours

        for e in range(4):
            current = userInput[e]

            # get colour name from letter
            if len(current) == 1:
                for pair in colours:
                    if current in (pair[1], pair[2]):
                        userGuess.append(pair[0])
                        break
            else:
                userGuess.append(current)

        Game.printColored(self, userGuess, '\nYour guess:\n')
        return userGuess

    def printColored(self, userGuess, pre):
        'print colored user guess'
        print(pre, end='')
        colourvalues = Game.Colourvalues()
        for element in userGuess:
            match element:
                case 'red':
                    curCol = colourvalues.red
                case 'magenta':
                    curCol = colourvalues.magenta
                case 'green':
                    curCol = colourvalues.green
                case 'yellow':
                    curCol = colourvalues.yellow
                case 'white':
                    curCol = colourvalues.white
                case 'black':
                    curCol = colourvalues.black
            print(f"{curCol}{element}{colourvalues.normal}", end='   ')
        print()


def gameInitializer():
    while True:
        maxPasses = input(
            'In how much passes you want to win this game? (0 for ∞ tries):\n')
        try:
            maxPasses = int(maxPasses)
            break
        except:
            print("Somethin is wrong with your input. Please try again.")

    while True:
        numberOfColours = input(
            'With how many colours to guess you want to play?\n')
        try:
            numberOfColours = int(numberOfColours)
            break
        except:
            print("Somethin is wrong with your input. Please try again.")

    game = Game(maxPasses, numberOfColours)
    game.startGame()


gameInitializer()
