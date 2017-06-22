"""
Contains Python source code for the O(\log^3{n})-approximation
algorithm for the smallest grammar problem as described in [1]
on pages 15--17.

References:

[1] M. Charikar, E. Lehman, A. Lehman, D. Liu, R. Panigrahy, 
M. Prabhakaran, A. Sahai, a. shelat, The smallest grammar problem, 
IEEE Trans. on Info. Theory, 51(7), 2554--2576, 2005.

[2] A. Blum, T. Jiang, M. Li, J, Tromp, M. Yannakakis,
Linear approximation of shortest superstrings, 
Journal of the ACM, 41(4): 630--647, 1994.
"""

import math
import unittest
import copy
import random
import string

"""
Description:
Computes the amount of overlap between two strings, i.e.
the longest prefix/suffix pair (a prefix of one string and
suffix of the other). 

Discussion:
Overlap here is defined as it is on page 3 of [2], namely 
``...let v be the longest string such that s = uv, t = vw
for some non-empty strings u and w. We call |v| the amount of
overlap between s and t''.

Input:
A pair of strings s1 and s2.

Output:
A tuple containing the length of the longest overlap between
these two strings, and the indices in s1 and s2 where the
overlap starts. By definition one of the indices must be 0.
Returns (0, length of s1, 0) if no overlap exists. 
"""
def computeOverlap(s1, s2):
        max_overlap = (0, len(s1), 0)
	# slide s1 to the right over s2
	# do not slide all the way: prefix and suffix
	# must each be non-empty
        for i in xrange(1, min(len(s1), len(s2))): 
                if (s1[-i:] == s2[:i]):
                       max_overlap = max(max_overlap, (i, len(s1)-i, 0))   
        return max_overlap 


"""
Description:
Returns the two strings of a collection with the greatest overlap, i.e.
the two strings with the longest prefix/suffix pair (a prefix of one string
and a suffix of the other).

Input:
A list of strings.

Output:
A 2-tuple containing the two strings in the list with maximum overlap.
"""
def pairWithMaximumOverlap(Ss):
        max_overlap = (-1, None, None) # triple with (overlap, first string index, second string index)
        for i in xrange(len(Ss)):
                for j in xrange(i+1, len(Ss)):
                        max_overlap = max(max_overlap, (computeOverlap(Ss[i], Ss[j])[0], i, j))
        return (Ss[max_overlap[1]], Ss[max_overlap[2]])  


"""
Description:
First, produces a single string containing an input set of strings.
Uses a greedy approach (attributed to [2]) and gives a 4-approximation
to the smallest such string.
Second, it breaks the single string produced in the first step into
a sequence of strings according to the locations at which the input 
string set appear in the superstring.

Input:
A set of strings to produce a single output string for.

Output:
A sequence of strings whose concatenation is a small superstring produced from
the input string set, and whose substrings each start at a location in the superstring
at which an input string started.
"""
def blumSmallestSuperstringAndBreaking(Ss):
	# compute the small superstring
        strings = copy.deepcopy(Ss)
	substringSubstringIndices = {}
	for i in xrange(0, len(strings)):
		substringSubstringIndices[strings[i]] = [0]
        while (len(strings) > 1):
                s1, s2 = pairWithMaximumOverlap(strings)
                strings.remove(s1)
                strings.remove(s2)
                overlap = computeOverlap(s1, s2)
		strings.append(s1[:overlap[1]] + s2) 
		if strings[-1] not in substringSubstringIndices:
			substringSubstringIndices[strings[-1]] = []
		substringSubstringIndices[strings[-1]] += substringSubstringIndices[s1] + [i + overlap[1] for i in substringSubstringIndices[s2]]

	# break it into the sequence
	superstring = strings[0]
	substringIndices = substringSubstringIndices[superstring]
	substringIndices = [0] + substringIndices + [len(superstring)]
	substringIndices = list(set(substringIndices)) # remove duplicates
	substringIndices.sort()
	brokenSequence = []
	for start, end in zip(substringIndices[:-1], substringIndices[1:]):
		brokenSequence.append(superstring[start:end])

        return brokenSequence

"""
Description:
Modifies a list of strings by breaking strings at their midpoint
if they exceed an input length.

Input:
A list of strings and a threshold length.

Output:
Nothing. The input string list is modified by removing strings
that are too long and replacing them with two halves.
"""
def splitTooBigs(strings, split_len):
        result = []
        for s in strings: # Compute images of excessively-long strings  
                if len(s) > split_len:
                        result.append(s[:len(s)/2]) 
                        result.append(s[len(s)/2:]) 
                else:
                        result.append(s)
        return result        

"""
Description:
Takes in a string S and returns a sequence of lists
corresponding to the sets C_n, C_{n/2}, C_{n/4}, \ldots, C_4 
as described on page 16. 

Input:
A string.

Output:
A sequence of sequences, according to the decomposition
C_n, C_{n/2}, C_{n/4}, \ldots, C_2.
"""
def generateCs(S):
        n = len(S)
        k = 2**(int(math.ceil(math.log(n, 2))) - 1)
        Cs = [[S]]
        while (k >= 2):
                pk = blumSmallestSuperstringAndBreaking(Cs[-1])
                pkp = splitTooBigs(pk, k)
                Cs.append(pkp)
                k /= 2
        return Cs


"""
Description:
Finds where a string occurs in a sequence of smaller strings and
returns the interval of the smaller strings creating the longest
prefix of the string, along with the length of the prefix.

Input:
A string and a sequence of smaller strings whose concatenation is 
a superstring of the input string.

Output:
A triple specifying the indices of the first and last strings in
the sequence whose concatenation contains the longest prefix of 
input string, along with the length of this prefix.
"""
def findLongestPrefix(s, small_strings):

	def findPrefixStart():
		for i in xrange(len(small_strings)):
			if s == ("".join(small_strings[i:]))[:len(s)]: # if s is a prefix 
				return i
		raise Exception, "String not found as a prefix"

	sPrefixStart = findPrefixStart()
	sPrefixEnd = sPrefixStart
	remSLen = len(s)
	while sPrefixEnd < len(small_strings) and len(small_strings[sPrefixEnd]) <= remSLen:
		remSLen -= len(small_strings[sPrefixEnd])
		sPrefixEnd += 1
        return (sPrefixStart, sPrefixEnd, len(s) - remSLen) 

"""
Description:
Creates a grammar using the \emph{substring construction} as
defined on pages 15--16.

Input:
A string.

Output:
A grammar in the form of a dictionary created using the
substring construction. Each production is a (key, value)
pair in the dictionary, with the key being a LHS non-terminal
(represented as a string) and the value being a sequence of
non-terminals/terminals (also strings).
"""
def generateSubstringConstructionGrammar(S):

        def recursiveCall(S, grammar):
                if len(S) == 1:
                        return
                for i in xrange(len(S)/2-1):
                        grammar["".join(S[i:len(S)/2])] = [S[i], "".join(S[i+1:len(S)/2])]
                for i in xrange(len(S)/2+1, len(S)):
                        grammar["".join(S[len(S)/2:i+1])] = ["".join(S[len(S)/2:i]), S[i]]
                recursiveCall(S[:len(S)/2], grammar)
                recursiveCall(S[len(S)/2:], grammar)

        grammar = {}
        recursiveCall(S, grammar)
        return grammar 

"""
The algorithm, the myth, the legend.
"""
def getLehman1Grammar(S):

	# Get the C_k sequence 
        Cs = generateCs(S)
	
	# Get the substring construction for each C_k sequence
	grammar = {}
	for C in Cs:
		grammar.update(generateSubstringConstructionGrammar(C))
	grammar.update(generateSubstringConstructionGrammar([char for char in S]))

	# For each string, find its decomposition into sequences of nonterminals
	# from each C_k and use the substring construction to create <= 2
	# nonterminals for the sequence from each C_k 
        for i in xrange(0, len(Cs)):
                for j in xrange(len(Cs[i])):
                        s = Cs[i][j]
			if len(s) == 1:
				continue
			sRemainder = s
			grammar[s] = []
			for C in Cs[i+1:]:
				start, end, used = findLongestPrefix(sRemainder, C)
				if (start == end):
					continue
				elif (start + 1 == end):
					grammar[s].append(C[start])
					sRemainder = sRemainder[used:] 
				elif (start + 2 == end):
					grammar[s].append(C[start])
					grammar[s].append(C[start+1])
					sRemainder = sRemainder[used:] 
				else:
					for split in xrange(start + 1, end):
						half1 = "".join(C[start:split])			
						half2 = "".join(C[split:end])
						if ((split == start + 1 or half1 in grammar) and
							(split == end - 1 or half2 in grammar)):
							break			
					grammar[s].append(half1)
					grammar[s].append(half2)
					sRemainder = sRemainder[used:] 
			grammar[s].extend([c for c in sRemainder])

	for k in grammar.keys():
		for v in grammar[k]:
			if len(v) > 1 and v not in grammar:
				raise Exception, "FUUU"

        return grammar

class Test__computeOverlap(unittest.TestCase):

        def test1(self):
                self.assertEquals(computeOverlap("abc", "def"), (0, 3, 0))
                self.assertEquals(computeOverlap("def", "abc"), (0, 3, 0))

        def test2(self):
                self.assertEquals(computeOverlap("abc", "cde"), (1, 2, 0))
                self.assertEquals(computeOverlap("cde", "abc"), (0, 3, 0))

        def test3(self):
                self.assertEquals(computeOverlap("abc", "bcd"), (2, 1, 0))
                self.assertEquals(computeOverlap("bcd", "abc"), (0, 3, 0))

        def test4(self):
                self.assertEquals(computeOverlap("a", "a"), (0, 1, 0))
                self.assertEquals(computeOverlap("ab", "ab"), (0, 2, 0))
                self.assertEquals(computeOverlap("abc", "abc"), (0, 3, 0))

        def test5(self):
                self.assertEquals(computeOverlap("b", "abc"), (0, 1, 0))
                self.assertEquals(computeOverlap("bcd", "abcde"), (0, 3, 0))
                self.assertEquals(computeOverlap("ab", "ababab"), (0, 2, 0))


class Test__pairWithMaximumOverlap(unittest.TestCase):

        def test1(self):
                self.assertEquals(pairWithMaximumOverlap(["abc", "def", "bcd"]), ("abc", "bcd"))
                self.assertEquals(pairWithMaximumOverlap(["abc", "def", "ghi", "jkl", "efg"]), ("def", "efg"))
                self.assertEquals(pairWithMaximumOverlap(["abc", "def", "ghi", "jkl", "def", "bcz"]), ("abc", "bcz"))

class Test__blumSmallestSuperstringAndBreaking(unittest.TestCase):

        def test1(self):
                self.assertEquals(blumSmallestSuperstringAndBreaking(["abc", "cde"]), ["ab", "cde"])
                self.assertEquals(blumSmallestSuperstringAndBreaking(["abc", "cde", "efg", "ghi"]), 
			["ab", "cd", "ef", "ghi"])

        def test2(self):
                self.assertEquals(blumSmallestSuperstringAndBreaking(["abc", "cde", "efg", "fgh"]), 
			["ab", "cd", "e", "fgh"])

        def test3(self):
                self.assertEquals(blumSmallestSuperstringAndBreaking(["abc", "ab"]), ["abc", "ab"])
                self.assertEquals(blumSmallestSuperstringAndBreaking(["ab", "abc"]), ["ab", "abc"])

class Test__splitTooBigs(unittest.TestCase):

        def test1(self):
                self.assertEquals(splitTooBigs(["ab", "def", "ghij"], 1), ["a", "b", "d", "ef", "gh", "ij"])
                self.assertEquals(splitTooBigs(["ab", "def", "ghij"], 2), ["ab", "d", "ef", "gh", "ij"])
                self.assertEquals(splitTooBigs(["ab", "def", "ghij"], 3), ["ab", "def", "gh", "ij"])
        
        def test2(self):
             	self.assertEquals(splitTooBigs(["abcd"], 2), ["ab", "cd"])

class Test__generateCs(unittest.TestCase):

        def test1(self):
		self.assertEquals(generateCs("abcd"), [["abcd"], ["ab", "cd"]])

	def test2(self):
		self.assertEquals(generateCs("abcdefgh"),
			[["abcdefgh"], ["abcd", "efgh"], ["ab", "cd", "ef", "gh"]])

        def test3(self):
		self.assertEquals(generateCs("aabcdababcbd"),
			[["aabcdababcbd"], ["aabcda", "babcbd"], ["aab", "cda", "bab", "cbd"], 
			["c", "bd", "cd", "aa", "b", "ab"]])

	def test4(self):
		self.assertEquals(generateCs("aabbababbaa"),
			[["aabbababbaa"], ["aabba", "babbaa"], ["aab", "bab", "baa"],
			["aa", "ba", "b", "aa"]])

	def test5(self):
		self.assertEquals(generateCs("aaaaaaaaa"),
			[["aaaaaaaaa"], ["aaaa", "aaaaa"], ["a", "aa", "aaa"], ["a", "a", "a", "aa"]])

class Test__findLongestPrefix(unittest.TestCase):

        def test1(self):
                self.assertEquals(findLongestPrefix("abcdefg", ["ab", "cd", "ef","gh"]), (0, 3, 6))

	def test2(self):
                self.assertEquals(findLongestPrefix("cde", ["cd", "ab", "cd", "ef"]), (2, 3, 2)) 

	def test3(self):
		self.assertEquals(findLongestPrefix("abcde", ["abcd", "qq", "abc", "d", "ef"]), (2, 4, 4))

class Test__generateSubstringConstructionGrammar(unittest.TestCase):

        def test1(self):
                grammar = generateSubstringConstructionGrammar(["a", "b", "c", "d", "e", "f", "g", "h"])
                self.assertEquals(len(grammar), 8)
                self.assertEquals(grammar["abcd"], ["a", "bcd"])
                self.assertEquals(grammar["bcd"], ["b", "cd"])
                self.assertEquals(grammar["cd"], ["c", "d"])
                self.assertEquals(grammar["efgh"], ["efg", "h"])
                self.assertEquals(grammar["efg"], ["ef", "g"])
                self.assertEquals(grammar["ef"], ["e", "f"])
                self.assertEquals(grammar["ab"], ["a", "b"])
                self.assertEquals(grammar["cd"], ["c", "d"])
                self.assertEquals(grammar["ef"], ["e", "f"])
                self.assertEquals(grammar["gh"], ["g", "h"])

	def test2(self):
		grammar = generateSubstringConstructionGrammar(
			["ab", "cd", "ef", "gh"])
		self.assertEquals(len(grammar), 2)
		self.assertEquals(grammar["abcd"], ["ab", "cd"])
		self.assertEquals(grammar["efgh"], ["ef", "gh"])

	def test3(self):
                grammar = generateSubstringConstructionGrammar(
			["aa", "bb", "cc", "dd", "ee", "ff", "gg", "hh"])
                self.assertEquals(len(grammar), 8)
                self.assertEquals(grammar["aabbccdd"], ["aa", "bbccdd"])
                self.assertEquals(grammar["bbccdd"], ["bb", "ccdd"])
                self.assertEquals(grammar["ccdd"], ["cc", "dd"])
                self.assertEquals(grammar["eeffgghh"], ["eeffgg", "hh"])
                self.assertEquals(grammar["eeffgg"], ["eeff", "gg"])
                self.assertEquals(grammar["eeff"], ["ee", "ff"])
                self.assertEquals(grammar["aabb"], ["aa", "bb"])
                self.assertEquals(grammar["ccdd"], ["cc", "dd"])
                self.assertEquals(grammar["eeff"], ["ee", "ff"])
                self.assertEquals(grammar["gghh"], ["gg", "hh"])

class Test__getLehman1Grammar(unittest.TestCase):

	def test1(self):
		grammar = getLehman1Grammar("ab")
		self.assertEquals(grammar["ab"], ["a", "b"])		               

	def test2(self):
		grammar = getLehman1Grammar("abcdefgh")
		self.assertEquals(grammar["abcdefgh"], ["abcd", "efgh"])		               
		self.assertEquals(grammar["abcd"], ["ab", "cd"])
		self.assertEquals(grammar["efgh"], ["ef", "gh"])
		self.assertEquals(grammar["ab"], ["a", "b"])
		self.assertEquals(grammar["cd"], ["c", "d"])
		self.assertEquals(grammar["ef"], ["e", "f"])
		self.assertEquals(grammar["gh"], ["g", "h"])

	def test3(self):
		grammar = getLehman1Grammar("abab")
		self.assertEquals(grammar["abab"], ["ab", "ab"])
		self.assertEquals(grammar["ab"], ["a", "b"])

	def test4(self):
		grammar = getLehman1Grammar("aababbabababbaba")
		self.assertEquals(grammar["aababbabababbaba"], ["aababbab", "ababbaba"])
		self.assertEquals(grammar["aababbab"], ["a", "abab", "ba", "b"])
		self.assertEquals(grammar["ababbaba"], ["abab", "baba"])
		self.assertEquals(grammar["abab"], ["a", "ba", "b"])
		self.assertEquals(grammar["baba"], ["ba", "ba"])
		self.assertEquals(grammar["ba"], ["b", "a"])

	def test5(self):
		getLehman1Grammar("abcabcbacbabcbbcbacbabcbabbacbabacbabcaacbabcababcba")

	def test6(self):
		getLehman1Grammar("ababbabaaabbbbabbabbababbabbbbabbbababbabaaaaabababaabbbbbabbbabbaaabbbbbbaabbabbaaaaabbbbbbabaabbbbbaaaaaaabbabaabbbbaababbbbbaaabbbbbbaaabaabbaabbbaaabbbbbbaababababbaabbbaaabaaaaaabbbbaabbabbabbbbbaaaabbabbaaaabbbbbbaabaabaabbabaababaabaabbbbbaababbaaaaaaaababbbbabaabbaaaaaababbbbbabbababbbaaababbabbbbbaaaaabbbbbabbaaababbbaaabbabbbbbbbaababababbbbbbbbbaaaaababaabbabbbbbbabbbbbbaababbbabbbbaaaabaaaabbbbabbabbbaaaabaaabbabbaabaaaabbaaba")

	def test7(self):
		# Fuzzing
		for i in xrange(1):
			s = "".join([random.choice(string.ascii_lowercase[:2]) for j in xrange(random.randrange(5000, 5001))])
			try:
				getLehman1Grammar(s)
			except Exception:	
				print s
				self.assertTrue(False)

if __name__ == '__main__':
        unittest.main()



