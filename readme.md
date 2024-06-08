# DP Bloom Filter

## 1 Installation

Current Code is test on Python 3.10.14 

```bash
pip install -r requirements.txt
```

## 2 Run

### 2.1 Run a single trial
```bash
bash demo.sh
```

`demo.sh` will create a folder named `log_data` and store its results in `log_data/demo.json`. And it will also output the result on the terminal. 

If you open `log_data/demo.json`, you will get something like:
```
{
    "random": <Total Error Rate>,
    "inside": <True Negative Error Rate>,
    "outside": <False Positive Error Rate>
}
```

### 2.2 Run multiple trials

You can run the following code to run the trials on different m, na, and k.
```bash
bash scripts/run_dp_diff_m.sh
bash scripts/run_dp_diff_na.sh
bash scripts/run_dp_diff_k.sh
```

The results will be store under the following folders, respectively.
```
log_data/diff_m/*.json
log_data/diff_na/*.json
log_data/diff_k/*.json
```

## 3 Draw Figures

You can choose one from the following commands to draw your figures. 
```bash
python draw/draw_diff.py --name "diff_m" --save_type "pdf"
python draw/draw_diff.py --name "diff_m" --save_type "png"
python draw/draw_diff.py --name "diff_na" --save_type "pdf"
python draw/draw_diff.py --name "diff_na" --save_type "png"
python draw/draw_diff.py --name "diff_k" --save_type "pdf"
python draw/draw_diff.py --name "diff_k" --save_type "png"
```

