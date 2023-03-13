package main

import "fmt"

func main() {
	fmt.Println(enumerateGrayCodes(3))
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
