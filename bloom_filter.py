import bitarray
import hashlib
import argparse
import math
import random
import sys
from tqdm import tqdm
import numpy as np

############## global parameters #############
seed = 42
min_value=0
max_value=sys.maxsize
############## global parameters #############

np.random.seed(seed)
random.seed(seed)

def create_hash_functions(k):
    # 创建一个生成器函数，用于生成 k 个不同的哈希函数
    def hash_functionFactory(salt):
        def hash_function(number):
            # print(type(str(number)))
            # print(type(salt))
            # breakpoint()
            # 将数字和盐值组合成一个字符串
            message = str(number) + str(salt)
            # 对组合后的字符串进行编码并哈希
            hash_object = hashlib.sha256(message.encode())
            # 返回哈希值的整数形式
            return int(hash_object.hexdigest(), 16)
        return hash_function

    salts = [i for i in range(k)]
    
    # 为每个盐值创建一个哈希函数
    hash_functions = [hash_functionFactory(salt) for salt in salts]
    
    return hash_functions

class DPBloomFilter:
    def __init__(self, m, k, eps_0=None, delta=None):
        self.m = m
        self.k = k
        self.eps_0 = eps_0
        self.delta = delta

        self.hash_functions = create_hash_functions(k)
        self.bitarray = bitarray.bitarray(m)
        self.bitarray.setall(False)

    def add(self, item):
        for hash_function in self.hash_functions:
            idx = hash_function(item)
            idx = idx % self.m
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

    def __contains__(self, query):
        for hash_function in self.hash_functions:
            idx = hash_function(query)
            idx = idx % self.m
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

def test_bloom(bloom_filter, inserted_set, query_time=int(1e5), test_type="random"):

    inserted_list = list(inserted_set)

    disable_tqdm = False

    assert test_type in ["random", "inside", "outside"]
    fail_cnt = 0
    for i in tqdm(range(query_time), desc="querying", disable=disable_tqdm):
        if test_type == "random":
            query_value = random.randint(min_value, max_value)
        elif test_type == "inside":
            query_value = inserted_list[random.randint(0, len(inserted_set) - 1)]
        elif test_type == "outside":
            query_value = random.randint(min_value, max_value)
            while query_value in inserted_set:
                query_value = random.randint(min_value, max_value)
        bloom_answer = query_value in bloom_filter
        gt_answer = query_value in inserted_set
        if bloom_answer != gt_answer:
            fail_cnt += 1

    print("-" * 50)
    print(f"{test_type} Fail count: {fail_cnt}")
    print(f"{test_type} Fail ratio: {(fail_cnt / query_time) * 100}%")
    print("-" * 50)

def run_bloom(m, n, k, query_time=int(1e5), dp=False, eps_0=None):

    bloom_filter = DPBloomFilter(m, k, eps_0=eps_0)

    # store ground truth
    inserted_set = []
    for i in tqdm(range(n), desc="inserting"):
        inserted_value = random.randint(min_value, max_value)
        bloom_filter.add(inserted_value)
        inserted_set.append(inserted_value)
    inserted_set = set(inserted_set)

    bloom_filter.bitarray_ratio(msg="before flip")

    if dp:
        bloom_filter.filp()

        bloom_filter.bitarray_ratio(msg="after flip")


    test_bloom(bloom_filter, inserted_set, query_time, test_type="random")
    print("before inside")
    test_bloom(bloom_filter, inserted_set, query_time, test_type="inside")
    print("after inside")

    test_bloom(bloom_filter, inserted_set, query_time, test_type="outside")

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--m_exp", type=int, required=True)
    parser.add_argument("--n", type=float, required=True)
    parser.add_argument("--k", type=int, default=None)

    parser.add_argument("--dp", type=str, default="False")
    parser.add_argument("--eps_0", type=float, default=None)

    args = parser.parse_args()

    # m = args.m
    m = 2 ** args.m_exp
    n = int(args.n)

    if args.k is not None:
        k = args.k
    else:
        k = int(round((m / n) * math.log(2)))
        if k == 0:
            k += 1

    dp = args.dp == "True"
    eps_0 = args.eps_0

    # sanity check
    if dp:
        assert eps_0 is not None, "Epsilon_0 must be set when using DP"

    print("-" * 50)
    print(f"m {m}")
    print(f"n {n}")
    print(f"k {k}")
    print(f"dp {dp}")
    print(f"eps_0 {eps_0}")
    print("-" * 50)

    run_bloom(m, n, k, dp=dp, eps_0=eps_0)





