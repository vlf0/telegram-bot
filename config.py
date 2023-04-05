import os

BOT_TOKEN = '5362967182:AAEv2W1S3AmfyaDCRhXKqAC6nhoY84BnSuA'
files_dir = r'C:\Users\dr_dn\Desktop\Кошки'
photo_rel_path = (os.listdir(r'C:\Users\dr_dn\Desktop\Кошки'))  # list of short paths of files
photo_abs_path = [os.path.join(files_dir, ph) for ph in photo_rel_path]  # list of full paths of files

