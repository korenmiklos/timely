from datetime import datetime, timedelta
from dateutil.parser import parse
from shapely.geometry import Point, LineString, MultiLineString
from shapely.ops import linemerge

ORIGIN = datetime.fromordinal(1)
_BOT = ORIGIN
_EOT = datetime(9999,12,31)

def coerce(what):
	'''
	Coerces 'what' into a date.
	'''
	if isinstance(what, Instant):
		return what.datetime
	if isinstance(what, datetime):
		return what
	if isinstance(what, basestring):
		return parse(what)

def simplify(shape):
	if isinstance(shape, MultiLineString):
		return linemerge(shape)
	return shape

def shape_as_time(shape):
	simple = simplify(shape)
	if isinstance(simple, Point):
		t = ORIGIN+x_as_timedelta(shape.x)
		return Instant(t)
	if isinstance(simple, LineString):
		(x1, _, x2, __) = shape.bounds
		t1 = ORIGIN+x_as_timedelta(x1)
		t2 = ORIGIN+x_as_timedelta(x2)
		return Interval((t1, t2))
	if isinstance(shape, MultiLineString):
		return MultiInterval([shape_as_time(segment) for segment in shape.geoms])
	return Instant('', empty=True)

def time_as_shape(timelyobject):
	if isinstance(timelyobject, Instant):
		if timelyobject.is_empty:
			return Point()
		x = timedelta_as_x(timelyobject.datetime-ORIGIN)
		return Point((x, 0))
	if isinstance(timelyobject, Interval):
		if timelyobject.is_empty:
			return LineString()
		x1 = timedelta_as_x(timelyobject.beginning.datetime-ORIGIN)
		x2 = timedelta_as_x(timelyobject.end.datetime-ORIGIN)
		return LineString([(x1, 0), (x2, 0)])
	if isinstance(timelyobject, MultiInterval):
		if timelyobject.is_empty:
			return MultiLineString()
		return MultiLineString([time_as_shape(interval) for interval in timelyobject.intervals])
	return Point()

def timedelta_as_x(t):
	# time is measured in days
	return float(t.days)

def x_as_timedelta(x):
	return timedelta(days=x)

class TimelyObject(object):
	# properties
	# properties
	@property
	def length(self):
		return x_as_timedelta(time_as_shape(self).length)

	@property
	def bounds(self):
		raise NotImplementedError

	# binary relations
	# pythonic style
	def __eq__(self, other):
		return self.equals(other)

	def __le__(self, other):
		return self.bounds[1]<=other.bounds[0]

	def __ge__(self, other):
		return self.bounds[0]>=other.bounds[1]

	def __add__(self, other):
		return self.union(other)

	def __sub__(self, other):
		return self.difference(other)

	def __mul__(self, other):
		return self.intersection(other)

	def __contains__(self, other):
		return self.contains(other)

	def __and__(self, other):
		return self.intersection(other)

	def __or__(self, other):
		return self.union(other)

	def __nonzero__(self):
		return not self.is_empty

	def __len__(self, other):
		raise NotImplementedError

	def __iter__(self, other):
		raise NotImplementedError

	# shapely style
	def equals(self, other):
		return time_as_shape(self).equals(time_as_shape(other))

	def contains(self, other):
		return time_as_shape(self).contains(time_as_shape(other))

	def disjoint(self, other):
		return time_as_shape(self).disjoint(time_as_shape(other))

	def intersects(self, other):
		return time_as_shape(self).intersects(time_as_shape(other))

	def distance(self, other):
		return x_as_timedelta(time_as_shape(self).distance(time_as_shape(other)))

	# binary operators
	def difference(self, other):
		return shape_as_time(time_as_shape(self).difference(time_as_shape(other)))

	def intersection(self, other):
		return shape_as_time(time_as_shape(self).intersection(time_as_shape(other)))

	def union(self, other):
		return shape_as_time(time_as_shape(self).union(time_as_shape(other)))

	# unary constructors
	def offset(self, difference):
		raise NotImplementedError

	# string representation
	def __unicode__(self):
		raise NotImplementedError

	def __str__(self):
		return unicode(self)

class Instant(TimelyObject):
	def __init__(self, what, BOT=False, EOT=False, empty=False):
		assert not (BOT and EOT)
		if not (not what or BOT or EOT or empty):
			self.datetime = coerce(what)
		else:
			if BOT or empty:
				self.datetime = _BOT
			if EOT:
				self.datetime = _EOT
		self.BOT = BOT
		self.EOT = EOT
		self.is_empty = empty or (not what and not (BOT or EOT))

	def __unicode__(self):
		if not self.is_empty:
			return self.datetime.isoformat()
		else:
			return 'Empty Instant'

	@property
	def bounds(self):
		return (self, self)

	def __le__(self, other):
		return self.BOT or other.EOT or (self.is_empty and other.is_empty) or (self.datetime<=other.datetime)

	def __ge__(self, other):
		return other<=self


class Interval(TimelyObject):
	def __init__(self, what, empty=False):
		if empty:
			self.is_empty = True
		else:
			self.is_empty = empty
			if isinstance(what, basestring):
				(b, e) = what.split('/')
			else:
				(b, e) = what
			self.beginning = Instant(b)
			self.end = Instant(e)
			if self.end<=self.beginning:
				self.is_empty = True
			if self.beginning.is_empty:
				self.beginning = Instant('', BOT=True)
			if self.end.is_empty:
				self.end = Instant('', EOT=True)

	def __unicode__(self):
		if not self.is_empty:
			return u'%s/%s' % (unicode(self.beginning), unicode(self.end))
		else:
			return 'Empty Interval'

	@property
	def bounds(self):
		return (self.beginning, self.end)

	def split(self, instant):
		if instant in self:
			(b, e) = self.bounds
			x = instant
			return MultiInterval([Interval((b, x)), Interval((x, e))])
		return self

class MultiInstant(TimelyObject):
	pass

class MultiInterval(TimelyObject):
	def __init__(self, list_of_intervals, empty=False):
		if empty:
			self.is_empty = True
		else:
			self.is_empty = empty
			self.intervals = list_of_intervals

	def __unicode__(self):
		if not self.is_empty:
			return u','.join([unicode(i) for i in self.intervals])
		else:
			return 'Empty MultiInterval'

	@property
	def bounds(self):
		b = min([i.beginning for i in self.intervals])
		e = max([i.end for i in self.intervals])
		return (b, e)

