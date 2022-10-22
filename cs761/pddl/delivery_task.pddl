(define (problem delivery_task)
	(:domain delivery)
	(:objects c1 c2 akl wlg p)
	(:init
		(at c1 akl) (at c2 wlg)
		(cargo c1) (cargo c2)
		(plane p)
		(airport akl) (airport wlg)
	)
	(:goal
		(and
			(at c1 wlg)
			(at c2 akl)
		)
	)
)
