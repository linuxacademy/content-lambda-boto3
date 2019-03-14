# Working with Lambda Layers

Create a new virtual environment using `pipenv` and install the required libraries:

```sh
pipenv --python 3.7
pipenv shell
pipenv install requests
```

Note: If you are on macOS, you can install `pipenv` using Homebrew:

```sh
brew install pipenv
```

on Amazon Linux, or another environment, you can install using `pip`:

```sh
pip3 install pipenv --user
```

Create the ZIP deployment package:

```sh
PY_DIR='build/python/lib/python3.7/site-packages'
# Create temporary build directory
mkdir -p $PY_DIR
# Generate requirements file
pipenv lock -r > requirements.txt
# Install packages into the target directory
pip install -r requirements.txt --no-deps -t $PY_DIR
cd build
# Zip files
zip -r ../requests_layer.zip .
cd ..
# Remove temporary directory
rm -r build
```

Create the Lambda Layer

```sh
aws lambda publish-layer-version \
--layer-name requests \
--compatible-runtimes python3.7 \
--zip-file fileb://requests_layer.zip
```

Note the `LayerArn` in the output.
