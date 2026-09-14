from dataclasses import dataclass

from adapters import ArtifactStore, Notifier
from contracts import Formatter


@dataclass(frozen=True)
class Result:
    mode: str
    body: str


class Publisher:
    def __init__(self, formatter: Formatter, store: ArtifactStore, notifier: Notifier):
        self.formatter = formatter
        self.store = store
        self.notifier = notifier

    def publish(self, rows, preview=False):
        body = self.formatter.format(rows)
        if preview:
            return Result("preview", body)
        self.store.save(body)
        self.notifier.notify(body)
        return Result("published", body)
