# rez-kit

Better use Python 3.7
Rez 2.75+ required

#### Rez Production Install

```shell
python ./install.py
```

> IMPORTANT:
>
> If you are using Python 3.7+ to run Rez production install, `venv` is used to create virtual environment for Rez. And the Python binary in that virtual environment will be linked to the binary that was used to create it.
> 
> Which means, the Python you used to install Rez, cannot be relocated nor removed.


#### Install packages

Use [`rez-deliver`](https://github.com/davidlatwe/rez-deliver)

Additional packages

* https://github.com/davidlatwe/rez-pipz
