"""
    Justin went through an interview question with Booking.com, it was of special interest to me
    since it was a classic search problem and I built a strong understanding of the problem via a
    very successful knee jerk intuition due to this class...

    The problem, given a set of flights (directed); [["Amsterdam", "Bern"], ["Berlin", "Munich"], ["Berlin", "Shanghai"], ...],
    yield a single connected flight across all mentioned paths.
"""

input = [['A', 'B'], ['B', 'C'], ['C', 'A'], ['B', 'D']]

def find_path(input):
    if len(input) == 0:
        return []

    first = input.pop()

    node = {
        "path": [first],
        "remaining_paths": input
    }
    frontier = [node]

    while len(frontier) != 0:
        so_far = frontier.pop() ## treats it like a DFS search, pop(0) treats it like a BFS search (stack vs queue)
        if so_far["remaining_paths"] == []:
            return so_far["path"]

        def give_me_the_ends(path_so_far): # candidates are either the start or the end
            return path_so_far[0][0], path_so_far[-1][-1]

        beginning, tail = give_me_the_ends(so_far["path"])

        for index, candidate_path in enumerate(so_far["remaining_paths"]):
            if tail == candidate_path[0]:
                frontier.append({
                                    "path": so_far["path"] + [candidate_path],
                                    "remaining_paths": so_far["remaining_paths"][:index] + so_far["remaining_paths"][index+1:]
                                })
            if beginning == candidate_path[1]:
                frontier.append({
                                    "path": [candidate_path] + so_far["path"],
                                    "remaining_paths": so_far["remaining_paths"][:index] + so_far["remaining_paths"][index+1:]
                                })

print(find_path(input))
