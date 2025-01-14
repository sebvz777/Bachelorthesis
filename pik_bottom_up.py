import time


def precompute_binom(n):
    """
    Precompute binomial coefficients up to n
    """
    binom = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        binom[i][0] = binom[i][i] = 1
        for k in range(1, i):
            binom[i][k] = binom[i - 1][k - 1] + binom[i - 1][k]
    return binom


def precompute_W(max_u, max_v, binom):
    """
    Precompute W(u, v) using DP bottom up.
    """
    W = [[0] * (max_v + 1) for _ in range(max_u + 1)]

    # Base case: W(0, 0) = 1
    W[0][0] = 1

    # Fill the DP table for W(u, v)
    for u in range(max_u + 1):
        for v in range(max_v + 1):
            if v == 0:
                W[u][v] = 1 if u == 0 else 0  # simplification 1
                continue
            if u == 0:
                W[u][v] = 0  # simplification 2
                continue
            total = 0
            for i in range(1, v + 1):
                binom_i = binom[v - 1][i - 1]
                for j in range(v - i, u - i + 1):
                    w_i_j = W[j][v - i]
                    for l in range(0, u - i - j + 1):
                        total += (
                            W[u - i - j][l]
                            * binom[l + i - 1][i - 1]
                            * binom_i
                            * w_i_j
                        )
            W[u][v] = total
    return W


def compute_moments(n):
    """
    Compute the sequence A094149 up to the n-th number using precomputed DP tables (bottom up).
    """
    # Precompute binomial coefficients and W(u, v) values
    binom = precompute_binom(n)
    W = precompute_W(n, n, binom)

    # Compute the moments
    sequence = []
    for k in range(1, n + 1):
        m_k = sum(W[k][r] for r in range(k + 1))
        sequence.append(m_k)
    return sequence


if __name__ == "__main__":
    start = time.time()
    result = compute_moments(100)
    print(f"Time taken: {time.time() - start:.2f} seconds")
    print(result)
