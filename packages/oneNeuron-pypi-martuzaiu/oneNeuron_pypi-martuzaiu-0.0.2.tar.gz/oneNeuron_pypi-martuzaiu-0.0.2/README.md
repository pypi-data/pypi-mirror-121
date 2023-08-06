# oneNeuron_pypi
oneNeuron_pypi

# How to use this
get X and y then follow the below command

```python
from oneNeuron.perceptron import Perceptron
model = Perceptron(eta=eta, epochs=epochs)
model.fit(X,y)
```



# COMMANDS


## Make directory
```bash
mkdir -p src/oneNeuron
```

## Git add commit and push
```bash
git add . && git commit -m "Command added" && git push origin main
```
## Create files
```bash
touch src/oneNeuron/__init__.py
```

# References
[Python Pachaging](https://packaging.python.org/tutorials/packaging-projects/)

[github docs for github actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries)
