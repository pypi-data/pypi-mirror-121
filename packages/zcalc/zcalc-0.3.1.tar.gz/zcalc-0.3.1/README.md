# zcalc

[![Build Status](https://app.travis-ci.com/blackchip-org/zcalc.svg?branch=main)](https://app.travis-ci.com/blackchip-org/zcalc)

A fun RPN calculator.

Work in progress.

To run:

```bash
pip3 install -e .
zcalc
```

Setup python 3.7 environment on macOS:

```bash
brew install python@3.7
/usr/local/opt/python@3.7/bin/python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

Setup environment on Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Running tests:

```bash
pip install pytest
python -m unittest
```

## License

MIT
