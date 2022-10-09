/* we take a slightly less obvious approach, rather than
 * exhaustively describing neighbours of g11, g12, ...
 * we generalise a little via associating each cell to a coordinate
 */
grid(g11,coordinate(1,1)).
grid(g12,coordinate(1,2)).
grid(g13,coordinate(1,3)).
grid(g14,coordinate(1,4)).

grid(g21,coordinate(2,1)).
grid(g22,coordinate(2,2)).
grid(g23,coordinate(2,3)).
grid(g24,coordinate(2,4)).

grid(g31,coordinate(3,1)).
grid(g32,coordinate(3,2)).
grid(g33,coordinate(3,3)).
grid(g34,coordinate(3,4)).

grid(g41,coordinate(4,1)).
grid(g42,coordinate(4,2)).
grid(g43,coordinate(4,3)).
grid(g44,coordinate(4,4)).

/* here we can reap the rewards of the coordinate system a little
 * edges are simply those with an X=1,4 OR Y= 1,4... negation is
 * easier to write
 */
inner(G) :- grid(G, coordinate(X, Y)), X=\=1, X=\=4, Y=\=1, Y=\=4.
edge(G) :- \+ inner(G).

/* was debating whether to pass coordinates or not into these
 * neighbour functions, since after playing around with trace 
 * I see grid(A, coordinate(AX, AY)) takes a step to resolve
 */

% A is below B
below(A, B) :-
	grid(A, coordinate(AX, AY)),
	grid(B, coordinate(BX, BY)),
	AX = BX,
	AY =:= BY - 1.

% A is above B
above(A, B) :- below(B, A).

% A is to the left of B
left(A, B) :-
	grid(A, coordinate(AX, AY)),
	grid(B, coordinate(BX, BY)),
	AX =:= BX - 1,
	AY = BY.

% A is to the right of B
right(A, B) :- left(B, A).

neighbours(A, B) :- below(A,B).
neighbours(A, B) :- above(A,B).
neighbours(A, B) :- right(A,B).
neighbours(A, B) :- left(A,B).

% G is a negative neighbour of N
negative_neighbour(N, G) :- neighbours(G, N), neg(N).

/* here we take a lot of inspiration from the tutorial, I spent way too long
 * on trying to build constructively the "is_surrounded" rule
 */
not_surrounded(G) :- edge(G).
not_surrounded(G) :- pos(G).

/* in direct reference of tutorial held on 30th September, we define the rules
 * that demonstrate the "1, 2 and 3 hop rules". If the grid were to expand in size
 * with this approach we'd have to increase the number of hop rules.              /
 */ 
not_surrounded(G) :- 
	negative_neighbour(N, G),
	edge(N).

not_surrounded(G) :- 
	negative_neighbour(N1, G),
	negative_neighbour(N, N1),
	edge(N).

not_surrounded(G) :-
	negative_neighbour(N1, G),
	negative_neighbour(N2, N1),
	negative_neighbour(N, N2),
	edge(N).

/* we restrict the group to grid members early to restrict the size
 * of the search tree, otherwise PROLOG actually fails to resolve
 * G on it's own
 */
is_surrounded(G) :- grid(G, _), \+ not_surrounded(G).

neg(g21).
neg(g23).
neg(g32).
neg(g33).

pos(g11).
pos(g12).
pos(g13).
pos(g14).
pos(g24).
pos(g31).
pos(g34).
pos(g41).
pos(g42).
pos(g43).
pos(g44).
