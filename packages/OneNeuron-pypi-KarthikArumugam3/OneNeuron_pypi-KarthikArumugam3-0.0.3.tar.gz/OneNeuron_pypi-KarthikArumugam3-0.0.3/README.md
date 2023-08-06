# OneNeuron_pypi
OneNeuron_pypi

In this repository I have published a python package named - [OneNeuron](https://pypi.org/project/OneNeuron-pypi-KarthikArumugam3/) which implements the use cases of my [One neuron/perceptron demo project](https://github.com/KarthikArumugam3/perceptron-demo)

Using this package/module along with the my [One neuron/perceptron demo project](https://github.com/KarthikArumugam3/perceptron-demo) anyone can implement the basic functionality of the a single neuron/perceptron such as AND and OR gates:-

## How to use:-

```python
from OneNeuron.perceptron import Perceptron

## get X and y and then use below commands
model = Perceptron(eta=eta, epochs=epochs)
model.fit(X, y)
```

#### Official python projects pakacking:-
I have used [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/) as a guide to create and publish my own package t0 Python Package Index.

#### Setting up workflow
For setting up the CICD for this project i have used [github docs for github actions](https://docs.github.com/en/actions/guides/building-and-testing-python#publishing-to-package-registries) to setup the whole process.


## Authors

- [@KarthikArumugam](https://github.com/KarthikArumugam3/)