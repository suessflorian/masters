( define (domain sokoban)
	( :requirements :strips :equality )
	( :predicates
		( wall ?x ?y ) ( box ?x ?y ) (at ?x ?y) (inc ?p ?q) (dec ?p ?q)
	)

	( :action move_up
	    :parameters(?x ?y ?to_x ?to_y)
			:precondition(and (at ?x ?y) (inc ?y ?to_y) (= ?x ?to_x) (not ( wall ?to_x ?to_y )) (not ( box ?to_x ?to_y )) )
			:effect(and (not (at ?x ?y)) (at ?to_x ?to_y))
	)

	( :action move_down
	    :parameters(?x ?y ?to_x ?to_y)
			:precondition(and (at ?x ?y) (dec ?y ?to_y) (= ?x ?to_x) (not ( wall ?to_x ?to_y )) (not ( box ?to_x ?to_y )) )
			:effect(and (not (at ?x ?y)) (at ?to_x ?to_y))
	)

	( :action move_right
	    :parameters(?x ?y ?to_x ?to_y)
			:precondition(and (at ?x ?y) (inc ?x ?to_x) (= ?y ?to_y) (not ( wall ?to_x ?to_y )) (not ( box ?to_x ?to_y )) )
			:effect(and (not (at ?x ?y)) (at ?to_x ?to_y))
	)

	( :action move_left
	    :parameters(?x ?y ?to_x ?to_y)
			:precondition(and (at ?x ?y) (dec ?x ?to_x) (= ?y ?to_y) (not ( wall ?to_x ?to_y )) (not ( box ?to_x ?to_y )) )
			:effect(and (not (at ?x ?y)) (at ?to_x ?to_y))
	)
)
