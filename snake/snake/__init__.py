# used to import from the parent folder
# contains registration code for environment name and where to find the enviornment file.

from gym.envs.registration import register

register(id = 'snake-v0', 
         entry_point='snake.envs:SnakeEnv' #find inside snake envs folder the class called SnakeEnv
         )