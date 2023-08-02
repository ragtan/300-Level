% CISC 360 a4, Winter 2022
%
% See a4.pdf for instructions

/*
 * Q1: Student ID
 */
student_id( 20058783 ).
% other_student_id(  ).
% if in a group, uncomment the above line and put the other student ID between the ( )

/*
 * Q2: evalF in Prolog
 *
 */
/*
  This question uses formulas similar to Haskell a3:

  top              truth (always true)
  bot              falsehood (contradiction)
  and( P1, P2)     conjunction of P1 and P2
  or( P1, P2)      disjunction of P1 and P2
  implies( P, Q)   implication (P -> Q)
  atom( a)         atomic proposition

For example, the a3 Haskell expression

   Implies (And vA vB) Top

where vA = Atom "A"
  and vB = Atom "B"

can be represented in Prolog as

   implies( and( atom(a), atom(b)), top)
*/

/*
  A valuation is a list of pairs of atom names and booleans.
  For example:

      [(a, false), (b, true)]

  is a valuation that says "a is false and b is true".
 
  evalF( Valu, Q, Result)
  
  Given a valuation Valu and a formula Q,
    Result = true   if  Q evaluates to true under Valu,
  and
    Result = false  if  Q evaluates to false under Valu.
*/
evalF( _, top, true).
evalF( _, bot, false).

% member: built-in predicate: member(Elem, List) is true iff
%  Elem is an element of List.
evalF( Valu, atom(V), Result) :- member((V, Result), Valu).

evalF( Valu, and(Q1, Q2), true)  :- evalF( Valu, Q1, true),
                                    evalF( Valu, Q2, true).
evalF( Valu, and(Q1, _),  false) :- evalF( Valu, Q1, false).
evalF( Valu, and(_,  Q2), false) :- evalF( Valu, Q2, false).

/* 
Q2:  Add clauses for:  or
                       implies
*/

evalF( Valu, or(Q1, Q2), true) 	:- 	evalF( Valu, Q1, true),
    								                evalF( Valu, Q2, true).
evalF( Valu, or(Q1, _), true) 	:-	evalF( Valu, Q1, true).
evalF( Valu, or(_, Q2), true) 	:-	evalF( Valu, Q2, true).
evalF( Valu, or(Q1, Q2), false) :-	evalF( Valu, Q1, false),
    								                evalF( Valu, Q2, false).

evalF( Valu, implies(Q1, Q2), true)	 :-	evalF( Valu, Q1, true),
    									                  evalF( Valu, Q2, true).
evalF( Valu, implies(Q1, Q2), false) :-	evalF( Valu, Q1, true),
    									                  evalF( Valu, Q2, false).
evalF( Valu, implies(Q1, Q2), true)	 :- evalF( Valu, Q1, false),
    									                  evalF( Valu, Q2, true).
evalF( Valu, implies(Q1, Q2), true)  :-	evalF( Valu, Q1, false),
    									                  evalF( Valu, Q2, false).

/*
 * Q3: Prime numbers
 */
 
/*
  findFactor(N, F): Given an integer N ≥ 2,
                     look for a factor F' of N, starting from F:
                     findFactor(N, F) true iff
                                           there exists F' in {F' | (F' >= F) and (F' * F') < N}
                                             such that (N mod F) = 0.
*/
findFactor(N, F) :- N mod F =:= 0.

findFactor(N, F) :- N mod F =\= 0,
                    F * F < N,
                    Fplus1 is F + 1,
                    findFactor(N, Fplus1).
/*
  isPrime(N, What)

  Given an integer N >= 2:
    What = prime           iff   N is prime
    What = composite       iff   N is composite
*/

isPrime(2, prime).
isPrime(N, composite) :- N > 2,    findFactor(N, 2).
isPrime(N, prime)     :- N > 2, \+ findFactor(N, 2).
%                               ^^
%                               "not"

/*
  findPrimes(Numbers, Primes)
    Primes = all prime numbers in Numbers
 
  Q3a. Replace the word "change_this" in the rules below.
       Hint:  Try to use  findPrimes(Xs, Ys).
*/
findPrimes([], []).

/*
  In this rule, we include X in the output: [X | Ys].
  So this rule should check that X is prime.
*/
findPrimes([X | Xs], [X | Ys]) :- isPrime(X, prime), findPrimes(Xs, Ys).

/*
  In this rule, we do not include X in the output.
  So this rule should check that X is composite.
*/
findPrimes([X | Xs], Ys) :- isPrime(X, composite), findPrimes(Xs, Ys).

/*
  upto(X, Y, Zs):
  Zs is every integer from X to Y

  Example:
     ?- upto(3, 7, Range)
     Range = [3, 4, 5, 6, 7]
*/
upto(X, X, [X]).
upto(X, Y, [X | Zs]) :-
    X < Y,
    Xplus1 is X + 1,
    upto(Xplus1, Y, Zs).

/*
  primes_range(M, N, Primes)
    Primes = all prime numbers between M and N
    Example:
      ?- primes_range(60, 80, Primes).
      Primes = [61, 67, 71, 73, 79] .

 Q3b. Replace the word "change_this" in the rule below.
      HINT: Use upto and findPrimes.
*/

primes_range(M, N, Primes) :- upto(M, N, Range), findPrimes(Range, Primes).

/*
  Q4: Trees

  Consider the tree     (We are *not* representing
                          trees with Empty "leaves":
             4                         4
            / \                      /   \
           2   5                   2       5
          / \                    /  \     / \
         1   3                 1     3   E   E
                              / \   / \
                          Empty  E E   E            )

  We will express the above tree in Prolog as

    node( 4, node( 2, leaf(1), leaf(3)), leaf(5))
  
  What we are doing here is similar to the Haskell type
  
    data A4Tree = Node Integer A4Tree A4Tree
                | Leaf Integer

  An *in-order traversal* of a tree is the keys we get when we traverse
  (walk through) a tree, visiting the left subtree first, then the root,
  then the right subtree.

  For example, the in-order traversal of the above tree is

    [1, 2, 3, 4, 5]
                                                         which adds:
  We start at 4, and go to its left child:
    the tree node(2, leaf(1), leaf(3)),
      then we go to 2's left child, which is
        leaf(1)                                          1
      then we add 2                                      2
      then we go to 2's right child, which is
        leaf(3)                                          3
    then we add 4                                        4
    then we go to 4's right child, which is
      leaf(5)                                            5

  The predicate

    inorder(T, Keys)

  is true iff, given a tree T, its in-order traversal is Keys.

  ?- inorder( node( 4, node( 2, leaf(1), leaf(3)), leaf(5)), Keys).
  Keys = [1, 2, 3, 4, 5].
*/

inorder(leaf(K), [K]).

inorder(node(K, L, R), Keys) :-
  inorder(L, Lkeys),
  inorder(R, Rkeys),
  append(Lkeys, [K | Rkeys], Keys).  % similar to Haskell
                                     %   Keys  =  Lkeys ++ (K : Rkeys)

/*
Q4a. Define a predicate

  postorder(T, Keys)

that is true iff, given a tree T, its *post-order* traversal is Keys.

In a post-order traversal, we visit the left subtree, the right subtree,
and *then* the root.

For example, you should get

  ?- postorder( node( 4, node( 2, leaf(1), leaf(3)), leaf(5)), Keys).
  Keys = [1, 3, 2, 5, 4]
*/

postorder(leaf(K), [K]).

postorder(node(K, L, R), Keys) :-
    postorder(L, LKeys),
    postorder(R, RKeys),
    append(LKeys, RKeys, LRKeys),
    append(LRKeys, [K], Keys).

/*
Q4b.  In-order and post-order traversals are paths through the entire tree.
  In this part of the question, we consider "vertical" paths from the leaves to a root.
  
  In the tree            4
                        / \      
                       2   5     
                      / \        
                     1   3       
                     
  the paths starting from the leaves are:

    1 to 2 to 4          [1, 2, 4]
    3 to 2 to 4          [3, 2, 4]
    5 to 4               [5, 4]

  The above tree can be represented in Prolog as

    node(4, node(2, leaf(1), leaf(3)), leaf(5))

  In this question, define a Prolog predicate

    findpath(Tree, Path)

  such that if we start from the root of Tree,
  then Path is a list of numbers from the root to a leaf.

  For example:
  
    ?- findpath(node(2, leaf(1), leaf(3)), [1, 2]).
    true
    ?- findpath(node(2, leaf(1), leaf(3)), [3, 2]).
    true

  Your predicate should be written so that when the first argument is a specific tree
  (containing no variables) and the second argument is a variable, typing ; returns
  *all* possible paths to all the leaves, from left to right.  For example:

    ?- findpath(node(4, node(2, leaf(1), leaf(3)), leaf(5)), Path).
    Path = [1, 2, 4]
    Path = [3, 2, 4]
    Path = [5, 4].

  Hint:
    ?- findpath(leaf(2), [2]).
  should be true.

  Finish defining clauses for 'findpath' below.
*/

findpath(leaf(K), [K]).

findpath(node(K, L, _), Path) :-
    findpath(L, LPath),
    append(LPath, [K], Path).

findpath(node(K, _, R), Path) :-
    findpath(R, RPath),
    append(RPath, [K], Path).