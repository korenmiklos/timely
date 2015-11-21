from datetime import datetime
from timely import Interval, MultiInterval
import csv
import sys

START_DATE = 'start_date'
END_DATE = 'end_date'
GROUP_KEYS = ('frame_id',)

def extract_group_keys(row, group_keys):
	return tuple([row[key] for key in group_keys])

def read_as_dict_of_groups(input_rows, group_keys=GROUP_KEYS):
	output = {}
	for row in input_rows:
		key = extract_group_keys(row, group_keys)
		if key not in output:
			output[key] = []
		row['_spell'] = Interval((row[START_DATE], row[END_DATE]))
		output[key].append(row)
	return output

def days_alone(interval, list_of_intervals):
	other_intervals = list_of_intervals[:]
	other_intervals.remove(interval)
	mi = MultiInterval(other_intervals)
	return interval.difference(mi).length.days

def tag_spells(data):
	for group in data.keys():
		list_of_intervals = [item['_spell'] for item in data[group]]
		for item in data[group]:
			item['days_alone'] = days_alone(item['_spell'], list_of_intervals)
			del item['_spell']
			yield item

def main():
    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=list(reader.fieldnames) + ['days_alone'])
    writer.writeheader()
    writer.writerows(tag_spells(read_as_dict_of_groups(reader)))

if __name__ == '__main__':
    main()

