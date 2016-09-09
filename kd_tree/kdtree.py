__author__='harounh'
__mailto__='haroun7@gmail.com'

'''
Motivation: Programming Assignment 1, COL752 1st sem 2016-2017.
Implementation of 3D KD Trees which support orthogonal range queries.

Class supports:
	build/construction
	orthogonal range query (range r)
	orthogonal cardinality query (range r)

'''
class KDNode:
	'''
		A vestigial function, really.
	'''
	def __init__(self, ndim):
		self.ndim = ndim # default for now
		self.sz = 0 # This will tell us the size of the kd tree... i.e., the number of points.
		self.split_dim = None # dimension along which split happens
		self.split_val = None # the value used for binary split.
		self.splitting_point = None
	'''
		Takes in a list of points (point_list) and constructs the KD Tree.
		@params point_list: a python array of any iterable of length 3, containing doubles/floats
		@params split_dim: indicates along which dimension to split
	'''
	def build(self, point_list, split_dim):
		# step 1, selecting splitting_point.

	'''
		performs a range query on the kd tree rooted at self.
		@params min_point, max_point: represent the orthogonal range in which to query
	'''
	def range_query(self, min_point, max_point):

	'''
		performs a cardinality query on the kd tree rooted at self
		@params min_point, max_point: represent the orthogonal range in which to query
	'''
	def cardinality_query(self, min_point, max_point): 