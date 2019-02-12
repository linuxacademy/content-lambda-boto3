# Resizing Images

## Pillow - Python Imaging Library (Fork)

Download the `Pillow-5.4.1-cp37-cp37m-manylinux1_x86_64.whl` package from <https://pypi.org/project/Pillow/>. Direct download [here](https://files.pythonhosted.org/packages/ae/2a/0a0ab2833e5270664fb5fae590717f867ac6319b124160c09f1d3291de28/Pillow-5.4.1-cp37-cp37m-manylinux1_x86_64.whl).

Download using `wget`:

```sh
wget https://files.pythonhosted.org/packages/ae/2a/0a0ab2833e5270664fb5fae590717f867ac6319b124160c09f1d3291de28/Pillow-5.4.1-cp37-cp37m-manylinux1_x86_64.whl
```

Extract the wheel file in the same folder as `lambda_handler.py`:

```sh
unzip Pillow-5.4.1-cp37-cp37m-manylinux1_x86_64.whl
```

The `Pillow-5.4.1.dist-info` isn't needed:

```sh
rm -rf Pillow-5.4.1.dist-info
```

Zip the `PIL` directory along with `lambda_handler.py`:

```sh
zip -r9 lambda.zip PIL lambda_handler.py
```

Upload `lambda.zip` to AWS Lambda.