# DP Bloom Filter

## 1 Enviornment Setup

Current Code is test on Python 3.10.14 

```bash
pip install -r requirements.txt
```

## 2 Run Experiments

### 2.1 Run a single trial

If you want to run a single demo trial, you can run the following command.

```bash
bash demo.sh
```

`demo.sh` will create a folder named `log_data` and store its results in `log_data/demo.json`. And it will also output the result on the terminal. 

If you open `log_data/demo.json`, you will get something like:
```
{
    "random": <Total Error Rate>,
    "inside": <False Negative Error Rate>,
    "outside": <False Positive Error Rate>
}
```

### 2.2 Run multiple trials

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

Please refer to the instructions in ``notebooks/draw_figs.ipynb``.

## 4 Explanation for some code files

> If you just want run experiments, please ignore this section, and follow the instructions in Section 2 and 3.

- ``bloom_filter_eps.py`` contains the implementation of the DP Bloom Filter. 
- ``get_N_by_delta.py`` contains code for calculating $1 - \delta$ quntail $N$ according to the distribution of the random variable $W$. More details about the distribution of $W$ can be found in our paper.

