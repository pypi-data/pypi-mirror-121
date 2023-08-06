
EvoCov
======

GPlib extension to learn the kernel function.

Setup evocov
------------

- Create and activate virtualenv (for python2) or
  venv (for python3)

```bash
  # for python3
  python3 -m venv .env
  # or for python2
  python2 -m virtualenv .env

  source .env/bin/activate
```

- Upgrade pip

```bash
  python -m pip install --upgrade pip
```

- Install EvoCov package

```bash
  python -m pip install evocov
```


Use EvoCov
----------------------

- Import EvoCov and GPlib to use it in your python script.

```python
  import gplib
  import evocov
```

- Configure the fitting method.

```python
  lml = gplib.me.LML()
  bic = gplib.me.BIC()

  fitting_method = evocov.fit.EvoCov(
      obj_fun=bic.fold_measure,
      max_fun_call=25000,
      nested_fit_method=gplib.fit.MultiStart(
          obj_fun=lml.fold_measure,
          max_fun_call=250,
          nested_fit_method=gplib.fit.LocalSearch(
              obj_fun=lml.fold_measure,
              method="Powell",
              max_fun_call=100
          )
      )
  )
```

- Initialize the GP with None covariance function.

```python
  gp = gplib.GP(
      mean_function=gplib.mea.Fixed(),
      covariance_function=fitting_method.get_random_kernel()
  )
```

- Generate some random data.

```python
  import numpy as np
  data = {
    'X': np.arange(3, 8, 1.)[:, None],
    'Y': np.random.uniform(0, 2, 5)[:, None]
  }
```

- Fit the kernel and the hyperparameters to the training set.

```python
  validation = gplib.dm.Full()

  log = fitting_method.fit(gp, validation.get_folds(
      data
  ))
```

- Finally plot the posterior GP.

```python
  posterior_gp = gp.get_posterior(data)
  gplib.plot.gp_1d(posterior_gp, data, n_samples=10)
```

- There are more examples in examples/ directory. Check them out!

Develop EvoCov
--------------

-  Update API documentation

```bash
  source ./.env/bin/activate
  pip install Sphinx
  cd docs/
  sphinx-apidoc -f -o ./ ../evocov
```
