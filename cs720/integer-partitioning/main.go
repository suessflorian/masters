package main

import (
	"fmt"
)

func main() {
	var start = []int{7}
	rank := 0
	fmt.Println(rank, start)
	for true {
		start = paritionSucessor(start[:], 7) // woah add a : here
		rank++
		fmt.Println(rank, start)
	}
}

func paritionSucessor(current []int, k int) []int {
	// scan right to left
	end := len(current) - 1
	for i := end; i >= 0; i-- {
		// if current is greater then one, then we decrement and pad
		if current[i] > 1 {
			decremented := current[:i]
			oneLessForPadding := current[i] - 1
			decremented = append(decremented, oneLessForPadding)

			decrementedSum := sum(decremented)

			bufferedRemaining := k - decrementedSum
			numberOf := bufferedRemaining / oneLessForPadding

			for i := 0; i < numberOf; i++ {
				decremented = append(decremented, oneLessForPadding)
			}

			if bufferedRemaining%oneLessForPadding != 0 {
				decremented = append(decremented, bufferedRemaining%oneLessForPadding)
			}

			return decremented
		}
	}

	panic("cannot iterate")
}

func sum(nums []int) int {
	var result int
	for _, num := range nums {
		result += num
	}
	return result
}
