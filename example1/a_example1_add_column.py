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

from dataset import DatasetWriter

description = r'''
Append a new column to an input dataset by multiplting two
existing columns together.
'''

datasets = ('source',)

def prepare():
	dw = DatasetWriter(parent=datasets.source)
	dw.add('prod', 'number')  # works for float as well as int
	return dw

def analysis(sliceno, prepare_res):
	dw = prepare_res
	for x, y in datasets.source.iterate(sliceno, ('rflt', 'rint')):
		dw.write(x * y)
