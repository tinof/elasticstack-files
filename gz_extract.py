import os, gzip, shutil
from tqdm import tqdm

dir_name = ''


def gz_extract(directory):
    extension = ".gz"
    os.chdir(directory)
    for item in tqdm(os.listdir(directory), desc="Extracting files"):  # loop through items in dir
        if item.endswith(extension):  # check for ".gz" extension
            gz_name = os.path.abspath(item)  # get full path of files
            file_name = (os.path.basename(gz_name)).rsplit('.', 1)[0]  # get file name for file within
            with gzip.open(gz_name, "rb") as f_in, open(file_name, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
            os.remove(gz_name)  # delete zipped file


gz_extract(dir_name)
