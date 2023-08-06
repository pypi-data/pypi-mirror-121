# OneNeuron_PyPI
demo for package upload on the PyPI

## How to use

```python
from oneNeuron.perceptron import Perceptron

# get x and y first, and then use below command
model = Perceptron(eta=eta, epochs=epochs)
model.fit(X, y)
```


# Reference - 

[official python docs](https://packaging.python.org/tutorials/packaging-projects/)

[github docs for github actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries)