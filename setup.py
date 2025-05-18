from setuptools import setup

APP = ['print_meunbar.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'LSUIElement': True,
        'CFBundleName': "Reminder Menu Bar",
        'CFBundleDisplayName': "Reminder Menu Bar",
        'CFBundleIdentifier': "com.yourdomain.remindermenubar",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSAppleEventsUsageDescription': 'This app needs access to Reminders to display your tasks.',
    },
    'packages': [
        'rumps',
        'rumps.packages',
        'rumps.packages.ordereddict',
        'collections',
    ],
    'includes': [
        'subprocess',
        'logging',
        'threading',
        '__future__',
    ],
    # 'frameworks': ['/System/Library/Frameworks/Cocoa.framework'],
    'resources': [],
    'strip': True,
    'dylib_excludes': ['libffi.8.dylib'],  # Force py2app to use the system one
    'frameworks': [],  # Empty frameworks list
}

setup(
    name="Reminder Menu Bar",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 