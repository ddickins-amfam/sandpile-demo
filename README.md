# sandpile-demo

Repository for the Abelian sandpile model, a.k.a. the chip-firing game.  

## [sandpile.py](./sandpile.py)
Contains the class for the Abelian sandpile model.  Methods currently implemented allow for running the chip-firing game. [test_sandpile.py](./test_sandpile.py) has the tests for the Sandpile class.

## [stabilizing.py](./stabilizing.py)
Demonstrates some of the commutative features of the Abelian sandpile; these powerful properties allow for interesting applications of the model.

## [self_organized_criticality.py](./self_organized_criticality.py)
One of the most interesting features of the Abelian sandpile model is that it shows self-organized criticality (SOC).  This program repeatedly runs the chip firing game on a uniform grid to demonstrate the property.  Several plots of avalanches created during the game are produced, as well as a graph of avalanche sizes following the power law.

## [graph_coloring.py](./graph_coloring.py)
Based on https://www.nature.com/articles/s41598-018-20275-7, this program uses the SOC property of the sandpile model to solve the graph coloring problem on a uniform grid.  

## [subset_sum.py](./subset_sum.py)
Another application of https://www.nature.com/articles/s41598-018-20275-7, the script tackles the subset sum (a non-convex optimization) problem using SOC.  
