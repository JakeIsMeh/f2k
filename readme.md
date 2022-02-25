# f2k
A simple LaunchPad/Take2Launcher replacement for Civ VI

# Installation

Place f2k.exe in `[PATH_TO_STEAM]/steamapps/common/Sid Meier's Civilization VI`

In Steam:
1. Select the game
2. Gear icon > Properties
3. Under General, set launch options to the following:
```
"[PATH_TO_STEAM]\steamapps\common\Sid Meier's Civilization VI\f2k.exe" %command%
```
## Sidenotes
### SmartScreen blocked this program from running
Right-click f2k.exe and click on properties.  
At the bottom of the window there should be a checkbox to unblock it.  
Hit Apply and OK.

### Epic Games Store
Nothing about f2k is written to be Steam-specific, with the exception of the hidden launch option cleaning,  
which might eliminate some EGS-specific launch options.

# Building from source

## Requirements: 
- Windows
- Python >=3.10
- Git
### Optional:
- UPX
  - Highly recommended for reducing filesize
```sh
# If you have Python2 (why), make sure to substitute python for python3

# Clone the repository
git clone https://github.com/JakeIsMeh/f2k.git && cd f2k

# Creating a virtual environment
python -m venv venv --update-deps

# Activate the virtuakl environment
call venv/Scripts/activate

# Installing dependencies
pip install -r requirements.txt

# Check for UPX
# If your UPX isn't in PATH, you should edit build.py to
# point PyInstaller to your UPX install
where upx

# Build
# Optionally, add 'clean' as an argument to force a clean build
python build.py [clean]

# Build output should be located in ./dist/
```

# Open Source Acknowledgements
- Python (PSFL2)
- Qt (LGPL3)
- PySide6 (LGPL3)

# License
f2k is licensed under the permissive `MIT (Expat)` license.  
Despite that, I humbly ask you to open source your own changes to f2k.