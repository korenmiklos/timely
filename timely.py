from datetime import datetime, timedelta
from dateutil.parser import parse
from shapely.geometry import Point, LineString

def coerce(what):
	'''
	Coerces 'what' into a datetime.
	'''
	if isinstance(what, datetime):
		return what
	if isinstance(what, basestring):
		return parse(what)

class TimelyObject(object):
	# properties
	# properties
	@property
	def length(self):
		return self.end.datetime-self.beginning.datetime

	@property
	def bounds(self):
		return (self.beginning, self.end)

	@property 
	def is_empty(self):
		return False

	# binary relations
	# pythonic style
	def __eq__(self, other):
		return self.equals(other)

	def __le__(self, other):
		return self.bounds[1].datetime<=other.bounds[0].datetime

	def __ge__(self, other):
		return self.bounds[0].datetime>=other.bounds[1].datetime

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

	def __nonzero__(self, other):
		return not self.is_empty

	def __len__(self, other):
		raise NotImplementedError

	def __iter__(self, other):
		raise NotImplementedError

	# shapely style
	def equals(self, other):
		raise NotImplementedError

	def contains(self, other):
		return self.union(other).equals(self)

	def disjoint(self, other):
		return self.intersection(other).is_empty

	def intersects(self, other):
		return not self.disjoint(other)

	def distance(self, other):
		raise NotImplementedError

	# binary operators
	def difference(self, other):
		raise NotImplementedError

	def intersection(self, other):
		return other.intersection(self)

	def union(self, other):
		return other.union(self)

	# unary constructors
	@property
	def envelope(self):
		return shape_to_time(self.time_geometry.envelope)

	def offset(self, difference):
		raise NotImplementedError

	# string representation
	def __unicode__(self):
		raise NotImplementedError

class Empty(TimelyObject):
	pass

class Instant(TimelyObject):
	def __init__(self, what, BOT=False, EOT=False, empty=False):
		assert not (BOT and EOT)
		if not BOT or EOT or empty:
			self.datetime = coerce(what)
		self.BOT = BOT
		self.EOT = EOT

	@property
	def length(self):
		return timedelta(0)

	@property
	def bounds(self):
		return (self, self)

	def equals(self, other):
		if not isinstance(other, Instant):
			return False
		if self.BOT:
			return other.BOT
		if self.EOT:
			return other.EOT
		return self.datetime==other.datetime

	def distance(self, other):
		raise NotImplementedError

	# binary operators
	def difference(self, other):
		raise NotImplementedError

	def intersection(self, other):
		if isinstance(other, Instant):
			if self.equals(other):
				return self
			else:
				return EMPTY
		elif isinstance(other, Interval):
			if (self>=other.beginning) and (self<=other.end):
				return self
			else:
				return Empty()

class Interval(TimelyObject):
	def __init__(self, what):
		if isinstance(what, basestring):
			(b, e) = what.split('/')
		else:
			(b, e) = what
		self.beginning = Instant(b)
		self.end = Instant(e)

	def split(self):
		pass

	@property
	def length(self):
		return self.end.datetime-self.beginning.datetime

	def equals(self, other):
		if not isinstance(other, Interval):
			return False
		return (self.beginning==other.beginning) and (self.end==other.end)

	def distance(self, other):
		raise NotImplementedError

	# binary operators
	def difference(self, other):
		raise NotImplementedError

	def intersection(self, other):
		if isinstance(other, Instant):
			return other.intersection(self)
		elif isinstance(other, Interval):
			b = max(self.beginning, other.beginning)
			e = min(self.end, other.end)
			if e>=b:
				return Interval((b,e))
			else:
				return Empty()

	def union(self, other):
		if isinstance(other, Instant):
			if self.intersects(other):
				return self
		if isinstance(other, Interval):
			if self.intersects(other):
				b = min(self.beginning, other.beginning)
				e = max(self.end, other.end)
				return Interval((b,e))


class MultiInstant(TimelyObject):
	pass

class MultiInterval(TimelyObject):
	pass

# beginning and end of time
BOT = Instant('', BOT=True)
EOT = Instant('', EOT=True)
EMPTY = Instant('', empty=True)

