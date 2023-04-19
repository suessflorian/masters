package main

import (
	"errors"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"unicode"
)

func main() {
	tParseInput := os.Args[1]
	fmt.Printf("parsing: \"%s\" \n", tParseInput)

	ast := new(tParseAST)
	_ = ast.from(tParseInput)

	fmt.Println(ast.treeWidth)
	// TODO: build an AST
}

// tParseAST represent a traversable abstract syntax tree of a t-parse input string.
type tParseAST struct {
	treeWidth int
	// root node could either be an addition of two nodes, or a graph
	// TODO: for now we will just parse the graph, but we need to include possibility of addition
	root graph
}

func (t *tParseAST) from(s string) error {
	// header represents the treewidth of the t-parse input string
	var withHeader = []rune(strings.TrimSpace(s))
	t.treeWidth, _ = strconv.Atoi(string(withHeader[0]))

	tokenizer := &tokenizer{input: withHeader[1:]}
	for {
		run, token, err := tokenizer.next()
		if errors.Is(err, io.EOF) {
			return nil
		}

		switch token {
		case OPEN:
			continue
		case GRAPH:
			rawNums := strings.Split(run, " ")
			nums := make([]int, len(rawNums))
			for i, s := range rawNums {
				nums[i], err = strconv.Atoi(s)
				if err != nil { // NOTE: shouldn't happen, but shows the need for another error handling layer over the core tokenizer
					panic(fmt.Errorf("tokenizer returned a non-int slice of numbers %v: %w", rawNums, err))
				}
			}
			graph := newGraph(nums, t.treeWidth) // TODO: continue
			panic(fmt.Sprintf("%+v", graph))
		}
	}
}

// graph represents the core graph nodes of the tParseAST. Each graph is undirected with a slice of
// vertices and unordered pair of vertices.
type graph struct {
	// boundary is an ordered set of vertices, each element representing the vertix "seen" index
	boundary []int
	// raw represents the raw input string used to build this graph
	raw []int

	// edges described via tuples using the "seen" index
	edges []pair
	// vertices contained in the graph, described via "seen" index
	vertices []int
}

type pair struct {
	a int
	b int
}

// newGraph takes an int slice that indicates the construction of this graph, plus the tree width
// and returns the new parsed graph instance.
func newGraph(build []int, treeWidth int) *graph {
	if treeWidth > 9 {
		panic("cannot construct a graph with a tree width greater than 9")
	}

	g := &graph{
		boundary: make([]int, treeWidth + 1),
		raw:      build,
		edges:    []pair{},
		vertices: []int{},
	}

	for i := range g.boundary {
		g.boundary[i] = i
		g.vertices = append(g.vertices, i)
	}

	// nextIndex holds the index to be assigned to the next vertex when added to the graph
	var nextIndex = len(g.boundary)
	for _, num := range build {
		if num <= treeWidth { // we are replacing a boundary vertex with a new one
			g.vertices = append(g.vertices, nextIndex)
			g.boundary[num] = nextIndex
			nextIndex++
			continue
		}
		if num >= 10 && num < 100 { // we have an edge definition
			first := num / 10
			second := num % 10

			// WARN: assumes correct input, would ideally validate these two references are in fact
			// proper edge references, below will panic if referencing out of boundary.
			g.edges = append(g.edges, pair{g.boundary[first], g.boundary[second]})
			continue
		}
		panic(fmt.Errorf("received an invalid numeric atom in the graph string: %v", build))
	}

	return g
}

// the types of tokens to be parsed, we expect the indexer to only yield GRAPH
// and OPEN tokens
type token int

const (
	// OPEN brace "(", indicates the start of a graph
	OPEN token = iota
	// GRAPH is the token word to represent a series of graph numbers
	GRAPH
	// NULL reserved to represent a invalid token
	NULL
)

// tokenizer is used to statefully increment through an input string skipping all whitespace
// allow an iteration through tokens
type tokenizer struct {
	index int
	input []rune
}

// next returns a triple, the raw parsed string and the associated token. Returns an
// io.EOF error when the end of the string has been hit.
func (i *tokenizer) next() (string, token, error) {
	for {
		if i.index >= len(i.input) {
			return "", NULL, io.EOF
		}

		// we want the index to increment on any return to set up the indexer for the
		// next call
		defer func() {
			i.index++
		}()

		if unicode.IsSpace(i.input[i.index]) {
			i.index++
			continue
		}

		r := i.input[i.index]

		if r == '(' {
			return "(", OPEN, nil
		}

		// if a number is identified, we want to capture the run up until a close brace
		if unicode.IsNumber(r) {
			var run string
			for {
				r := i.input[i.index]
				if r == ')' {
					return strings.TrimSpace(run), GRAPH, nil
				}
				run += string(r)
				i.index++
			}
		}
	}
}
