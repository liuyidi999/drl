import unittest

from dataset import Dataset
from numpy import array, append
from numpy.testing import assert_array_almost_equal

class TestDataset(unittest.TestCase):

    def setUp(self):
        self.raw = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.side = [ [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                      [3, 4, 5, 6, 7, 8, 9, 10, 11, 12] ]
        self.d = Dataset(self.raw, self.side)

    def generate(self, window, lookback, slide):
        self.train_examples = []
        self.train_returns = []
        self.test_examples = []
        self.test_returns = []

        self.d.reset(window=window, lookback=lookback, slide=slide)

        while(self.d.can_gen()):
            trX, trY, tsX, tsY = self.d.gen()
            self.train_examples.append(trX)
            self.train_returns.append(trY)
            self.test_examples.append(tsX)
            self.test_returns.append(tsY)

    def test_creates_training_examples(self):
        self.generate(5, 3, 4)

        self.assertEqual(2, len(self.train_examples[0]))

        assert_array_almost_equal(self.train_examples[0][0],
                append([1., 1./1, 1./2], [1./2, 1./3, 1./3, 1./4]))
        assert_array_almost_equal(self.train_examples[0][1],
                append([1., 1./2, 1./3], [1./3, 1./4, 1./4, 1./5]))

        self.assertEqual(2, len(self.train_examples[1]))

        assert_array_almost_equal(self.train_examples[1][0],
                append([1., 1./5, 1./6], [1./6, 1./7, 1./7, 1./8]))
        assert_array_almost_equal(self.train_examples[1][1],
                append([1., 1./6, 1./7], [1./7, 1./8, 1./8, 1./9]))

    def test_creates_training_returns(self):
        self.generate(5, 3, 4)

        self.assertEqual(2, len(self.train_returns[0]))
        assert_array_almost_equal(self.train_returns[0][0], 1./3)
        assert_array_almost_equal(self.train_returns[0][1], 1./4)

        self.assertEqual(2, len(self.train_returns[1]))
        assert_array_almost_equal(self.train_returns[1][0], 1./7)
        assert_array_almost_equal(self.train_returns[1][1], 1./8)

    def test_creates_testing_examples(self):
        self.generate(5, 3, 4)

        self.assertEqual(4, len(self.test_examples[0]))

        assert_array_almost_equal(self.test_examples[0][0],
                append([1., 1./3, 1./4], [1./4, 1./5, 1./5, 1./6]))
        assert_array_almost_equal(self.test_examples[0][1],
                append([1., 1./4, 1./5], [1./5, 1./6, 1./6, 1./7]))
        assert_array_almost_equal(self.test_examples[0][2],
                append([1., 1./5, 1./6], [1./6, 1./7, 1./7, 1./8]))
        assert_array_almost_equal(self.test_examples[0][3],
                append([1., 1./6, 1./7], [1./7, 1./8, 1./8, 1./9]))

        self.assertEqual(1, len(self.test_examples[1]))

        assert_array_almost_equal(self.test_examples[1][0],
                append([1., 1./7, 1./8], [1./8, 1./9, 1./9, 1./10]))

    def test_creates_testing_returns(self):
        self.generate(5, 3, 4)

        self.assertEqual(4, len(self.test_returns[0]))
        assert_array_almost_equal(self.test_returns[0][0], 1./5)
        assert_array_almost_equal(self.test_returns[0][1], 1./6)
        assert_array_almost_equal(self.test_returns[0][2], 1./7)
        assert_array_almost_equal(self.test_returns[0][3], 1./8)

        self.assertEqual(1, len(self.test_returns[1]))
        assert_array_almost_equal(self.test_returns[1][0], 1./9)

    def test_generates_with_no_ending_test_examples(self):
        self.generate(5, 3, 5)
        self.assertEqual(1, len(self.train_returns))
        self.assertEqual(1, len(self.test_returns))
    
