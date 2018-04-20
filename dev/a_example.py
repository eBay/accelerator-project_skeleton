description = r'''
This is just an example. It doesn't even try to do anything useful.

You can run it to see that your installation works.
'''

def analysis(sliceno):
	return sliceno

def synthesis(analysis_res):
	print("Sum of all sliceno:", sum(analysis_res))
