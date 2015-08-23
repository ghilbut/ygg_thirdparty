#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import platform
import sys

BASEPATH = os.path.dirname(__file__)
BASEPATH = os.path.abspath(BASEPATH)

print BASEPATH

# ready depot_tools environment
DEPOT_TOOLS_PATH = os.path.join(BASEPATH, 'depot_tools')
if not os.path.exists(DEPOT_TOOLS_PATH):
  os.system('git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git')

if not os.path.isdir(DEPOT_TOOLS_PATH):
  print '%s is not a directory. process is stopped.' % DEPOT_TOOLS_PATH
  exit(-1)

os.chdir(DEPOT_TOOLS_PATH)
os.system('git pull')
os.chdir(BASEPATH)

os.environ["PATH"] += os.pathsep + DEPOT_TOOLS_PATH
os.system('gclient')

# ready v8 environment
V8_PATH = os.path.join(BASEPATH, 'v8')
if not os.path.exists(V8_PATH):
  os.system('fetch v8')
  os.chdir(V8_PATH)
  os.system('git config branch.autosetupmerge always')
  os.system('git config branch.autosetuprebase always')
  os.system('git new-branch work')
  os.chdir(BASEPATH)

if not os.path.isdir(V8_PATH):
  print '%s is not a directory. process is stopped.' % V8_PATH
  exit(-1)

# update
os.chdir(V8_PATH)
os.system('git pull')
os.system('gclient sync')

# build
PLATFORM = platform.architecture()[0]
OPTIONS = { '32bit': 'ia32', '64bit': 'x64' }
os.system('build/gyp_v8 -Dtarget_arch=%s' % OPTIONS[PLATFORM])

CMD = {
    'linux2': '', # Linux (2.x and 3.x)
    'win32': '', # Windows
    'cygwin': '', # Windows/Cygwin
    'darwin': 'xcodebuild -project build/all.xcodeproj -configuration Release', # Mac OS X
    'os2': None,    # OS/2
    'os2emx': None, # OS/2 EMX
    'riscos': None, # RiscOS
    'atheos': None  # AtheOS
  }
cmd = CMD[sys.platform]
if cmd != None:
  os.system(cmd)
  os.system('xcodebuild/Release/unittests')

