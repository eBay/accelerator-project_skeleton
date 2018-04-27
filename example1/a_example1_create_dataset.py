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

from random import uniform, randint, seed

from dataset import DatasetWriter

description = r'''
Write a dataset containing two columns:
  'rflt', which is uniformly distributed between 0 and 1 (a float), and
  'rint', which is an integer uniformly distributed between
          options.randint_low and options.randint_high.
          For details, see help(random).

The random seed may be passed through an option.  This ensures
determinism, and can also be used to create several datasets with
different "random" contents.

The total number of rows written is
  slices * floor(options.approx_rows / slices)
'''


datasets = ('previous',)

options = dict(
	seed=37,
	approx_rows=10000,  # actual number of rows will be a multiple of the number of slices
	randint_low = -1000,
	randint_high = 1000,
)

def prepare():
	dw = DatasetWriter(previous=datasets.previous)
	dw.add('rflt', 'float64')
	dw.add('rint', 'int64')
	return dw

def analysis(sliceno, prepare_res, params):
	seed(options.seed*params.slices + sliceno) # random generator starting point
	dw = prepare_res
	for n in range(0, options.approx_rows // params.slices):
		dw.write(uniform(0, 1), randint(options.randint_low, options.randint_high))
