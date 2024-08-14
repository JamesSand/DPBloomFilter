
#### activate conda environment ####
# conda activate xxx

# base setting log2(m)=19, n=1e5, k=3
log2m=19
na=1e5
k=3
eps=15

# DP parameter delta = 0.01
delta=0.01

log_data_dir="log_data"
mkdir -p $log_data_dir

python bloom_filter_eps.py \
        --log2m $log2m \
        --na $na \
        --k $k \
        --dp True \
        --eps $eps  \
        --delta $delta \
        --output_path "${log_data_dir}/demo.json" 


