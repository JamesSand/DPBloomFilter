from tqdm import tqdm
import random
import copy
import json
import os
from multiprocessing import Pool
from bloom_filter import DPBloomFilter, min_value, max_value


m = int(2 ** 20)
na = int(1e5)
k = 8

disable_tqdm = False
output_dir = "xor_data"
os.makedirs(output_dir, exist_ok=True)
statistic_repeat_time = int(1e3)

# in this setting, we don't need eps
fixed_bloom_filter = DPBloomFilter(m, k)
fixed_inserted_list = []
for i in tqdm(range(na), desc="inserting", disable=disable_tqdm):
    inserted_value = random.randint(min_value, max_value)
    fixed_bloom_filter.add(inserted_value)
    fixed_inserted_list.append(inserted_value)
# inserted_set = set(inserted_set)

# create a list with 2*k 0

def calculate_bloom_diff(bloom_filter_1, bloom_filter_2):
    bitarray1 = bloom_filter_1.bitarray
    bitarray2 = bloom_filter_2.bitarray
    # caclcute xor result
    xor_result = bitarray1 ^ bitarray2

    # count xor
    difference_count = xor_result.count()
    return difference_count

count_list = [0] * (2 * k)

def run_neighbor(fixed_inserted_list):
    neighbor_inserted_list = copy.deepcopy(fixed_inserted_list)
    # chanege one element
    change_idx = random.randint(0, len(fixed_inserted_list) - 1)
    change_value = random.randint(min_value, max_value)
    neighbor_inserted_list[change_idx] = change_value
    neighbor_bloom_filter = DPBloomFilter(m, k)
    for value in neighbor_inserted_list:
        neighbor_bloom_filter.add(value)

    # do xor
    xor_count = calculate_bloom_diff(fixed_bloom_filter, neighbor_bloom_filter)

    return xor_count

# multiprocess
p = Pool()
results = []
for i in range(statistic_repeat_time):
    results.append(p.apply_async(run_neighbor, args=(fixed_inserted_list,)))
print('Waiting for all subprocesses done...')
p.close()
p.join()
print('All subprocesses done.')
for res in results:
    xor_count = res.get()
    count_list[xor_count] += 1

# save count list
save_path = os.path.join(output_dir, "F_distribution.json")
with open(save_path, "w") as f:
    json.dump(count_list, f, indent=4)


