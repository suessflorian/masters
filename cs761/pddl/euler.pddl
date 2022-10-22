( define (domain euler)
	( :requirements :strips )
	( :predicates
		( node ?n ) ( edge ?n1 ?n2 ?e ) (at ?n) (used ?n)
	)
	( :action move
	    :parameters(?n1 ?n2 ?e)
		:precondition(and (at ?n1) (node ?n1) (node ?n2) (edge ?n1 ?n2 ?e) (not (used ?e)))
		:effect(and (at ?n2) (not (at ?n1)) (used ?e))
	)
)
