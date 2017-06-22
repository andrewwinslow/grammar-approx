# grammar-approx
Implementations of smallest grammar approximation algorithms.

The _smallest grammar problem_ asks for the smallest [context-free grammar (CFG)](http://en.wikipedia.org/wiki/Context-free_grammar) whose language is a single given string. The _size_ of a CFG is the total number of distinct symbols on the righthand sides of the grammar's rules. 

As this problem is NP-hard[2], it's unlikely any efficient algorithm can compute an optimally small CFG for any given string. Instead, one can ask for an efficient algorithm that always gives a solution whose size is some small multiplicative ratio of the optimal solution. If the ratio is always at most f(n), then such an algorithm is called a _f(n)-approx algorithm_. 

A variety of such algorithms are known.  
Implementations of the following algorithms are provided:
* BISECTION: The O((n/log(n))^0.5)-approx algorithm described in [1].   
* LEHMAN1: The O((log(n))^3)-approx algorithm described on pages 15-17 of [2].
* SAKAMOTO: The O(log(n))-approx algorithm described in [3]. 
* EXHAUSTIVE: A naive brute-force, exponential-time algorithm (used for comparison).

[1] J. C. Kieffer, E. h. Yang, G. J. Nelson, P. Cosman, Universal lossless compression via multilevel pattern matching, IEEE Transactions on Information Theory, 46(5), 1227--1245, 2000.

[2] M. Charikar, E. Lehman, A. Lehman, D. Liu, R. Panigrahy, M. Prabhakaran, A. Sahai, a. shelat, The smallest grammar problem, IEEE Transactions on Information Theory, 51(7), 2554--2576, 2005. 
 
[3] H. Sakamoto, A fully linear-time approximation algorithm for grammar-based compression, Combinatorial Pattern Matching 2003, LNCS 2676, 348--360.

