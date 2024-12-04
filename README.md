# CGN_pipelines

Quantifying similarities between fMRI processing pipelines for efficient multiverse analysis

## Installation

As stellargraph requires Python 3.8, we recommend using a dedicated environment (e.g. through conda):

```
conda create -n gcn-piplines python==3.8.0
conda activate gcn-piplines
pip install -r requirements.txt
```

To re-run the multiverse analysis, a separate environment with Python 3.11 is required:

```
conda create -n gcn-multiverse python==3.11
conda activate gcn-multiverse
pip install comet-toolbox pandas numpy matplotlib nilearn nibabel
```

## Usage

- The main script which reproduces the results fom the paper is located in `evaluate_gcn.ipynb`
- The multiverse analysis can be performed by running `multiverse/run_multiverse.py`
- The results from multiverse analysis are visualized in `evaluate_multiverse.ipynb`
