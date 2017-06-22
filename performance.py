
import lehman1
import bisection
import exhaustive
import sakamoto
import random
import string
import time
import matplotlib.pyplot

def grammarSize(G):
	# the sum of the number of right-hand size symbols for all rules
	return sum([len(v) for v in G.values()])
	
def algorithmAsymptoticPerformance(grammarFunction):
	sampleSize = 10
	string_size = []
	grammar_size = []
	times = []
	for n in xrange(10, 201, 10):
		total = 0
		startTime = time.time()
		for i in xrange(sampleSize):
			S = "".join([random.choice(string.letters) for c in xrange(n)])
			total += grammarSize(grammarFunction(S))
		endTime = time.time()
		string_size.append(n)
		grammar_size.append(total / float(sampleSize))
		times.append((endTime-startTime) / float(sampleSize)) 
	return string_size, grammar_size, times

def algorithmSmallStringPerformance():
	n = 1024	
	print "bisection lehman1 sakamoto"
	algorithms = [bisection.getBisectionGrammar, lehman1.getLehman1Grammar,
				sakamoto.getSakamotoGrammar]
	for i in xrange(100):
		S = "".join(['a' for c in xrange(n)])
		print [grammarSize(function(S)) for function in algorithms]
			
if __name__ == '__main__':
	ln, lg, lt = algorithmAsymptoticPerformance(lehman1.getLehman1Grammar)
	bn, bg, bt = algorithmAsymptoticPerformance(bisection.getBisectionGrammar)
	sn, sg, st = algorithmAsymptoticPerformance(sakamoto.getSakamotoGrammar)
	#print str(n) + " " + str(g) + " " + str(t)
	#en, eg, et = algorithmAsymptoticPerformance(exhaustive.getExhaustiveGrammar)
	print "Grammar sizes:"
	print "String length    Lehman1    Bisection    Sakamoto"
	for i in xrange(len(ln)):
		print str(ln[i]).ljust(17) + str(lg[i]).ljust(11) + str(bg[i]).ljust(13) + str(sg[i])
	print ""
	print "Time taken (in ms):"
	print "Lehman1    Bisection    Sakamoto"
	for i in xrange(len(ln)):
		print str(round(lt[i]*1000)).ljust(11) + str(round(bt[i]*1000)).ljust(13) + str(round(st[i]*1000))




