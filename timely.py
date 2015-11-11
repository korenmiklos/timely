from datetime import DateTime

class TimelyObject(object):
	# properties
	@property
	def length(self):
		raise NotImplementedError

	@property
	def bounds(self):
		raise NotImplementedError

	@property
	def beginning(self):
		raise NotImplementedError

	@property
	def end(self):
		raise NotImplementedError

	@property
	def timely_type(self):
		raise NotImplementedError

	@property
	def distance(self):
		raise NotImplementedError

	@property 
	def is_empty(self):
		raise NotImplementedError

	# binary relations
	def equals(self, other):
		raise NotImplementedError

	def almost_equals(self, other):
		raise NotImplementedError

	def contains(self, other):
		raise NotImplementedError

	def disjoint(self, other):
		raise NotImplementedError

	def intersects(self, other):
		raise NotImplementedError

	def touches(self, other):
		raise NotImplementedError

	def within(self, other):
		raise NotImplementedError

	# binary operators
	def difference(self, other):
		raise NotImplementedError

	def intersection(self, other):
		raise NotImplementedError

	def symmetric_difference(self, other):
		raise NotImplementedError

	def union(self, other):
		raise NotImplementedError

	# unary constructors
	def envelope(self):
		raise NotImplementedError

	def offset(self, difference):
		raise NotImplementedError

	# string representation
	def __unicode__(self):
		raise NotImplementedError

class Instant(TimelyObject):
	'''
	Represents an instant in time. Inherits from the DateTime class, 
	but may be plus or minus infinity to help define open intervals.
	'''

class Interval(TimelyObject):
	pass

class MultiInstant(TimelyObject):
	pass

class MultiInterval(TimelyObject):
	pass
