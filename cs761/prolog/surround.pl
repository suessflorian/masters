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

inner(G) :- grid(G, coordinate(X, Y)), X=\=1, X=\=4, Y=\=1, Y=\=4.
edge(G) :- \+ inner(G).

below(A, B) :-
	grid(A, coordinate(AX, AY)),
	grid(B, coordinate(BX, BY)),
	AX = BX,
	AY =:= BY - 1.

above(A, B) :- below(B, A).

left(A, B) :-
	grid(A, coordinate(AX, AY)),
	grid(B, coordinate(BX, BY)),
	AX =:= BX - 1,
	AY = BY.

right(A, B) :- left(B, A).

neighbours(A, B) :- below(A,B).
neighbours(A, B) :- above(A,B).
neighbours(A, B) :- right(A,B).
neighbours(A, B) :- left(A,B).


negative_neighbour(G, N) :- neighbours(G, N), neg(N).

not_surrounded(G) :- edge(G).
not_surrounded(G) :- pos(G).

/*
	And now in direct reference of tutorial held on 30th September, we define the rules
	that demonstrate the "1, 2 and 3 hop rules".
*/

not_surrounded(G) :- 
	negative_neighbour(G, N),
	edge(N).

not_surrounded(G) :- 
	negative_neighbour(G, N1),
	negative_neighbour(N1, N),
	edge(N).

not_surrounded(G) :-
	negative_neighbour(G, N1),
	negative_neighbour(N1, N2),
	negative_neighbour(N2, N),
	edge(N).

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
