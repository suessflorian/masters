package main

import "fmt"

func colexSuccesor(current []int, k int) []int {
	// find smallest j
	var prefix = []int{}
	for i := 0; i < len(current)-1; i++ { // -1 because we're forward looking
		if current[i]+1 < current[i+1] {
			returningArray := prefix
			returningArray = append(returningArray, current[i]+1)
			return append(returningArray, current[i+1:]...)
		}
		prefix = append(prefix, i+1)
	}

	if current[len(current)-1] < k {
		return append(prefix, current[len(current)-1]+1)
	}

	panic("cannot iterate")
}

func main() {
	pointer, k := []int{1, 2, 3}, 5
	rank := 0
	fmt.Println(rank, pointer)
	rank++
	for true {
		pointer = colexSuccesor(pointer, k)
		fmt.Println(rank, pointer)
		rank++
	}
}
