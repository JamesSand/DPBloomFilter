import json

json_path = "/mnt/nvme2/xuhaiyang/szz/DPBloom_filter/xor_data/m_524288_na_100000_k_4.json"
with open(json_path, "r") as fr:
    data = json.load(fr)

cumulative = 0
cumulative_list = []
for i in range(len(data)):
    cumulative += data[i]
    cumulative_list.append(cumulative)

for i, value in enumerate(cumulative_list):
    print(i, value)


