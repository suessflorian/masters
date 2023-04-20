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

	ast := new(ast)
	ast.from(tParseInput)

	root := ast.root.(*addition)

	leftGraph := root.left.(*graph)

	rightAddition := root.right.(*addition)
	leftAdditionGRaph := rightAddition.left.(*graph)
	righttAdditionGRaph := rightAddition.right.(*graph)

	fmt.Println(leftGraph)
	fmt.Println(leftAdditionGRaph)
	fmt.Println(righttAdditionGRaph)
}

// ast represent a traversable abstract syntax tree of a t-parse input string.
type ast struct {
	treeWidth int
	root      node
}

func (t *ast) from(s string) error {
	// header represents the treewidth of the t-parse input string
	var withHeader = []rune(strings.TrimSpace(s))
	t.treeWidth, _ = strconv.Atoi(string(withHeader[0]))

	tokenizer := &tokenizer{input: withHeader[1:]}
	tokenizer.next() // we skip the first open

	t.root = t.parseNode(tokenizer)
	return nil
}

func (t *ast) evaluate() graph {
	panic("not implemented")
}

func (t *ast) parseNode(tokenizer *tokenizer) node {
	run, token, err := tokenizer.next() // TODO: properly evaluate
	if errors.Is(err, io.EOF) {
		return nil
	}

	switch token {
	case GRAPH:
		rawNums := strings.Split(run, " ")
		nums := make([]int, len(rawNums))
		for i, s := range rawNums {
			nums[i], err = strconv.Atoi(s)
			if err != nil { // NOTE: shouldn't happen, but shows the need for another error handling layer over the core tokenizer
				panic(fmt.Errorf("tokenizer returned a non-int slice of numbers %v: %w", rawNums, err))
			}
		}
		return newGraph(nums, t.treeWidth)
	case OPEN:
		left := t.parseNode(tokenizer)
		tokenizer.next() // accounts for the next expected open brace
		return &addition{
			left:  left,
			right: t.parseNode(tokenizer),
		}
	}

	return nil
}

// node could either be an addition of two nodes, or a graph
type node interface {
	astNode()
}


// addition of two graphs
type addition struct {
	left  node
	right node
}

// sum recursively sums up the graph tree
func (a *addition) sum() *graph {
	panic("not implemented")
}

func (a addition) astNode() {}

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

// degreeSequence for assignment part 1
func (g *graph) degreeSequence() string {
	panic("not implemented")
}

// adjacencyList for assignment part 2
func (g *graph) adjacencyList() string {
	panic("not implemented")
}

func (g graph) astNode() {}

func (g *graph) String() string {
	var sb strings.Builder
	sb.WriteString("G = (V, E)\n")
	sb.WriteString(fmt.Sprintf("V = %v \n", g.vertices))
	sb.WriteString("E = ")
	for i, edge := range g.edges {
		sb.WriteString(fmt.Sprintf("(%d, %d)", edge.a, edge.b))
		if i+1 < len(g.edges) {
			sb.WriteString(", ")
		}
	}
	sb.WriteString(fmt.Sprintf("\n with boundary = %v", g.boundary))

	return sb.String()
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
		boundary: make([]int, treeWidth+1),
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
	// we want the index to increment on any return
	defer func() {
		i.index++
	}()

	for {
		if i.index >= len(i.input) {
			return "", NULL, io.EOF
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

		// all else skipped
		i.index++
	}
}
