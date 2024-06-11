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

Warning: the following command will start python programm running in the background. 

You need to kill they via command line to stop them. So be careful running the following commands. 

You can run the following code to run the trials on different m, na, and k.
```bash
bash scripts/run_eps_diff_m.sh
bash scripts/run_eps_diff_na.sh
bash scripts/run_eps_diff_k.sh
```

The results will be store under the following folders, respectively.
```
log_data/eps_diff_m/*.json
log_data/eps_diff_na/*.json
log_data/eps_diff_k/*.json
```

## 3 Draw Figures for Error rate and Epsilon

You can choose one from the following commands to draw your figures. 
```bash
python draw/draw_diff.py --name "diff_m" --save_type "pdf"
python draw/draw_diff.py --name "diff_m" --save_type "png"
python draw/draw_diff.py --name "diff_na" --save_type "pdf"
python draw/draw_diff.py --name "diff_na" --save_type "png"
python draw/draw_diff.py --name "diff_k" --save_type "pdf"
python draw/draw_diff.py --name "diff_k" --save_type "png"
```

## 4 Draw Figures for Distribution of W. 

Choose from the following command
```bash
python draw/draw_w.py --save_type "pdf"
python draw/draw_w.py --save_type "png"
```
