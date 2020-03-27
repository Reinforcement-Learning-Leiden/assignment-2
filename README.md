# Reinforcement Learning 2020 Assignment 2, Adaptive Sampling
## Group 9
### Julius Cathalina, Faezeh Amou, Georgios Tzimitras

## If you're not sure you have all the right packages, remember to run
### pip install -r requirements.txt

# Important files:
### MCTS_v_IDTT.py
- Contains the scripts for evaluation of MCTS vs IDTT players with varying parameters
- parameters to set: RED_SEC_TO_THINK: the number of seconds IDTT is allowed to take for iterative deepening
                     NUMBER_OF_GAMES,
                     itermax: number of iterations for the MCTS algorithm, ignored if MAX_SECONDS_MCTS != None,
                     MAX_SECONDS_MCTS: the number of seconds MCTS is allowed to simulate paths
                     Cp: exploration/exploitation parameter

### tuning.py
- contains the scripts for evaluation of effect of hyperparameters in MCTS
- With simulating the game n times, the results are shown in bar-graphs
- parameters to set: NUMBER_OF_GAMES, 
                     itermax:number of iterations for the MCTS algorithm, ignored if MAX_SECONDS_MCTS != None,
                     MAX_SECONDS_MCTS: the number of seconds MCTS is allowed to simulate paths
                     Cp: exploration/exploitation parameter


### play_hex.py
- Lets you play against either the TTID variant or MCTS variant
- Or choose two algorithms to play agains each other
- parameters to set: Cp: exploration/exploitation parameter for MCTS, itermax: max number of iterations for MCTS and IDTT, 
                      max_seconds: time for each algorithm in case of fixed time experiment, boardSize: size of the hexboard
