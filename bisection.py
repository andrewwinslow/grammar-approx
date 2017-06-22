"""
Contains Python source code for the O(\sqrt{n}/\log{n})-approximation
algorithm referred to as BISECTION described on page 9 of [1].
The algorithm was originally proposed in [2].

All source is owned by Andrew Winslow (awinslow@cs.tufts.edu). 
Not for distribution or use in any way.

References:

[1] M. Charikar, E. Lehman, A. Lehman, D. Liu, R. Panigrahy, 
M. Prabhakaran, A. Sahai, a. shelat, The smallest grammar problem, 
IEEE Trans. on Info. Theory, 51(7), 2554--2576, 2005.

[2] J. C. Kieffer, E. h. Yang, G. J. Nelson, P. Cosman,
Universal lossless compression via multilevel pattern matching,
IEEE Trans. on Info. Theory, 46(5), 1227--1245, 2000.
"""

import unittest

"""
The algorithm, the myth, the legend.
"""
def getBisectionGrammar(S):

	def _recurse(S, grammar):
		if len(S) <= 1:
			return
		grammar[S] = [S[:len(S)/2], S[len(S)/2:]]
		_recurse(S[:len(S)/2], grammar)
		_recurse(S[len(S)/2:], grammar)

	grammar = {}
	_recurse(S, grammar)

	return grammar


class Test__getBisectionGrammar(unittest.TestCase):

	def test1(self):
		grammar = getBisectionGrammar('abcdefgh')
		self.assertEquals(grammar['abcdefgh'], ['abcd', 'efgh'])
		self.assertEquals(grammar['abcd'], ['ab', 'cd'])
		self.assertEquals(grammar['efgh'], ['ef', 'gh'])
		self.assertEquals(grammar['ab'], ['a', 'b'])
		self.assertEquals(grammar['cd'], ['c', 'd'])
		self.assertEquals(grammar['ef'], ['e', 'f'])
		self.assertEquals(grammar['gh'], ['g', 'h'])

	def test2(self):
		grammar = getBisectionGrammar('abababab')
		self.assertEquals(grammar['abababab'], ['abab', 'abab'])	
		self.assertEquals(grammar['abab'], ['ab', 'ab'])
		self.assertEquals(grammar['ab'], ['a', 'b'])

if __name__ == '__main__':
	unittest.main()
		

