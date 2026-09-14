"""Contracts for an invented, entirely in-memory report publisher."""

from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def format(self, rows):
        raise NotImplementedError


class Auditable:
    """A label with no implementation."""
