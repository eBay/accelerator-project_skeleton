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

from dataset import Dataset
from jobid import resolve_jobid_filename
import blob

def main(urd):

	# Example 1.  Create a chain of datasets containing random data.
	jid_prev = None
	for n in range(5):
		jid_ds = urd.build('example1_create_dataset',
			datasets=dict(previous=jid_prev),
			options=dict(approx_rows=100000, seed=n),
			name='Created_number_%s' % (n,),
		)
		jid_prev = jid_ds

	# Example 2.  Export the last dataset in the chain to a tab
	#             separated textfile.
	jid_exp = urd.build('csvexport',
		datasets=dict(source=jid_ds),
		options=dict(filename='random.tsv', separator='\t'),
	)
	filename = resolve_jobid_filename(jid_exp, 'random.tsv')
	print('Exported file stored in \"%s\"' % (filename,))

	# Example 3.  Import the tab separated textfile and type it
	jid_imp = urd.build('csvimport',
		options=dict(filename=filename, separator='\t', labelsonfirstline=True),
	)
	jid_typ = urd.build('dataset_type',
		datasets=dict(source=jid_imp),
		options=dict(column2type=dict(rflt='number', rint='number')),
	)

	# Example 4.  Run a method computing the average of a column, in a
	#             loop, one column at a time.  The column name is an
	#             input parameter.
	for column in Dataset(jid_typ).columns:
		jid_avg = urd.build('example1_calc_average',
			datasets=dict(source=jid_typ),
			options=dict(column=column),
		)
		(s, n) = blob.load(jobid=jid_avg)
		print("Column %s:  sum=%f, length=%d, average=%f" % (column, s, n, s/n))

	# Example 5.  Create a new column that is the product of two
	#             existing columns.
	jid_add = urd.build('example1_add_column',
		datasets=dict(source=jid_typ),
	)

	# Example 6.  Export a dataset with named columns in specified
	#             order.
	jid_add_exp = urd.build('csvexport',
		datasets=dict(source=jid_add),
		options=dict(filename='prod.csv', labels=('prod', 'rflt', 'rint',)),
	)


	print(urd.joblist.pretty)
