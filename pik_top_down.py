from functools import lru_cache
import time


@lru_cache(maxsize=None)  # dp like approach (store all intermediate steps in cache)
def binom(n, k):
    if k < 0 or k > n:
        return 0
    if n == 0:
        return 1
    return binom(n - 1, k - 1) + binom(n - 1, k)


@lru_cache(maxsize=None)  # dp like approach (store all intermediate steps in cache)
def W(u, v):
    """
    Recursive function to compute W_u(v). See https://arxiv.org/pdf/math-ph/0009028
    """

    # Base case
    if v == 0:
        return 1 if u == 0 else 0

    total = 0
    for i in range(1, v + 1):
        binom_i = binom(v - 1, i - 1)
        for j in range(v - i, u - i + 1):
            w_i_j = W(j, v - i)
            for l in range(0, u - i - j + 1):
                total += W(u - i - j, l) * binom(l + i - 1, i - 1) * binom_i * w_i_j
    return total


def compute_moments(n):
    """
    Compute the sequence A094149 up to the n-th number.
    Parameters:
        n (int): The index of the sequence up to which we compute
    Returns:
        list: Sequence values up to the n-th term
    """
    sequence = []
    for k in range(1, n + 1):
        m_k = sum(W(k, r) for r in range(k + 1))
        sequence.append(m_k)
    return sequence


if __name__ == "__main__":
    start = time.time()
    sequence = compute_moments(100)
    print(time.time()-start)
    print(sequence)
