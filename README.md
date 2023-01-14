# Cricket Game MDP
This repository contains code for simulating a cricket game as a Markov Decision Process (MDP). The game is played by two players, a batsman A and a batsman B, with the goal of maximizing the number of runs scored by A. The game is defined by a set of states, actions, and rewards, and can be solved using various algorithms for MDP planning such as value iteration, policy iteration, and linear programming.

## File Structure
The repository contains the following files:

### encoder.py: 
Contains the implementation of the encoder class which is used to encode the game rules and parameters into the MDP transition and reward matrices.

### generateMDP.py: 
Contains the implementation of the MDP class which is used to generate an episodic or continuing MDP.

### planner.py: 
Contains the implementation of the plan_my_MDP class which is used to solve the MDP using various algorithms such as value iteration, policy iteration and linear programming.

### reader.py: 
A sample script that reads an episodic MDP file and prints the transition and reward matrices

data/: A folder that contains the data files for the MDP.

data/mdp/: A folder that contains the episodic MDP files.

## Encoding the Game
The game is encoded using the encoder.py file which contains the implementation of the encoder class. The class takes the following inputs:

playp: a text file that contains the probability distribution of the actions of the batsman A.
states: a text file that contains a list of all possible states in the game.
q : a parameter that

## How to use the code
The main.py file is the entry point of the code. It takes in three command line arguments: the path to the MDP file, the path to the player parameters file, and the value of q. The MDP file is in the /data/mdp/ directory, and the player parameters file is in the /data/player_params/ directory.

The main.py file first creates an instance of the encoder class by passing the path to the player parameters file and the value of q. The encoder class reads the player parameters file and initializes the action-outcome matrix, the list of states, and the transition and reward matrices.

The main.py file then creates an instance of the generateMDP class by passing the path to the MDP file, the number of states, and the number of actions. The generateMDP class reads the MDP file and initializes the transition and reward matrices.

The main.py file then creates an instance of the plan_my_MDP class by passing the transition and reward matrices, the discount factor, and the type of MDP. The plan_my_MDP class calculates the value function and the policy for the given MDP using value iteration, policy iteration or linear programming.

## How the code works
The encoder.py file contains a class encoder which is used to encode the problem of scoring runs in a cricket match as an MDP. The class takes in the path to the player parameters file and the value of q as inputs. The player parameters file contains the probabilities of different outcomes for different actions taken by the
