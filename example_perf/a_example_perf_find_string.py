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

datasets=('source',)

options=dict(colname='a string', text='ebay')

def analysis(sliceno):
	text = options.text # faster if dict lookup is outside of the loop
	c = 0
	for x in datasets.source.iterate_chain(sliceno, options.colname):
		if text in x:
			c += 1
	return c

def synthesis(analysis_res):
	c = analysis_res.merge_auto()
	return c
