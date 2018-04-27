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

description = r'''
Calculate the arithmetic average of all values in a given single
column.
'''


datasets = ('source',)

options = dict(
	column = 'name',
)

def analysis(sliceno):
	s = 0
	for data in datasets.source.iterate_chain(sliceno, options.column):
		s += data
	return s

def synthesis(analysis_res):
	s = analysis_res.merge_auto()

	# iterate_chain may iterate several datasets, so just
	# sum(datasets.source.lines) is not correct.
	n = sum(sum(x.lines) for x in datasets.source.chain())

	return (s, n)
