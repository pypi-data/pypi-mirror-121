# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['high_order_layers_torch']

package_data = \
{'': ['*']}

install_requires = \
['pytorch-lightning', 'torch']

setup_kwargs = {
    'name': 'high-order-layers-torch',
    'version': '1.0.1',
    'description': 'High order layers in pytorch',
    'long_description': '[![Build Status](https://travis-ci.org/jloveric/high-order-layers-torch.svg?branch=master)](https://travis-ci.org/jloveric/high-order-layers-torch)\n\n# Functional Layers in PyTorch\nThis is a PyTorch implementation of my tensorflow [repository](https://github.com/jloveric/high-order-layers) and is more complete due to the flexibility of PyTorch.\n\nLagrange Polynomial, Piecewise Lagrange Polynomial, Discontinuous Piecewise Lagrange Polynomial, Fourier Series, sum and product layers in PyTorch.  The sparsity of using piecewise polynomial layers means that by adding new segments the computational power of your network increases, but the time to complete a forward step remains constant.  Implementation includes simple fully connected layers and convolution layers using these models.  More details to come.  This is a PyTorch implementation of this [paper](https://www.researchgate.net/publication/276923198_Discontinuous_Piecewise_Polynomial_Neural_Networks) including extension to Fourier Series and convolutional neural networks.\n\nThe layers used here do not require additional activation functions and use a simple sum or product in place of the activation.  Product is performed in this manner...\n\n# Fully Connected Layer Types\nLagrange Polynomial Chebyshev Points\nPiecewise Continuous Lagrange Polynomial Chebyshev Points\nPiecewise Discontinuous Lagrange Polynomial Chebyshev Points\nPiecewise Discontinuous Lagrange Polynomial Chebyshev Points\nFourier Series\n\nA helper function is provided in selecting and switching between these layers\n```python\nfrom high_order_layers_torch.layers import *\nlayer1 = high_order_fc_layers(\n    layer_type=layer_type,\n    n=n, \n    in_features=784,\n    out_features=100,\n    segments=segments,\n    alpha=linear_part\n)\n```\nwhere `layer_type` is on of \n```\n"continuous" -> PiecewisePolynomial,\n"continuous_prod" -> PiecewisePolynomialProd,\n"discontinuous" -> PiecewiseDiscontinuousPolynomial,\n"discontinuous_prod" -> PiecewiseDiscontinuousPolynomialProd,\n"polynomial"-> Polynomial,\n"polynomial_prod"-> PolynomialProd,\n"product"-> Product,\n"fourier"-> FourierSeries\n```\n`n` is the number of interpolation points per segment (if there are any), `segments` is the number of segments for piecewise polynomials, `alpha` is used in product layers and when set to 1 keeps the linear part of the product, when set to 0 it subtracts the linear part from the product.\n## Product Layers\nProduct layers \n\n# Convolutional Layer Types\nLagrange Polynomial Chebyshev Points\nPiecewise Continuous Lagrange Polynomial Chebyshev Points\nPiecewise Discontinuous Lagrange Polynomial Chebyshev Points\nPiecewise Discontinuous Lagrange Polynomial Chebyshev Points\nFourier Series\n\n# Installing\n## Installing locally\nThis repo uses poetry, so run\n```\npoetry install\n```\nand then\n```\npoetry shell\n```\n\n## Installing from pypi\n```bash\npip install high-order-layers-torch\n```\nor\n```\npoetry add high-order-layers-torch\n```\n\n# Examples\n\n## Simple function approximation\nApproximating a simple function using a single input and single output (single layer) with no hidden layers\nto approximate a function using continuous and discontinuous piecewise polynomials (with 5 pieces) and simple\npolynomials and fourier series.  The standard approach using ReLU is non competitive.  To see more complex see\nthe implicit representation page [here](https://github.com/jloveric/high-order-implicit-representation).\n\n![piecewise continuous polynomial](plots/piecewise_continuous.png)\n![piecewise discontinuous polynomial](plots/piecewise_discontinuous.png)\n![polynomial](plots/polynomial.png)\n![fourier series](plots/fourier_series.png)\n\n\n\n## mnist (convolutional)\n```python\npython mnist.py max_epochs=1 train_fraction=0.1 layer_type=continuous n=4 segments=2\n```\n## cifar100 (convolutional)\n```\npython cifar100.py -m max_epochs=20 train_fraction=1.0 layer_type=polynomial segments=2 n=7 nonlinearity=False rescale_output=False periodicity=2.0 lr=0.001 linear_output=False\n```\n## invariant mnist (fully connected)\n```python\npython invariant_mnist.py max_epochs=100 train_fraction=1 layer_type=polynomial n=5\n```\nConstructing the network\n```\nself.layer1 = high_order_fc_layers(\n    layer_type=cfg.layer_type, n=cfg.n, in_features=784, out_features=100, segments=cfg.segments, alpha=cfg.linear_part)\nself.layer2 = nn.LayerNorm(100)\nself.layer3 = high_order_fc_layers(\n    layer_type=cfg.layer_type, n=cfg.n, in_features=100, out_features=10, segments=cfg.segments, alpha=cfg.linear_part)\nself.layer4 = nn.LayerNorm(10)\n```\n## Implicit Representation\nAn example of implicit representation can be found [here](https://github.com/jloveric/high-order-implicit-representation)\n',
    'author': 'jloverich',
    'author_email': 'john.loverich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
