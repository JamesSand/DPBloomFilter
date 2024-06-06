
# conda activate galore

log_dir="logs"
mkdir -p $log_dir

# n_values=(1e3 5e3 1e4 5e4 1e5)
# eps_0_values=(0 5 10 15 20)
eps_0_values=(1 2 3 4)
# m_exp_values=(16 20)

# m_exp_values=(16)
# n=1e4

m_exp_values=(20)
n=1e5

for m_exp in "${m_exp_values[@]}"; do
    for eps_0 in "${eps_0_values[@]}"; do
        file_path="${log_dir}/DP_True_mexp_${m_exp}_n_${n}_eps0_${eps_0}.txt"
        # echo $file_path
        nohup python bloom_filter.py \
            --m_exp $m_exp \
            --n $n \
            --dp True \
            --eps_0 $eps_0 > $file_path &

        # exit 0
    done
done

echo "Done."


