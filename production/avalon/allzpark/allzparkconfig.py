

def environment_plugin():
    import allzparkplugin
    return allzparkplugin.AvalonLauncher


def themes():
    _themes = []

    try:
        from ozark import style
    except ImportError:
        print("Failed to load Ozark CSS stylesheet.")
    else:
        _themes.append({
            "name": "avalon",
            "source": style.load_stylesheet(),
        })

    return _themes
