# OneNeuron_PyPI
demo for package upload on the PyPI

## How to use

```python
from oneNeuron.perceptron import Perceptron
from oneNeuron.all_utils import prepare_data, save_model, save_plot

# get x and y first, and then use below command
X,y = prepare_data(df)

model = Perceptron(eta=eta, epochs=epochs)
model.fit(X, y)

save_model(model, filename=str(filename)+".model")

save_plot(df, file_name=str(filename)+".png",model_=model)

```


# Reference - 

[official python docs](https://packaging.python.org/tutorials/packaging-projects/)

[github docs for github actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries)