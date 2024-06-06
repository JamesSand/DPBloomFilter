
# conda activate galore

python bloom_filter.py \
    --m_exp 20 \
    --n 1e5 \
    --k 7 \
    --dp True \
    --eps_0 10 \
    --output_path "log_data/demo.json"


# python bloom_filter.py \
#     --m_exp 4 \
#     --n 5 \
#     --dp True \
#     --eps_0 10 \

