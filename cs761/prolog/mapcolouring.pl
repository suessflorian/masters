/*
* given knowledge base, one thing to check would be that
* different(C1, C2) :- different(C2, C1)
* but that is already implied due to the exhaustive listing
*/

different(red, green).
different(red, blue).
different(green, blue).
different(green, red).
different(blue, red).
different(blue, green).

/*
* pretty straight forward - and due to the above comment,
* we don't need to say that for example;
* "WA should be different to A"
* and "A should be different to WA", just one of those is
* sufficient.
*/

mapcolouring(N, A, WA, B, G, T, M, H, WE) :-
	different(N, A),
	different(A, WA),
	different(WA, T),
	different(WA, M),
	different(WA, H),
	different(WA, B),
	different(M, WE),
	different(M, H),
	different(H, B),
	different(H, G),
	different(B, G).
