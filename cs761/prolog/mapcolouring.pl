different(red, green).
different(red, blue).
different(green, blue).
different(green, red).
different(blue, red).
different(blue, green).

mapcolouring(N, A, WA, B, G, T, M, H, WE) :-
				different(N, A),
				different(A, WA),
				different(WA, T),
				different(WA, H),
				different(WA, B),
				different(WA, M),
				different(M, WE),
				different(M, H),
				different(B, H),
				different(B, G).
