
name = "qt"

version = "5.12.5-m1"

build_command = False

download_link = "http://download.qt.io/official_releases/qt/5.12/5.12.5/" \
                "qt-opensource-windows-x86-5.12.5.exe"


def commands():
    env = globals()["env"]

    # X64
    root = "C:/Qt/Qt5.12.5/5.12.5/msvc2017_64"

    env.PATH.append("{root}/bin".format(root=root))
    env.PATH.append("{root}/lib".format(root=root))
    env.QT_LOCATION = "{root}/lib/cmake/Qt5".format(root=root)
