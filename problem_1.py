# Given an array A of integer of size n and an integer as B which will be length of subsequence
# count - will return number of non-empty subsequences of A of size B having sum <= 1000
import itertools

A = [5, 17, 1000, 11]
B = 4
count = 0


def find_subsets(a: list, b: int) -> list:
    """
    A: The set for which you want to find subsets
    B: The number of elements in the subset
    """
    return list(set(itertools.combinations(a, b)))


# subsets give unique no of non-empty subsequences
subsets = find_subsets(A, B)

for subset in subsets:
    if sum(subset) <= 1000:
        count += 1
print(count)

