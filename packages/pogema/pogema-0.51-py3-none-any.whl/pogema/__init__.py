from gym import register
from pogema.grid_config import GridConfig

__version__ = '0.51'

__all__ = [
    'GridConfig',
]

register(
    id="Pogema-v0",
    entry_point="pogema.envs:Pogema",
)
