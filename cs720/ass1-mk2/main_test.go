package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestUniqueSortedEdges(t *testing.T) {
	type test struct {
		name     string
		input    [][]int
		expected [][]int
	}

	tests := []test{
		{
			name: "basic uniqueness",
			input: [][]int{
				{1, 2},
				{1, 2},
				{1, 2},
				{1, 2},
				{1, 2},
			},
			expected: [][]int{
				{1, 2},
			},
		},
		{
			name: "same same",
			input: [][]int{
				{1, 2},
				{1, 3},
			},
			expected: [][]int{
				{1, 2},
				{1, 3},
			},
		},
		{
			name: "order agnostic",
			input: [][]int{
				{1, 3},
				{1, 3},
				{1, 3},
				{1, 3},
				{1, 2},
			},
			expected: [][]int{
				{1, 3},
				{1, 2},
			},
		},
		{
			name: "first index cases",
			input: [][]int{
				{1, 3},
				{2, 3},
				{2, 3},
				{2, 3},
				{3, 2},
			},
			expected: [][]int{
				{1, 3},
				{2, 3},
				{3, 2},
			},
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			assert.ElementsMatch(t, test.expected, uniqueSortedEdges(test.input))
		})
	}
}

func TestCirclePlus(t *testing.T) {
	type test struct {
		name     string
		left     *graph
		right    *graph
		expected *graph
	}

	tests := []test{
		{
			name: "base",
			left: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{},
				seenIndex: 1,
			},
			right: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{},
				seenIndex: 1,
			},
			expected: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{},
				seenIndex: 1,
			},
		},
		{
			name: "right has orphaned vertex",
			left: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{},
				seenIndex: 1,
			},
			right: &graph{
				boundary:  []int{0, 2},
				edges:     [][]int{},
				seenIndex: 2,
			},
			expected: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{},
				seenIndex: 2,
			},
		},
		{
			name: "right has one edge",
			left: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{},
				seenIndex: 1,
			},
			right: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{{0, 1}},
				seenIndex: 1,
			},
			expected: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{{0, 1}},
				seenIndex: 1,
			},
		},
		{
			name: "left has one edge",
			left: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{{0, 1}},
				seenIndex: 1,
			},
			right: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{},
				seenIndex: 1,
			},
			expected: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{{0, 1}},
				seenIndex: 1,
			},
		},
		{
			name: "both have overlapping edges",
			left: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{{0, 1}},
				seenIndex: 1,
			},
			right: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{{0, 1}},
				seenIndex: 1,
			},
			expected: &graph{
				boundary:  []int{0, 1},
				edges:     [][]int{{0, 1}},
				seenIndex: 1,
			},
		},
		{
			name: "adding together two different edges",
			left: &graph{
				boundary:  []int{0, 1, 2},
				edges:     [][]int{{0, 1}},
				seenIndex: 2,
			},
			right: &graph{
				boundary:  []int{0, 1, 2},
				edges:     [][]int{{1, 2}},
				seenIndex: 2,
			},
			expected: &graph{
				boundary:  []int{0, 1, 2},
				edges:     [][]int{{0, 1}, {1, 2}},
				seenIndex: 2,
			},
		},
		{
			name: "stitching by the boundary",
			left: &graph{
				boundary:  []int{0, 1, 2},
				edges:     [][]int{{0, 2}},
				seenIndex: 2,
			},
			right: &graph{
				boundary:  []int{0, 1, 3},
				edges:     [][]int{{0, 3}},
				seenIndex: 3,
			},
			expected: &graph{
				boundary:  []int{0, 1, 2},
				edges:     [][]int{{0, 2}},
				seenIndex: 3,
			},
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			actual := test.left.circlePlus(test.right)

			assert.Equal(t, test.expected.seenIndex, actual.seenIndex)
			assert.ElementsMatch(t, test.expected.boundary, actual.boundary)
			assert.ElementsMatch(t, test.expected.edges, actual.edges)
		})
	}
}

func TestDegreeSequence(t *testing.T) {
	type test struct {
		name     string
		graph    *graph
		expected string
	}

	tests := []test{
		{
			name: "no edges",
			graph: &graph{
				boundary:  []int{8, 9, 10, 11, 12},
				edges:     [][]int{},
				seenIndex: 12,
			},
			expected: "0 0 0 0 0 0 0 0 0 0 0 0 0",
		},
		{
			name: "equal",
			graph: &graph{
				boundary:  []int{0, 1, 2, 3, 4, 5},
				edges:     [][]int{{0, 1}, {2, 3}, {4, 5}},
				seenIndex: 5,
			},
			expected: "1 1 1 1 1 1",
		},
		{
			name: "overlapping run, should be desc",
			graph: &graph{
				boundary:  []int{0, 1, 2, 3, 4, 5},
				edges:     [][]int{{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 5}},
				seenIndex: 5,
			},
			expected: "2 2 2 2 1 1",
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			assert.Equal(t, test.expected, test.graph.degreeSequence())
		})
	}
}
