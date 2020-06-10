from .long_short_strategy import LongShortStrategy
from .ml_model_strategy import MLModelStrategy

STRATEGIES = {
    LongShortStrategy.__name__: LongShortStrategy,
    MLModelStrategy.__name__: MLModelStrategy
}
