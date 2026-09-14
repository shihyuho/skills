class ArtifactStore:
    def __init__(self):
        self.saved = []

    def save(self, body):
        self.saved.append(body)


class Notifier:
    def __init__(self, fail=False):
        self.fail = fail
        self.attempts = []

    def notify(self, body):
        self.attempts.append(body)
        if self.fail:
            raise RuntimeError("notification failed")
