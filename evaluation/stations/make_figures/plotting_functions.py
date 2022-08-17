import numpy as np

def legend_positions(x,y):
	""" Calculate position of labels to the right in plot... """
	positions = []
	half = (x[1] - x[0])*0.8
	positions.append(x[-1] + half)
	positions.append(y[-1])
	return positions
