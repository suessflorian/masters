package main

import (
	"fmt"
	"strconv"
	"strings"
	"unicode"

	"golang.org/x/exp/slices"
)

func main() {
	tParseInput := "3 ( ( 30 ) ( 20 ) 0 21 10 30 20 )"
	fmt.Printf("parsing: \"%s\" \n", tParseInput)

	// header represents the treewidth of the t-parse input string
	var withHeader = []rune(strings.TrimSpace(tParseInput))
	treeWidth, _ := strconv.Atoi(string(withHeader[0]))
	ast := newParser(&tokenizer{input: withHeader[1:]}, treeWidth).parse() // TODO: returns this AST

	fmt.Println(ast)
}

type parser struct {
	treeWidth int

	tokenizer *tokenizer
	currToken lexicalToken
	currValue string
}

// newParser returns an initialised parser
func newParser(tokenizer *tokenizer, treeWidth int) *parser {
	parser := &parser{
		tokenizer: tokenizer,
		treeWidth: treeWidth,
	}
	parser.setNext()
	return parser
}

// setNext sets the parser position onto the next tokenized literal
func (p *parser) setNext() {
	p.currValue, p.currToken = p.tokenizer.next()
	fmt.Println("-", p.currValue)
}

var (
	// TODO: comment
	compounding = []lexicalToken{
		CIRCLEPLUS, VERTEX, EDGE,
	}
)

func (p *parser) parse() ast {
	var result = p.base()

	for slices.Contains(compounding, p.currToken) {
		switch p.currToken {
		case CIRCLEPLUS:
			p.setNext()
			var right = p.base()
			result = &astCirclePlus{
				left:  result,
				right: right,
			}
		case VERTEX:
			vertex, err := strconv.Atoi(p.currValue)
			if err != nil {
				panic(fmt.Errorf("failed to parse vertex int: %w", err))
			}
			result = &astVertex{
				bottomless: bottomless{p.treeWidth}, // TODO: can't we remove?
				child:      result,
				vertex:     vertex,
			}
			p.setNext()
		case EDGE:
			edge, err := strconv.Atoi(p.currValue)
			if err != nil {
				panic(fmt.Errorf("failed to parse vertex int: %w", err))
			}
			result = &astEdge{
				bottomless: bottomless{p.treeWidth},
				child:      result,
				edge:       edge,
			}
			p.setNext()
		}
	}
	return result
}

func (p *parser) base() ast {
	defer func() {
		p.setNext()
	}()

	if p.currToken == LBRACE {
		p.setNext()
		base := p.parse()
		if p.currToken != RBRACE {
			panic(fmt.Sprint("wtf.. i expect a matching right brace here, but got: ", p.currValue))
		}
		return base
	}

	if p.currToken == VERTEX {
		vertex, err := strconv.Atoi(p.currValue)
		if err != nil {
			panic(fmt.Errorf("failed to base vertex: %w", err))
		}
		return &astVertex{
			bottomless: bottomless{p.treeWidth},
			child:      nil,
			vertex:     vertex,
		}
	}

	if p.currToken == EDGE {
		edge, err := strconv.Atoi(p.currValue)
		if err != nil {
			panic(fmt.Errorf("failed to parse base edge: %w", err))
		}
		return &astEdge{
			bottomless: bottomless{p.treeWidth},
			child:      nil,
			edge:       edge,
		}
	}

	return nil
}

// ast could either be an addition of two asts, or a leaf (graph)
type ast interface {
	node()
	eval() *graph
}

type astCirclePlus struct {
	left  ast
	right ast
}

func (a *astCirclePlus) node() {}
func (a *astCirclePlus) eval() *graph {
	return a.left.eval().circlePlus(a.right.eval())
}

// bottomless is a utility that separates the property of the astEdge and astVertex
// being optionally childless. If a graph is not set for an astEdge or astVertex child
// it means we begin the construction of a graph via the treeWidth parameter exclusively.
type bottomless struct {
	treeWidth int
}

// base constructs a graph given a treewidth set.
func (b *bottomless) base() *graph {
	g := &graph{
		boundary: make([]int, b.treeWidth+1),
		raw:      []int{},
		edges:    []pair{},
		vertices: []int{},
	}

	for i := range g.boundary {
		g.boundary[i] = i
		g.vertices = append(g.vertices, i)
	}

	return g
}

type astEdge struct {
	bottomless
	child ast
	edge  int
}

func (a *astEdge) node() {}
func (a *astEdge) eval() *graph {
	if a.child == nil {
		return a.base().addEdge(a.edge)
	}
	return a.child.eval().addEdge(a.edge)
}

type astVertex struct {
	bottomless
	child  ast
	vertex int
}

func (a *astVertex) node() {}
func (a *astVertex) eval() *graph {
	if a.child == nil {
		return a.base().addVertex(a.vertex)
	}
	return a.child.eval().addVertex(a.vertex)
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

func (g *graph) circlePlus(right *graph) *graph {
	panic("not implemented")
}

func (g *graph) addVertex(i int) *graph {
	panic("not implemented")
}

func (g *graph) addEdge(i int) *graph {
	panic("not implemented")
}

// degreeSequence for assignment part 1
func (g *graph) degreeSequence() string {
	panic("not implemented")
}

// adjacencyList for assignment part 2
func (g *graph) adjacencyList() string {
	panic("not implemented")
}

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
type lexicalToken int

const (
	// LBRACE brace "("
	LBRACE lexicalToken = iota
	// RBRACE brace ")" without a immediate "("
	RBRACE
	// CIRCLEPLUS is the immediate ")(" combination
	CIRCLEPLUS
	// EDGE is the token to represent an addition of an edge
	EDGE
	// VERTEX is the token to represent an addition of a vertex
	VERTEX
	// EOF represent end of input string
	EOF
)

// tokenizer is used to statefully increment through an input string skipping all whitespace
// allow an iteration through tokens
type tokenizer struct {
	index int
	input []rune
}

// increment the tokenizer to the next token, making sure to skip any whitespace at all
// times.
func (i *tokenizer) increment() {
	i.index += 1
	if i.index >= len(i.input) {
		return
	}
	if unicode.IsSpace(i.input[i.index]) {
		i.increment()
	}
}

// decrement the tokenizer to the previous token, making sure to skip any whitespace at all
// times.
func (i *tokenizer) decrement() {
	i.index -= 1
	if i.index <= 0 {
		return
	}
	if unicode.IsSpace(i.input[i.index]) {
		i.decrement()
	}
}

// next returns a triple, the raw parsed string and the associated token. Returns an
// io.EOF error when the end of the string has been hit.
func (i *tokenizer) next() (string, lexicalToken) {
	// we want the index to increment on any return
	defer func() {
		i.increment()
	}()

	for {
		if i.index >= len(i.input) {
			return "", EOF
		}

		r := i.input[i.index]
		if r == '(' {
			return "(", LBRACE
		}
		if r == ')' {
			// two possibilies here, either just an RBRACE or CIRCLEPLUS

			// first, is there even another character available?
			if i.index+1 >= len(i.input) {
				return ")", RBRACE
			}

			i.increment()
			if i.input[i.index] == '(' {
				return ")(", CIRCLEPLUS
			}
			i.decrement() // otherwise reload tokenizer and return RBRACE
			return ")", RBRACE
		}

		// two possibilities here, either a vertex addition, or an edge
		if unicode.IsNumber(r) {
			// first, is there even another character available?
			if i.index+1 >= len(i.input) {
				return string(r), VERTEX
			}

			i.index++
			if unicode.IsNumber(i.input[i.index]) {
				return string(r) + string(i.input[i.index]), EDGE
			}
			i.index--
			return string(r), VERTEX
		}

		// all else skipped for now...
		i.increment() // NOTE: what if we use \n as a means of terminating a line
	}
}
