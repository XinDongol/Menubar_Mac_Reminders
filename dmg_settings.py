# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path

# Basic settings
application = defines.get('app', 'dist/Reminder Menu Bar.app')
appname = os.path.basename(application)

# Volume format (see `hdiutil create -help` for more info)
format = defines.get('format', 'UDBZ')

# Volume size
size = defines.get('size', '100M')

# Files to include
files = [application]

# Symlinks to create
symlinks = {'Applications': '/Applications'}

# Background
background = None
icon_size = 128
icon_locations = {
    appname:        (140, 120),
    'Applications': (500, 120)
}

# Window configuration
window_rect = ((100, 100), (640, 280))
default_view = 'icon-view' 