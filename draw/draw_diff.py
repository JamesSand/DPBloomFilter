import matplotlib.pyplot as plt
import os
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import ticker
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, required=True)
parser.add_argument("--save_type", type=str, required=True)

args = parser.parse_args()

save_fig_dir = "draw/figs"
os.makedirs(save_fig_dir, exist_ok=True)


log_data_base_dir="log_data"

target_key_mapping = {
    "random" : "Random",
    "inside" : "True_Negative",
    "outside" : "False_Positive"
}

title_mapping = {
    "random" : "Total Error",
    "inside" : "True Negative Error",
    "outside" : "False Positive Error"
}

log2m_values = [20, 21, 22, 23, 24]
# n_values = ["1e3", "1e4", "1e5", "1e6", "1e7"]
n_values = ["1e1", "1e2", "1e3", "1e4", "1e5"]
# k_values = [2, 4, 8, 16, 32]
k_values = [1, 2, 4, 8, 16]

if args.name == "diff_m":
    name="diff_m"
    lengend_name = "logm"
    key_list = log2m_values
elif args.name == "diff_k":
    name="diff_k"
    lengend_name="k"
    key_list = k_values
elif args.name == "diff_na":
    name="diff_n"
    lengend_name="|A|"
    key_list = n_values



def gen_single_pdf(target_key):

    save_file_name=f"{name}_{target_key_mapping[target_key]}"
    title_name = f"{title_mapping[target_key]} with {name.replace('_', ' ').replace('n', '|A|')}"

    log_data_dir=os.path.join(log_data_base_dir, name)

    diff_value2list_dict = {}

    log2m=20
    n="1e5"
    k=8

    for dict_key in key_list:

        value_list = []
        for eps_0 in range(21):

            if name == "diff_k":
                k = dict_key
            elif name == "diff_m":
                log2m = dict_key
            elif name == "diff_n":
                n = dict_key

            file_name = f"log2m_{log2m}_n_{n}_k_{k}_eps0_{eps_0}.json"
            # print(file_name)
            file_path = os.path.join(log_data_dir, file_name)
            # print(file_path)
            with open(file_path, 'r') as fr:
                data = json.load(fr)
                value_list.append(data[target_key])
        # post process value list
        value_list = [value / 100 for value in value_list]
        diff_value2list_dict[dict_key] = value_list

    font_size = 20
    line_width=5.0
    marker_size=13
    color_list = ["#ffc470", "#f6a865", "#ee8d5b", "#e57250", "#dd5746"]
    # color_list = [
    # "#ff0000",
    # "#c80d17",
    # "#921a2e",
    # "#5c2745",
    # "#26355d",
    # ]
    marker_list = ["o", "D", "^", "p", "X"]

    # create a new figure
    plt.figure()
    # get current axis
    ax = plt.gca()
    # turn background into lightgrey
    ax.set_facecolor('#f0f0f0')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=1))

    x_data = list(range(21))
    for i, key in enumerate(key_list):
        y_data = diff_value2list_dict[key]
        plt.plot(x_data, y_data, label=f"{lengend_name}={key}", marker=marker_list[i], color=color_list[i], linewidth=line_width, markersize=marker_size)

    plt.grid(True)  # show grid
    # add legend
    plt.legend(fontsize=font_size, loc='upper right')

    # add title and labels for x and y
    plt.title(title_name, fontsize=font_size)
    plt.xlabel('Epsilon_0', fontsize=font_size)
    plt.ylabel('Error Rate', fontsize=font_size)

    # set stick font size
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    # # show fig
    # plt.show()

    if args.save_type == "pdf":
        save_fig_path = os.path.join(save_fig_dir, f"{save_file_name}.pdf")
        print(save_fig_path)
        plt.savefig(save_fig_path, format='pdf', bbox_inches='tight', pad_inches=0.05)
    elif args.save_type == "png":
        save_fig_path = os.path.join(save_fig_dir, f"{save_file_name}.png")
        print(save_fig_path)
        plt.savefig(save_fig_path, format='png', bbox_inches='tight', pad_inches=0.05)

    # clean up plt
    plt.clf()


# target_key = "random"
# target_key = "inside"
# target_key = "outside"

target_key_values = ["random", "inside", "outside"]
for target_key in target_key_values:
    gen_single_pdf(target_key)
