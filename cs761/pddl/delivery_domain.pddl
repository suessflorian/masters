( define (domain delivery)
	( :requirements :strips )
	( :predicates
		(at ?thing ?place) (plane ?pl) (airport ?a) (in ?thing ?plane) (cargo ?thing)
	)

	( :action load
			:parameters (?thing ?pl ?a)
			:precondition (and (at ?thing ?a) (at ?pl ?a) (cargo ?thing) (plane ?pl) (airport ?a))
			:effect (and (in ?thing ?pl) (not (at ?thing ?a)))
	)

	( :action unload
			:parameters (?thing ?pl ?a)
			:precondition (and (in ?thing ?pl) (at ?pl ?a) (cargo ?thing) (plane ?pl) (airport ?a))
			:effect (and (at ?thing ?a) (not (in ?thing ?pl)))
	)

	( :action fly
			:parameters (?pl ?from ?to)
			:precondition ( and (plane ?pl) (airport ?from) (airport ?to) (at ?pl ?from) )
			:effect ( and (at ?pl ?to) (not (at ?pl ?from)) )
	)
)
