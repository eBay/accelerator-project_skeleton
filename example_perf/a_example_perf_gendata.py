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

description = r"""
Generates a dataset with num_rows rows, evenly split between slices
and the following columns:
	a string: a short string, stored as "ascii"
	large number: an integer evenly spread in the range [-1e20, 1e20], stored as "number"
	small number: an integer evenly spread in the range [-99, 99], stored as "number"
	small integer: the same integer as in the previous column, stored as "int32"
	gauss number: a gaussian distribution around 0 with stddev 1, stored as "number"
	gauss float: the same float as the previous column, stored as "float64"
"""

options = dict(
	num_rows=int,
)

datasets = (
	'previous',
)

def prepare():
	from dataset import DatasetWriter
	# previous allows chaining this method, should you wish to do so
	dw = DatasetWriter(previous=datasets.previous)
	dw.add('a string', 'ascii')  # ascii is not "any string", use 'unicode' for that
	dw.add('large number', 'number') # number is any (real) number, a float or int of any size
	dw.add('small number', 'number')
	dw.add('small integer', 'int32') # int32 is a signed 32 bit number
	dw.add('gauss number', 'number')
	dw.add('gauss float', 'float64') # float64 is what many other languages call double
	return dw

def analysis(sliceno, prepare_res, params):
	from random import choice, randint, gauss
	from string import ascii_letters
	dw = prepare_res
	# To get exactly num_rows rows we may need one extra line in early slices
	num_rows = options.num_rows // params.slices + (options.num_rows % params.slices > sliceno)
	for _ in range(num_rows):
		ascii = ''.join(choice(ascii_letters) for _ in range(10))
		large = randint(-1e20, 1e20)
		small = randint(-99, 99)
		g = gauss(0, 1)
		dw.write(ascii, large, small, small, g, g)
