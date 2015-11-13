import timely as module
import unittest

class TestInstant(unittest.TestCase):
	def test_create_from_datetime(self):
		pass

	def test_create_from_string(self):
		instant = module.Instant('1996-01-01')
		self.failUnless(isinstance(instant, module.Instant))

	def test_empty_string(self):
		instant = module.Instant('')
		self.failUnless(isinstance(instant, module.Instant))

	def test_envelope_is_self(self):
		instant = module.Instant('1996-01-01')
		self.assertEqual(instant, instant.envelope)

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

	def test_interval_ends_midnight(self):
		interval = module.Interval(('1996-01-01', '1996-01-03'))
		desired = module.Instant('1996-01-03T24:00:00')
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
		self.assertEqual(interval.beginning, module.Instant.BOT)

	def test_end_is_open(self):
		interval = module.Interval(('1996-01-03', ''))
		self.assertEqual(interval.end, module.Instant.EOT)

	def test_envelope_is_self(self):
		instant1 = module.Instant('1996-01-01')
		instant2 = module.Instant('1996-01-03')
		interval = module.Interval((instant1, instant2))
		self.assertEqual(interval.envelope, interval)

	def test_string_is_iso8601(self):
		interval = module.Interval(('2007-03-01T13:00:00', '2008-05-11T15:30:00'))
		self.assertEqual(unicode(interval), u'2007-03-01T13:00:00/2008-05-11T15:30:00')

class TestMultiInstant(unittest.TestCase):
	pass

class TestMultiInterval(unittest.TestCase):
	pass

class TestInstantRelation(unittest.TestCase):
	def test_instant_equal(self):
		instant1 = module.Instant('1996-01-01')
		instant2 = module.Instant('1996-01-01')
		self.assertEqual(instant1, instant2)

	def test_0_and_24h_are_same(self):
		instant1 = module.Instant('2007-04-05T00:00:00')
		instant2 = module.Instant('2007-04-04T24:00:00')
		self.assertEqual(instant1, instant2)

	def test_instant_greater(self):
		instant1 = module.Instant('1996-01-01')
		instant2 = module.Instant('1996-01-03')
		self.failUnless(instant2 > instant1)

	def test_beginningoftime_smaller(self):
		instant1 = module.Instant.BOT
		instant2 = module.Instant('1996-01-03')
		self.failUnless(instant2 > instant1)

	def test_endoftime_bigger(self):
		instant1 = module.Instant.EOT
		instant2 = module.Instant('1996-01-03')
		self.failUnless(instant2 < instant1)

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
		
class TestOperation(unittest.TestCase):
	def test_interval_intersection(self):
		interval1 = module.Interval(('1996-01-01', '1996-01-03'))
		interval2 = module.Interval(('1996-01-02', '1996-01-08'))
		desired = module.Interval(('1996-01-02', '1996-01-03'))
		self.assertEqual(interval1.intersection(interval2), desired)

	def test_interval_union(self):
		interval1 = module.Interval(('1996-01-01', '1996-01-03'))
		interval2 = module.Interval(('1996-01-02', '1996-01-08'))
		desired = module.Interval(('1996-01-01', '1996-01-08'))
		self.assertEqual(interval1.union(interval2), desired)

	def test_union_is_the_larger(self):
		interval1 = module.Interval(('1996-01-01', '1996-01-08'))
		interval2 = module.Interval(('1996-01-02', '1996-01-03'))
		self.assertEqual(interval1.union(interval2), interval1)

	def test_interval_split(self):
		interval = module.Interval(('1996-01-01', '1996-01-03'))
		instant = module.Instant('1996-01-02')
		desired1 = module.Interval(('1996-01-01', '1996-01-01'))
		desired2 = module.Interval(('1996-01-02', '1996-01-03'))
		self.assertEqual(interval.split(instant), module.MultiInterval([desired1, desired2]))

if __name__ == '__main__':
	unittest.main()