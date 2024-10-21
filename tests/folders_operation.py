import os
your_folder_path = r'D:\Documents\Shared_Files'
list_of_files = os.listdir(your_folder_path)

for ur_fname in list_of_files:
    print(ur_fname)

for ur_fname in list_of_files:
    if '.csv' in ur_fname:
        print(ur_fname)

for root, dirs, files in os.walk(your_folder_path):
    print(str(root) + ' ' + str(dirs) + ' ' + str(files))