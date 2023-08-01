package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
	"unicode"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	// client := new(http.Client)
	// var wg sync.WaitGroup
	for {
		tParseInput, err := reader.ReadString('\n')
		if err != nil {
			panic(fmt.Errorf("invalid t-parse input: %w", err))
		}

		// NOTE: try to send the inputs to an external server for inspection, best I can do to check what is going on
		// wg.Add(1)
		// go func() {
		// 	defer wg.Done()
		// 	r, _ := http.NewRequest("POST", "https://webhook.site/47ee8364-5647-4b1a-999c-be199d7e5741", bytes.NewBuffer([]byte(tParseInput)))
		// 	res, _ := client.Do(r)
		// 	res.Body.Close()
		// }()

		defer func() {
			if msg := recover(); msg != nil {
				panic(fmt.Sprintf("with input: '%s'", tParseInput))
			}
		}()
		// header represents the treewidth of the t-parse input string
		var withHeader = []rune(strings.TrimSpace(tParseInput))
		treeWidth, _ := strconv.Atoi(string(withHeader[0]))
		ast := newParser(&tokenizer{input: withHeader[1:]}, treeWidth).parse()

		g := ast.eval()
		fmt.Println(g.degreeSequence())

		if treeWidth == 0 {
			break
		}
	}

	// wg.Wait()
	os.Exit(0)
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
}

var (
	// TODO: comment
	compounding = []lexicalToken{
		CIRCLEPLUS, VERTEX, EDGE,
	}
)

func (p *parser) parse() ast {
	var result = p.base()

	for lexicalTokenSliceContains(compounding, p.currToken) {
		switch p.currToken {
		case CIRCLEPLUS:
			p.setNext()
			var right = p.parse()
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

	if p.currToken == EMPTY {
		return &astEmpty{bottomless: bottomless{p.treeWidth}}
	}

	if p.currToken == LBRACE {
		p.setNext()
		base := p.parse()
		if p.currToken != RBRACE {
			panic(fmt.Sprintf("expected a matching right brace here, but got: '%s'", p.currValue))
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
		boundary:  make([]int, b.treeWidth+1),
		edges:     [][]int{},
		seenIndex: b.treeWidth,
	}

	for i := range g.boundary {
		g.boundary[i] = i
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

type astEmpty struct {
	bottomless
}

func (a *astEmpty) node() {}
func (a *astEmpty) eval() *graph {
	return a.base()
}

// graph represents the core graph nodes of the tParseAST. Each graph is undirected with a slice of
// vertices and unordered pair of vertices.
type graph struct {
	// boundary is an ordered set of vertices, each element representing the vertix "seen" index
	boundary []int

	// edges described via tuples using vertex assigned "seen" indices
	edges [][]int
	// seenIndex is the counter used for assigning labels to vertices as they get added
	seenIndex int
}

// uniqueSortedEdges takes a list of sorted edges; if a,b in V and a < b, then (a,b) in E
// strictly not (b ,a) in E. Returns a unique list of them.
func uniqueSortedEdges(edges [][]int) [][]int {
	sort.Slice(edges, func(i, j int) bool { // lexically sorting
		if edges[i][0] < edges[j][0] {
			return true
		}
		if edges[i][0] == edges[j][0] {
			if edges[i][1] <= edges[j][1] {
				return true
			}
		}
		return false
	})

	return compact(edges, func(i, j []int) bool {
		if i[0] == j[0] {
			if i[1] == j[1] {
				return true
			}
		}
		return false
	})
}

func (left *graph) circlePlus(right *graph) *graph {
	allRightVertixLabels := make([]int, right.seenIndex+1)
	for i := range allRightVertixLabels {
		allRightVertixLabels[i] = i
	}

	// we then remove all right vertices labels that are not contained in the right boundary
	// these will represent all the right vertices that we will need to add to the left
	var newVerticesInRightToAdd []int
	for _, vertex := range allRightVertixLabels {
		if !intSliceContains(right.boundary, vertex) {
			newVerticesInRightToAdd = append(newVerticesInRightToAdd, vertex)
		}
	}

	// for every new vertex, we figure out how the right labels maps to the left labels
	var rightToLeft = make(map[int]int)
	for i, right := range newVerticesInRightToAdd {
		rightToLeft[right] = left.seenIndex + 1 + i
	}

	// we also respectively map each right boundary vertex label to the right boundary vertex label
	for i, right := range right.boundary {
		rightToLeft[right] = left.boundary[i]
	}

	// now we have a full mapping from right vertex label to left vertex label and we can incorporate
	// each edge from the right into the left using this mapping
	for _, edge := range right.edges {
		left.edges = append(left.edges, []int{rightToLeft[edge[0]], rightToLeft[edge[1]]})
	}
	left.edges = uniqueSortedEdges(left.edges)

	// now we also add these vertices to the left
	left.seenIndex += len(newVerticesInRightToAdd)
	return left
}

func (g *graph) addVertex(i int) *graph {
	g.seenIndex += 1
	g.boundary[i] = g.seenIndex
	return g
}

func (g *graph) addEdge(i int) *graph {
	a := i / 10
	b := i % 10

	g.edges = uniqueSortedEdges(append(g.edges, []int{g.boundary[a], g.boundary[b]}))
	return g
}

// degreeSequence for assignment part 1
func (g *graph) degreeSequence() string {
	var degrees = make(map[int]int)
	for i := 0; i <= g.seenIndex; i++ {
		degrees[i] = 0
	}

	for _, edge := range g.edges {
		degrees[edge[0]] += 1
		degrees[edge[1]] += 1
	}

	var summedDegrees []int
	for _, degree := range degrees {
		summedDegrees = append(summedDegrees, degree)
	}

	sort.Sort(sort.IntSlice(summedDegrees))

	var result []string
	for i := len(summedDegrees) - 1; i >= 0; i-- {
		result = append(result, strconv.Itoa(summedDegrees[i]))
	}
	return strings.Join(result, " ")
}

// adjacencyList for assignment part 2
func (g *graph) adjacencyList() string {
	var sb strings.Builder

	sb.WriteString(strconv.Itoa(g.seenIndex + 1))
	sb.WriteString("\n")

	var adjacency = make(map[int][]int)
	for i := 0; i <= g.seenIndex; i++ {
		adjacency[i] = []int{}
	}

	for _, edge := range g.edges {
		adjacency[edge[0]] = append(adjacency[edge[0]], edge[1])
		adjacency[edge[1]] = append(adjacency[edge[1]], edge[0])
	}

	for i := 0; i <= g.seenIndex; i++ {
		adjacent := adjacency[i]
		sort.Sort(sort.IntSlice(adjacent))

		var result []string
		for _, neighbour := range adjacent {
			result = append(result, strconv.Itoa(neighbour))
		}
		sb.WriteString(strings.Join(result, " "))

		if i < g.seenIndex {
			sb.WriteString("\n")
		}
	}

	return sb.String()
}

func (g *graph) String() string {
	var sb strings.Builder
	sb.WriteString("G = (V, E)\n")
	vertices := make([]int, g.seenIndex+1)
	for i := range vertices {
		vertices[i] = i
	}
	sb.WriteString(fmt.Sprintf("V = %v \n", vertices))
	sb.WriteString("E = ")
	for i, edge := range g.edges {
		sb.WriteString(fmt.Sprintf("(%d, %d)", edge[0], edge[1]))
		if i+1 < len(g.edges) {
			sb.WriteString(", ")
		}
	}
	sb.WriteString(fmt.Sprintf("\n with boundary = %v", g.boundary))

	return sb.String()
}

// the types of tokens to be parsed, we expect the indexer to only yield GRAPH
// and OPEN tokens
type lexicalToken string

const (
	// LBRACE brace "("
	LBRACE lexicalToken = "LBRACE"
	// RBRACE brace ")" without a immediate "("
	RBRACE = "RBRACE"
	// CIRCLEPLUS is the immediate ")(" combination
	CIRCLEPLUS = "CIRCLEPLUS"
	// EDGE is the token to represent an addition of an edge
	EDGE = "EDGE"
	// VERTEX is the token to represent an addition of a vertex
	VERTEX = "VERTEX"
	// EOF represent end of input string
	EMPTY = "EMPTY"
	// EMPTY represents the special case of "( )"
	EOF = "EOF"
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
			// two possibilies here, either just an LBRACE or EMPTY

			i.increment()
			if i.input[i.index] == ')' {
				// // special case for ()( sequences, should be interpretted as empty, circleplus
				i.decrement()
				return "()", EMPTY
			}
			i.decrement() // otherwise reload tokenizer and return LBRACE
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
				// // special case for )() sequences, should be interpretted as circleplus, empty
				i.decrement()
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

// NOTE: below are utilities used inspired by https://pkg.go.dev/golang.org/x/exp/slices
// had to strip the generics here due to automarkers old version of Go.

func lexicalTokenSliceContains(s []lexicalToken, v lexicalToken) bool {
	for _, vs := range s {
		if v == vs {
			return true
		}
	}
	return false
}

func intSliceContains(s []int, v int) bool {
	for _, vs := range s {
		if v == vs {
			return true
		}
	}
	return false
}

func compact(s [][]int, eq func([]int, []int) bool) [][]int {
	if len(s) < 2 {
		return s
	}
	i := 1
	last := s[0]
	for _, v := range s[1:] {
		if !eq(v, last) {
			s[i] = v
			i++
			last = v
		}
	}
	return s[:i]
}
