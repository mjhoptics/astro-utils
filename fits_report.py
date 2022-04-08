#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2022 Michael J. Hayford
""" read a night's worth of fits file headers and return useful report

Input a list of header items that will be collected from each fits file.

Given a root directory, traverse it and its children and find every fits file.

For each fits file, read the fits header info and return the requested fits 
header items in a .csv file located in the fits_root directory

Created on Sun Jan 30 22:47:12 2022

.. codeauthor: Michael J. Hayford
"""

import csv
from pathlib import Path
from astropy.io import fits
from astropy.time import Time

# Fits keywords to extract
fits_keywords = [
    'file_name',
    'DATE-OBS',
    'IMAGETYP',
    'FILTER',
    'FOCTEMP',
    'FOCPOS',
    'EXPOSURE',
    'CCD-TEMP',
    'XBINNING',
    'GAIN',
    'EGAIN',
    'FOCALLEN',
    'XPIXSZ',
    'PIXSCALE',
    'ANGLE',
    'AOCSKYQU',
    ]

# Location with subdirectories
fits_root = Path("/Users/Mike/astro processing/20220402")

# Get List of all images
fits_image_files = fits_root.glob('**/*.fit')

fits_report = []

# For each image
for fits_image_filename in fits_image_files:
    # Get File name and extension
    with fits.open(fits_image_filename) as hdul:
        hdu = hdul[0]
        if hdu.header['IMAGETYP'] == 'LIGHT':
            new_record = [fits_image_filename.name]
            for keywd in fits_keywords[1:]:
                try:
                    keywd_value = hdu.header[keywd]
                except KeyError:
                    keywd_value = ''
                finally:
                    if keywd == 'DATE-OBS':
                        date_obs = hdu.header['DATE-OBS']
                        keywd_value = Time(date_obs).to_datetime()
                new_record.append(keywd_value)
            
            fits_report.append(new_record)

# Write the accumulated file/header info to a csv file.
date_str = Time(date_obs).to_value('iso', subfmt='date')
report_file = 'fits_report_' + date_str + '.csv'
with open(fits_root / report_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fits_keywords)
    csvwriter.writerows(fits_report)
