"""scanimage wrapper"""
from datetime import datetime
import subprocess
from pathlib import Path
from typing import Final
import sys

# ID for my Brother DS 720D
SANE_SCAN_ID: Final[str] = 'dsseries:usb:0x04F9:0x60E0'

# Can also do PDF, probably the only two options that will ever be used.
FORMAT: Final[str] = 'png'

#Linear | Color | Gray
MODE: Final[str] = 'Gray'

#What's DPI again?
DPI: Final[str] = '300'

# Various Document Sizes
SCAN_COORDS: Final[dict[tuple]] = {
    'US_Letter': ('215.9', '279.4')   
    }

#Where all the scans go.
OUTPUT_DIR: Final[Path] = Path('./scans')

def filename(name: str=None, num: int=None, folder: Path=None, batch: bool=False) -> Path:
    """Finding out the name of the file and where it needs to go for a scan."""
    #Determine file extension/format
    extension: str = f'.{FORMAT}'

    # Pass argument as filename or timestamp if there is none.
    if batch:
        if name:

            output_filename = str(name + f'_{num:03}{extension}')

        else:
            output_filename = datetime.now().strftime(f"%Y-%m-%d_%H-%M-%S_{num:03}{extension}")

    else:
        if name:

            output_filename = name + extension

        else:

            output_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + extension

    return folder / output_filename

def scan(file: Path) -> None:
    """Scan subprocess using scanimage command"""

    try:
        subprocess.run([
            'scanimage',
            f'--device-name={SANE_SCAN_ID}',
            f'--format={FORMAT}', f'--mode={MODE}',
            f'--resolution={DPI}',
            '-x', SCAN_COORDS['US_Letter'][0],
            '-y', SCAN_COORDS['US_Letter'][1],
            f'--output-file={file}'
            ],
            check=True
            )
    except subprocess.CalledProcessError as e:
        print(f'Scan failed with return code {e}.')

def main() -> None:
    """Main loop"""

    # Main Loop
    while True:
        scan_num: int = 0
        batch: bool = None

        job_type: str = input('s for single | b for batch | e to exit > ')
        if job_type in ('e', 'E', 'exit', 'quit'):
            sys.exit(0)

        elif job_type in ('b', 'B', 'batch'):
            batch = True
        elif job_type in ('s', 'S', 'single'):
            batch = False

        else:
            print(f'Invalid selection: {job_type}')
            continue

        # Determining filename
        while True:
            job_name: str = input('Enter job name or leave blank for timestamp. > ')

            BAD_CHAR: Final[tuple[str]] = ('\\', '/', ':', '?', '"', '<', '>', '|')
            # Preventing any no-no characters and long filenames.
            if any(char in BAD_CHAR for char in job_name) or len(job_name) >= 100:
                print('Illegal characters in job name or maximum length exceeded.')
                continue

            if not job_name:
                job_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                #Creates Job folder if none exists.
                job_folder: Path = OUTPUT_DIR / job_name
                job_folder.mkdir(parents=True, exist_ok=True)
                break

        # The Loop for the Job
        while True:
            scan_prompt: str = input(f'Insert Document #{scan_num + 1}. (e to end job) > ')

            if scan_prompt in ('e', 'E', 'exit', 'quit'):
                print(f'Job Complete. Number of Documents Scanned: {scan_num}')
                break

            scan_num += 1


            scan(file=filename(name=job_name, num=scan_num, folder=job_folder, batch=batch))

            #Breaking loop if this is isn't a batch job
            if not batch:
                print('Job Complete.')
                break

if __name__ == "__main__":
    main()
