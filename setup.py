from setuptools import setup

APP = ['keytracker.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'includes': ['Quartz', 'AppKit', 'Foundation'],
    'packages': ['objc'],
    'plist': {
        'CFBundleName': 'Key Smasher',
        'CFBundleIdentifier': 'com.weijie.keysmasher',
        'CFBundleShortVersionString': '1.0',
        'LSUIElement': True  # Hides from dock
    },
}

setup(
    app=APP,
    name='Key Smasher',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
