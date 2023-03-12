package main

import (
	"fmt"
)

func main() {
	var start = []int{7}
	rank := 0
	fmt.Println(rank, start)
	for true {
		start = uniqueParitionSuccessor(start[:]) // woah add a : here
		rank++
		fmt.Println(rank, start)
	}
}

func uniqueParitionSuccessor(current []int) []int {
	successor := paritionSucessor(current)
	for !isReverseSorted(successor) {
		successor = paritionSucessor(successor)
	}
	return successor
}

func paritionSucessor(current []int) []int {
	// scan right to left
	end := len(current) - 1
	for i := end; i >= 0; i-- {
		// if current is greater then one, then we decrement and pad
		if current[i] > 1 {
			if i == end {
				decremented := current[:]
				decremented[end]--
				decremented = append(decremented, 1)
				return decremented
			}

			decremented := current[:]
			decremented[i]--
			decremented[i+1]++
			return decremented
		}
	}

	panic("cannot iterate")
}

func isReverseSorted(input []int) bool {
	if len(input) == 0 || len(input) == 1 {
		return true
	}
	for i := 0; i < len(input)-1; i++ {
		if input[i] < input[i+1] {
			return false
		}
	}
	return true
}
