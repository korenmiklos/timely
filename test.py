import timely as module
import unittest
from datetime import timedelta
from shapely.geometry import Point, LineString

def equal(self, desired, actual):
    self.assertEqual(desired, actual, msg='\n%s\n%s' % (desired, actual))

class TestConversionFunctions(unittest.TestCase):
    def test_x_is_float(self):
        dt = timedelta(days=1)
        x = module.timedelta_as_x(dt)
        self.failUnless(isinstance(x, float))

    def test_dt_is_timedelta(self):
        self.failUnless(isinstance(module.x_as_timedelta(1.0), timedelta))

    def test_known_valuues(self):
        dt = timedelta(days=1)
        x = module.timedelta_as_x(dt)
        self.assertEqual(x, 1.0)

    def test_invertible(self):
        for x in [1.0,2.0,3.0]:
            self.assertEqual(module.timedelta_as_x(module.x_as_timedelta(x)), x)

    def test_instant_becomes_point(self):
        t = module.Instant('1996-01-12')
        self.assertEqual(module.time_as_shape(t).geom_type, 'Point')

    def test_point_becomes_instant(self):
        t = module.Instant('1996-01-12')
        x = module.time_as_shape(t)
        desired = t
        actual = module.shape_as_time(x)
        equal(self, desired, actual)

class TestInstant(unittest.TestCase):
    def test_create_from_datetime(self):
        pass

    def test_create_from_string(self):
        instant = module.Instant('1996-01-01')
        self.failUnless(isinstance(instant, module.Instant))

    def test_empty_string(self):
        instant = module.Instant('')
        self.failUnless(isinstance(instant, module.Instant))

    def test_string_is_8601(self):
        instant = module.Instant('2007-04-05')
        self.assertEqual(unicode(instant), u'2007-04-05T00:00:00')

class TestInterval(unittest.TestCase):
    def test_create_from_instants(self):
        instant1 = module.Instant('1996-01-01')
        instant2 = module.Instant('1996-01-03')
        interval = module.Interval((instant1, instant2))
        self.failUnless(isinstance(interval, module.Interval))

    def test_create_from_datetimes(self):
        pass

    def test_create_from_strings(self):
        interval = module.Interval(('1996-01-01', '1996-01-03'))
        self.failUnless(isinstance(interval, module.Interval))

    def test_reverse_interval_empty(self):
        interval = module.Interval(('1998-01-01', '1996-01-03'))
        self.failUnless(interval.is_empty)

    def test_interval_ends_midnight(self):
        interval = module.Interval(('1996-01-01', '1996-01-03'))
        desired = module.Instant('1996-01-04T00:00:00')
        self.assertEqual(interval.end, desired)

    def test_create_from_mix(self):
        instant1 = module.Instant('1996-01-01')
        interval = module.Interval((instant1, '1996-01-03'))
        self.failUnless(isinstance(interval, module.Interval))

    def test_beginning_is_instant(self):
        instant1 = module.Instant('1996-01-01')
        instant2 = module.Instant('1996-01-03')
        interval = module.Interval((instant1, instant2))
        self.assertEqual(interval.beginning, instant1)

    def test_end_is_instant(self):
        instant1 = module.Instant('1996-01-01')
        instant2 = module.Instant('1996-01-03')
        interval = module.Interval((instant1, instant2))
        self.assertEqual(interval.end, instant2)

    def test_beginning_is_open(self):
        interval = module.Interval(('', '1996-01-03'))
        self.failUnless(interval.beginning.BOT)

    def test_end_is_open(self):
        interval = module.Interval(('1996-01-03', ''))
        self.failUnless(interval.end.EOT)

    def test_string_is_iso8601(self):
        interval = module.Interval(('2007-03-01T13:00:00', '2008-05-11T15:30:00'))
        self.assertEqual(unicode(interval), u'2007-03-01T13:00:00/2008-05-11T15:30:00')

class TestMultiInstant(unittest.TestCase):
    pass

class TestMultiInterval(unittest.TestCase):
    def test_create_from_intervals(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-02', '1996-01-08'))
        actual = module.MultiInterval([interval1, interval2])
        self.failUnless(isinstance(actual, module.MultiInterval))

    def test_bounds(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-02', '1996-01-08'))
        actual = module.MultiInterval([interval1, interval2]).bounds
        desired = (interval1.beginning, interval2.end)
        equal(self, desired, actual)

class TestInstantRelation(unittest.TestCase):
    def test_instant_equal(self):
        instant1 = module.Instant('1996-01-01')
        instant2 = module.Instant('1996-01-01')
        self.assertEqual(instant1, instant2)

    def test_instant_greater(self):
        instant1 = module.Instant('1996-01-01')
        instant2 = module.Instant('1996-01-03')
        self.failUnless(instant2 >= instant1, msg='%s/%s' % (instant1, instant2))

    def test_beginningoftime_smaller(self):
        instant1 = module.Instant('', BOT=True)
        instant2 = module.Instant('1996-01-03')
        self.failUnless(instant2 >= instant1)

    def test_endoftime_bigger(self):
        instant1 = module.Instant('', EOT=True)
        instant2 = module.Instant('1996-01-03')
        self.failUnless(instant2 <= instant1)

class TestIntervalRelation(unittest.TestCase):
    def test_interval_equal(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-01', '1996-01-03'))
        self.assertEqual(interval1, interval2)

    def test_interval_contains_instant(self):
        interval = module.Interval(('1996-01-01', '1996-01-03'))
        instant = module.Instant('1996-01-02')
        self.failUnless(instant in interval)

    def test_interval_does_not_contain_instant(self):
        interval = module.Interval(('1996-01-01', '1996-01-03'))
        instant = module.Instant('1996-01-04')
        self.failIf(instant in interval)

    def test_interval_intersects(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-02', '1996-01-08'))
        self.failUnless(interval1.intersects(interval2))
        
    def test_interval_does_not_intersect(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-07', '1996-01-08'))
        self.failIf(interval1.intersects(interval2))

    def test_interval_contains(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-08'))
        interval2 = module.Interval(('1996-01-02', '1996-01-05'))
        self.failUnless(interval2 in interval1)
        
    def test_intersects_but_does_not_contain(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-02', '1996-01-08'))
        self.failIf((interval2 in interval1) or (interval1 in interval2))

class TestMIRelation(unittest.TestCase):
    def test_multiinterval_contains_instant(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-07', '1996-01-08'))
        mi = module.MultiInterval([interval1, interval2])
        instant = module.Instant('1996-01-02')
        self.failUnless(instant in mi)

    def test_multiinterval_does_not_contain_instant(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-07', '1996-01-08'))
        mi = module.MultiInterval([interval1, interval2])
        instant = module.Instant('1996-01-05')
        self.failIf(instant in mi)
        
    def test_multiinterval_does_not_intersect_interval(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-07', '1996-01-08'))
        interval3 = module.Interval(('1996-01-04', '1996-01-06'))
        mi = module.MultiInterval([interval1, interval2])
        self.failIf(mi.intersects(interval3))
        
class TestOperation(unittest.TestCase):
    def test_interval_intersection(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-02', '1996-01-08'))
        actual = interval1.intersection(interval2)
        desired = module.Interval(('1996-01-02', '1996-01-03'))
        self.assertEqual(desired, actual, msg='\n%s\n%s' % (desired, actual))

    def test_interval_difference(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-02', '1996-01-08'))
        actual = interval1.difference(interval2)
        desired = module.Interval(('1996-01-01', '1996-01-02'))
        self.assertEqual(desired, actual, msg='\n%s\n%s' % (desired, actual))

    def test_difference_of_disjoint_intervals(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-02'))
        interval2 = module.Interval(('1996-01-03', '1996-01-08'))
        actual = interval1.difference(interval2)
        desired = interval1
        self.assertEqual(desired, actual, msg='\n%s\n%s' % (desired, actual))

    def test_difference_of_equal_intervals(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-02'))
        actual = interval1.difference(interval1)
        self.failUnless(actual.is_empty, msg=actual)

    def test_interval_union(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-03'))
        interval2 = module.Interval(('1996-01-02', '1996-01-08'))
        actual = interval1.union(interval2)
        desired = module.Interval(('1996-01-01', '1996-01-08'))
        self.assertEqual(desired, actual, msg='\n%s\n%s\n%s' % (desired, actual, module.time_as_shape(actual)))

    def test_union_is_the_larger(self):
        interval1 = module.Interval(('1996-01-01', '1996-01-08'))
        interval2 = module.Interval(('1996-01-02', '1996-01-03'))
        self.assertEqual(interval1.union(interval2), interval1)

    def test_interval_split(self):
        interval = module.Interval(('1996-01-01', '1996-01-03'))
        instant = module.Instant('1996-01-02')
        desired1 = module.Interval(('1996-01-01', '1996-01-02'))
        desired2 = module.Interval(('1996-01-02', '1996-01-03'))
        actual = interval.split(instant)
        equal(self, module.MultiInterval([desired1, desired2]), actual)

if __name__ == '__main__':
    unittest.main()