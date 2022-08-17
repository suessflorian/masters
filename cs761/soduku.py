def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

rows, cols = 'ABCDEFGHI', '123456789'
squares = cross(rows, cols)

unit_list = (
        [cross(rows, col) for col in cols] +
        [cross(row, cols) for row in rows] +
        [cross(box_rows, box_cols) for box_rows in ('ABC','DEF','GHI') for box_cols in ('123','456','789')]
)

constraints = {square: [unit for unit in unit_list if square in unit] for square in squares}
print(constraints)
