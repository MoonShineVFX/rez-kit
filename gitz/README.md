
## rez-gitz

1. git clone from github
2. `rez-build` it

#### Usage
```bash
$ python -m gitz https://github.com/mottosso/rez-pipz.git --install
```

You may clone specific branch
```bash
$ python -m gitz https://github.com/mottosso/rez-pipz.git --install --branch=dev
``` 

#### Notice

* `gitz` will append breadcrumb attributes into cloned package:
    ```python
    gitz = True
    gitz_from_branch = "branch-name"
    ```
