import numpy as np
import itertools

class PermutationGroup():
	"""
	Group of Permutations S_n. Each permutation is a list from 0 to {length of each list}, and the set is treated as numpy array of lists of equal length.

	Parameters
	----------
	- subset: list of elements, where each element is a list, a ser or a numpy array.

	Attributes
	----------
	- n_: int, the length of each list. The same n in the group S_n.
	- identity_: list, the identity of the group.
	- subgroup_: numpy array, the minimum subgroup containing each permutation in the subset.
	- group_: numpy array, the S_n permutation group.
	"""
	def __init__(self, subset):
		self.subset = subset

	def generate_group(self):
		"""
		Create a full permutation group S_n, for the given {length n: the length of each list}.

		Outputs
		-------
		- self: object
				Added all the permutations of S_n.
		"""
		self.n_ = len(self.subset[0])
		n_permutations = [np.array(item) for item in itertools.permutations(np.arange(self.n_))]
		self.group_ = np.unique(n_permutations, axis=0)
		return self

	def generate_subgroup(self):
		"""
		Add the minimum permutations to create a subgroup containing the given {elements: the self.subset}. 
		It firsts add the identity and inverses, and then all posible multiples. No need to add inverses again, as the inverse of a multiple
		is the multiple of the inverses ordered backwards.

		Outputs
		-------
		- self: object
				Added the minimum permutations required to form a subgroup.
		"""
		self.n_ = len(self.subset[0])
		if self.n_ == 0:
			self.subgroup_ = np.array([[]])
			return self
		accumulation = []
		accumulation.append(np.arange(self.n_))
		for a in self.subset:
			accumulation.append(np.array(a))
			accumulation.append(np.argsort(a))
		self.subgroup_ = np.unique(accumulation, axis=0).copy()
		if len(self.subgroup_) == 1:
			return self
		iterations = 0
		while True:
			iterations += 1
			if iterations == 1:
				for a, b in itertools.product(self.subgroup_, self.subgroup_):
					accumulation.append(a[b])
			else:
				for a, b in itertools.product(self.subgroup_, diff):
					accumulation.append(a[b])
					accumulation.append(b[a])
				for a, b in itertools.product(diff, diff):
					accumulation.append(a[b])
			accumulation = np.unique(accumulation, axis=0)
			if all(any((a == b).all() for a in self.subgroup_) for b in accumulation):
				break
			else:
				accumulation_rows = accumulation.view([("", accumulation.dtype)] * accumulation.shape[1])
				subgroup_rows = self.subgroup_.view([("", self.subgroup_.dtype)] * self.subgroup_.shape[1])
				diff = np.setdiff1d(accumulation_rows, subgroup_rows, assume_unique=True).view(accumulation.dtype).reshape(-1, accumulation.shape[1])
				self.subgroup_ = np.unique(accumulation, axis=0).copy()
				accumulation = list(accumulation)
			if iterations == 10_000:
				break 	# Just in case
		self.subgroup_ = np.unique(accumulation, axis=0)
		return self

	def is_permutation_group(self):
		"""
		Check if subset has a permutation group structure. If it satisifes:
			* Multiplication Closure
			* Associativity
			* Identity
			* Inverses.

		Outputs
		-------
		- True or False: bool, True if the subset has the 4 properties required for the structure, False if not.
		"""
		self.n_ = len(self.subset[0])
		if self.n_ == 0:
			return True
		if not all(any((np.array(x)[np.array(y)] == np.array(z)).all() for z in self.subset) for x, y in itertools.product(self.subset, self.subset)):
			return False
		self.identity_ = "null"
		for x in self.subset:
			if all((np.array(x)[np.array(y)] == np.array(y)).all() and (np.array(y)[np.array(x)] == np.array(y)).all() for y in self.subset):
				self.identity_ = x
				break
		if type(self.identity_) == str:
			return False
		elif not all(
			(np.array(x)[np.array(y)[np.array(z)]] == np.array(x)[np.array(y)][np.array(z)]).all() 
			for x, y, z in itertools.product(self.subset, self.subset, self.subset)
		):
			return False
		elif not all(
			any((np.array(x)[np.array(y)] == np.array(self.identity_)).all() and (np.array(y)[np.array(x)] == np.array(self.identity_)).all() 
			for y in self.subset) for x in self.subset
		):
			return False
		else:
			return True