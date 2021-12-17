# Final_Project

This is a code for the mine sweeper game. 

## How To Use
Method 1:
1. Set the parameters you want in the file custom.py
2. Run main.py file

Method 2:

Run advanced.py file
This is an extra file we wrote that includes a start screen to let the user key in the total number of mines they want in the minefield.

## How to play
### Know your symbols
* Flag: Put a flag in a zone when you have confirmed that there is a mine.
* Question Mark: Put a question mark when you suspect that there is a mine. But it is useless.
* Smiley face: Click it if you want to reset the game.

### Window
![mineswp_1](https://user-images.githubusercontent.com/43463024/146459371-e2d87b28-ba68-4190-8c7a-a3dc720d7627.png)

This is what our game looks like. Below is the minefield grid.
From top left to right is the number of total mines remaining, the face(smiley when you win and sad when you lose), and the stopwatch.


### Clicking stuff

You can start by clicking at any random place. Chances are you'll have something like the image above. The number is the number of mines adjacent to the block. If you think the block contains a mine, flag it by right clicking. Do the same with others.
When you accidentally step on a mine, the below image will show:

![2](https://user-images.githubusercontent.com/43463024/146460384-dc00180a-4354-4da5-8dc0-a9fbce2c34f9.png)

## Code description
1. main.py : This is the main function of the mine sweeper game.
2. objects.py : This code file contains all the objects and algorithms necessary to run the game.
3. custom.py: This code file contains parameters that the user can change including number of mines, grid size, and size of smiley face image.

Contributors: Po-I Hsieh, Vina Ro
