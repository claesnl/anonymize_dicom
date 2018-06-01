#!/usr/bin/env python
import os, sys, argparse
import dicom
from dicom.errors import InvalidDicomError
from shutil import copyfile


"""

Date: 1/6-2018
Author: Claes Ladefoged ( claes.noehr.ladefoged@regionh.dk )

###

Anonymize script for DICOM file or folder containing dicom files
Simply removes or replaces patient sensitive information.

-----------------------------------------------------------------
### USAGE OUTSIDE PYTHON ###
usage: anonymize_dicom.py [-h] [--name NAME] original output

Convert DICOM to MINC

positional arguments:
  original     Folder or file of original dicom files
  output       Folder or file of anonymized dicom files

optional arguments:
  -h, --help   show this help message and exit
  --name NAME  Name instead of patient name

-----------------------------------------------------------------

### USAGE INSIDE PYTHON AFTER ADDING TO PYTHONPATH AND PATH ###
import anonymize_dicom as DCM
DCM.anonymize(dicom_original,dicom_anonymized)
or
DCM.anonymize_folder(dicom_original_folder,dicom_anonymized_folder)

-----------------------------------------------------------------

"""

def anonymize(filename, output_filename, new_person_name="anonymous", remove_private_tags=False, copy_non_dicom=True):

	def PN_callback(ds, data_element):
		"""Called from the dataset "walk" recursive function for all data elements."""
		if data_element.VR == "PN":
			data_element.value = new_person_name
	def curves_callback(ds, data_element):
		"""Called from the dataset "walk" recursive function for all data elements."""
		if data_element.tag.group & 0xFF00 == 0x5000:
			del ds[data_element.tag]

	try:
		# Load the current dicom file to 'anonymize'
		dataset = dicom.read_file(filename)

		# Remove patient name and any other person names
		dataset.walk(PN_callback)

		# Remove data elements (should only do so if DICOM type 3 optional) 
		for name in ['OtherPatientIDs', 'OtherPatientIDsSequence']:
			if name in dataset:
				delattr(dataset, name)

		# Same as above but for blanking data elements that are type 2.
		for name in ['PatientBirthDate','PatientID','PatientsAddress','PatientsTelephoneNumbers']:
			if name in dataset:
				dataset.data_element(name).value = ''

		if remove_private_tags:
			dataset.remove_private_tags()

		# write the 'anonymized' DICOM out under the new filename
		dataset.save_as(output_filename)   
	except InvalidDicomError:
		# Copy over files that are not DICOM
		copyfile(filename,output_filename.replace(os.path.basename(output_filename),os.path.basename(filename)))


# Anonymize all files within a folder.
# If folder contains subfolders, keep their hierachy, and also anonymize their files.
def anonymize_folder(foldername,output_foldername,new_person_name="anonymous",remove_private_tags=False):

	def _anonymize_folder(_foldername,_output_foldername,_new_person_name,_remove_private_tags):
		if os.path.exists(_output_foldername):
			if not os.path.isdir(_output_foldername):
				raise IOError, "Input is directory; output name exists but is not a directory"
		else: # out_dir does not exist; create it.
			os.makedirs(_output_foldername)

		print("Anonymizing folder: %s" % _foldername)
		if len(os.listdir(_foldername)) > 9999:
			exit('Too many files in folder for script..')
		for fid,filename in enumerate(os.listdir(_foldername)):
			extention = '.dcm' if os.path.splitext(filename)[1]=='' else os.path.splitext(filename)[1]
			filename_out = "dicom"+str(fid+1).zfill(4)+extention
			if not os.path.isdir(os.path.join(_foldername, filename)):
				#print filename + " -> " + filename_out + "...",
				anonymize(os.path.join(_foldername, filename), os.path.join(_output_foldername, filename_out),_new_person_name)
				print "done\r",

	# Anonymize all files in current folder
	_anonymize_folder(foldername,output_foldername,new_person_name,remove_private_tags)
	# Go through all subfolders - anonymize each of them
	for root, dirs, files in os.walk(foldername):
		for subfolder in dirs:
			to_folder = os.path.join(root,subfolder).replace(foldername,output_foldername)
			_anonymize_folder(os.path.join(root,subfolder),to_folder,new_person_name,remove_private_tags)	


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert DICOM to MINC')

	parser.add_argument('original', type=str, help='Folder or file of original dicom files')
	parser.add_argument('output', type=str, help='Folder or file of anonymized dicom files')
	parser.add_argument('--name', help='Name instead of patient name', default='anonymous')

	args = parser.parse_args()

	if os.path.isdir(args.original):
		anonymize_folder(args.original,args.output,args.name)
	else:
		anonymize(args.original,args.output,args.name)

