
# conda activate galore

log_dir="logs"
log_data_dir="log_data"

name="eps_diff_k"

log_dir="${log_dir}/${name}"
log_data_dir="${log_data_dir}/${name}"

mkdir -p $log_dir
mkdir -p $log_data_dir

# base setting log2(m)=20, n=1e5, k=8

log2m=19
na=1e5
# k=8
k=3

delta=0.01

# log2m_values=(20 21 22 23 24)
# log2m_values=(18 19 20 21 22)
# na_values=(1e1 1e2 1e3 1e4 1e5)
k_values=(1 2 3 4 5)

# eps_0_values=(0.0 0.3 0.6 0.9 1.2 1.5 1.8 2.1 2.4 2.7 3.0)

# for log2m in "${log2m_values[@]}"; do
# for na in "${na_values[@]}"; do
for k in "${k_values[@]}"; do
    # for eps_0 in "${eps_0_values[@]}"; do
    for eps in {0..30..3}; do
        log_path="${log_dir}/log2m_${log2m}_na_${na}_k_${k}_eps_${eps}.txt"
        log_data_path="${log_data_dir}/log2m_${log2m}_na_${na}_k_${k}_eps_${eps}.json"

        nohup python bloom_filter_eps.py \
            --log2m $log2m \
            --na $na \
            --k $k \
            --dp True \
            --eps $eps  \
            --delta $delta \
            --output_path $log_data_path > $log_path &

        # python bloom_filter_eps.py \
        #     --log2m $log2m \
        #     --na $na \
        #     --k $k \
        #     --dp True \
        #     --eps $eps  \
        #     --delta $delta \
        #     --output_path $log_data_path > $log_path 

        # exit 0
    done
done



