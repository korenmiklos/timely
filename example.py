import timely

start_date = timely.Instant('1996-01-01')
end_date = timely.Instant('1996-12-31') # watch for time within day?
year_1996 = timely.Interval((start_date, end_date))

worker_spell = timely.Interval(('1996-11-01', '2009-06-30'))
period_worked_in_1996 = worker_spell.intersection(year_1996)
worker_joined_in_1996 = worker_spell.beginning in year_1996

other_worker_spell = timely.Interval(('2007-01-01', '')) # open spell
two_workers_overlapped = worker_spell.intersects(other_worker_spell)

sample_period = timely.MultiInterval([year_1996, worker_spell, other_worker_spell]).envelope
# = Interval(('1996-01-01', ''))

# A more advanced example. Count the number of workers at the firm over time.
worker_spells = [worker_spell, other_worker_spell]
sample_period = timely.MultiInterval(worker_spells).envelope
events = [spell.beginning for spell in worker_spells] + [spell.end for spell in worker_spells]
segments = sample_period.split(events)

output = []
for segment in segments:
	output.append(dict(time_period=segment, number_of_workers=sum([1 for spell in worker_spells if spell.intersects(segment)])))