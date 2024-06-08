from tqdm import tqdm
import random
import copy
import json
import os
from multiprocessing import Pool
# from bloom_filter import DPBloomFilter, min_value, max_value

################# code from Bloom filter.py ##################
import bitarray
import hashlib
import argparse
import math
import random
import sys
from tqdm import tqdm
import numpy as np
import json

############## global parameters #############
seed = 42
min_value=0
max_value=sys.maxsize
disable_tqdm = True
############## global parameters #############

np.random.seed(seed)
random.seed(seed)

# def create_hash_functions(k):
#     # create a generator function, generate k different hash functions
#     def hash_functionFactory(salt):
#         def hash_function(number):
#             # combine number and salt into a str
#             message = str(number) + str(salt)
#             # hash the message using SHA256
#             hash_object = hashlib.sha256(message.encode())
#             # convert the hash to an integer
#             return int(hash_object.hexdigest(), 16)
#         return hash_function

#     salts = [i for i in range(k)]
    
#     # generate different hash function using different salt
#     hash_functions = [hash_functionFactory(salt) for salt in salts]
    
#     return hash_functions

class DPBloomFilter:
    def __init__(self, m, k, eps_0=None, delta=None):
        self.m = m
        self.k = k
        self.eps_0 = eps_0
        self.delta = delta

        # self.hash_functions = create_hash_functions(k)
        self.bitarray = bitarray.bitarray(m)
        self.bitarray.setall(False)

    def get_k_hash_values(self, item):
        salts = [i for i in range(k)]
        hash_value_list = []
        for salt in salts:
            message = str(item) + str(salt)
            hash_object = hashlib.sha256(message.encode())
            # convert the hash to an integer
            hash_value_list.append(int(hash_object.hexdigest(), 16))
        return hash_value_list

    def add(self, item):
        hash_value_list = self.get_k_hash_values(item)
        for hash_value in hash_value_list:
            idx = hash_value % self.m
        # for hash_function in self.hash_functions:
        #     idx = hash_function(item)
        #     idx = idx % self.m
            self.bitarray[idx] = True

    def filp(self):
        assert self.eps_0 is not None, "Epsilon_0 must be set before flipping"
        # use binomial to decide wether filp
        # let 1 denotes remain, 0 denotes flip
        remain_prob = math.exp(self.eps_0) / (math.exp(self.eps_0) + 1)
        binomial_results = np.random.binomial(1, remain_prob, self.m)
        for i in range(self.m):
            if binomial_results[i] == 0:
                self.bitarray[i] = 1 - self.bitarray[i]

    def __contains__(self, item):
        # for hash_function in self.hash_functions:
        #     idx = hash_function(query)
        #     idx = idx % self.m
        hash_value_list = self.get_k_hash_values(item)
        for hash_value in hash_value_list:
            idx = hash_value % self.m
            if self.bitarray[idx] == False:
                return False
        return True   
    
    def bitarray_ratio(self, msg=None):
        one_cnt = 0
        zero_cnt = 0
        for bit in self.bitarray:
            if bit == True:
                one_cnt += 1
            else:
                zero_cnt += 1
        print("-" * 50)
        if msg is not None:
            print(msg)
        print(f"One ratio: {one_cnt / self.m}")
        print(f"Zero ratio: {zero_cnt / self.m}")
        print(F"One conut {one_cnt}")
        print(f"Zero count {zero_cnt}")
        print("-" * 50)

    def print_bitarray(self):
        print(self.bitarray)



################# end code from Bloom filter ##################


# m = int(2 ** 20)
# na = int(1e5)
# k = 8

global_N_dict = {}

def calculate_bloom_diff(bloom_filter_1, bloom_filter_2):
    bitarray1 = bloom_filter_1.bitarray
    bitarray2 = bloom_filter_2.bitarray
    # caclcute xor result
    xor_result = bitarray1 ^ bitarray2

    # count xor
    difference_count = xor_result.count()
    return difference_count

def run_neighbor(fixed_inserted_list, m, k, fixed_bloom_filter):
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

def run_mnk_pair(m, na, k, save_name):

    # save_name = f"m_{m}_na_{na}_k_{k}.json"

    print(save_name)
    # exit(0)

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

    count_list = [0] * (2 * k + 1)

    # multiprocess
    p = Pool()
    results = []
    for i in range(statistic_repeat_time):
        results.append(p.apply_async(run_neighbor, args=(fixed_inserted_list, m, k, fixed_bloom_filter,)))
    # print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    # print('All subprocesses done.')
    for res in results:
        xor_count = res.get()
        count_list[xor_count] += 1
        # try:
        #     count_list[xor_count] += 1
        # except Exception as e:
        #     print(e)
        #     print(xor_count)
        #     # print(count_list)
        #     # exit(0)

    # save count list
    save_path = os.path.join(output_dir, save_name)
    with open(save_path, "w") as f:
        json.dump(count_list, f, indent=4)

    # calculate N
    delta = 0.1
    cumulate = 0
    for i in range(len(count_list)):
        cumulate += count_list[i]
        if cumulate / statistic_repeat_time >= 1 - delta:
            N = i
            break
    global global_N_dict
    global_N_dict[save_name.rstrip(".json")] = N

def save_result():
    save_name = "global_N_dict.json"
    print(f"save results to {save_name}")

    # read first
    with open(save_name, "r") as fr:
        data = json.load(fr)

    data.update(global_N_dict)

    with open(save_name, "w") as fw:
        fw.write(json.dumps(data, indent=4))

if __name__ == "__main__":
    log2m = 15
    m = int(2 ** log2m)
    na = int(1e5)
    k = 2

    # log2m_values = [19, 20, 21, 22, 23]
    log2m_values = [19, 20, 21, 22, 23]

    # n_values = ["1e3", "1e4", "1e5", "1e6", "1e7"]
    # na_values = ["1e1", "1e2", "1e3", "1e4", "1e5"]
    na_values = [1e1, 1e2, 1e3, 1e4, 1e5]
    # k_values = [2, 4, 8, 16, 32]
    k_values = [1, 2, 4, 8, 16]

    # run diff m
    print("-" * 50)
    print("running log2m")
    for log2m_ in log2m_values:
        save_name = f"log2m_{log2m_}_na_{na}_k_{k}.json"
        run_mnk_pair(int(2 ** log2m_), na, k)
        save_result()

    # run diff na
    print("-" * 50)
    print("running na")
    for na_ in na_values:
        save_name = f"log2m_{log2m}_na_{na_}_k_{k}.json"
        run_mnk_pair(m, int(na_), k)
        save_result()

    # run diff k
    print("-" * 50)
    print("running k")
    for k_ in k_values:
        save_name = f"log2m_{log2m}_na_{na}_k_{k_}.json"
        run_mnk_pair(m, na, k_)
        save_result()
    
    


