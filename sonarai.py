'''
This program is based off of the game "Sonar Treasure Hunt" by Al Sweigart, featured
in Chapter 13 of his book "Invent Your Own Computer Games With Python".

Sonar AI by Timothy Eden
Date Last Updated: June 11, 2023

This program is a modification of the code of "Sonar Treasure Hunt", removing the user
inputs and instead taking inputs from an AI player that follows a set strategy to have
the highest chance of finding all the treasure chests. In a test of 1000 attempts, the AI
showed an 80.7% win rate.

The reason the AI player currently cannot have a 100% win rate is because the game has three
chests to find, and the feedback from the sonar device to the player does not specify which chest
it is closest to for a particular guess. There is also a bug where, if it tries to move on a space
it already moved on and receives the message "You already moved there", it does not have adequate
logic to make a new guess and will continue to try to guess that same spot over and over again,
effectively making it lose the game. So, there is room for improvement in debugging and possible
improvement of the strategy.
'''

import random
import sys
import math

# here, I initialize some global variables that will be used later
eliminations = []
sonar_log = {}
next_sonar_number = 1
guess_list = []
# the "stuck" variable tells you whether the AI got stuck in a loop of "You already moved there"
stuck = False

def getNewBoard():
    '''
    This function was included in the original program, and I did not modify it.
    '''
    # Create a new 60x15 board data structure.
    board = []
    for x in range(60): # The main list is a list of 60 lists.
        board.append([])
        for y in range(15): # Each list in the main list has 15 single-character strings.
            # Use different characters for the ocean to make it more readable.
            if random.randint(0, 1) == 0:
                board[x].append('~')
            else:
                board[x].append('`')
    return board

def drawBoard(board):
    '''
    This function was included in the original program, and I did not modify it.
    '''
    # Draw the board data structure.
    tensDigitsLine = '    ' # Initial space for the numbers down the left side of the board
    for i in range(1, 6):
        tensDigitsLine += (' ' * 9) + str(i)

    # Print the numbers across the top of the board.
    print(tensDigitsLine)
    print('   ' + ('0123456789' * 6))
    print()

    # Print each of the 15 rows.
    for row in range(15):
        # Single-digit numbers need to be padded with an extra space.
        if row < 10:
            extraSpace = ' '
        else:
            extraSpace = ''

        # Create the string for this row on the board.
        boardRow = ''
        for column in range(60):
            boardRow += board[column][row]

        print('%s%s %s %s' % (extraSpace, row, boardRow, row))

    # Print the numbers across the bottom of the board.
    print()
    print('   ' + ('0123456789' * 6))
    print(tensDigitsLine)

def getRandomChests(numChests):
    '''
    While this function was part of the original program, I modified it to try and
    experiment with a way to remedy the problem of unclear feedback from sonar devices
    due to chests being too close to each other. This function now will only generate
    chest positions more than 21 spaces away from each other.

    When the program was tested without this modification, it showed a 75.9% win rate.
    '''
    # Create a list of chest data structures (two-item lists of x, y int coordinates).
    chests = []
    while len(chests) < numChests:
        newChest = [random.randint(0, 59), random.randint(0, 14)]
        if newChest not in chests: # Make sure a chest is not already here.
            if len(chests) != 0:
                for chest in chests:
                    distance = math.sqrt((chest[0] - newChest[0]) ** 2 + (chest[1] - newChest[1]) ** 2)
                    if distance > 21:
                        chests.append(newChest)
            else:
                chests.append(newChest)
    return chests

def isOnBoard(x, y):
    '''
    This function was included in the original program, and I did not modify it.
    '''
    # Return True if the coordinates are on the board; otherwise, return False.
    return x >= 0 and x <= 59 and y >= 0 and y <= 14

def makeMove(board, chests, x, y):
    '''
    This function was included in the original program, and I did not modify it.
    '''
    # Change the board data structure with a sonar device character. Remove treasure chests from the chests list as they are found.
    # Return False if this is an invalid move.
    # Otherwise, return the string of the result of this move.
    smallestDistance = 100 # Any chest will be closer than 100.
    for cx, cy in chests:
        distance = math.sqrt((cx - x) * (cx - x) + (cy - y) * (cy - y))

        if distance < smallestDistance: # We want the closest treasure chest.
            smallestDistance = distance

    smallestDistance = round(smallestDistance)

    if smallestDistance == 0:
        # xy is directly on a treasure chest!
        chests.remove([x, y])
        return 'You have found a sunken treasure chest!'
    else:
        if smallestDistance < 10:
            board[x][y] = str(smallestDistance)
            return 'Treasure detected at a distance of %s from the sonar device.' % (smallestDistance)
        else:
            board[x][y] = 'X'
            return 'Sonar did not detect anything. All treasure chests out of range.'

def enterPlayerMove(previousMoves):
    '''
    This function was included in the original program, and I did not modify it.
    Due to the lack of user input, this function is not used in this program.
    '''
    # Let the player enter their move. Return a two-item list of int xy coordinates.
    print('Where do you want to drop the next sonar device? (0-59 0-14) (or type quit)')
    while True:
        move = input()
        if move.lower() == 'quit':
            print('Thanks for playing!')
            sys.exit()

        move = move.split()
        if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and isOnBoard(int(move[0]), int(move[1])):
            if [int(move[0]), int(move[1])] in previousMoves:
                print('You already moved there.')
                continue
            return [int(move[0]), int(move[1])]

        print('Enter a number from 0 to 59, a space, then a number from 0 to 14.')


def get_distance(chests, x, y):
    '''
    This function gets the distance between a point on the board and the
    nearest treasure chest. In reality, all I did was copy the first part
    of the makeMove function included in the original program.

    :param chests: The list containing the coordinates of all the chests.
    :param x: The x coordinate of the point being compared.
    :param y: The y coordinate of the point being compared.
    :return: Returns the distance between the point and the nearest chest, which
    would be the smallest distance found.
    '''
    smallestDistance = 100 # Any chest will be closer than 100.
    for cx, cy in chests:
        distance = math.sqrt((cx - x) * (cx - x) + (cy - y) * (cy - y))

        if distance < smallestDistance: # We want the closest treasure chest.
            smallestDistance = distance

    smallestDistance = round(smallestDistance)

    return smallestDistance


def get_possible():
    '''
    This function is used only once at the beginning of the program. It generates
    a list of every single point on the board, which is a list that will be removed
    from each time it is determined that a space cannot be the location of a treasure
    chest.

    :return: Returns a list of every single point on the board.
    '''
    all_possible = []
    for x in range(0, 60):
        for y in range(0, 15):
            all_possible.append([x, y])
    return all_possible


def get_optimal_count(point, possible):
    '''
    This function takes in a point and the list of possible points, and counts the number
    of possible points that are within a distance of 10 from the point. In Sonar, a device
    will only give you information on each space within a distance of 10.

    The reason we need this information is because if a guess must be made randomly,
    it is important that the guess will give insight on the most number of points. For
    example, you wouldn't want to guess in the very corner and only get insight on half the
    number of points due to there being less surrounding points.

    :param point: the point being evaluated
    :param possible: list of possible guesses
    :return: returns the number of surrounding possible guesses
    '''
    count = 0
    for other_point in possible:
            distance = math.sqrt((point[0] - other_point[0])**2 + (point[1] - other_point[1])**2)
            distance = round(distance)
            if distance < 10:
                count += 1
    return count


def get_optimal_winner(possible):
    '''
    This function is called anytime the AI must make a guess randomly; when there is
    no available information about the coordinates of the nearest chest. This function
    uses get_optimal_count on every possible guess, and finds out which point has the most
    surrounding points in the possible list. If multiple points tie, it chooses randomly.

    :param possible: the list of possible guesses
    :return: returns the point that will be guessed
    '''
    points_list = []
    winners_list = []
    winner = None
    for point in possible:
        count = get_optimal_count(point, possible)
        points_list.append([point, count])
    largest_count = 0
    for item in points_list:
        if item[1] > largest_count:
            largest_count = item[1]
    for item in points_list:
        if item[1] == largest_count:
            winners_list.append(item[0])
    if len(winners_list) == 1:
        winner = winners_list[0]
    else:
        x = random.randint(0, len(winners_list) -1)
        winner = winners_list[x]
    return winner


def get_eliminations(point, possible):
    '''
    Eliminations is a global list that is continuously appended to throughout
    the program. In essence, it contains every point that certainly does not
    contain a treasure chest. This list is evaluated in order to update the possible
    list to remove guesses that definitely aren't the treasure chest.

    If a guess is made and the sonar device displays 'X', every single point within a
    distance of 10 from that guess will be added to eliminations, because none of those
    points could be the treasure chest.

    :param point: the point guessed which returned an 'X'
    :param possible: the list of possible guesses
    :return: This function does not return anything, as it edits a global list.
    '''
    global eliminations
    for other_point in possible:
        distance = math.sqrt((point[0] - other_point[0]) ** 2 + (point[1] - other_point[1]) ** 2)
        distance = round(distance)
        if distance < 10:
            eliminations.append(other_point)


def edit_possible():
    '''
    This function uses the global list of eliminations, and creates an updated
    possible list which does not contain any of these points.

    :return: The new possible list.
    '''
    new_list = []
    global eliminations
    for x in range(0, 60):
        for y in range(0, 15):
            if [x,y] not in eliminations:
                new_list.append([x, y])
    return new_list


def zone_in(coordinates, number, possible):
    '''
    This function is called when a guess is made, and the sonar device displays a number.
    For example, if the sonar device says '5', that means there is a chest within a distance
    of exactly 5 from the device, so we have greatly narrowed down the possible locations of
    said chest. This function creates a list of all the possible locations of this chest, and
    randomly selects one of these points to be the next guess.

    :param coordinates: The coordinates of the guess.
    :param number: The number displayed on the sonar device, which is the exact distance
    between it and the nearest chest.
    :param possible: The list of possible guesses.
    :return: The point that will be guessed next.
    '''
    zone_in_list = []
    for other_point in possible:
        distance = math.sqrt((coordinates[0] - other_point[0]) ** 2 + (coordinates[1] - other_point[1]) ** 2)
        distance = round(distance)
        if distance == number:
            zone_in_list.append(other_point)
    if len(zone_in_list) == 1:
        winner = zone_in_list[0]
    #elif zone_in_list == []:
        #print('ZONE IN LIST EMPTY')
    else:
        x = random.randint(0, len(zone_in_list) -1)
        winner = zone_in_list[x]
    #print('zone in list:')
    #print(zone_in_list)
    return winner


def zone_in_2(c1, c2, c1number, c2number, possible):
    '''
    If the function zone_in is called, and the point guessed is not the location of
    the chest, we now have 2 sonar devices displaying numbers. This means that the
    chest is one distance away from one point, and another distance from another point,
    and in order for a point to be where the chest is, it must be the correct distance from
    both points.

    This function makes a list of all points that meet these criteria.

    :param c1: The coordinates of one of the sonar devices being evaluated.
    :param c2: The coordinates of the other sonar device being evaluated.
    :param c1number: The number displayed on the first sonar device.
    :param c2number: The number displayed on the second sonar device.
    :param possible: The list of possible guesses.
    :return: This function does not return, it edits a global list.
    '''
    global guess_list
    for other_point in possible:
        p1distance = math.sqrt((c1[0] - other_point[0]) ** 2 + (c1[1] - other_point[1]) ** 2)
        p1distance = round(p1distance)
        p2distance = math.sqrt((c2[0] - other_point[0]) ** 2 + (c2[1] - other_point[1]) ** 2)
        p2distance = round(p2distance)
        if p1distance == c1number and p2distance == c2number:
            guess_list.append(other_point)


def add_to_sonar_log(coordinates, distance):
    '''
    sonar_log is a global list that contains the data on each guess made. It contains
    the coordinates of the sonar device, and the number displayed indicating its distance
    from the nearest chest. If it displays an 'X', the distance is listed as '-1'.

    The reason this is needed later is that when a chest is found, the information on all
    sonar devices is subject to change. Any sonar device displaying a number could either change
    to a higher number (indicating distance from a different chest), or change to X. The
    eliminations list must be updated accordingly, and we also need to be able to reevaluate
    sonar devices with numbers based on the new information.

    :param coordinates: The coordinates of the sonar device being added
    :param distance: The number displayed (or -1 for X)
    :return: No return, edits a global list
    '''
    global next_sonar_number
    global sonar_log
    sonar_name = 'sonar' + str(next_sonar_number)
    if distance < 10:
        sonar_log[sonar_name] = {'coordinates': coordinates, 'distance': distance}
    else:
        sonar_log[sonar_name] = {'coordinates': coordinates, 'distance': -1}
    next_sonar_number += 1


def update_sonar_log(chests, possible):
    '''
    This function is called if a chest is found. It iterates through every sonar device
    in the sonar log, and updates the 'distance' information if that has changed. If it
    has changed to an 'X', or '-1' in the log, the eliminations and possible lists are
    updated accordingly.

    :param chests:
    :param possible:
    :return:
    '''
    global sonar_log
    for device in sonar_log:
        x_cord = sonar_log[device]['coordinates'][0]
        y_cord = sonar_log[device]['coordinates'][1]
        distance = get_distance(chests, x_cord, y_cord)
        if distance > 9:
            sonar_log[device]['distance'] = -1
        else:
            sonar_log[device]['distance'] = distance
    for device in sonar_log:
        point = sonar_log[device]['coordinates']
        if sonar_log[device]['distance'] == -1:
            get_eliminations(point, possible)
            possible = edit_possible()
    return possible


def get_computer_move(previous_moves, possible):
    '''
    This function evaluates all information about possible guesses and if any
    sonar devices display a number, and puts it all together to generate the
    computer's next move.

    If there are no sonar devices displaying a number, it
    calls get_optimal_winner. If there is one sonar device displaying a number,
    it calls zone_in. If there is more than one sonar device displaying a number,
    it will start by calling zone_in_2 to get guess_list, and then guess every
    point in the list.

    This function also updates the global Boolean variable "stuck", and changes
    it to True if the computer gets stuck in the loop of "You already moved there",
    which currently does not have a solution and effectively causes the computer
    to lose the game.

    :param previous_moves: All previous moves made.
    :param possible: The list of possible guesses.
    :return: The point that will be guessed next.
    '''
    global stuck
    global guess_list
    global sonar_log
    print('Where do you want to drop the next sonar device? (0-59 0-14) (or type quit)')
    if previous_moves == []:
        #print('if previous moves empty')
        point = get_optimal_winner(possible)
        return point
    else:
        #print('else, previous moves not empty')
        good_sonars = 0
        good_list = []
        for device in sonar_log:
            if sonar_log[device]['distance'] == -1:
                pass
            else:
                good_list.append(sonar_log[device])
                good_sonars += 1
        if good_sonars == 0:
            #print('if good sonars is 0, point = get optimal winner')
            point = get_optimal_winner(possible)
            return point
        elif good_sonars == 1:
            #print('if good sonars is 1, use zone in')
            coordinates = good_list[0]['coordinates']
            number = good_list[0]['distance']
            point = zone_in(coordinates, number, possible)
            return point
        elif good_sonars > 1:
            # call zone in 2 when we get a second good sonar
            if guess_list == []:
                #print('if good sonars is over 1, use zone in 2')
                coordinates1 = good_list[0]['coordinates']
                number1 = good_list[0]['distance']
                coordinates2 = good_list[1]['coordinates']
                number2 = good_list[1]['distance']
                zone_in_2(coordinates1, coordinates2, number1, number2, possible)
            #print('guess list')
            #print(guess_list)
            if guess_list == []:
                point = get_optimal_winner(possible)
                return point
            point = guess_list[0]
            guess_list.remove(guess_list[0])
            if [int(point[0]), int(point[1])] in previous_moves:
                print('You already moved there.')
                stuck = True
                guess_list = []
                point = get_optimal_winner(possible)
            return point


def showInstructions():
    '''
    This function was part of the original program and I did not modify it.
    It displays the game's instructions if a player inputs 'yes', however the
    program is written to simulate that the computer always inputs 'no', so this
    function is never called.
    '''
    print('''Instructions:
You are the captain of the Simon, a treasure-hunting ship. Your current mission
is to use sonar devices to find three sunken treasure chests at the bottom of
the ocean. But you only have cheap sonar that finds distance, not direction.

Enter the coordinates to drop a sonar device. The ocean map will be marked with
how far away the nearest chest is, or an X if it is beyond the sonar device's
range. For example, the C marks are where chests are. The sonar device shows a
3 because the closest chest is 3 spaces away.

1 2 3
012345678901234567890123456789012

0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0
1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1
2 `~`C``3`~~~~`C`~~~~`````~~``~~~`` 2
3 ````````~~~`````~~~`~`````~`~``~` 3
4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4

012345678901234567890123456789012
1 2 3
(In the real game, the chests are not visible in the ocean.)

Press enter to continue...''')

    print('''When you drop a sonar device directly on a chest, you retrieve it and the other
sonar devices update to show how far away the next nearest chest is. The chests
are beyond the range of the sonar device on the left, so it shows an X.

1 2 3
012345678901234567890123456789012

0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0
1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1
2 `~`X``7`~~~~`C`~~~~`````~~``~~~`` 2
3 ````````~~~`````~~~`~`````~`~``~` 3
4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4

012345678901234567890123456789012
1 2 3

The treasure chests don't move around. Sonar devices can detect treasure chests
up to a distance of 9 spaces. Try to collect all 3 chests before running out of
sonar devices. Good luck!

Press enter to continue...''')



print('S O N A R !')
print()
print('Would you like to view the instructions? (yes/no)')
print('no')

while True:
    # Game setup
    sonarDevices = 20
    theBoard = getNewBoard()
    theChests = getRandomChests(3)
    drawBoard(theBoard)
    previousMoves = []
    possible = get_possible()

    while sonarDevices > 0:
        # Show sonar device and chest statuses.
        print('You have %s sonar device(s) left. %s treasure chest(s) remaining.' % (sonarDevices, len(theChests)))

        # this is just visual board code
        point = get_computer_move(previousMoves, possible)
        x = point[0]
        y = point[1]
        print('{} {}'.format(x, y))
        previousMoves.append([x, y]) # We must track all moves so that sonar devices can be updated.

        moveResult = makeMove(theBoard, theChests, x, y)
        distance = get_distance(theChests, x, y)
        #print('smallest distance:')
        #print(distance)
        if moveResult == False:
            continue
        else:
            #guess_the_other_one = False
            add_to_sonar_log(point, distance)
            if moveResult == 'You have found a sunken treasure chest!':
                # Update all the sonar devices currently on the map.
                for x, y in previousMoves:
                    makeMove(theBoard, theChests, x, y)
                possible = update_sonar_log(theChests, possible)
                guess_list = []
            drawBoard(theBoard)
            print(moveResult)

        if len(theChests) == 0:
            print('You have found all the sunken treasure chests! Congratulations and good game!')
            break

        sonarDevices -= 1

        if distance > 9:
            #print('updating eliminations and possible list')
            get_eliminations(point, possible)
            possible = edit_possible()

    if sonarDevices == 0:
        print('We\'ve run out of sonar devices! Now we have to turn the ship around and head')
        print('for home with treasure chests still out there! Game over.')
        print(' The remaining chests were here:')
        for x, y in theChests:
            print(' %s, %s' % (x, y))

    print('Do you want to play again? (yes or no)')
    print('no')
    if stuck == True:
        print('stuck = True')
    sys.exit()
