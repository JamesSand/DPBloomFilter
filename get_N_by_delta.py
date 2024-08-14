from scipy.special import comb, perm

# W depends on m, na, and k

# we first need to know PNF of Y
# Y only depends on m and k
def Y_PMF(m, k):
    # Y value range is [1, k]
    prob_list = [1 / (m ** (k - 1))]
    # calcualte from 2 to k
    for y in range(2, k + 1):
        prob = (comb(m, y) * (y ** k)) / (m ** k)
        for i, prev_prob in enumerate(prob_list):
            # start from 0, change to start from 1
            i = i + 1
            prob -= prev_prob * comb(m - i, y - i)
        prob_list.append(prob)
    return prob_list

# we need the probability of z, conditioned on a and b
def Z_cond_a_b(z, a, b, m):
    if b > a:
        # make sure a \geq b
        a, b = b, a

    # We must have z > max(a, b)
    if z < a:
        return 0.0

    t = z - a
    prob = (perm(m, a) * comb(b, t) * perm(m - a, t) * perm(a, b - t)) / (perm(m, a) * perm(m, b))
    return prob

# the function return is the PMF of W
def W_PMF(m, na, k):
    Y_prob_list = Y_PMF(m, k)
    p0 = (1 - 1 / m) ** ((na - 1) * k)
    # w value range is [0, 2k]
    prob_list = []
    for w in range(0, 2 * k + 1):
        # calcualte probability for each w
        prob = 0.0
        for a in range(1, k + 1):
            for b in range(1, k + 1):
                for z in range(1, a + b + 1):
                    if z < max(a, b):
                        continue

                    n2 = 2 * z - a - b
                    if n2 < w:
                        continue

                    item1 = comb(n2, w) * (p0 ** w) * (1 - p0) ** (n2 - w)

                    item2 = Z_cond_a_b(z, a, b, m) * Y_prob_list[a - 1] * Y_prob_list[b - 1]

                    cur_prob = item1 * item2

                    prob += cur_prob

        prob_list.append(prob)
    return prob_list

def get_N_by_delta(m, na, k, delta):
    w_prob_list = W_PMF(m, na, k)
    print(f"W prob list {w_prob_list}")
    print(sum(w_prob_list))
    cumulation = 0.0
    for i, w_prob in enumerate(w_prob_list):
        cumulation += w_prob
        if cumulation >= (1 - delta):
            return i
    
    raise Exception("Cannot find N")


# ########### test Y code ###########
# m = 100
# k = 10

# y_prob_list = Y_PMF(m, k)
# print(y_prob_list)
# print(sum(y_prob_list))
# ########### test Y code ###########

# ########## test Z code ###########
# m = 10
# a = 5
# b = 5
# prob_list = []
# for z in range(max(a, b), a + b + 1):
#     prob = Z_cond_a_b(z, a, b, m)
#     prob_list.append(prob)
# print(prob_list)
# print(sum(prob_list))
# ########## test Z code ###########

# ########## test W code ###########
# m = 10
# na = 1
# k = 2
# y_prob_list = Y_PMF(m, k)
# # print(y_prob_list)
# # print(sum(y_prob_list))
# w_prob_list = W_PMF(m, na, k)
# print(f"m = {m}, na = {na}, k = {k}")
# print(w_prob_list)
# for i, w_prob in enumerate(w_prob_list):
#     print(f"w = {i}, prob = {w_prob}")
# print(sum(w_prob_list))
# ########## test W code ###########


if __name__ == "__main__":
    k = 5
    # k = (m / n) ln2
    # 3 / ln2 * n = m
    log2m = 19
    m = int(2 ** log2m)
    na = int(1e5)

    delta_list = [1e-1, 1e-2, 1e-3, 1e-4]
    for delta in delta_list:
        N = get_N_by_delta(m, na, k, delta)
        print(f"log2m = {log2m}, na = {na}, k = {k}, delta = {delta}, N = {N}")
