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

from collections import Counter

options = dict(
	colname=str,
)
datasets = ('source',)

def analysis(sliceno):
	return Counter(int(round(num * 4)) for num in datasets.source.iterate_chain(sliceno, options.colname))

def synthesis(analysis_res):
	c = analysis_res.merge_auto()
	div = (max(c.values()) - min(c.values())) / 60
	for k, v in sorted(c.items()):
		print("%5d: %s" % (k, "*" * int(v / div + 0.5)))
	return c
