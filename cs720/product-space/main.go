package main

import (
	"fmt"
	"strconv"
)

func main() {
	// fmt.Println(enumerateGrayCodes(3))
	for i, value := range enumerateProductSpaces([]int{3, 5, 10}) {
		fmt.Println(i, value)
	}
}

func enumerateGrayCodes(n int) []string {
	if n == 0 {
		return []string{""}
	}

	var list []string
	var childrenCodes = enumerateGrayCodes(n - 1)
	for _, code := range childrenCodes {
		list = append(list, "0"+code)
	}
	for i := len(childrenCodes) - 1; i >= 0; i-- {
		list = append(list, "1"+childrenCodes[i])
	}

	return list
}

func enumerateProductSpaces(spaces []int) []string {
	if spaces == nil || len(spaces) == 0 {
		return []string{""}
	}

	var list []string
	var childrenEnumerations = enumerateProductSpaces(spaces[1:])
	currentSpace := spaces[0]

	for prefix := 0; prefix < currentSpace; prefix++ {
		if prefix%2 == 0 {
			for _, enumeration := range childrenEnumerations {
				list = append(list, strconv.Itoa(prefix)+","+enumeration)
			}
		} else {
			for i := len(childrenEnumerations) - 1; i >= 0; i-- {
				list = append(list, strconv.Itoa(prefix)+","+childrenEnumerations[i])
			}
		}
	}

	return list
}
