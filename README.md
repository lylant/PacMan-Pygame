# Pac-Man

This repo involves producing a Pac-Man style game in Python.

## Game Contents

* **The Essencial:** to make Pac-Man eat all available pellets, while avoiding collisions with ghosts chasing him.
* **Ghosts:** Ghosts always start at their home base. All ghosts move toward random direction. 
* **Game Levels:** All levels are generated based on the map data from the resource files.

## Languages

* Python
  * Tkinter
  * Pygame


# Project Details

## Installation

1. Clone the repo with Git
2. Check you installed Python
3. Check you installed [Pygame](https://www.pygame.org "Pygame Link")
4. Execute *main.py* with Python


## Map Generator

The map generator will read a map file in `/resource` folder. The file name should be `level#.txt` or `level##.txt`, `##` refers to the number of the level. The file contains 32×32 characters, each character indicates a block/item in the game field.


### Symbol Legends

* `_` passage (empty)
* `#` wall
* `$` ghost spawn point
* `.` pellet
* `@` Pac-Man (starting point)
* `&` free ghost
* `%` caged ghost


### Example

```
############################
#............##............#
#.####.#####.##.#####.####.#
#.####.#####.##.#####.####.#
#.####.#####.##.#####.####.#
#..........................#
#.####.##.########.##.####.#
#.####.##.########.##.####.#
#......##....##....##......#
######.#####_##_#####.######
######.#####_##_#####.######
######.##____&_____##.######
######.##_###_####_##.######
######.##_###_####_##.######
______.___###$####___.______
######.##_###%####_##.######
######.##_########_##.######
######.##__________##.######
######.##_########_##.######
######.##_########_##.######
#............##............#
#.####.#####.##.#####.####.#
#.####.#####.##.#####.####.#
#...##.......@........##...#
###.##.##.########.##.##.###
###.##.##.########.##.##.###
#......##....##....##......#
#.##########.##.##########.#
#.##########.##.##########.#
#..........................#
############################
############################
```
