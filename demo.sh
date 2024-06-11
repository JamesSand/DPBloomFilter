
# conda activate galore

log_data_dir="log_data"
mkdir -p $log_data_dir

# python bloom_filter.py \
#     --log2m 20 \
#     --na 1e5 \
#     --k 7 \
#     --dp True \
#     --eps_0 10 \
#     --output_path "${log_data_dir}/demo.json"

python bloom_filter_eps.py \
    --log2m 20 \
    --na 1e5 \
    --k 3 \
    --dp True \
    --eps 10 \
    --delta 0.1 \
    --output_path "${log_data_dir}/demo.json"


