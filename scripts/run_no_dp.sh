
# conda activate galore

log_dir="logs"
mkdir -p $log_dir

n_values=(1e3 5e3 1e4 5e4 1e5)
m_exp_values=(16 20)

for m_exp in "${m_exp_values[@]}"; do
    for n in "${n_values[@]}"; do
        file_path="${log_dir}/DP_False_mexp_${m_exp}_n_${n}.txt"
        # echo $file_path
        nohup python bloom_filter.py \
            --m_exp $m_exp \
            --n $n \
            --dp False \
            --eps_0 10 > $file_path &

        # exit 0
    done
done

echo "Done."


