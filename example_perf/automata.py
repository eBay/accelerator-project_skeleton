############################################################################
#                                                                          #
# Copyright (c) 2018 eBay Inc.                                             #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#  http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
#                                                                          #
############################################################################

from locale import resetlocale

from extras import resolve_jobid_filename
from extras import job_params
import blob

def main(urd):
	resetlocale()

	if False:
		# One BILLION rows
		# This takes about half an hour on a fast machine
		num_rows = int(1e7)
		num_datasets = 100
	else:
		# One MILLION rows
		num_rows = int(1e6)
		num_datasets = 10

	# Create datasets
	print("\x1b[1m(1) Create chain of datasets.\x1b[m")
	jid = None
	for _ in range(num_datasets):
		jid = urd.build('example_perf_gendata', options=dict(num_rows=num_rows), datasets=dict(previous=jid))

	# Export chain of datasets to CSV-file.
	print("\x1b[1m(2) Export dataset chain to CSV file.\x1b[m")
	jid = urd.build('csvexport', datasets=dict(source=jid), options=dict(filename='out.csv.gz', chain_source=True))

	filename = resolve_jobid_filename(jid, 'out.csv.gz')
	print('Exported file stored in \"%s\"' % (filename,))

	# Import and type previously exported CSV-file.
	print("\x1b[1m(3) Import dataset from CVS file.\x1b[m")
	jid = urd.build('csvimport', options=dict(filename=filename))
	opts = dict(
		column2type={
			'a string': 'ascii',
			'large number': 'number',
			'small number': 'number',
			'small integer': 'int32_10', # you must specify base for integers
			'gauss number': 'number',
			'gauss float': 'float64',
		},
	)
	print("\x1b[1m(4) Type imported dataset.\x1b[m")
	jid = urd.build('dataset_type', datasets=dict(source=jid), options=opts)

	# Sum all values in a column.  Repeat for a set of columns with different types.
	print("\x1b[1m(5) Run some methods on the typed dataset.\x1b[m")
	jid_single = jid
	source = jid_single
	for colname in ('small number', 'small integer', 'large number', 'gauss number', 'gauss float'):
		print(colname)
		jid = urd.build('example_perf_sum', datasets=dict(source=source), options=dict(colname=colname), name='sum ' + colname)
		jid = urd.build('example_perf_sum_positive', datasets=dict(source=source), options=dict(colname=colname), name='sum positive ' + colname)

	# Compute histograms of a column
	print('histogram')
	jid = urd.build('example_perf_histogram', datasets=dict(source=source), options=dict(colname='gauss number'), name='histogram_number')
	jid = urd.build('example_perf_histogram', datasets=dict(source=source), options=dict(colname='gauss float'), name='histogram_float')

	# Find string
	print('find string')
	jid = urd.build('example_perf_find_string', datasets=dict(source=source), options=dict(colname='a string', text='ExAx'), name='find_string')
	print("Number of lines containing string \"%s\" is %d." %(job_params(jid).options['text'], blob.load(jobid=jid)),)

	# Print resulting profiling information
	from automata_common import profile_jobs
	print()
	def pl(text, time):
		print("%-30s %10.3f %14s" %(text, time, '{0:n}'.format(round(num_rows * num_datasets / time)),))
	print()
	print('-' * 56 )
	print("operation                       exec time         rows/s")
	print()
	pl('csvexport', profile_jobs(urd.joblist.find('csvexport')))
	print()
	pl('reimport total', profile_jobs(urd.joblist.find('csvimport') + urd.joblist.find('dataset_type')))
	pl("   csvimport         ", profile_jobs(urd.joblist.find('csvimport')))
	pl("   type              ", profile_jobs(urd.joblist.find('dataset_type')))
	print()
	print("sum")
	pl("  small number       ", profile_jobs(urd.joblist.find('sum small number')))
	pl("  small integer      ", profile_jobs(urd.joblist.find('sum small integer')))
	pl("  large number       ", profile_jobs(urd.joblist.find('sum large number')))
	pl("  gauss number       ", profile_jobs(urd.joblist.find('sum gauss number')))
	pl("  gauss float        ", profile_jobs(urd.joblist.find('sum gauss float')))
	print()
	print("sum positive")
	pl("  small number       ", profile_jobs(urd.joblist.find('sum positive small number')))
	pl("  small integer      ", profile_jobs(urd.joblist.find('sum positive small integer')))
	pl("  large number       ", profile_jobs(urd.joblist.find('sum positive large number')))
	pl("  gauss number       ", profile_jobs(urd.joblist.find('sum positive gauss number')))
	pl("  gauss float        ", profile_jobs(urd.joblist.find('sum positive gauss float')))
	print()
	print("histogram")
	pl("  number             ", profile_jobs(urd.joblist.find('histogram_number')))
	pl("  float              ", profile_jobs(urd.joblist.find('histogram_float')))
	print()
	pl("find string          ", profile_jobs(urd.joblist.find('find_string')))
	print()
	print("Total test time                %10.3f" %(profile_jobs(urd.joblist),))
	print()
	print('Example size is %s lines.' % ('{0:n}'.format(num_datasets * num_rows),))
	print('Number of slices is %d.' % (urd.info.slices,))
	print('-' * 56 )
