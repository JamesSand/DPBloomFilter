from scipy.special import comb, perm
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

import argparse

parser = argparse.ArgumentParser()
# parser.add_argument('--name', type=str, required=True)
parser.add_argument("--save_type", type=str, required=True)

args = parser.parse_args()

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
    # print(f"Y prob list {Y_prob_list}")
    p0 = (1 - 1 / m) ** ((na - 1) * k)
    # print(f"p0 {p0}")
    # print(f"2k * p0 {2 * k * p0}")
    # w value range is [0, 2k]
    prob_list = []
    for w in range(0, 2 * k + 1):
        # print(f"w {w}")
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

                    # if w == 3 and cur_prob > 0.0:
                    #     print(f"z = {z}, a = {a}, b = {b}, w = {w}, prob = {cur_prob}")
                    #     print(f"item1 {item1} item2 {item2}")
                    #     print(f"Z cond {Z_cond_a_b(z, a, b, m)} Y1 {Y_prob_list[a - 1]} Y2 {Y_prob_list[a - 1]}")

                    prob += cur_prob

        prob_list.append(prob)
    return prob_list

def get_N_by_delta(m , na, k, delta):
    w_prob_list = W_PMF(m, na, k)
    print(f"W prob list {w_prob_list}")
    print(sum(w_prob_list))
    cumulation = 0.0
    for i, w_prob in enumerate(w_prob_list):
        cumulation += w_prob
        if cumulation >= (1 - delta):
            return i
    
    raise Exception("Cannot find N")

k = 3
# k = (m / n) ln2
# 3 / ln2 * n = m
log2m = 18
m = int(2 ** log2m)
na = int(1e5)

w_prob_list = W_PMF(m, na, k)

# delta_list = [1e-1, 1e-2, 1e-3, 1e-4]
# for delta in delta_list:
#     N = get_N_by_delta(m, na, k, delta)
#     print(f"log2m = {log2m}, na = {na}, k = {k}, delta = {delta}, N = {N}")

font_size = 16

# Given probability distribution list
probabilities = w_prob_list

# Corresponding values of the random variable
values = list(range(len(probabilities)))

# Create figure and axis
fig, ax = plt.subplots()

# Plot the bar chart
bars = ax.bar(values, probabilities, color='skyblue', edgecolor='black', width=1.0)

# Set x-axis label
ax.set_xlabel('W', fontsize=font_size)
# Set y-axis label
ax.set_ylabel('Probability in Percentage', fontsize=font_size)
# Set chart title
ax.set_title('Probability Mass Function of W', fontsize=font_size)

# Format y-axis as percentages
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))

# Add grid lines for better readability
ax.grid(axis='y', linestyle='--', alpha=0.7)

ax.tick_params(axis='both', which='major', labelsize=12)

# Add probability values (as percentages) on top of the bars
for bar, prob in zip(bars, probabilities):
    height = bar.get_height()
    ax.annotate(f'{prob:.1%}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 0),  # 3 points vertical offset
                textcoords='offset points',
                ha='center', va='bottom', fontsize=11)

# # Display the plot
# plt.show()


# base_dir = "w_figs"
save_fig_dir = "draw/figs"
os.makedirs(save_fig_dir, exist_ok=True)
if args.save_type == "pdf":
    save_name = "w_pmf.pdf"
    save_path = os.path.join(save_fig_dir, save_name)
    plt.savefig(save_path, format='pdf', bbox_inches='tight', pad_inches=0.05)

elif args.save_type == "png":
    save_name = "w_pmf.png"
    save_path = os.path.join(save_fig_dir, save_name)
    plt.savefig(save_path, format='png', bbox_inches='tight', pad_inches=0.05)


print(f"figure save to {save_path}")

