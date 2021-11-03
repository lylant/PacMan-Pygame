# Pac-Man

# Introduction

## Project Backgrounds
This project aims to practice building a Pac-Man style game using Python.

* **The Essencial:** to make Pac-Man eat all available pellets, while avoiding collisions with ghosts chasing him.
* **Ghosts:** Ghosts always start at their home base. All ghosts move toward random direction. 
* **Game Levels:** All levels will be generated based on the map data from the resource files.


## Demo Video Available
* [Link](https://youtu.be/Xkj524OOgvA "Public Demo Video on YouTube")


## Main Tech-Stacks for the Project
* Python


# Installation

## Required Packages
Following packages are required to install the game. Please prepare following packages installed on your machine before the installation. Most recent version is recommended. `Tkinter` and `Pygame` can be installed using `pip`.

* Python 3
* Tkinter
* Pygame

## Installation
As the product is not using any game framework or engine, the installation process is simple copy and paste.

1. Create a directory for the game.
2. Copy the product into the new directory.


## Map Generator

The map generator will read a map file in `/resource` directory. The file name should be `level#.txt` or `level##.txt`, `##` refers to the number of the level. The file contains 32×32 characters, each character indicates a block/item in the game field.


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