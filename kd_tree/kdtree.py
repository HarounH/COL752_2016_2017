from __future__ import print_function # I like my beloved print() function.

__author__='harounh'
__mailto__='haroun7@gmail.com'

import numpy as np # used for median function.


'''

Motivation: Programming Assignment 1, COL752 1st sem 2016-2017.
Implementation of 3D KD Trees which support orthogonal range queries.

The file also contains print_tree(root_node) ... not very friendly on the eyes, but it exists.

'''

''''
	a quick and dirty function to see if a point is in a given orthogonal range
	@params point: the query point
	@params min_point, max_point: the min and max points of our orthogonal range
'''
def point_in_range(point, min_point, max_point):
	for d in range(0, len(point)):
		if point[d]<min_point[d] or point[d]>max_point[d]:
			return False
	return True

'''
KDNode Class supports:
	build/construction
	range query (orthogonal range r)
	cardinality query (orthogonal range r)

	there is also:
	__init__
	and node2str
'''
class KDNode:
	'''
		A vestigial function, really.
	'''
	def __init__(self, ndim, depth=0):
		self.ndim = ndim # default for now
		self.sz = 0 # This will tell us the size of the kd tree... i.e., the number of points.
		self.depth = depth
		self.left = None
		self.right = None
		
		self.split_dim = None # dimension along which split happens
		self.split_val = None # the value used for binary split.

		# abuse of notation in self.splitting_points
		self.splitting_points = None # the points which have point[self.split_dim] == self.split_val
		# if self is a leaf, then splitting_points is all the points in this region.

	def is_leaf(self):
		return self.left is None and self.right is None
	'''
		Takes in a list of points (point_list) and constructs the KD Tree.
		@params point_list: a python array of any iterable of length 3, containing doubles/floats
		@params split_dim: indicates along which dimension to split

		@behaviour sorting is done in-place, hence input can be affected.

		Not an optimal function because median finding is done in O(nlogn) time instead of O(n) time.
	'''
	def build(self, point_list, split_dim=None):
		# step 1, selecting splitting_points.
		if split_dim is None:
			split_dim = 0 # Split on axis-0
		
		self.split_dim = split_dim
		self.sz = len(point_list)
		if len(point_list)==1:
			# this is leaf
			self.splitting_points = point_list
			return

		# median search... ideally O(n). But this will do too.
		point_list.sort(key=lambda x:x[split_dim]) # Sort by 0th dimension.
		val = point_list[self.sz/2][split_dim]
		self.split_val = val

		left_list = []
		right_list = []
		self.splitting_points = []
		for point in point_list:
			if point[split_dim] < val:
				left_list.append(point)
			elif point[split_dim] > val:
				right_list.append(point)
			else:
				self.splitting_points.append(point)

		if len(self.splitting_points)>1:
			print('warning, more than one point with ' + str(self.split_dim) + 'th coordinate=' + str(val), )

		self.left = None
		if len(left_list)>0:
			self.left = KDNode(self.ndim, depth=self.depth+1)
			self.left.build(left_list, split_dim=((self.split_dim+1)%self.ndim))

		self.right = None
		if len(right_list)>0:
			self.right = KDNode(self.ndim, depth=self.depth+1)
			self.right.build(right_list, split_dim=((self.split_dim+1)%self.ndim))
	'''
		performs a range query on the kd tree rooted at self.
		@params min_point, max_point: represent the orthogonal range in which to query
	'''
	def range_query(self, min_point, max_point):
		ret_list = []
		for point in self.splitting_points:
			if point_in_range(point, min_point, max_point):
				ret_list.append(point)
		# if it's a leaf, we're done!
		if self.is_leaf():
			return ret_list
		#since we aren't a leaf, we have kids and split_val != None.

		# leftside
		# if the range is not entirely in the right side, we must search in the left side too.
		if min_point[self.split_dim] < self.split_val:
			# the range must lie on both sides of the split
			left_ret_list = self.left.range_query(min_point, max_point) if self.left is not None else []
		else:
			left_ret_list = []
		# rightside
		if max_point[self.split_dim] > self.split_val:
			right_ret_list = self.right.range_query(min_point, max_point) if self.right is not None else []
		else:
			right_ret_list = []
		return ret_list + left_ret_list + right_ret_list
			

	'''
		performs a cardinality query on the kd tree rooted at self
		@params min_point, max_point: represent the orthogonal range in which to query
	'''

	def cardinality_query(self, min_point, max_point): 
		ret_list = []
		for point in self.splitting_points:
			if point_in_range(point, min_point, max_point):
				ret_list.append(point)
		# if it's a leaf, we're done!
		if self.is_leaf():
			return len(ret_list)
		#since we aren't a leaf, we have kids and split_val != None.

		# leftside
		# if the range is not entirely in the right side, we must search in the left side too.
		if min_point[self.split_dim] < self.split_val:
			# the range must lie on both sides of the split
			left_retval = self.left.cardinality_query(min_point, max_point) if self.left is not None else 0
		else:
			left_retval = 0
		# rightside
		if max_point[self.split_dim] > self.split_val:
			right_retval = self.right.cardinality_query(min_point, max_point) if self.right is not None else 0
		else:
			right_retval = 0
		return ret_list + left_retval + right_retval

	def to_str(self):
		s = 'kdnode('+ str(self.ndim) +') @ depth=' + str(self.depth) + '\n'
		s += '\tsplit_dim=' + str(self.split_dim) + '\n'
		s += '\tsplit_val=' + str(self.split_val) + '\n'
		s += '\tsplitting_points=' + str(self.splitting_points) + '\n'
		return s
def print_tree(root):
	# BFS printing
	fringe = [root]
	s = ''
	while len(fringe)>0:
		next_level = []
		while len(fringe)!=0:
			node = fringe.pop()
			s += node.to_str()
			if node.left is not None:
				next_level.append(node.left)
			if node.right is not None:
				next_level.append(node.right)
		fringe = next_level
	print(s)


# Executed code.
if __name__ == '__main__': # This is the testing thingy.
	P = [ [0,1,2],[3,4,5],[6,7,8],[9,10,11],[12,13,14] ]
	tree = KDNode(3)
	tree.build(P) # Construct a tree.
	print_tree(tree)
	print(tree.range_query([2,4,6],[13,11,15]))