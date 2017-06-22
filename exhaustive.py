"""
Contains Python source code for the brute-force
algorithm for the smallest S2F grammar problem.
"""
import unittest

def generateAllGrammars(goal):
	if(len(goal) == 1):
		yield {}
		raise StopIteration
	else:
		for i in xrange(1, len(goal)):
			left = goal[:i]
			right = goal[i:]
			for g in generateAllGrammars(left):
				for h in generateAllGrammars(right):
					G = {goal: [left, right]}
					G.update(h) 
					G.update(g) # left side gets precedence
					yield G
		raise StopIteration

"""
Description:
Creates a grammar for the string which is
the smallest (srsly!). 
"""
def getExhaustiveGrammar(S):

	def stageCount(G, s):
		if s not in G:
			return 0
		else:
			return max([stageCount(G, t) for t in G[s]]) + 1 


	return min([g for g in generateAllGrammars(S)], key=lambda G: (len(G), stageCount(G, S)))
		
class Test__generateAllGrammars(unittest.TestCase):	

	def test1(self):
		grammars = [g for g in generateAllGrammars('ababc')]
		self.assertEquals(len(grammars), 14) # 5th catalan number
		G = grammars[0]
		self.assertEquals(G['ababc'], ['a', 'babc'])
		self.assertEquals(G['babc'], ['b', 'abc'])
		self.assertEquals(G['abc'], ['a', 'bc'])
		self.assertEquals(G['bc'], ['b', 'c'])
		G = grammars[13]
		self.assertEquals(G['ababc'], ['abab', 'c'])
		self.assertEquals(G['abab'], ['aba', 'b'])
		self.assertEquals(G['aba'], ['ab', 'a'])
		self.assertEquals(G['ab'], ['a', 'b'])
		

class Test__getExhaustiveGrammar(unittest.TestCase):

	def test1(self):
		G = getExhaustiveGrammar('abab')
		self.assertEquals(G['abab'], ['ab', 'ab'])
		self.assertEquals(G['ab'], ['a', 'b'])

	def test2(self):
		G = getExhaustiveGrammar('abababab')
		self.assertEquals(G['abababab'], ['abab', 'abab'])
		self.assertEquals(G['abab'], ['ab', 'ab'])
		self.assertEquals(G['ab'], ['a', 'b'])

	def test3(self):
		G = getExhaustiveGrammar('abcabcabc')
		self.assertTrue(G['abcabcabc'] == ['abc', 'abcabc'] or G['abcabcabc'] == ['abcabc', 'abc'])
		self.assertEquals(G['abcabc'], ['abc', 'abc'])
		self.assertTrue(G['abc'] == ['a', 'bc'] or G['abc'] == ['ab', 'c'])
		self.assertTrue(('ab' in G and G['ab'] == ['a', 'b']) or
			('bc' in G and G['bc'] == ['b', 'c']))

if __name__ == '__main__':
	unittest.main()
		

