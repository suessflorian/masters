(define (problem euler1)
	( :domain euler)
	( :objects a b c e1 e2 e3)
	( :init
		(at a)
		(node a) (node b) (node c)
		(edge a b e1) (edge b c e2) (edge c a e3)
	)
	( :goal 
		(and (used e1) (used e2) (used e3) (at a))
	)
)
