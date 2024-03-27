# Zero noise extrapolation challenge
In this repo, I 
- Implement Depolarizing noise from scratch
- Implement ZNE from scratch
- Compare with the result of reference Mitiq implementation 
- Experiment with ZNE algorithms to optimize its hyperparameters

There are two notebooks. 
- `zne.ipynb` uses the provided noise model, so that I can compare my implementation of global folding and extrapolation. It is because it is not straightforward for me to integrate a custom noise model in Pennylane into `qml.transforms.insert()`. I have some analyses here as well.
- `zne_custom_noise.ipynb` is slightly different from the above. It uses the noise model that I implemented end to end, without comparing with any implementation from the library.



## How to run
Install packages from `requirements.txt` and `jupyterlab`.

## Notebook
Readers are welcome to read the notebook `zne.ipynb` first. It contains the experiments with my implementation in `util.py`.
The first cell has all the config and comments. One can change this before running the notebook, but the config leaving there already works.

The implementation of the global folding and the extrapolation as requested by the task are in `utils.py`.


## Running on a real quantum machine
I tried to run the IBM but the queueing is quite long. I am based in the EU but somehow my available region is only in Australia and Japan

[Notebook (older than this version)](https://lab.quantum.ibm.com/user/654e84109e53ed4e26de133b/lab/tree/zne.ipynb)

[Job](https://quantum.ibm.com/jobs/cqyb5sqqwzy0008kcp90)

## Tests
From the home directory, please run `python -m unittest discover test`