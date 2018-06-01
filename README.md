# anonymize_dicom

Anonymize script for DICOM file or folder containing dicom files.

Simply removes or replaces patient sensitive information.

## Authors
Rigshospitalet
  - Claes Ladefoged <claes.noehr.ladefoged@regionh.dk>

## Installation (under /opt/bin/rtx2mnc_py):
```
git clone https://github.com/claesnl/anonymize_dicom.git
ln -s $HOME/anonymize_dicom/anonymize_dicom.py /opt/bin/anonymize_dicom
```

## Usage:
```
usage: anonymize_dicom.py [-h] [--name NAME] original output

Convert DICOM to MINC

positional arguments:
  original     Folder or file of original dicom files
  output       Folder or file of anonymized dicom files

optional arguments:
  -h, --help   show this help message and exit
  --name NAME  Name instead of patient name
```

## Requires/Dependencies:
- dicom

## Installation of dependencies:

### Python tools:
```
pip install dicom
```

# Version changes:
- 1.0.0 :: 2018-06-01 :: Added basic functionality working for one or more dicom-files