from itertools import islice


LF = "\n"
CRLF = "\r\n"


def count_lines(text: str) -> int:
    lf_count = text.count(LF)
    crlf_count = text.count(CRLF)
    return lf_count + crlf_count + 1


class BatchTextFileReader:
    def __init__(
        self,
        file_path: str,
        batch_size: int,
    ):
        self._file_path = file_path
        self._batch_size = batch_size

    def __enter__(self):
        self._fd = open(self._file_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._fd.close()

    def next(self) -> str:
        batch = []
        for i in range(0, self._batch_size):
            line = self._fd.readline()

            if str.isspace(line):
                continue

            if line is None:
                print("End reader")
                return ''.join(batch)

            batch.append(line)

        return ''.join(batch)


class TextSplitter:
    def __init__(
        self,
        text: str,
        batch_size: int,
    ):
        self._text = text
        self._batch_size = batch_size

    def batch(self):
        lines = self._text.splitlines(keepends=True)
        iterator = iter(lines)

        return [
            ''.join(batch)
            for batch in iter(
                lambda: list(islice(iterator, self._batch_size)),
                [],
            )
        ]
