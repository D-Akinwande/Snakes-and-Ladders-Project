import numpy as np
import random as rd
import types as tp


class SnakesAndLadders:
    '''Implements a Snake and Ladder Game that can be played.

        Attributes:
    numSquares: the number of squares on the board.
    Snakes: the 2D list/ndarray containing the start and end square for every snake.
    Ladders: the 2D list/ndarray containing the start and end square for every ladder.
    Overflow: What to do if the rolled square is beyond the last on the board. 'classic': overflows count as last square; 'rollback': overflows are subtracted from last; 'ignore': overflows aren't counted.
    Squares: The list that stores each square (defined as Square class) on the board.

        Methods:
    __init__(...): instantiates the class (defines and creates a Snakes and Ladders game).
    play_game(...): plays Snakes and Ladder game a specified number of times.
    '''


    def __init__(self, numSquares, Snakes, Ladders, Overflow='classic'):
        '''Instantiates the class (defines and creates a Snakes and Ladders game).

            Inputs:
        numSquares: the number of squares on the board.
        Snakes: the 2D list/ndarray containing the start and end square for every snake.
        Ladders: the 2D list/ndarray containing the start and end square for every ladder.
        Overflow: What to do if the rolled square is beyond the last on the board. 'classic': overflows count as last square; 'rollback': overflows are subtracted from last; 'ignore': overflows aren't counted.
           
            Outputs:
        [No Outputs]
        '''    

        ## Makes sure that numSquares is the correct type
        if type(numSquares) == int: 
            self.numSquares = numSquares
        else:
            print("WARNING: The given numbers of squares isn't an integer, so it is set to 100.")
            self.numSquares = 100


        def check_snake_ladder(snkOrLddr, name):
            '''Checks the shape (dimensions) and bounds of the Snakes or Ladders list, and replaces/remove it respectively if it isn't the correct type.

                Inputs:
            snkOrLddr: the Snakes or Ladders list/ndarray to be checked.
            name: the name of the Snakes or Ladders list/ndarray, for the warning messages.

               Outputs: 
            newSnkOrLddr: the checked or changed Snakes or Ladders list/ndarray, for assignment into the attributes.
            '''

            match np.shape(snkOrLddr): ### Matches the dimensions of the list
                case (n, 2): #### Correct shape
                    newSnkOrLddr = snkOrLddr
                case (2, n): #### Transposed shape
                    print(f"WARNING: The {name} array should have a n by 2 shape, where n is the number of {name}. Therefore, its axes are swapped.")
                    newSnkOrLddr = np.swapaxes(snkOrLddr, 0, 1)
                case (n, m): #### Wrong dimensions
                    print(f"WARNING: The {name} array should have a n by 2 shape, where n is the number of {name}. Therefore, replaced with empty list.")
                    newSnkOrLddr = []
                case (0,)|(1,0): #### Empty 1D or 2D list respectively
                    newSnkOrLddr = []
                case _: #### Not a (2D) list
                    if not isinstance(snkOrLddr, tp.NoneType): ##### If snkOrLddr is not equal to None
                        print(f"WARNING: {name} should be an (n by 2) array but is {type(snkOrLddr)}, where n is the number of {name}. Therefore, replaced with empty list.")
                    newSnkOrLddr = []

            ## Predefines number for counting number of Snakes list rows, and flag for invalid 'snake'
            num = 0
            invalid = False

            ### Removes 'snakes/ladders' from the list with invalid bound(s)
            for nsl in newSnkOrLddr:
                invalid = False

                if np.min(nsl) < 1: ### Less than minimum
                    print(f"WARNING: A min. bound in {name} can't be less than 1, therefore bound {nsl} is deleted.")
                    invalid = True
                elif np.max(nsl) > self.numSquares: ### More than maximum
                    print(f"WARNING: A max. bound in {name} can't be greater than {self.numSquares}, therefore bound {nsl} is deleted.")
                    invalid = True
                elif np.min(nsl) == np.max(nsl): ### Same square values
                    print(f"WARNING: The bounds in {name} can't be the same, therefore bound {nsl} is deleted.")
                    invalid = True
                else: 
                    num = num + 1

                if invalid == True:
                    newSnkOrLddr = np.delete(newSnkOrLddr, num, 0) #### Deletes bounds (row of list) if it is invalid

            return newSnkOrLddr


        ## Stores Snakes and Ladders lists as attributes
        self.Snakes = check_snake_ladder(Snakes, "snakes")
        self.Ladders = check_snake_ladder(Ladders, "ladders")

        ## Makes sure that Overflow type is valid and stores it as an attribute
        try:
            match Overflow.lower():
                case 'classic'|'c':
                    self.Overflow = 'classic'
                case 'rollback'|'r'|'rb':
                    self.Overflow = 'rollback'
                case 'ignore'|'i':
                    self.Overflow = 'ignore'
                case _: #### Invalid type
                    print("WARNING: Overflow is not valid. Setting to Classic.")
                    self.Overflow = 'classic'
        except Exception as e: ## Catch any exceptions, especially AttributeError from not having lower() method
            print(f"WARNING: {str(e)}, so Overflow is not valid. Setting to Classic.") ### e is the error message
            self.Overflow = 'classic'

        ## Predefines list of squares
        self.Squares = []

        ## Square creation loop
        for i in range(0, self.numSquares):
            ### Predefines Square parameters
            sqrNum = i+1
            nxtSqrs = None
            hsSnk = False
            hsLdr = False

            ### Checks if the square has a snake
            for s in self.Snakes:
                if sqrNum == np.max(s):
                    if sqrNum == self.numSquares:
                        print("WARNING: The last square can't have a snake.")
                    else:
                        nxtSqrs = int(np.min(s)) ###### Converted from numpy.int64 to int to make datatype comparison in roll_die() easier
                        hsSnk = True
                    break
            
            ### Checks if the square has a ladder
            for l in self.Ladders:
                if sqrNum == np.min(l):
                    if sqrNum == self.numSquares:
                        print("WARNING: The last square can't have a ladder.")
                    else:
                        nxtSqrs = int(np.max(l)) ###### Converted from numpy.int64 to int to make datatype comparison in roll_die() easier
                        hsLdr = True
                    break

            ### Sets nxtSqrs (nextSquares) if the square doesn't have a snake/ladder 
            if nxtSqrs == None:
                if sqrNum == self.numSquares:
                    nxtSqrs = None
                
                elif (self.numSquares - 6) < sqrNum < self.numSquares: #### 5th last to penultimate squares

                    match self.Overflow.lower():
                        case 'classic'|'c'|'ignore'|'i': ###### Both 'classic' and 'ignore'
                            nxtSqrs = np.arange(sqrNum + 1, sqrNum + 7) ####### NP array with next 6 square numbers from current
                        case 'rollback'|'r':
                            nxtSqrs = np.arange(self.numSquares - 5, self.numSquares + 1) ####### NP array with last 6 square numbers from end
                            
                else:
                    nxtSqrs = np.arange(sqrNum + 1, sqrNum + 7)
                        
            
            ### Creates square and adds it to the list
            square = Square(squareNum=sqrNum, nextSquares=nxtSqrs, hasSnake=hsSnk, hasLadder=hsLdr)
            self.Squares.append(square)



    def play_game(self, numPlayers, numTimes, maxTurns=100):
        '''Plays Snakes and Ladder game a specified number of times.

            Inputs:
        numPlayers: the number of players for the game. 
        numTimes: the number of times to play the game.
        maxTurns: the maximum number of turns before the game ends automatically.

            Outputs:
        gamesList: the list of arrays containing the square number of each player for each turn of a game (starting from the zeroth turn).
        '''

        ## Predefines gamesList
        gamesList = []

        ## Loop per game
        for i in range(0,numTimes):
            game = i + 1
            turn = 0
            gameEnd = False
            gameSqrNums = np.ones((numPlayers,1)) ### Rows are the players, columns are the turns

            print(f"\n \t Game: {game}")


            ### Loop within each game
            while gameEnd == False:
                turn = turn + 1
                turnSqrNums = np.empty((numPlayers,1)) #### Predefines current turn square number array for later
                firstWinner = True #### Indicates whether the first winner has been found
                player = 1 #### Player number

                print(f"\n \t \t Turn: {turn}")


                #### Turn loop
                for j in range(0,numPlayers):
                    player = j + 1
                    prevNum = int(gameSqrNums[j,turn-1]) ##### The previous turn's square number for the player, converted from numpy.float64 to integers
                    prevSqr = self.Squares[prevNum-1] ##### The Square class with the corresponding previous number

                    ##### Messages for reaching a snake/ladder
                    if prevSqr.hasSnake == True:
                        print(f"Player {player} went down the snake at square {prevNum}.")
                    elif prevSqr.hasLadder == True:
                        print(f"Player {player} went up the ladder at square {prevNum}.")

                    currNum = prevSqr.roll_die() ##### The current turn's (rolled) square number for the player

                    ##### Special cases of currNum
                    if (currNum == self.numSquares)|(currNum == False): ##### Player reaches the last square
                        gameEnd = True
                        
                        ###### Makes sure that this is the first valid winner
                        if firstWinner == True: 
                            winner = player
                            firstWinner = False
                    elif currNum > self.numSquares: ##### Player rolls a higher square than the last (if possible)

                        match self.Overflow:
                            ###### case 'rollback' was already dealt with by generated square numbers
                            case 'classic':
                                currNum = self.numSquares
                                gameEnd = True

                                ######## Makes sure that this is the first valid winner
                                if firstWinner == True: 
                                    winner = player
                                    firstWinner = False
                            case 'ignore':
                                print(f"Player {player}'s roll ({currNum}) was too big.")
                                currNum = gameSqrNums[j,turn-1] ######## Use previous turn's square number                           


                    ##### Shows player's next (current) square
                    print(f"Player {player}, next square: {currNum}")

                    ##### Adds player's current square number to the array
                    turnSqrNums[j, 0] = currNum 


                #### Adds current turn square number array to previous turns array
                gameSqrNums = np.concat((gameSqrNums, turnSqrNums), axis=1) 

                #### Deals with end game
                if gameEnd == True:
                    print(f"Player {winner} won the game.")
                elif turn == maxTurns: 
                    #### Ends game if maximum number of turns are reached
                    print(f"Max turns ({maxTurns}) exceeded, ending game.")
                    gameEnd = True

            ## Adds array of square numbers for the game to the list for all games
            gamesList.append(gameSqrNums) 

        return gamesList




class Square:
    '''Implements each square on a snakes and ladder board.

        Attributes:
    squareNum: the number of the square.
    hasSnake = True (has a snake) if square is on the top of a snake.
    hasLadder = True (has a ladder) if square is on the bottom of a ladder.
    nextSquares: the list/ndarray of the numbers, or value of the number, of the square(s) that can be reached by this square.

        Methods:
    __init__(...): instantiates the class (defines and creates a square).
    roll_die(...): Gets a random square that can be reached from current square.
    '''


    def __init__(self, squareNum, nextSquares=None, hasSnake=False, hasLadder=False):
        '''instantiates the class (defines and creates a square). 

           Inputs:
        squareNum: the number of the square.
        hasSnake = True (has a snake) if square is on the top of a snake.
        hasLadder = True (has a ladder) if square is on the bottom of a ladder.
        nextSquares: the list/ndarray of the numbers, or value of the number, of the square(s) that can be reached by this square.

           Outputs:
        [No Outputs]
        '''

        ## Makes sure that squareNum is the correct type
        if type(squareNum) == int: 
            self.squareNum = squareNum
        else:
            print("WARNING: The given square number isn't an integer, so it is set to zero.")
            self.squareNum = 0


        if ( isinstance(nextSquares, tp.NoneType) ) or (np.size(nextSquares) == 0): ## Square has no following squares
            ### Checks if it has a snake/ladder
            if (hasSnake == True) and (hasLadder == False): 
                print("WARNING: Square",self.squareNum,"can't have a snake as it has no following squares, so it is removed.")
            elif (hasSnake == False) and (hasLadder == True):
                print("WARNING: Square",self.squareNum,"can't have a ladder as it has no following squares, so it is removed.")
            elif (hasSnake == True) and (hasLadder == True):
                print("WARNING: Square",self.squareNum,"can't have a snake or ladder as it has no following squares, so both are removed.")
                
            self.hasSnake = False
            self.hasLadder = False
            self.nextSquares = None
            
        elif (hasSnake == True) and (hasLadder == True): ## Square has both a snake and ladder
            print("WARNING: Square",self.squareNum,"can't have both snakes and ladders, so it will have neither.")
            
            self.nextSquares = nextSquares
            self.hasSnake = False
            self.hasLadder = False

        elif ((hasSnake == True) or (hasLadder == True)) and (np.size(nextSquares) > 1):
            ## If there is a snake/ladder and more than one following square
            print("WARNING: Square",self.squareNum,"has a snake/ladder, so it should have only one following square.")

            self.hasSnake = hasSnake
            self.hasLadder = hasLadder

            for i in nextSquares:
                if ((hasSnake == True) and (i < squareNum)) or ((hasLadder == True) and (i > squareNum)):
                    #### If next square in list is on the bottom of a snake or the top of a ladder (whichever is applicable)
                    if self.hasSnake == True:
                        print(f"Valid nextSquares number found ({i}) for square {self.squareNum} (with snake). Setting nextSquares to it.")
                    elif self.hasLadder == True:
                        print(f"Valid nextSquares number found ({i}) for square {self.squareNum} (with ladder). Setting nextSquares to it.")                    

                    self.nextSquares = i
                    break
            else:
                print("WARNING: Square",self.squareNum,"has no valid following squares, so none will be selected.")
                self.nextSquares = None

        else: ### Default case
            self.hasSnake = hasSnake
            self.hasLadder = hasLadder
            self.nextSquares = nextSquares

    

    def roll_die(self):
        '''Gets a random square that can be reached from current square.

           Inputs:
        [No Inputs]

           Output:
        Next: the number/ID of a random square following this one (False if there is no next square available).
        '''

        match self:
            
            case Square(nextSquares=None): ### If there are no squares after this one
                print("WARNING: Square",self.squareNum,"has no connections.")
                Next = False
            
            case _: ### Anything else 
                if isinstance(self.nextSquares,int): #### nextSquares is an integer
                    Next = self.nextSquares
                else:
                    Next = rd.choice(self.nextSquares) ## Gets random square from nextSquares list
        
        return Next





'''
# Testing
## 1. Squares Class 
### 1.1 __init__ function (Definition and assignment)
#### 1.1.1 squareNum assignment test
print("\n \t","squareNum assignment test")
sqr1_1_1_1 = Square(squareNum=1)
print("Square 1:",sqr1_1_1_1.squareNum,"\n")

sqr1_1_1_2 = Square(squareNum="a")
print("Square 2:",sqr1_1_1_2.squareNum,"\n")


#### 1.1.2 No nextSquares with snake/ladder test
print("\n \t","No nextSquares with snake/ladder test")
sqr1_1_2_1 = Square(squareNum=1, nextSquares=None, hasSnake=True, hasLadder=False)
print(f"Square 1: hasSnake = {sqr1_1_2_1.hasSnake}, hasLadder = {sqr1_1_2_1.hasLadder} \n")
sqr1_1_2_2 = Square(squareNum=2, nextSquares=None, hasSnake=False, hasLadder=True)
print(f"Square 2: hasSnake = {sqr1_1_2_2.hasSnake}, hasLadder = {sqr1_1_2_2.hasLadder} \n")
sqr1_1_2_3 = Square(squareNum=3, nextSquares=None, hasSnake=True, hasLadder=True)
print(f"Square 3: hasSnake = {sqr1_1_2_3.hasSnake}, hasLadder = {sqr1_1_2_3.hasLadder} \n")

sqr1_1_2_4 = Square(squareNum=4, nextSquares=[], hasSnake=True, hasLadder=False)
print(f"Square 4: hasSnake = {sqr1_1_2_4.hasSnake}, hasLadder = {sqr1_1_2_4.hasLadder} \n")
sqr1_1_2_5 = Square(squareNum=5, nextSquares=[], hasSnake=False, hasLadder=True)
print(f"Square 5: hasSnake = {sqr1_1_2_5.hasSnake}, hasLadder = {sqr1_1_2_5.hasLadder} \n")
sqr1_1_2_6 = Square(squareNum=6, nextSquares=[], hasSnake=True, hasLadder=True)
print(f"Square 6: hasSnake = {sqr1_1_2_6.hasSnake}, hasLadder = {sqr1_1_2_6.hasLadder} \n")

sqr1_1_2_7 = Square(squareNum=7, nextSquares=np.array([]), hasSnake=True, hasLadder=False)
print(f"Square 7: hasSnake = {sqr1_1_2_7.hasSnake}, hasLadder = {sqr1_1_2_7.hasLadder} \n")
sqr1_1_2_8 = Square(squareNum=8, nextSquares=np.array([]), hasSnake=False, hasLadder=True)
print(f"Square 8: hasSnake = {sqr1_1_2_8.hasSnake}, hasLadder = {sqr1_1_2_8.hasLadder} \n")
sqr1_1_2_9 = Square(squareNum=9, nextSquares=np.array([]), hasSnake=True, hasLadder=True)
print(f"Square 9: hasSnake = {sqr1_1_2_9.hasSnake}, hasLadder = {sqr1_1_2_9.hasLadder} \n")


#### 1.1.3 Both snake and ladder test
print("\n \t","Both snake and ladder test")
sqr1_1_3_1 = Square(squareNum=1, nextSquares=2, hasSnake=True, hasLadder=True)
print(f"Square 1: hasSnake = {sqr1_1_3_1.hasSnake}, hasLadder = {sqr1_1_3_1.hasLadder} \n")


#### 1.1.4 Multiple following squares with a snake/ladder test
print("\n \t","Multiple following squares with a snake/ladder test")
sqr1_1_4_1 = Square(squareNum=2, nextSquares=[1,3], hasSnake=True, hasLadder=False)
print(f"Square 1: nextSquares = {sqr1_1_4_1.nextSquares} \n")
sqr1_1_4_2 = Square(squareNum=2, nextSquares=[1,3], hasSnake=False, hasLadder=True)
print(f"Square 2: nextSquares = {sqr1_1_4_2.nextSquares} \n")
sqr1_1_4_3 = Square(squareNum=1, nextSquares=[2,3], hasSnake=True, hasLadder=False)
print(f"Square 3: nextSquares = {sqr1_1_4_3.nextSquares} \n")
sqr1_1_4_4 = Square(squareNum=3, nextSquares=[1,2], hasSnake=False, hasLadder=True)
print(f"Square 4: nextSquares = {sqr1_1_4_4.nextSquares} \n")

sqr1_1_4_5 = Square(squareNum=2, nextSquares=np.array([1,3]), hasSnake=True, hasLadder=False)
print(f"Square 5: nextSquares = {sqr1_1_4_5.nextSquares} \n")
sqr1_1_4_6 = Square(squareNum=2, nextSquares=np.array([1,3]), hasSnake=False, hasLadder=True)
print(f"Square 6: nextSquares = {sqr1_1_4_6.nextSquares} \n")
sqr1_1_4_7 = Square(squareNum=1, nextSquares=np.array([2,3]), hasSnake=True, hasLadder=False)
print(f"Square 7: nextSquares = {sqr1_1_4_7.nextSquares} \n")
sqr1_1_4_8 = Square(squareNum=3, nextSquares=np.array([1,2]), hasSnake=False, hasLadder=True)
print(f"Square 8: nextSquares = {sqr1_1_4_8.nextSquares} \n")



### 1.2 roll_die function
print("\n \t","roll_die test")
sqr1_2_1 = Square(squareNum=1, nextSquares=None)
next_1 = sqr1_2_1.roll_die()
print(f"Square 1: Next square: {next_1}\n")

sqr1_2_2 = Square(squareNum=2, nextSquares=[])
next_2 = sqr1_2_2.roll_die()
print(f"Square 2: Next square: {next_2}\n")

sqr1_2_3 = Square(squareNum=3, nextSquares=np.array([]))
next_3 = sqr1_2_3.roll_die()
print(f"Square 3: Next square: {next_3}\n")

sqr1_2_4 = Square(squareNum=4, nextSquares=[6,7,8,9,10])
next_4 = sqr1_2_4.roll_die()
print(f"Square 4: Next square: {next_4}\n")

sqr1_2_5 = Square(squareNum=5, nextSquares=np.array([6,7,8,9,10]))
next_5 = sqr1_2_5.roll_die()
print(f"Square 5: Next square: {next_5}\n")

sqr1_2_6 = Square(squareNum=6, nextSquares=[6])
next_6 = sqr1_2_6.roll_die()
print(f"Square 6: Next square: {next_6}\n")

sqr1_2_7 = Square(squareNum=7, nextSquares=np.array([6]))
next_7 = sqr1_2_7.roll_die()
print(f"Square 7: Next square: {next_7}\n")

sqr1_2_8 = Square(squareNum=8, nextSquares=6)
next_8 = sqr1_2_8.roll_die()
print(f"Square 8: Next square: {next_8}\n")





## 2. SnakesAndLadders Class
### 2.1 __init__ function (Definition and assignment)
#### 2.1.1 Default square creation testing
print("\n \t","squareNum assignment test")
slg2_1_1_1 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow='classic')
print('\n')
slg2_1_1_2 = SnakesAndLadders(numSquares=10.5, Snakes=[], Ladders=[], Overflow='classic')
print('\n')
slg2_1_1_3 = SnakesAndLadders(numSquares="10", Snakes=[], Ladders=[], Overflow='classic')
print('\n')

sqrList2_1_1_1 = slg2_1_1_1.Squares
print("Snakes and Ladder game:")
print(f"Number of squares: {len(sqrList2_1_1_1)}, squares: {sqrList2_1_1_1}\n")

sqr2_1_1_1 = sqrList2_1_1_1[0]
print("1st square:")
print(f"Square number: {sqr2_1_1_1.squareNum}, next squares: {sqr2_1_1_1.nextSquares}\n")

sqr2_1_1_2 = sqrList2_1_1_1[4]
print("2nd square:")
print(f"Square number: {sqr2_1_1_2.squareNum}, next squares: {sqr2_1_1_2.nextSquares}\n")
      
sqr2_1_1_3 = sqrList2_1_1_1[9]
print("3rd square:")
print(f"Square number: {sqr2_1_1_3.squareNum}, next squares: {sqr2_1_1_3.nextSquares}\n")


#### 2.1.2 Snakes and Ladders lists test
print("\n \t","Snakes and Ladders lists test")
##### 2.1.2.1 Correct format test
print("\t \t","Correct format test")
slg2_1_2_1_1 = SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,10],[4,6]], Overflow='classic')
print(f"Snakes: {slg2_1_2_1_1.Snakes}; Ladders: {slg2_1_2_1_1.Ladders}\n")

print("Squares:")
for i in slg2_1_2_1_1.Squares:
    print(f"Square number: {i.squareNum}, next squares: {i.nextSquares}\n")


##### 2.1.2.2 Incorrect format test
print("\n \t \t","Incorrect format test")
print("Game 1:")
slg2_1_2_2_1 = SnakesAndLadders(numSquares=20, Snakes=[[9,2],[8,0],[3,7],[21,4],[6,5],[5,5]], Ladders=[[11,13,15],[12,14,16]], Overflow='classic')
print(f"Snakes: {slg2_1_2_2_1.Snakes}; Ladders: {slg2_1_2_2_1.Ladders}\n")

print("Squares:")
for i in slg2_1_2_2_1.Squares:
    print(f"Square number: {i.squareNum}, next squares: {i.nextSquares}")

print("\nGame 2:")
slg2_1_2_2_2 = SnakesAndLadders(numSquares=10, Snakes=[[10,9,8],[7,6,5],[4,3,2]], Ladders="Ladder List", Overflow='classic')
print(f"Snakes: {slg2_1_2_2_2.Snakes}; Ladders: {slg2_1_2_2_2.Ladders}\n")

print("Game 3:")
slg2_1_2_2_3 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=None, Overflow='classic')
print(f"Snakes: {slg2_1_2_2_3.Snakes}; Ladders: {slg2_1_2_2_3.Ladders}\n")

print("Game 4:")
slg2_1_2_2_4 = SnakesAndLadders(numSquares=10, Snakes=[[9,1],[10,2]], Ladders=[[3,8],[4,10]], Overflow='classic')
print(f"Snakes: {slg2_1_2_2_4.Snakes}; Ladders: {slg2_1_2_2_4.Ladders}\n")

print("Game 5:")
slg2_1_2_2_5 = SnakesAndLadders(numSquares=12, Snakes=[1,2,3,4], Ladders=[[[3,4],[5,6]],[[7,8],[9,10]]], Overflow='classic')
print(f"Snakes: {slg2_1_2_2_5.Snakes}; Ladders: {slg2_1_2_2_5.Ladders}\n")


#### 2.1.3 Overflow test
print("\n \t","Overflow test")
##### 2.1.3.1 Correct format test
print("\t \t","Correct (overflow) format test")

print(f"Game 1 (classic):")
slg2_1_3_1_1 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow='classic')
print("Squares:")
for i in slg2_1_3_1_1.Squares[3:]:
    print(f"Square number: {i.squareNum}, next squares: {i.nextSquares}")

print(f"\nGame 2 (rollback):")
slg2_1_3_1_2 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow='rollback')
print("Squares:")
for i in slg2_1_3_1_2.Squares[3:]:
    print(f"Square number: {i.squareNum}, next squares: {i.nextSquares}")

print(f"\nGame 3 (ignore):")
slg2_1_3_1_3 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow='ignore')
print("Squares:")
for i in slg2_1_3_1_3.Squares[3:]:
    print(f"Square number: {i.squareNum}, next squares: {i.nextSquares}")

print(f"\nGame 4 (c):")
slg2_1_3_1_4 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow='c')
sqr2_1_3_1_4 = slg2_1_3_1_4.Squares[8]
print(f"Square number: {sqr2_1_3_1_4.squareNum}, next squares: {sqr2_1_3_1_4.nextSquares}")

print(f"\nGame 5 (r):")
slg2_1_3_1_5 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow='r')
sqr2_1_3_1_5 = slg2_1_3_1_5.Squares[8]
print(f"Square number: {sqr2_1_3_1_5.squareNum}, next squares: {sqr2_1_3_1_5.nextSquares}")

print(f"\nGame 6 (rb):")
slg2_1_3_1_6 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow='rb')
sqr2_1_3_1_6 = slg2_1_3_1_6.Squares[8]
print(f"Square number: {sqr2_1_3_1_6.squareNum}, next squares: {sqr2_1_3_1_6.nextSquares}")

print(f"\nGame 7 (i):")
slg2_1_3_1_7 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow='i')
sqr2_1_3_1_7 = slg2_1_3_1_7.Squares[8]
print(f"Square number: {sqr2_1_3_1_7.squareNum}, next squares: {sqr2_1_3_1_7.nextSquares}")

print(f"\nGame 8 (ClAsSiC):")
slg2_1_3_1_8 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow='ClAsSiC')
sqr2_1_3_1_8 = slg2_1_3_1_8.Squares[8]
print(f"Square number: {sqr2_1_3_1_8.squareNum}, next squares: {sqr2_1_3_1_8.nextSquares}")


##### 2.1.3.2 Inorrect format test
print("\n \t \t","Incorrect (overflow) format test")
print(f"Game 1: (different string)")
slg2_1_3_2_1 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow='different')
print("Squares:")
for i in slg2_1_3_2_1.Squares[3:]:
    print(f"Square number: {i.squareNum}, next squares: {i.nextSquares}")

print(f"\nGame 2: (integer)")
slg2_1_3_2_2 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow=1)

print(f"\nGame 3: (None)")
slg2_1_3_2_3 = SnakesAndLadders(numSquares=10, Snakes=[], Ladders=[], Overflow=None)



### 2.2 play_game function
#### 2.2.1 Single game, single player test
print("\n \t","Single game, single player test")
##### 2.2.1.1 Classic game test
print("\n \t \t","Classic game test")
slg2_2_1_1_1 = SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,8],[4,6]], Overflow='classic')
#slg2_2_1_1_1 = SnakesAndLadders(numSquares=2, Snakes=[], Ladders=[[1,2]], Overflow='classic') # Test issues with snakes/ladders

# Double checks Square generation works properly
#print("Squares:")
#for i in slg2_2_1_1_1.Squares:
#    print(f"Square number: {i.squareNum}, next squares: {i.nextSquares}\n")

gl2_2_1_1_1 = slg2_2_1_1_1.play_game(numPlayers=1, numTimes=1, maxTurns=100)
print(f"\n Game List (classic): {gl2_2_1_1_1}")


##### 2.2.1.2 Rollback game test
print("\n \t \t","Rollback game test")
slg2_2_1_2_1 = SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,8],[4,6]], Overflow='rollback')

# Double checks Square generation works properly
#print("Squares:")
#for i in slg2_2_1_2_1.Squares:
#    print(f"Square number: {i.squareNum}, next squares: {i.nextSquares}\n")

gl2_2_1_2_1 = slg2_2_1_2_1.play_game(numPlayers=1, numTimes=1, maxTurns=100)
print(f"\n Game List (rollback): {gl2_2_1_2_1}")


##### 2.2.1.3 Ignore game test
print("\n \t \t","Ignore game test")
slg2_2_1_3_1 = SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,8],[4,6]], Overflow='ignore')

# Double checks Square generation works properly
# print("Squares:")
# for i in slg2_2_1_3_1.Squares:
#     print(f"Square number: {i.squareNum}, next squares: {i.nextSquares}\n")

gl2_2_1_3_1 = slg2_2_1_3_1.play_game(numPlayers=1, numTimes=1, maxTurns=100)
print(f"\n Game List (ignore): {gl2_2_1_3_1}")


#### 2.2.2 Multiple games, single players test
print("\n \t","Multiple games, single player test")
##### 2.2.2.1  2 Games test
print("\n \t \t","2 Games test")
slg2_2_2_1_1= SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,8],[4,6]], Overflow='classic')

gl2_2_2_1_1 = slg2_2_2_1_1.play_game(numPlayers=1, numTimes=2, maxTurns=100)
print(f"\n Game List (2 games): {gl2_2_2_1_1}")


##### 2.2.2.2  5 Games test
print("\n \t \t","5 Games test")
slg2_2_2_2_1= SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,8],[4,6]], Overflow='classic')

gl2_2_2_2_1 = slg2_2_2_2_1.play_game(numPlayers=1, numTimes=5, maxTurns=100)
print(f"\n Game List (5 games): {gl2_2_2_2_1}")


#### 2.2.3 Single game, multiple players test
print("\n \t","Single game, multiple players test")
##### 2.2.3.1  2 Players test
print("\n \t \t","2 Players test")
slg2_2_3_1_1= SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,8],[4,6]], Overflow='classic')

gl2_2_3_1_1 = slg2_2_3_1_1.play_game(numPlayers=2, numTimes=1, maxTurns=100)
print(f"\n Game List (2 players): {gl2_2_3_1_1}")


##### 2.2.3.2  5 Players test
print("\n \t \t","5 Players test")
slg2_2_3_2_1= SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,8],[4,6]], Overflow='classic')

gl2_2_3_2_1 = slg2_2_3_2_1.play_game(numPlayers=5, numTimes=1, maxTurns=100)
print(f"\n Game List (5 players): {gl2_2_3_2_1}")


#### 2.2.4 Multiple games, multiple players test
print("\n \t","Multiple games, multiple players test")
##### 2.2.4.1  2 Players, 2 games test
print("\n \t \t","2 Players, 2 games test")
slg2_2_4_1_1= SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,8],[4,6]], Overflow='classic')

gl2_2_4_1_1 = slg2_2_4_1_1.play_game(numPlayers=2, numTimes=2, maxTurns=100)
print(f"\n Game List (2 players, 2 games): {gl2_2_4_1_1}")


##### 2.2.4.2  5 Players, 5 games test
print("\n \t \t","5 Players, 5 games test")
slg2_2_4_2_1= SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,8],[4,6]], Overflow='classic')

gl2_2_4_2_1 = slg2_2_4_2_1.play_game(numPlayers=5, numTimes=5, maxTurns=100)
print(f"\n Game List (5 players, 5 games): {gl2_2_4_2_1}")


#### 2.2.5 maxTurns test
print("\n \t","maxTurns test")
slg2_2_5_1= SnakesAndLadders(numSquares=10, Snakes=[[9,2],[7,5]], Ladders=[[3,8],[4,6]], Overflow='rollback')

gl2_2_5_1 = slg2_2_5_1.play_game(numPlayers=1, numTimes=5, maxTurns=3)
print(f"\n Game List (maxTurn = 3): {gl2_2_5_1}")
'''