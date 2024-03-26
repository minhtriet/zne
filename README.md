# Zero noise extrapolation challenge

Project structure
```
zne
├── zne.ipynb     # see section Notebook
└── util.py       # see section Util
```

## Notebook
In the notebook, the first cell has all the config and comments. One may want to change this before running the notebook, but the config leaving there already works.

The implement of the global folding and the extrapolation are in utils.py.
The notebook is for experimenting with the implementation in session Util below.

## Util
Contains the implementation of the extrapolation and the unitary folding

## Running on a real quantum machine
I tried to run the IBM but the queueing is quite long. I am based in EU but somehow my available region is only in Australia and Japan

[Notebook (older than this version)](https://lab.quantum.ibm.com/user/654e84109e53ed4e26de133b/lab/tree/zne.ipynb)

[Job](https://quantum.ibm.com/jobs/cqyb5sqqwzy0008kcp90)

## Exponential extrapolation
Eventhough it is implemented, none of the circuits I tried can make exponential extrapolation converge. It is also the case with the reference implementation, which always ask me to switch to linear extrapolation instead.