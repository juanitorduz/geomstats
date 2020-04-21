# Geomstats
[![PyPI version](https://badge.fury.io/py/geomstats.svg)](https://badge.fury.io/py/geomstats)[![Build Status](https://travis-ci.org/geomstats/geomstats.svg?branch=master)](https://travis-ci.org/geomstats/geomstats)[![Coverage Status](https://codecov.io/gh/geomstats/geomstats/branch/master/graph/badge.svg?flag=numpy)](https://codecov.io/gh/geomstats/geomstats)[![Coverage Status](https://codecov.io/gh/geomstats/geomstats/branch/master/graph/badge.svg?flag=tensorflow)](https://codecov.io/gh/geomstats/geomstats)[![Coverage Status](https://codecov.io/gh/geomstats/geomstats/branch/master/graph/badge.svg?flag=pytorch)](https://codecov.io/gh/geomstats/geomstats) (Coverages for: numpy, tensorflow, pytorch)


Geomstats is an open-source Python package for computations and statistics on manifolds. The package is organized into two main modules:
``geometry`` and ``learning``.

The module `geometry` implements concepts in differential geometry,and the module `learning` implements statistics and learning algorithms for data on manifolds.

<img align="left" src="https://raw.githubusercontent.com/ninamiolane/geomstats/master/examples/imgs/h2_grid.png" width=110 height=110>

- To get started with ```geomstats```, see the [examples directory](https://github.com/geomstats/geomstats/tree/master/examples).
- For more in-depth applications of ``geomstats``, see the [applications repository](https://github.com/geomstats/applications/).
- The documentation of ```geomstats``` can be found on the [documentation website](https://geomstats.github.io/).
- If you find ``geomstats`` useful, please kindly cite our [paper](https://arxiv.org/abs/1805.08308).

## Install geomstats via pip3

From a terminal (OS X & Linux), you can install geomstats and its requirements with ``pip3`` as follows::

```
pip3 install -r requirements.txt
pip3 install geomstats
```

This installs the latest version uploaded on PyPi.

## Install geomstats via Git

From a terminal (OS X & Linux), you can install geomstats and its requirements via Git as follows::
```
pip3 install -r requirements
git clone https://github.com/geomstats/geomstats.git

This installs the latest GitHub version, useful for developers.

## Choose the backend

You can choose your backend by setting the environment variable ``GEOMSTATS_BACKEND`` to ``numpy``, ``tensorflow`` or ``pytorch``. By default, the numpy backend is used. You should only use the numpy backend for examples with visualizations.

```
export GEOMSTATS_BACKEND=pytorch
```

Pytorch and tensorflow requirements are optional, as geomstats can be used with numpy only.

## Getting started

To use `geomstats` for learning
algorithms on Riemannian manifolds, you need to follow three steps:
- instantiate the manifold of interest,
- instantiate the learning algorithm of interest,
- run the algorithm.
The data should be represented by the structure ``gs.array``, which represents numpy arrays, tensorflow or pytorch tensors, depending on the choice of backend.

The following code snippet shows the use of tangent Principal Component Analysis on the
space of 3D rotations, assuming ``data`` belongs to this space.

```
from geomstats.geometry.special_orthogonal import SpecialOrthogonal
from geomstats.learning.pca import TangentPCA

so3 = SpecialOrthogonal(n=3)
metric = so3.bi_invariant_metric

tpca = TangentPCA(metric=metric, n_components=2)
tpca = tpca.fit(data, base_point=metric.mean(data))
tangent_projected_data = tpca.transform(data)
```

All geometric computations are performed behind the scenes.
The user only needs a high-level understanding of Riemannian geometry.
Each algorithm can be used with any of the manifolds and metric
implemented in the package.

## Contributing

See our [contributing](https://github.com/geomstats/geomstats/blob/master/docs/contributing.rst) guidelines!

## Acknowledgements

This work is supported by:
- the Inria-Stanford associated team [GeomStats](http://www-sop.inria.fr/asclepios/projects/GeomStats/),
- the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation program (grant agreement [G-Statistics](https://team.inria.fr/epione/en/research/erc-g-statistics/) No. 786854),
- the French society for applied and industrial mathematics ([SMAI](http://smai.emath.fr/)),
- the National Science Foundation (grant NSF DMS RTG 1501767).
