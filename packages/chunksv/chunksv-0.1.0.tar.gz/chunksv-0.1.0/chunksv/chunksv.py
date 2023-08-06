import csv
import copy


class reader(csv.DictReader):
    def __init__(self, input_stream, delimiter=",", max_bytes=None, header=None):
        self.max_bytes = max_bytes
        self.header = header if header is not None else []
        self.bytes_in = 0
        self.last_line = None
        self.empty = False
        super(reader, self).__init__(input_stream, delimiter=delimiter, fieldnames=self.header)

    def _limit_reached(self):

        if self.max_bytes is not None:
            return self.bytes_in > self.max_bytes
        return False

    @staticmethod
    def _calculate_size(row: list):
        return len(bytes(",".join(row), "utf-8"))

    def __next__(self):

        if self._limit_reached():
            raise StopIteration

        if self.last_line:
            last_line = copy.copy(self.last_line)
            self.last_line = None
            self.bytes_in += self._calculate_size(last_line)
            return last_line

        try:
            if self.header:
                next_line = list(super(reader, self).__next__().values())
            else:
                next_line = list(list(super(reader, self).__next__().values())[0])
        except StopIteration:
            self.empty = True
            raise StopIteration

        self.bytes_in += self._calculate_size(next_line)

        if self._limit_reached():
            self.last_line = next_line
            raise StopIteration

        return next_line

    def resume(self):
        self.bytes_in = 0
