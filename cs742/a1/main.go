package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		parts := strings.Split(scanner.Text(), ",")
		if len(parts) != 5 {
			continue
		}

		// If 'year' is in HH:MM format, replace it with "2007"
		if strings.Contains(parts[4], ":") {
			parts[4] = "2007"
		}

		// Parse the combined date string
		t, err := time.Parse("Jan 2 2006", parts[3]+" "+parts[4])
		if err != nil {
			panic(fmt.Sprintf("failed to parse %q", parts[3]+" "+parts[4]))
		}

		// generate corrected CSV
		fmt.Printf("%s,%s,%s,%d\n", parts[0], parts[1], parts[2], t.Unix())
	}

	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "Error reading from stdin:", err)
	}
}
