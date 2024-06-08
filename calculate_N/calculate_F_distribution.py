from scipy.special import comb, perm

m = int(2 ** 19)
na = int(1e5)
k = 4

def W_PMF(w):
    prob = 0.0
    for a in range(1, k + 1):
        for b in range(1, k + 1):
            for z in range(1, a + b):
                n2 = a + b - z
                if n2 < w:
                    continue

                cur_res = comb(n2, w) * \
                    ((1 - 1/m) ** ((na - 1) * k * w)) * \
                    ((1 - (1 - 1/m) ** ((na - 1) * k)) ** (n2 - w)) * \
                    (perm(a + b, z) * (z ** n2) / (m ** (a + b))) * \
                    (perm(k, a) * (a ** (k - a)) / (m ** a)) * \
                    (perm(k, b) * (b ** (k - b)) / (m ** b))
                
                prob += cur_res

    return prob

single_prob_list = []
for w in range(0, 2 * k + 1):
    single_prob_list.append(W_PMF(w))

# print(single_prob_list)
print("-" * 50)
print("single")
for i, prob in enumerate(single_prob_list):
    print(f"{i}: {prob}")
print("-" * 50)

cumulative_prob_list = []
cumulative_prob = 0.0
for prob in single_prob_list:
    cumulative_prob += prob
    cumulative_prob_list.append(cumulative_prob)

print("-" * 50)
print("cumulative")
for i, prob in enumerate(cumulative_prob_list):
    print(f"{i}: {prob}")
print("-" * 50)

# # permutation
# A=perm(4,2)
# # combination
# C=comb(45,2)
# print(A,C)


