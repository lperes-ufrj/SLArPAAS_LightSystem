import zipfile
import glob
import os

def compress_files_with_label(directory, label, zip_filename):
    # Create a zip file
    
    files_path = glob.glob(os.path.join(directory,label))
    #print(files_path)
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for filename in files_path:
            zipf.write(filename)

# Example usage
directory_to_search = './'
label_to_search = '2pf_2p7kohm_noradiosource_*'  # e.g. 'data'
output_zip = '2pf_2p7kohm_noradiosource.zip'

compress_files_with_label(directory_to_search, label_to_search, output_zip)
