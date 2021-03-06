# rez-kit

Better use Python 3.7
Rez 2.75+ required

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

Use [`rez-deliver`](https://github.com/davidlatwe/rez-deliver)

Additional packages

* https://github.com/davidlatwe/rez-pipz
* https://github.com/MoonShineVFX/rez-house
* https://github.com/MoonShineVFX/rez-production
