from config import math

class GameSpaceConfig():
    def __init__(self, dt, dt_steps, iterations, gravity, damping, sleep_time_threshold=math.inf):
        self.iterations: int = iterations
        self.gravity = gravity
        self.damping: float = damping
        self.sleep_time_threshold: float = sleep_time_threshold
        self.dt: float = dt
        self.dt_steps: int = dt_steps
