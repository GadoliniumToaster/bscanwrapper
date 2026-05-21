from datetime import datetime
import subprocess
import sys
from pathlib import Path
import time

# ID for my Brother DS 720D
SANE_SCAN_ID = 'dsseries:usb:0x04F9:0x60E0'

# Can also do PDF, probably the only two options that will ever be used.
FORMAT = 'png'

#Linear | Color | Gray
MODE = 'Gray'

#What's DPI again?
DPI = '300'

# US Letter
SCAN_COORDS = ('215.9', '279.4')

#Where all the scans go.
OUTPUT_DIR = './scans'

def init():
    # Ensuring that the scans directory exists and creates it if not.
    if not Path(OUTPUT_DIR).is_dir():

        Path(OUTPUT_DIR).mkdir()
    

def filename():
    # Pass argument as filename or timestamp if there is none.
    if len(sys.argv) > 1:

        output_filename = str(sys.argv[1])

    else:
 
        output_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    return output_filename

def scan():

    subprocess.run([
        'scanimage',
        f'--device-name={SANE_SCAN_ID}',
        f'--format={FORMAT}', f'--mode={MODE}',
        f'--resolution={DPI}',
        '-x', SCAN_COORDS[0],
        '-y', SCAN_COORDS[1],
        f'--output-file={OUTPUT_DIR}/{filename()}.png'
        ]
        )

if __name__ == "__main__":
    init()
    scan()