# AndroMolecules
Package containing useful functions for molecular simulations.

## How to use
```
import andromolecules as am



```

## Updating package

### Create new source code and wheel
Run:
```
python3 setup.py sdist bdist_wheel

```

### Upload new build to PyPi
Run:
```
twine upload dist/*

```