package main

import "fmt"

func main() {
	numberOf := 6
	rank := 0

	var partition []int
	for i := 0; i < numberOf; i++ {
		partition = append(partition, 1)
	}

	fmt.Println(rank, partition)
	for true {
		partition = growthFunctionSuccessor(partition)
		rank++
		// if inOnly2Parts(partition) {
		fmt.Println(rank, partition)
		// }
	}
}

func inOnly2Parts(incoming []int) bool {
	for _, val := range incoming {
		if val > 2 {
			return false
		}
	}
	return true
}

func growthFunctionSuccessor(current []int) []int {
	next := current[:]
	for i := len(current) - 1; i > 0; i-- {
		// if within max + 1, then increment

		if current[i] <= current[i-1] {
			next[i]++
			for k := 1; i+k < len(current); k++ {
				next[i+k] = 1
			}
			return next
		}
	}
	panic("cannot iterate")
}
