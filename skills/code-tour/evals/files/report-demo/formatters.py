from contracts import Auditable, Formatter


class CompactFormatter(Formatter):
    def format(self, rows):
        return ",".join(rows)


class DetailedFormatter(Formatter, Auditable):
    def format(self, rows):
        return "\n".join("{}: {}".format(i, row) for i, row in enumerate(rows, 1))
