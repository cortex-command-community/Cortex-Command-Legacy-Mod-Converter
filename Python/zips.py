import os, shutil, zipfile
from pathlib import Path

from Python import shared_globals as cfg


def unzip(input_folder_path):
	for f in os.listdir(input_folder_path):
		zip_path = os.path.join(input_folder_path, f)
		if zipfile.is_zipfile(zip_path):
			with zipfile.ZipFile(zip_path) as item:
				item.extractall(input_folder_path)
			os.remove(zip_path)


def create_zips(input_folder_path, output_folder):
	if input_folder_path.endswith(".rte"):
		create_single_zip(Path(input_folder_path).name, output_folder)
	else:
		# TODO: Move check if it's a directory out of this loop. 
		folder_names = [f for f in os.listdir(input_folder_path) if os.path.isdir(os.path.join(output_folder, f))]
		for mod_name in folder_names:
			if mod_name.endswith(".rte"):
				create_single_zip(mod_name, output_folder)


def create_single_zip(mod_name, output_folder):
	print("Zipping '{}'".format(mod_name))
	mod_path = os.path.join(output_folder, mod_name)
	shutil.make_archive(mod_path.replace(".rte", f"-v1.0-{cfg.GAME_VERSION}" + ".rte"), "zip", root_dir=output_folder, base_dir=mod_name)
	shutil.rmtree(mod_path)