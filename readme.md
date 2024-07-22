# Sokoban Solver

## Description

This project aims to find solutions to [Sokoban](https://en.wikipedia.org/wiki/Sokoban) levels

## Requirements


## Requirements

To run this project, you will need the following:

- Python 3
- SciPy library

You can install Python 3 from the official website: [Python.org](https://www.python.org/downloads/)

To install the SciPy library, you can use pip:

```shell
pip install scipy
```

Make sure to have both Python 3 and SciPy installed before running the project.


## Installation

To install this project, follow these steps:

1. Clone the repo and compile the code using the following commands:
```shell
git clone https://github.com/ShalevWen/AI-ex1.git
cd AI-ex1
```

## Usage

### 1. Select a level collection

To run one of the test level collections, select one from the `levels` and set the `levels_file` variable in the `main.py` [file](main.py#L7) to the name of the level collection file (no `.py`).

To use a custom collection, create a new python file with the following format:

```python
levels = [
    "level1",
    "level2",
    "level3",
    ...
]
```

Where each level is a 2D array of numbers, representing the level. The numbers are as follows:

`0` - empty space

`1` - target

`2` - player

`4` - box

`8` - wall

For spaces with multiple objects, sum the values. For example, a space with a box and a target will have the value `5`.

After creating the custom level collection, set the `leveles_file` variable in the `main.py` [file](main.py#L7) to the name of the custom level collection file (no `.py`).

### 2. Select the algorithm

To select the algorithm, set the `algorithm` variable in the `main.py` [file](main.py#L8) to the desired algorithm. The options are:

- `gbfs` - Greedy Best First Search. Finds a solution as fast as possible, but it may not be the optimal solution.

- `astar` - A* Search. Finds the optimal solution, but it may take longer to find it.


### 3. Run the program

To run the program, use the following command:

```shell
python main.py
```

The program will save the solutions in the `output` directory, the name of the file will be the name of the level with the `.txt` extension.



## More Information

### Heuristic

The heuristic used is calculated by relaxing the problem to a simpler one by allowing the player to "teleport" anywhere for free, and then calculating the minimum moves required to reach all the targets.

For each box, we find the minimum required moves to reach every terget, taking into account the walls and the fact that the player needs to push the box.
<br>Then, we find a minimum matching between the boxes and the targets, and sum the moves required for each box to reach its target.
<br> Finally, we add the manhattan distance between the player and the closest box.

### Test Levels

All test levels are taken from [sneezingtiger.com](http://sneezingtiger.com/sokoban/levels.html).