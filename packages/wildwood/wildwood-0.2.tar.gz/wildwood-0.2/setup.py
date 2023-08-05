# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wildwood', 'wildwood.datasets', 'wildwood.preprocessing']

package_data = \
{'': ['*'], 'wildwood.datasets': ['data/*']}

install_requires = \
['matplotlib>=3.1',
 'numba>=0.48',
 'numpy>=1.17',
 'pandas>=1.1.3',
 'scikit-learn>=0.22',
 'scipy>=1.3.2',
 'tqdm>=4.36',
 'xlrd>=1.2.0']

setup_kwargs = {
    'name': 'wildwood',
    'version': '0.2',
    'description': 'scikit-learn compatible alternative random forests algorithms',
    'long_description': '\n[![Build Status](https://travis-ci.com/pyensemble/wildwood.svg?branch=master)](https://travis-ci.com/pyensemble/wildwood)\n[![Documentation Status](https://readthedocs.org/projects/wildwood/badge/?version=latest)](https://wildwood.readthedocs.io/en/latest/?badge=latest)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wildwood)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/wildwood)\n[![GitHub stars](https://img.shields.io/github/stars/pyensemble/wildwood)](https://github.com/pyensemble/wildwood/stargazers)\n[![GitHub issues](https://img.shields.io/github/issues/pyensemble/wildwood)](https://github.com/pyensemble/wildwood/issues)\n[![GitHub license](https://img.shields.io/github/license/pyensemble/wildwood)](https://github.com/pyensemble/wildwood/blob/master/LICENSE)\n[![Coverage Status](https://coveralls.io/repos/github/pyensemble/wildwood/badge.svg?branch=master)](https://coveralls.io/github/pyensemble/wildwood?branch=master)\n\n# WildWood\n\nScikit-Learn compatible Random Forest algorithms\n\n[Documentation](https://wildwood.readthedocs.io) | [Reproduce experiments](https://wildwood.readthedocs.io/en/latest/experiments.html) |\n\n# Installation\n\nThe easiest way to install wildwood is using pip\n\n    pip install wildwood\n\nBut you can also use the latest development from github directly with\n\n    pip install git+https://github.com/pyensemble/wildwood.git\n\n# Experiments\n\n## Experiments with hyperparameters optimization\n\nTo run experiments with hyperparameters optimization, under directory `experiments/`, use\n\n    python run_hyperopt_classfiers.py --clf_name WildWood --dataset_name adult\n\n(with `WildWood` and on `adult` dataset in this example).\n\nSome options are\n\n- Setting `--n_estimators` or `-t` for number of estimators \n  (for maximal number of boosting iterations in case of gradient boosting algorithms), default 100.\n- Setting `--hyperopt_evals` or `-n` for number of hyperopt steps, default 50.\n\n## Experiments on default parameters\n\nTo run experiments with default parameters, under directory `experiments/`, use\n\n    python run_benchmark_default_params_classifiers.py --clf_name WildWood --dataset_name adult\n\n(with `WildWood` and on `adult` dataset in this example).\n\n## Datasets and classifiers\n\nFor both `run_hyperopt_classfiers.py` and `run_benchmark_default_params_classifiers.\npy`, the available options for `dataset_name` are:\n\n- `adult`\n- `bank`\n- `breastcancer`\n- `car`\n- `cardio`\n- `churn`\n- `default-cb`\n- `letter`\n- `satimage`\n- `sensorless`\n- `spambase`\n- `amazon`\n- `covtype`\n- `internet`\n- `kick`\n- `kddcup`\n- `higgs`\n\nwhile the available options for `clf_name` are\n\n- `LGBMClassifier`\n- `XGBClassifier`\n- `CatBoostClassifier`\n- `RandomForestClassifier`\n- `HistGradientBoostingClassifier`\n- `WildWood`\n\n## Experiments presented in the paper\n\nAll the scripts allowing to reproduce the experiments from the paper are available \nin the `experiments/` folder\n\n1. Figure 1 is produced using `fig_aggregation_effect.py`.\n1. Figure 2 is produced using `n_tree_experiment.py`. \n1. Tables 1 and 3 from the paper are produced using `run_hyperopt_classfiers.py` \n   with `n_estimators=5000` for gradient boosting algorithms and with \n   `n_estimators=n` for `RFn` and `WWn`\n   - call\n   ```shell\n   python run_hyperopt_classfiers.py --clf_name <classifier> --dataset_name <dataset> --n_estimators <n_estimators>\n   ```   \n   for each pair `(<classifier>, <dataset>)` to run hyperparameters optimization experiments;\n   - use for example\n   ```python\n   import pickle as pkl\n   filename = \'exp_hyperopt_xxx.pickle\'\n   with open(filename, "rb") as f:\n       results = pkl.load(f)\n   df = results["results"]\n   ```\n   to retrieve experiments information, such as AUC, logloss and their standard deviation.\n\n1. Tables 2 and 4 are produced using `benchmark_default_params.py`\n    - call\n   ```shell\n   python run_benchmark_default_params_classifiers.py --clf_name <classifier> --dataset_name <dataset>\n   ```   \n   for each pair `(<classifier>, <dataset>)` to run experiments with default parameters;\n   -  use similar commands to retrieve experiments information.\n    \n1. Using experiments results (AUC and fit time) done by `run_hyperopt_classfiers.py`, \n   then concatenating dataframes and using `fig_auc_fit_time.py` to produce Figure 3.\n\n',
    'author': 'Stéphane Gaïffas',
    'author_email': 'stephane.gaiffas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wildwood.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
