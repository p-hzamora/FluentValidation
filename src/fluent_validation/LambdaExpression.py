import inspect
import re
from typing import Any, Callable


class LambdaExpression:
    REGEX: re.Pattern = re.compile(r"lambda[^)]*?")

    def __init__(self, func: Callable[..., Any]) -> None:
        self._lambda: Callable[..., Any] = func

    @property
    def func(self) -> Callable[..., Any]:
        return self._lambda

    @property
    def lambda_to_string(self) -> str:
        get_source = inspect.getsource(self._lambda).strip()

        return self.get_real_lambda_from_source_code(get_source)

    @staticmethod
    def get_real_lambda_from_source_code(chain: str):
        chain = re.search(r"lambda.+", chain).group()
        n = len(chain)
        open_parenthesis: list[int] = [0] * n
        result: str = ""

        for i in range(n):
            char = chain[i]

            if char == "(":
                open_parenthesis[i] = 1

            if char == ")":
                open_parenthesis[i] = -1

            if sum(open_parenthesis) < 0:
                break

            result += char

        return result
