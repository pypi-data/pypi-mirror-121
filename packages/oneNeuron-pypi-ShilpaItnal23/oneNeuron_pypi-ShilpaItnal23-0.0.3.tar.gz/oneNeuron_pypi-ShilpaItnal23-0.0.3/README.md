# oneNeuron_pypi
oneNeuron_pypi

# Reference -
[official python doc](https://packaging.python.org/tutorials/packaging-projects/)

[github docs for github actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries)

# How to use this package
```python

from oneNeuron.perceptron import Perceptron

# Get x and y and then use below commands

model = Perceptron(eta=eta, epochs=epochs)
model.fit(X, y)
   
```
