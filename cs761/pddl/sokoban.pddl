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

	( :action push_up
	    :parameters(?x ?y ?box_from_x ?box_from_y ?box_to_x ?box_to_y)
			:precondition(and (at ?x ?y) (box ?box_from_x ?box_from_y)
				(= ?x ?box_from_x) (= ?box_from_x ?box_to_x)														; all along the same x-axis
				(inc ?y ?box_from_y) (inc ?box_from_y ?box_to_y)												; agent, box and above box all inline
				(not ( wall ?box_to_x ?box_to_y )) (not ( box ?box_to_x ?box_to_y ))		; no obstacles in the way of the push
			)
			:effect(and 
				(not (at ?x ?y)) (at ?box_from_x ?box_from_y)														; move to where box was
				(not (box ?box_from_x ?box_from_y)) (box ?box_to_x ?box_to_y)						; box moved upwards
			)
	)

	( :action push_down
	    :parameters(?x ?y ?box_from_x ?box_from_y ?box_to_x ?box_to_y)
			:precondition(and (at ?x ?y) (box ?box_from_x ?box_from_y)
				(= ?x ?box_from_x) (= ?box_from_x ?box_to_x)														; all along the same x-axis
				(dec ?y ?box_from_y) (dec ?box_from_y ?box_to_y)												; agent, box and above box all inline
				(not ( wall ?box_to_x ?box_to_y )) (not ( box ?box_to_x ?box_to_y ))		; no obstacles in the way of the push
			)
			:effect(and 
				(not (at ?x ?y)) (at ?box_from_x ?box_from_y)														; move to where box was
				(not (box ?box_from_x ?box_from_y)) (box ?box_to_x ?box_to_y)						; box moved upwards
			)
	)

	( :action push_right
	    :parameters(?x ?y ?box_from_x ?box_from_y ?box_to_x ?box_to_y)
			:precondition(and (at ?x ?y) (box ?box_from_x ?box_from_y)
				(= ?y ?box_from_y) (= ?box_from_y ?box_to_y)														; all along the same y-axis
				(inc ?x ?box_from_x) (inc ?box_from_x ?box_to_x)												; agent, box and above box all inline
				(not ( wall ?box_to_x ?box_to_y )) (not ( box ?box_to_x ?box_to_y ))		; no obstacles in the way of the push
			)
			:effect(and 
				(not (at ?x ?y)) (at ?box_from_x ?box_from_y)														; move to where box was
				(not (box ?box_from_x ?box_from_y)) (box ?box_to_x ?box_to_y)						; box moved upwards
			)
	)

	( :action push_left
	    :parameters(?x ?y ?box_from_x ?box_from_y ?box_to_x ?box_to_y)
			:precondition(and (at ?x ?y) (box ?box_from_x ?box_from_y)
				(= ?y ?box_from_y) (= ?box_from_y ?box_to_y)														; all along the same y-axis
				(dec ?x ?box_from_x) (dec ?box_from_x ?box_to_x)												; agent, box and above box all inline
				(not ( wall ?box_to_x ?box_to_y )) (not ( box ?box_to_x ?box_to_y ))		; no obstacles in the way of the push
			)
			:effect(and 
				(not (at ?x ?y)) (at ?box_from_x ?box_from_y)														; move to where box was
				(not (box ?box_from_x ?box_from_y)) (box ?box_to_x ?box_to_y)						; box moved upwards
			)
	)
)
