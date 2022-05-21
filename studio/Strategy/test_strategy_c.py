
import backtrader
from .default_strategy import TestStrategyDefault


class TestStrategyPlanC(TestStrategyDefault):

    params = (
        ("need_log", False),
        ("exitbars", 10)
    )

    def __init__(self):
        super().__init__()
        super().set_need_log(False)

        self.log(self.params.need_log)
