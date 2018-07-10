# QWOP_Learner
Learns how to walk in QWOP by randomly improving 

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
