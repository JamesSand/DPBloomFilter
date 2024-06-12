set -e

python draw/draw_diff.py --prefix "NeqK" --name "diff_m" --save_type "pdf"
python draw/draw_diff.py --prefix "NeqK" --name "diff_na" --save_type "pdf"
python draw/draw_diff.py --prefix "NeqK" --name "diff_k" --save_type "pdf"



# python draw/draw_diff.py --prefix "NeqK" --name "diff_m" --save_type "png"
# python draw/draw_diff.py --prefix "NeqK" --name "diff_na" --save_type "png"
# python draw/draw_diff.py --prefix "NeqK" --name "diff_k" --save_type "png"
