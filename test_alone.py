import alone as module
import unittest

class TestTagSpells(unittest.TestCase):
    def tag_spells(self, rows):
    	data = module.read_as_dict_of_groups(rows, group_keys=('id',))
        return list(module.tag_spells(data))

    def test_single_row_always_alone(self):
        row = dict(id=1, start_date='1991-01-01', end_date='1992-01-01')
        actual = self.tag_spells([row])
        desired = row.copy()
        desired['days_alone'] = 365
        self.assertDictEqual(actual[0], desired)

    def test_clones_never_alone(self):
        row1 = dict(id=1, start_date='1991-01-01', end_date='1991-12-31')
        row2 = dict(id=1, start_date='1991-01-01', end_date='1991-12-31')
        actual = self.tag_spells([row1, row2])
        desired = [row1.copy(), row2.copy()]
        desired[0]['days_alone'] = 0
        desired[1]['days_alone'] = 0
        self.assertListEqual(actual, desired)

    def test_partial_overlap(self):
        row1 = dict(id=1, start_date='1991-01-01', end_date='1991-01-31')
        row2 = dict(id=1, start_date='1991-01-15', end_date='1991-02-28')
        actual = self.tag_spells([row1.copy(), row2.copy()])
        desired = [row1, row2]
        desired[0]['days_alone'] = 14
        desired[1]['days_alone'] = 28
        self.assertListEqual(actual, desired)

    def test_three_spells(self):
        row1 = dict(id=1, start_date='1991-01-01', end_date='1991-01-15')
        row2 = dict(id=1, start_date='1991-01-10', end_date='1991-01-31')
        row3 = dict(id=1, start_date='1991-01-05', end_date='1991-01-20')
        actual = self.tag_spells([row1.copy(), row2.copy(), row3.copy()])
        desired = [row1, row2, row3]
        desired[0]['days_alone'] = 4
        desired[1]['days_alone'] = 11
        desired[2]['days_alone'] = 0
        self.assertListEqual(actual, desired)

    def test_clones_alone_in_different_groups(self):
        row1 = dict(id=2, start_date='1991-01-01', end_date='1991-12-31')
        row2 = dict(id=1, start_date='1991-01-01', end_date='1991-12-31')
        actual = self.tag_spells([row1, row2])
        desired = [row1.copy(), row2.copy()]
        desired[0]['days_alone'] = 364
        desired[1]['days_alone'] = 364
        self.assertListEqual(actual, desired)

if __name__ == '__main__':
    unittest.main()
