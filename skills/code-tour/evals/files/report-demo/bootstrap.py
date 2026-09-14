from adapters import ArtifactStore, Notifier
from formatters import CompactFormatter, DetailedFormatter
from publisher import Publisher


FORMATTERS = {"compact": CompactFormatter, "detailed": DetailedFormatter}


def build_publisher(kind="compact", fail_notification=False):
    formatter = FORMATTERS[kind]()
    return Publisher(formatter, ArtifactStore(), Notifier(fail_notification))
