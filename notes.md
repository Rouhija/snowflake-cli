### Compiling package
```sh
# Test
python setup.py develop
# Compile
python setup.py sdist
python setup.py bdist_wheel
# Upload
python -m twine upload dist/*
# Upgrade
pip install YOURPACKAGE --upgrade
```

### Reading
- [PyPi](https://dzone.com/articles/executable-package-pip-install)