# awesome-rez

Better use Python 3.7

#### Install Rez

```shell
python ./install.py
```

#### Setup `rez-kit/rezconfig.py`

```batch
:: rezin.bat
:: For entering Rez
@echo off
set PATH=%YOUR_REZ_LOCATION%\Scripts\rez;%PATH%
set SHARED_PACKAGES_PATH=\packages-path-on\shared\drive
set REZ_CONFIG_FILE=%YOUR_PATH_TO%\rez-kit\rezconfig.py
rez --version
```

#### Install packages

```shell
python ./deploy.py ozark
```

Essential packages will also be installed: `os`, `arch`.. and `rez`.
