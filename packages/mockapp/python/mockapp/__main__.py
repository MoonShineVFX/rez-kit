

def mock(appname):
    from Qt import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    button = QtWidgets.QPushButton(appname)
    button.clicked.connect(lambda: print("This is " + appname))
    button.show()
    app.exec_()


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Mock App")
    parser.add_argument("appname", help="App name to mock")

    opt, unknown = parser.parse_known_args()

    sys.exit(mock(opt.appname))
