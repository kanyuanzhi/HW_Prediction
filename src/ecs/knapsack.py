def knapsack(v, w, c, n, m):
    jMax = min(w[n] - 1, c)
    for j in range(jMax + 1):
        m[n][j] = 0
