from typing import Any


class MemoryModule:
    def __init__(self, short_term_limit: int = 1000):
        if short_term_limit < 1:
            raise ValueError("short_term_limit must be positive")
        self.short_term: list[dict[str, Any]] = []
        self.long_term: list[dict[str, Any]] = []
        self.short_term_limit = short_term_limit

    def store_short_term(self, item: dict[str, Any]) -> None:
        self.short_term.append(item)
        del self.short_term[:-self.short_term_limit]

    def store_long_term(self, item: dict[str, Any]) -> None:
        self.long_term.append(item)

    def recall_recent(self, n: int = 5) -> list[dict[str, Any]]:
        if n < 0:
            raise ValueError("n must not be negative")
        return self.short_term[-n:] if n else []

    storeshortterm = store_short_term
    storelongterm = store_long_term
