# Near-duplicate detection

Recall, Jaccard and Containment similiarity via `shingles`. These improve on `exact hash` matching of objects and `edit distance`. But these *do not* scale...

- shingles takes up a lot of space (to create sets of two comparing documents)

## Odd Sketches
> Representing set of shingles as fixed size bit vectors.

Then we use bit operations like `XOR`. Bit slice differences can be marked, and we introduce a tolerance. Difference < tolerance => similar.

