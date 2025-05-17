from setuptools import setup

APP = ['keytracker.py']  # your script filename
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'includes': ['AppKit', 'Quartz', 'Foundation'],
    'plist': {
        'CFBundleName': 'Key Smasher',
        'CFBundleDisplayName': 'Key Smasher',
        'CFBundleIdentifier': 'com.weijie.keysmasher',
        'CFBundleVersion': '0.1.0',
        'LSUIElement': True,  # Prevents Dock icon
    },
}

setup(
    app=APP,
    name='Key Smasher',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
