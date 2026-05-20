import subprocess

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

def scan():
    subprocess.run([
        'scanimage',
        f'--device-name={SANE_SCAN_ID}',
        f'--format={FORMAT}', f'--mode={MODE}',
        f'--resolution={DPI}',
        '-x', SCAN_COORDS[0],
        '-y', SCAN_COORDS[1],
        f'--output-file=test_scan.png'
        ]
        )

if __name__ == "__main__":
    scan()