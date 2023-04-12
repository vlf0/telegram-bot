import os
import random

chat_id_list = ['2035624418', '406086387', '150662161']
BOT_TOKEN = '5362967182:AAEv2W1S3AmfyaDCRhXKqAC6nhoY84BnSuA'
welcome_picture, files_dir = open(r'C:\Users\dr_dn\Desktop\Cats\Picture\welcome.jpg', 'rb'), \
                             r'C:\Users\dr_dn\Desktop\Cats'
photo_rel_path = (os.listdir(r'C:\Users\dr_dn\Desktop\Cats'))  # list of short paths of files
# list of full paths of files
random_photo = open(random.choice([os.path.join(files_dir, ph) for ph in photo_rel_path]), 'rb')

