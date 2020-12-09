import unittest

from sorted_set import SortedSet


class TestConstruction(unittest.TestCase):
    def test_empty(self):
        s = SortedSet([])

    def test_with_duplicate(self):
        s = SortedSet([8, 8, 7])

    def test_from_iterable(self):
        def gen123():
            yield 1
            yield 2
            yield 3

        g = gen123()
        s = SortedSet(g)

    def test_default_empty(self):
        s = SortedSet()


class TestContainerProtocol(unittest.TestCase):

    def setUp(self):
        self.s = SortedSet([6, 7, 3, 9])

    def test_positive_test_contained(self):
        self.assertTrue(6 in self.s)

    def test_negative_test_contained(self):
        self.assertFalse(5 in self.s)

    def test_positive_not_contained(self):
        self.assertTrue(5 not in self.s)

    def test_negative_not_contained(self):
        self.assertFalse(9 not in self.s)


class TestSizedProtocol(unittest.TestCase):

    def test_empty(self):
        s = SortedSet()
        self.assertEqual(len(s), 0)

    def test_one(self):
        s = SortedSet([32])
        self.assertEqual(len(s), 1)

    def test_ten(self):
        s = SortedSet(range(10))
        self.assertEqual(len(s), 10)

    def test_with_duplicates(self):
        s = SortedSet([5, 5, 3])
        self.assertEqual(len(s), 2)


class TestIterableProtocol(unittest.TestCase):

    def setUp(self):
        self.s = SortedSet([7, 2, 1, 1, 9])

    def test_iter(self):
        i = iter(self.s)
        self.assertEqual(next(i), 1)
        self.assertEqual(next(i), 2)
        self.assertEqual(next(i), 7)
        self.assertEqual(next(i), 9)
        self.assertRaises(StopIteration, lambda: next(i))

    def test_for_loop(self):
        index = 0
        expected = [1, 2, 7, 9]
        for item in self.s:
            self.assertEqual(item, expected[index])
            index += 1


class TestSequenceProtocol(unittest.TestCase):

    def setUp(self):
        self.s = SortedSet([1, 4, 9, 13, 15])

    def test_index_zero(self):
        self.assertEqual(self.s[0], 1)

    def test_index_one_beyond_the_end(self):
        with self.assertRaises(IndexError):
            self.s[5]

    def test_minus_one(self):
        self.assertEqual(self.s[-1], 15)

    def test_minus_five(self):
        self.assertEqual(self.s[-5], 1)

    def test_slice_from_start(self):
        self.assertEqual(self.s[:3], SortedSet([1, 4, 9]))

    def test_slice_to_end(self):
        self.assertEqual(self.s[3:], SortedSet([13, 15]))

    def test_empty_slice(self):
        self.assertEqual(self.s[7:], SortedSet())

    def test_slice_arbitrary(self):
        self.assertEqual(self.s[2:4], SortedSet([9, 13]))

    def test_slice_full(self):
        self.assertEqual(self.s[:], self.s)

    def test_reversed(self):
        s = SortedSet([3, 5, 7, 9])
        r = reversed(s)
        self.assertEqual(next(r), 9)
        self.assertEqual(next(r), 7)
        self.assertEqual(next(r), 5)
        self.assertEqual(next(r), 3)
        self.assertRaises(StopIteration, lambda: next(r))
        # with self.assertRaises(StopIteration):
        #    next(r)

    def test_index_positive(self):
        s = SortedSet([7, 14, 22, 23])
        self.assertEqual(s.index(22), 2)

    def test_index_negative(self):
        s = SortedSet([7, 14, 22, 23])
        with self.assertRaises(ValueError):
            s.index(15)

    def test_count_zero(self):
        s = SortedSet([7, 14, 22, 23, 7])
        self.assertEqual(s.count(20), 0)

    def test_count_one(self):
        s = SortedSet([7, 14, 22, 23, 7])
        self.assertEqual(s.count(7), 1)

    def test_concatenating_disjoint(self):
        s = SortedSet([1, 2, 3])
        t = SortedSet([4, 5, 6])
        self.assertEqual(s+t, SortedSet([1, 2, 3, 4, 5, 6]))

    def test_concatenating_equal(self):
        s = SortedSet([1, 2,  3])
        self.assertEqual(s+s, s)

    def test_concatenating_intersecting(self):
        s = SortedSet([1, 2, 3])
        t = SortedSet([3, 4, 5])
        self.assertEqual(s+t, SortedSet([1, 2, 3, 4, 5]))

    def test_repetition_zero_right(self):
        s = SortedSet([1, 2, 3])
        self.assertEqual(s * 0, SortedSet())

    def test_repetition_nonzero_right(self):
        s = SortedSet([1, 2, 3])
        self.assertEqual(s * 99, s)

    def test_repetition_zero_left(self):
        s = SortedSet([1, 2, 3])
        self.assertEqual(0 * s, SortedSet())

    def test_repetition_nonzero_left(self):
        s = SortedSet([1, 2, 3])
        self.assertEqual(99 * s, s)


class TestReprProtocol(unittest.TestCase):

    def test_repr_empty(self):
        s = SortedSet()
        self.assertEqual(repr(s), "SortedSet()")

    def test_repr_some(self):
        s = SortedSet([42, 12, 38])
        self.assertEqual(repr(s), "SortedSet([12, 38, 42])")


class TestEqualityProtocol(unittest.TestCase):

    def test_positive_equals(self):
        self.assertTrue(SortedSet([1, 2, 3]) == SortedSet([3, 1, 2]))

    def test_negative_equals(self):
        self.assertFalse(SortedSet([1, 2, 3]) == SortedSet([6, 5, 4]))

    def test_type_mismatch(self):
        self.assertFalse(SortedSet([1, 2, 3]) == [1, 2, 3])

    def test_identical(self):
        s = SortedSet([1, 2, 3])
        self.assertTrue(s == s)


class TestInequalityProtocol(unittest.TestCase):

    def test_positive_unequals(self):
        self.assertFalse(SortedSet([1, 2, 3]) != SortedSet([3, 1, 2]))

    def test_negative_unequals(self):
        self.assertTrue(SortedSet([1, 2, 3]) != SortedSet([6, 5, 4]))

    def test_type_mismatch(self):
        self.assertTrue(SortedSet([1, 2, 3]) != [1, 2, 3])

    def test_identical(self):
        s = SortedSet([1, 2, 3])
        self.assertFalse(s != s)


class TestRelationalSetProtocol(unittest.TestCase):

    def test_lt_positive(self):  # lt for proper subset
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s < t)

    def test_lt_negative(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2, 3})
        self.assertFalse(s < t)

    def test_le_lt_positive(self):  # le for subset
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s <= t)

    def test_le_eq_positive(self):  # eq for equal
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s <= t)

    def test_le_negative(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2})
        self.assertFalse(s <= t)

    def test_gt_positive(self):  # gt for proper superset
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2})
        self.assertTrue(s > t)

    def test_gt_negative(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertFalse(s > t)

    def test_ge_gt_positive(self):  # ge for superset
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2})
        self.assertTrue(s > t)

    def test_ge_eq_positive(self):  # gt for superset
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s >= t)

    def test_ge_negative(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertFalse(s >= t)


class TestSetRelationMethod(unittest.TestCase):

    def test_issubset_proper_positive(self):
        s = SortedSet({1, 2})
        t = [1, 2, 3]
        self.assertTrue(s.issubset(t))

    def test_issubset_positive(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2, 3]
        self.assertTrue(s.issubset(t))

    def test_issubset_negative(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2]
        self.assertFalse(s.issubset(t))

    def test_issuperset_proper_positive(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2]
        self.assertTrue(s.issuperset(t))

    def test_issuperset_positive(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2, 3]
        self.assertTrue(s.issuperset(t))

    def test_issuperset_negative(self):
        s = SortedSet({1, 2})
        t = [1, 2, 3]
        self.assertFalse(s.issuperset(t))