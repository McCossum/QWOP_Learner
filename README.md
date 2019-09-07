# QWOP_Learner
This was my first attempt at writing a program which learns as it goes on. I previously had no experience writing or understanding learning models and used this to test the waters to know what I should investigate.

This model runs my creating a randon set of moves, excicuting them, then changing ~10%. It then runs again. If the result is better it will itterate off of the new set, and if worse will revert to itterating off the previous set. 

THis of course has downfalls as it can get stuck in false bottoms. Though this is true it has progressed from .2m walking distance to 4.8m walking distance over the course of ~2000 itterations. This is roughly on par with an actual player of the game. 

For use at:
http://www.foddy.net/Athletics.html
Must be scrolled to top of page on the leftmost screen needing 1080p resolution.
(otherwise change both bbox somewhere around line 130-131. The Find_Score_Location.py can help with this.)
This will take control of your Q, W, O, and P keys while running typing into any selected field.
PyAutoGUI has a fail-safe which triggers by moving mouse to upper-left corner. This will kill the program.
Please make sure to click on QWOP window when countdown starts to select that input field.

You will need Tesseract-OCR installed
https://github.com/tesseract-ocr/tesseract

By Mark Brown: McCossum@gmail.com
