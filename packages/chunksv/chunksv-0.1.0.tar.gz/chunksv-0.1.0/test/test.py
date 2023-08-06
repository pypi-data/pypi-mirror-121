import chunksv
import csv
import unittest
import os
import shutil


class TestChunksv(unittest.TestCase):

    fixtures_dir = f"{os.path.dirname(os.path.realpath(__file__))}/fixtures/"
    output_dir = f"{os.path.dirname(os.path.realpath(__file__))}/out/"

    def setUp(self):

        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

    def tearDown(self):

        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def _compare_row_count(self, fname: str, target_count: int):

        with open(f"{self.output_dir}/{fname}", "r") as f:
            return len(f.readlines()) == target_count

    def _compare_output(self, fname: str, num_parts: int, target_row_counts: list):

        self.assertTrue(
            all([os.path.isfile(f"{self.output_dir}/{fname}.{i}.part.csv") for i in range(num_parts)])
        )
        self.assertTrue(
            all([self._compare_row_count(f"{fname}.{i}.part.csv", target_row_counts[i]) for i in range(num_parts)])
        )

    def _split_file(self, fname: str, max_bytes=None, header: [list, None] = None):

        with open(f"{self.fixtures_dir}/{fname}.csv", "r") as f:
            f = chunksv.reader(f, max_bytes=max_bytes, header=header)

            if header is not None:
                next(f)

            if max_bytes is not None:

                i = 0
                while not f.empty:
                    with open(f"{self.output_dir}/{fname}.{i}.part.csv", "w") as of:
                        of = csv.writer(of)

                        if header is not None:
                            of.writerow(header)
                        of.writerows([r for r in f])

                    i += 1
                    f.resume()

            else:
                with open(f"{self.output_dir}/{fname}.csv", "w") as of:
                    of = csv.writer(of)
                    of.writerows([[header]] if header is not None else [] + [r for r in f])

    def test_file_one_split(self):

        self._split_file("file_one", 1024, ["a", "b"])
        self._compare_output("file_one", 7, [16, 16, 16, 16, 16, 16, 10])

        self._split_file("file_one", 1024)
        self._compare_output("file_one", 7, [16, 15, 15, 15, 15, 15, 9])

        self._split_file("file_one", 2048, ["a", "b"])
        self._compare_output("file_one", 4, [32, 32, 32, 7])

        self._split_file("file_one", 2048)
        self._compare_output("file_one", 4, [32, 31, 31, 6])

    def test_file_two_split(self):

        self._split_file("file_two", 512, ["a"])
        self._compare_output("file_two", 4, [25, 25, 27, 26])

        self._split_file("file_two", 512)
        self._compare_output("file_two", 4, [25, 24, 26, 25])

        self._split_file("file_two", 1024, ["a"])
        self._compare_output("file_two", 2, [49, 52])

        self._split_file("file_two", 1024)
        self._compare_output("file_two", 2, [49, 51])



