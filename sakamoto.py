"""
Python code for the O(log(n))-approximation algorithm for the
smallest grammar problem as described in [1].

Code written by Michelle Ichinco and Andrew Winslow.

[1] H. Sakamoto, A fully linear-time approximation algorithm 
for grammar-based compression, Combinatorial Pattern Matching 2003, 
LNCS 2676, 348--360.
"""

import unittest
import copy
import operator


"""
Description:
Takes a sequence and converts it into a binary grammar producing the sequence
from a 
# Just explodes a tuple into a set of binary productions producing the elements 
# converting P -> w into a tree of binary productions

Input:
A sequence of symbols (strings).

Output:
A grammar (dictionary) and start symbol (string) that produce exactly the sequence. 
"""
def produceTrivialGrammar(w):
        P = {}
	for i in xrange(2, len(w)+1):
		P["".join(w[:i])] = ["".join(w[:i-1]), w[i-1]]
        return P

"""
Description (pseudocode):

Algorithm LEVELWISE-REPAIR(w)
        initialize P = N = \emptyset
        while (there exists ab such that ab occurs at least twice in w) do {
                P \leftarrow repetition(w, N);  (replacing all repetitions)
                P \leftarrow arrangement(w, N); (replacing frequent pairs)
        }
        if (|w| = 1) return P;
        else return P \cup {S \rightarrow w};
end.

notation: X \leftarrow Y denotes the addition of the set Y to X.
"""
def levelwiseRepair(w):
        w = copy.copy(w)
        w = list(w)
        P = {} # A dictionary of production rules
        ID = set() #creates a set of ids
        while (hasRepeatingPairs(w)):
                # "P \leftarrow repetition(w, N);  (replacing all repetitions)"
                P.update(repetition(w))
                # "P \leftarrow arrangement(w, N); (replacing frequent pairs)"
                P.update(arrangement(w, ID))
        if (len(w) == 1):
                return P
        else:
                start_grammar = produceTrivialGrammar(w)
                P.update(start_grammar)
                return P

def getSakamotoGrammar(S):
	return levelwiseRepair(S)

"""
Description:
Returns a boolean indicating whether the sequence has
a pair of consecutive symbols that appears more than
once in the sequence. Overlapping of occurrances is
allowed, i.e. ababab contains two occurrances of bab.

Input:
A sequence of strings (terminal and non-terminal symbols
in the grammar).

Output:
A boolean indicating whether there is a pair of consecutive
symbols occurring more than once in the sequence.
"""
def hasRepeatingPairs(w):
	sequences = set()
        for i in xrange(len(w) - 1):
		pair = (w[i], w[i+1])
		if pair in sequences:
			return True
		sequences.add(pair)
	return False

"""
repetition()

Description (pseudocode):

procedure repetition(w, N):
        initialize P = \emptyset;
        while (there exists w[i, i+j] = a^+) do {
                replace w[i, i+j] by A_{(a, j)};
                P \leftarrow {A_{(a, j)} \rightarrow BC} and N \leftarrow {A_{(a, j)}, B, C} recursively;
        }
        return P;
end
"""
def repetition(w):
        # "initialize P = \emptyset;"
        P = {}
        # "while (there exists w[i, i+j] = a^+) do {"
        while (hasRepeatingSymbol(w)):
		i, j = hasRepeatingSymbol(w)
                A_a_j = w[i] * (j - i + 1)
                # "replace w[i, i+j] by A_{(a, j)};"
		for r in xrange(i, j+1):
			w.pop(i)
		w.insert(i, A_a_j)
                # "P \leftarrow {A_{(a, j)} \rightarrow BC} and N \leftarrow {A_{(a, j)}, B, C} recursively;"
                produceRepeatingSymbolGrammar(P, A_a_j)
        # "return P;"
        return P
	

"""
hasRepeatingSymbol()

Description:
Returns an interval indicating whether the input
sequence has a subsequence of length at least 2
in which every symbol is the same. For instance, 
ababab does not while abaaab does (aa occurs).

Input:
A sequence of strings.

Output:
Either an 2-tuple with the start and end of the
repeating sequence (both inclusive), or None.
"""
def hasRepeatingSymbol(w):
	
	def findMaxRepeating(w, i):
		j = i+1
		while j < len(w) and w[j] == w[i]:
			j += 1
		return (i, j-1)

	if len(w) < 2:
		return None

	for i in xrange(len(w)-1):
		r = findMaxRepeating(w, i)	
		if r[0] != r[1]:
			return r
	return None

#creates production rules and adds them to P, adds non-terminals to N
"""
produceRepeatingSymbolGrammar()

Input:
A dictionary of production rules P and the non-terminal needing to
be produced.

Output:
The production rules for deriving a repeated-symbol string 
are placed into P. These rules are as described on page 5 of [1]:

A^k -> A^{k/2}A^{k/2} if k >= 4 and even
A^k -> A^{k-1}A if k >= 3 and odd
A^k -> A^2 if k == 2
"""
def produceRepeatingSymbolGrammar(P, S):
	if len(S) == 2:
		P[S] = [S[0], S[1]]
	elif (len(S) % 2 == 0):
		rhs1 = S[:len(S)/2]
		rhs2 = S[len(S)/2:]
		P[S] = [rhs1, rhs2]
		produceRepeatingSymbolGrammar(P, rhs1)	
		produceRepeatingSymbolGrammar(P, rhs2)	
	else:
		rhs1 = S[:len(S)-1]
		rhs2 = S[len(S)-1]
		P[S] = [rhs1, rhs2]
		produceRepeatingSymbolGrammar(P, rhs1)	

"""
arrangement()

Description (pseudocode):

procedure arrangement(w, N)
	initialize D = emptyset
	make _list_: the frequency lists of all pairs in w;
	while (_list_ is not empty)do{
		pop the top pair ab in list;
		set the unique id = {d_1, d_2} for ab;
		compute the following sets based on C_{ab} = {w[i,i+1] = ab}:
			F_{ab} = {s in C_{ab} | s is free},
			L_{ab} = {s in C_{ab} | s is fixed},
			R_{ab} = {s in C_{ab} | s is right-fixed};
		D <- assignment(F_{ab} U assignment(L_{ab}) U assignment(R_{ab});
	}
	replace all segments in D by appropriate nonterminals;
	return the set P of production rules computed by D and update N by P;
end.

"""
def arrangement(w, ID):
        D = {} #saves segments and their ids in the form (i, i+1):id
        L = createSortedSegmentList(w)
        P = {}
        Assignments = {}
        while (len(L) > 0):
                #pops most frequent
                segment = L.pop(0)[1]

                #sets ids {d_1, d_2} equal to next two numbers in order
                id1 = len(ID)
                ID.add(id1)
                id2 = id1 + 1
                ID.add(id2)
		
                #gets sets
                C = make_set_c(segment, w)
                Free = set() #saves sets of segments as (i, i+1)
                Left = set()
                Right = set()
                make_sets(w, C, Free, Left, Right, Assignments)
	
                #add segments to D
                D.update(assignment(Free, Free, Left, Right, Assignments, id1, id2, w, D))
                D.update(assignment(Left, Free, Left, Right, Assignments, id1, id2, w, D))
                D.update(assignment(Right, Free, Left, Right, Assignments, id1, id2, w, D))

        #replace segments with non-terminals
        values = D.values()
        for v in values: #remove duplicates
                while values.count(v) > 1:
                        values.remove(v)

        segments = set()
        for v in values:
                for x in D:
                        if D[x] == v:
                                segments.add((w[x[0]], w[x[1]]))

        for s in segments:
                # find locations that the segment occurs 
                locs = []
                for i in xrange(len(w) - 1):
                        if (w[i], w[i+1]) == s:
                                locs.append(i)
		# replace the segment by a nonterminal
                for l in locs:
                        w[l] = s[0] + s[1]
                for li in xrange(len(locs)):
                        w.pop(locs[li] - li + 1)
		# add to the grammar 
                P[s[0] + s[1]] = [s[0], s[1]]

        #return the set P of production rules computed by D
        return P
	
#makes the list of segments and sorts them by count
def createSortedSegmentList(w):
	# compute counts
	segmentCounts = {}
        for i in xrange(len(w) - 1):
                segment = (w[i], w[i+1])
		if segment in segmentCounts:
			segmentCounts[segment] += 1
		else:
			segmentCounts[segment] = 1

	# create a sorted list
        segmentList = []
	for segment in segmentCounts:
		segmentList.append((segmentCounts[segment], segment))
        segmentList.sort() 
        segmentList.reverse()
        return segmentList
	
def make_set_c(seg, w):
	C = set()
	for i in xrange(len(w)-1):
		if (w[i], w[i+1]) == seg:
			C.add((i, i+1))
	return C
	
# compute F: neither right or left aligned
# compute L: w[i-1, i] is assigned an id
# compute R: w[i+1, i+2] is assigned an id
def make_sets(w, C, F, L, R, Assignments):
	for x in C:
		i = x
		if i[0] - 1 > 0 and Assignments.has_key((i[0]-1, i[0])):
			L.add(i)
		elif i[0] + 2 < len(w) and Assignments.has_key((i[0]+1, i[0]+2)):
			R.add(i)
		else:
			F.add(i)


def assignment(X, Free, Left, Right, assignments, d1, d2, w, dictionary):
	D = {}
	if (X is Free):
		for x in Free:
			assignments[x] = d1
			D[x] = d1
	if(X is Left):
		for x, y in Left:
			leftseg = (x-1, x)
			seq = (x, y)
			if subgroup(leftseg, assignments, dictionary) == "irregular":	
				assignments[seq] = d2
			if subgroup(leftseg, assignments, dictionary) == "unselected":
				assignments[seq] = d1
				D[seq] = d1
			if subgroup(leftseg, assignments, dictionary) == "selected":
				if group_contents(leftseg, w, assignments, dictionary) == "irregular":
					assignments[seq] = d2
				elif group_contents(leftseg, w, assignments, dictionary) == "unselected":
					assignments[seq] = d1
				#Y contains an irregular subgroup
				elif check_all(X, Left, Right, assignments, dictionary) == "irregular":
					assignments[seq] = d2
				else:
					assignments[seq] = d1
	
	if (X is Right):
		for x, y in Right:
			rightseg = (y, y+1)
			seq = (x, x+1)
			if subgroup(rightseg, assignments, dictionary) == "irregular":	
				assignments[seq] = d2
			if subgroup(rightseg, assignments, dictionary) == "unselected":
				assignments[seq] = d1
				D[seq] = d1
			if subgroup(rightseg, assignments, dictionary) == "selected":
				if group_contents(rightseg, w, assignments, dictionary) == "irregular":
					assignments[seq] = d2
				elif group_contents(rightseg, w, assignments, dictionary) == "unselected":
					assignments[seq] = d1
				# Y contains an irregular subgroup
				elif check_all(X, Left, Right, assignments, dictionary) == "irregular":		
					assignments[seq] = d2
				else:
					assignments[seq] = d1
	
	return D
	
#segment is in an irregular subgroup if, for all segments assigned that index, some are in D and some are not	
def subgroup(a, assignments, D):
	inD = False
	ninD = False
	index = assignments[a]				
	for x in assignments:			
		y = assignments[x]
		# check to see if an entry is in the same subgroup
		if y == index:						
			#if there is an entry that has been added to D
			if D.has_key(x):
				inD = True
			# if there is an entry with that id not added to D
			if not D.has_key(x):			
				ninD = True
	if inD and ninD:	
		return "irregular"
	if (not inD) and ninD:
		return "unselected"
	if inD and (not ninD):
		return "selected"

def group_contents(seg, w, assignments, dictionary):
	otherseg = seg
	#determine the other ids for this segment
	for x in assignments:
		y = assignments[x]
		if x[0] == seg[0] and x[1] == seg[1]:
			if y != assignments[seg]:
				index = y
				otherseg = (x)
				
	#check whether any subgroup with those indexes is an irregular subgroup
	if subgroup(otherseg, assignments, dictionary) == "irregular":
		return "irregular"
	if subgroup(otherseg, assignments, dictionary) == "unselected":
		return "unselected"
	
def check_all(a, Left, Right, assignments, dictionary):
	for x, y in a:
		if a is Left:
			check = (x-1, x) #checking all left segments 
		if a is Right:
			check = (y, y+1)
		#if it has an irregular subgroup return irregular
		if subgroup(check, assignments, dictionary) == "irregular":	
			return "irregular"
	else:
		return "other"


class Test__levelwiseRepair(unittest.TestCase):

        def test1(self):
               	levelwiseRepair('aaaaaabbbbbbbaaaaaa') 
                levelwiseRepair('aaaadadvxcvdfdfg') 
                levelwiseRepair('ghngngn') 
                levelwiseRepair('aaaabbbbccccceeeeffffftttt') 
                levelwiseRepair('ghaaaas') 

class Test__produceTrivialGrammar(unittest.TestCase):

	def test1(self):
		self.assertEquals({'abcd': ['abc', 'd'], 'abc': ['ab', 'c'], 'ab': ['a', 'b']}, 
			produceTrivialGrammar(['a', 'b', 'c', 'd']))

class Test__hasRepeatingPairs(unittest.TestCase):

        def test1(self):
                self.assertFalse(hasRepeatingPairs('abcdefg'))
                self.assertTrue(hasRepeatingPairs('aaaaaaa'))
                self.assertFalse(hasRepeatingPairs('aabbcc'))
                self.assertTrue(hasRepeatingPairs('abcdeab'))
                self.assertTrue(hasRepeatingPairs('abab'))

class Test__repetition(unittest.TestCase):

        def test1(self):        
                w = ['a', 'a', 'a', 'a']
                P = repetition(w)
                self.assertEquals(w, ['aaaa']) 
                self.assertEquals(P, {'aaaa': ['aa', 'aa'], 'aa': ['a', 'a']})

        def test2(self):
                w = ['a', 'a', 'b', 'a', 'a', 'b', 'b']
                P = repetition(w)
		self.assertEquals(w, ['aa', 'b', 'aa', 'bb'])
                self.assertEquals(P, {'aa': ['a', 'a'], 'bb': ['b', 'b']})
                
        def test3(self):
                w = ['a', 'b', 'a', 'b']
                P = repetition(w)
		self.assertEquals(w, ['a', 'b', 'a', 'b'])
                self.assertEquals(P, {})
                
class Test__createSortedSegmentList(unittest.TestCase):
	
	def test1(self):
		L = createSortedSegmentList(['a', 'b', 'c', 'd'])
		self.assertEquals(L, [(1, ('c', 'd')), (1, ('b', 'c')), (1, ('a', 'b'))])

	def test2(self):
		L = createSortedSegmentList(['a', 'b', 'a', 'b'])
		self.assertEquals(L, [(2, ('a', 'b')), (1, ('b', 'a'))])

	def test3(self):
		L = createSortedSegmentList(['a', 'a', 'a', 'a', 'a'])
		self.assertEquals(L, [(4, ('a', 'a'))])

class Test__hasRepeatingSymbol(unittest.TestCase):
	
	def test1(self):
		self.assertEquals(hasRepeatingSymbol(['a', 'b', 'a', 'b']), None)
		self.assertEquals(hasRepeatingSymbol(['a', 'b', 'c', 'd']), None)
		self.assertEquals(hasRepeatingSymbol(['a', 'b', 'c', 'c']), (2, 3))
		self.assertEquals(hasRepeatingSymbol(['a', 'a', 'a', 'a']), (0, 3))

class Test__produceRepeatingSymbolGrammar(unittest.TestCase):

        def test1(self):
                P = {}
                produceRepeatingSymbolGrammar(P, 'aaaaaaaa')    
                self.assertEquals(len(P), 3)
                self.assertEquals(P['aaaaaaaa'], ['aaaa', 'aaaa'])
                self.assertEquals(P['aaaa'], ['aa', 'aa'])
                self.assertEquals(P['aa'],['a', 'a'])


if __name__ == '__main__':
        unittest.main()





