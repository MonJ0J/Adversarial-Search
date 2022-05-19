# Adversarial-Search
Implementation game theory for agents competing in a game called Breakthrough.

## Dependencies:

* **argarse**
* **copy**
* **time**
* **math**
* **random**
* **collections**

## How to use:

* On the CLI: navigate to Breakthrough.py and type in command line: ```python3 Breakthrough.py #rows #columns #player_rows #utility_1 #utility_2```. Make sure to replace the first three with integers and the last two with one of the following letters K(Karnage), C(Conquerer), E(Evasive), F(Fortification) depending on your choice.

### example command:
```python3 Breakthrough.py 8 8 2 K F```
```python3 Breakthrough.py 6 6 2 C K```
```python3 Breakthrough.py 5 5 2 E K```


### example output:
```
XXXX.OX.
.XXX.X..
........
.....O..
X.......
..O.....
O..O.OOO
OOOOO.OO

Moves before victory: 31
----------------------------
Board Dimenssions:  8 x 8 , 2
pieces captured by white: 6
pieces captured by black: 1
Time to run the program: 107.68 sec
```
