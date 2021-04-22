import subprocess

base_dir = 'output/channel/'
def main():

    command_line = "python utils/0-create_metadata.py --base_dir {} ".format(base_dir)
    subprocess.call(command_line, shell=True)

    command_line = "python utils/1-delete_folders_with_erros.py --base_dir {} --erase".format(base_dir)
    subprocess.call(command_line, shell=True)

    command_line = "python utils/2-clear_dataset.py --base_dir {} --erase".format(base_dir)
    subprocess.call(command_line, shell=True)

    command_line = "python utils/3-create_metadata_min_lev.py --base_dir {}".format(base_dir)
    subprocess.call(command_line, shell=True)

    command_line = "python utils/4-create_internal_metadata_min_lev.py --base_dir {}".format(base_dir)
    subprocess.call(command_line, shell=True)

    command_line = "python utils/5-delete_wavs.py --base_dir {} --erase".format(base_dir)
    subprocess.call(command_line, shell=True)

    command_line = "python utils/6-downsampling_wavs.py --base_dir {} --convert".format(base_dir)
    subprocess.call(command_line, shell=True)

    command_line = "python utils/7-move_downsampled_wavs_folder.py --base_dir {} --erase".format(base_dir)
    subprocess.call(command_line, shell=True)

    command_line = "python utils/8-exclude_unecessary_files.py --base_dir {} --erase".format(base_dir)
    subprocess.call(command_line, shell=True)

    command_line = "python utils/9-change_filepath_metadata.py --base_dir {} --str_filepath_to_remove {}".format(base_dir, base_dir)
    subprocess.call(command_line, shell=True)

if __name__ == "__main__":
  main()
