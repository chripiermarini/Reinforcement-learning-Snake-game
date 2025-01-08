import gym
from gym import spaces


class gym_env(gym.Env):
    """
    OpenAI gym class to create the RL agent environment. In a first moment, 
    we will create the game as intende to be played by a human.
    Afterwards, we will convert the game into a gym enviornment
    in which the game will be played by the agent.
    
    Careful: this OpenAI gym environment must be installed through the following command:
    'pip install -e gym_env.py'
    """
    
    metadata = {"render.modes": ["human"]}

    def __init__(self):

        # number of possible discrete action spaces
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)

        # initializing the observation space
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(HEIGHT, WIDTH, N_CHANNELS), dtype=uint8
        )
    
    def step(self, action):
        """
        Step taken after the action being performed by the human/agent.
        """
        ...
        return observation, reward, done, info
    
    def reset(self):
        '''
        It returns the observation from the environment.
        '''
        ...
        return observation7
    
    def render(self, mode = 'human'):
        ...
        return 
    
    def close(self):
        '''
        Final closing of the enviornment.
        '''
        ...
        return     
    
    