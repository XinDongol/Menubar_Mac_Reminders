rm -rf build dist ./ReminderMenuBar.dmg ./Reminder\ Menu\ Bar.spec
pip install pyinstaller
pyinstaller --windowed --name "Reminder Menu Bar" --icon=icon.icns print_meunbar.py
dmgbuild -s dmg_settings.py "Reminder Menu Bar" "ReminderMenuBar.dmg"