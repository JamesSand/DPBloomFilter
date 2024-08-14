
#### activate conda environment ####
# conda activate xxx

log_dir="logs"
log_data_dir="log_data"

name="eps_diff_m"

# store log for experiments
log_dir="${log_dir}/${name}"

# store results for experiments
log_data_dir="${log_data_dir}/${name}"

mkdir -p $log_dir
mkdir -p $log_data_dir

# base setting log2(m)=19, n=1e5, k=3
log2m=19
na=1e5
k=3

# DP parameter delta = 0.01
delta=0.01

log2m_values=(18 19 20 21 22)

for log2m in "${log2m_values[@]}"; do
    # for run experiments range from 0 - 30, step = 3
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

    done
done



