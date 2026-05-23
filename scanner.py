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

# Various Document Sizes
SCAN_COORDS = {
    'US_Letter': ('215.9', '279.4')
    
    }

#Where all the scans go.
OUTPUT_DIR = './scans'

def init():
    # Ensuring that the scans directory exists and creates it if not.
    if not Path(OUTPUT_DIR).is_dir():

        Path(OUTPUT_DIR).mkdir()
    

def filename(name=None, num=None, batch=False):
    # Pass argument as filename or timestamp if there is none.
    if batch:
        if name:

            output_filename = str(name + f'_{num:03}')

        else:
    
            output_filename = datetime.now().strftime(f"%Y-%m-%d_%H-%M-%S_{num:03}")

    else:
        if name:

            output_filename = name

        else:
    
            output_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    return output_filename

def scan(file, folder):

    subprocess.run([
        'scanimage',
        f'--device-name={SANE_SCAN_ID}',
        f'--format={FORMAT}', f'--mode={MODE}',
        f'--resolution={DPI}',
        '-x', SCAN_COORDS['US_Letter'][0],
        '-y', SCAN_COORDS['US_Letter'][1],
        f'--output-file={OUTPUT_DIR}/{folder}/{file}.png'
        ]
        )

        
def main():

    init()

    # Main Loop
    while True:
        scan_num = 0
        batch = None

        job_type = input('s for single | b for batch | e to exit > ')
        if job_type in ('e', 'E', 'exit', 'quit'):
            exit(0)

        elif job_type in ('b', 'B', 'batch'):
            batch = True
        
        elif job_type in ('s', 'S', 'single'):
            batch = False
        
        else:
            print(f'Invalid selection: {job_type}')
            continue

        # Determining filename
        while True:
            job_name = input('Enter job name or leave blank for timestamp. > ')

            # Preventing any no-no characters and long filenames.
            if any(char in ('\\', '/', ':', '?', '"', '<', '>', '|') for char in job_name) or len(job_name) >= 100:
                print('Illegal characters in job name or maximum length exceeded.')
                continue
            else:
                #Creates Job folder if none exists.
                if not Path(f'{OUTPUT_DIR}/{job_name}').is_dir():
                    Path(f'{OUTPUT_DIR}/{job_name}').mkdir()
                break
        
        # The Loop for the Job
        while True:
            scan_prompt = input(f'Insert Document #{scan_num + 1}. (e to end job) > ')

            if scan_prompt in ('e', 'E', 'exit', 'quit'):
                print(f'Job Complete. Number of Documents Scanned: {scan_num}')
                break

            scan_num += 1

            scan(file=filename(name=job_name, num=scan_num, batch=batch), folder=job_name)

            #Breaking loop if this is isn't a batch job
            if not batch:
                print('Job Complete.')
                break

    
        


if __name__ == "__main__":
    main()