"""
For use at:
http://www.foddy.net/Athletics.html
For use with QWOP scrolled to top of page on the leftmost screen needing 1080p resolution.
(otherwise change both bbox somewhere around line 130-131. The Find_Score_Location.py can help with this.)
This will take control of your Q, W, O, and P keys while running typing into any selected field.
PyAutoGUI has a fail-safe which triggers by moving mouse to upper-left corner. This will kill the program.
Please make sure to click on QWOP window when countdown starts to select that input field.

You will need Tesseract-OCR installed
https://github.com/tesseract-ocr/tesseract

This code will go through a set of random commands to be played in QWOP.
It will record the game distance saving the moves for the best run.
From there it will modify a set percent of moves until improvement then start changing those moves.

By Mark Brown: mrb5142@rit.edu
"""


from pyautogui import keyUp
from pyautogui import keyDown
from pyautogui import press
from pyscreenshot import grab
from time import time
from time import sleep
from random import randint
from PIL import Image
import pytesseract
import pickle
import matplotlib.pyplot as plt

""" Begin things to change """
learning_rate = 0.1  # What percent of moves to be replaced each run (0.1 = 10%)
game_len = 5  # Time in seconds of one game
game_total = 100  # Total amount of games to play
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'  # Change if custom install
""" End things to change """

# Create lists, Set base game to 1, Set total number of moves and waits to make. [DO NOT CHANGE]
graph = []
graph2 = []
moves = []
waits = []
old_moves = []
old_waits = []
game = 1
txt2 = ''
total = int(game_len * 60)  # [REALLY DON'T CHANGE THIS ONE]
print()
print('Playing ' + str(game_total) +
      ' games of ' + str(game_len) + ' seconds each lasting about '
      + str(int((game_len * game_total + 5 * game_total)/60)) + ' minutes or ' +
      str(int((game_len * game_total + 5 * game_total)/3600)) + ' hours.')

# Load old best else creates list of random button presses and waits
try:
    old_distance = distance = pickle.load(open('QWOP_dist_' + str(game_len) + '_' + str(learning_rate) + '.p', 'rb'))
    old_moves = moves = pickle.load(open('QWOP_moves_' + str(game_len) + '_' + str(learning_rate) + '.p', 'rb'))
    old_waits = waits = pickle.load(open('QWOP_waits_' + str(game_len) + '_' + str(learning_rate) + '.p', 'rb'))
    graph = pickle.load(open('QWOP_graph_' + str(game_len) + '_' + str(learning_rate) + '.p', 'rb'))
    graph2 = pickle.load(open('QWOP_graph2_' + str(game_len) + '_' + str(learning_rate) + '.p', 'rb'))
    print('Loading files for QWOP_' + str(game_len) + '_' + str(learning_rate) + ' ...')
except OSError:
    print('Creating new files upon finish for QWOP_' + str(game_len) + '_' + str(learning_rate))
    old_distance = distance = -10  # This sets an unreasonable low to easily beat
    n = 0
    while n < total:
        moves.append(666)
        waits.append(666)
        n += 1

print('10 seconds till start')
sleep(10)

# This kills the guy :(
keyDown('Q')
sleep(2.5)
keyUp('Q')
keyDown('W')
sleep(2.5)
keyUp('W')


# Run game after game until max
while game <= game_total:

    # Reset random lists until survival
    if distance == -10:
        print('Resetting all')
        print()
        n = 0
        while n < total:
            a = randint(1, 4)
            if a == 1:
                moves[n] = 'Q'
            elif a == 2:
                moves[n] = 'W'
            elif a == 3:
                moves[n] = 'O'
            elif a == 4:
                moves[n] = 'P'
            waits[n] = a / 2
            n += 1
        old_moves = moves
        old_waits = waits

    # Start game reset
    press('space')
    print('Start: Game ' + str(game) + ' / ' + str(game_total))
    end = time() + game_len

# Run game
    for i in range(total):
        # print(i)
        # print('Time left: ' + str(int(end - time())))
        # print('Move: ' + str(moves[i]))
        # print('Wait: ' + str(waits[i]))
        # print('Moves left: ' + str(total - i))
        keyDown(str(moves[i]))
        sleep(int(waits[i]))
        keyUp(str(moves[i]))
        i += 1
        if time() > end:
            sleep(.5)  # Pause to count falling as death

            # Grab screenshot of score and death message then use OCR to read txt (if any)
            im1 = grab(bbox=(720, 350, 1190, 400), childprocess=False)  # CHANGE BBOX IF NEEDED grab distance + 'meters'
            im2 = grab(bbox=(800, 460, 1120, 510), childprocess=False)  # CHANGE BBOX IF NEEDED grab 'PARTICIPANT'
            im1.save('im1.png')
            im2.save('im2.png')
            txt1 = pytesseract.image_to_string(Image.open('im1.png'))
            txt1 = txt1[:-6]
            txt2 = pytesseract.image_to_string(Image.open('im2.png'))
            distance = float(txt1.strip(' '))
            if txt2 != 'PARTICIPANT':
                print('Game ' + str(game) + ': ' + str(distance) + ' / ' + str(old_distance))
                graph2.append(distance)
            else:
                print('Game ' + str(game) + ': DEATH(' + str(distance) + ') / ' + str(old_distance))
                graph2.append(0)
            print()

# This kills the guy :(
            keyDown('Q')
            sleep(2.5)
            keyUp('Q')
            keyDown('W')
            sleep(2.5)
            keyUp('W')
            game += 1
            break

# Only use top score (distance)
    if distance >= old_distance and txt2 != 'PARTICIPANT':
        old_distance = distance
        old_moves = moves
        old_waits = waits
    else:
        distance = old_distance
        moves = old_moves
        waits = old_waits
    graph.append(distance)

# Replace a percent of moves in the longest distance run each time
    n = 0
    while n <= int(len(moves) * learning_rate):
        a = randint(1, 4)
        if a == 1:
            moves[randint(0, total - 1)] = 'Q'
        elif a == 2:
            moves[randint(0, total - 1)] = 'W'
        elif a == 3:
            moves[randint(0, total - 1)] = 'O'
        elif a == 4:
            moves[randint(0, total - 1)] = 'P'
        else:
            print('Error 1')
        waits[randint(0, total - 1)] = a / 2
        n += 1

# Print and save results
print('Total games; ' + str(game - 1))
print('Best score: ' + str(old_distance))
print('Saving files for QWOP_' + str(game_len) + '_' + str(learning_rate) + ' ...')
pickle.dump(distance, open('QWOP_dist_' + str(game_len) + '_' + str(learning_rate) + '.p', 'wb'))
pickle.dump(moves, open('QWOP_moves_' + str(game_len) + '_' + str(learning_rate) + '.p', 'wb'))
pickle.dump(waits, open('QWOP_waits_' + str(game_len) + '_' + str(learning_rate) + '.p', 'wb'))
pickle.dump(graph, open('QWOP_graph_' + str(game_len) + '_' + str(learning_rate) + '.p', 'wb'))
pickle.dump(graph2, open('QWOP_graph2_' + str(game_len) + '_' + str(learning_rate) + '.p', 'wb'))
plt.plot(graph)
plt.plot(graph2)
plt.show()
