
# conda activate galore

log_dir="logs"
log_data_dir="log_data"

name="diff_n"

log_dir="${log_dir}/${name}"
log_data_dir="${log_data_dir}/${name}"

mkdir -p $log_dir
mkdir -p $log_data_dir

# base setting log2(m)=20, n=1e5, k=8

log2m=20
# n=1e5
k=8

# log2m_values=(12 16 20 24 28)
# k_values=(2 4 8 16 32)
# n_values=(1e3 1e4 1e5 1e6 1e7)
n_values=(1e1 1e2)

# for log2m in "${log2m_values[@]}"; do
# for k in "${k_values[@]}"; do
for n in "${n_values[@]}"; do
    for eps_0 in {0..20}; do
        log_path="${log_dir}/log2m_${log2m}_n_${n}_k_${k}_eps0_${eps_0}.txt"
        log_data_path="${log_data_dir}/log2m_${log2m}_n_${n}_k_${k}_eps0_${eps_0}.json"

        nohup python bloom_filter.py \
            --log2m $log2m \
            --n $n \
            --k $k \
            --dp True \
            --eps_0 $eps_0  \
            --output_path $log_data_path > $log_path &
    done
done



