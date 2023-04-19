import os

chat_id_list = [406086387, 150662161]
BOT_TOKEN = '5362967182:AAEv2W1S3AmfyaDCRhXKqAC6nhoY84BnSuA'
welcome_picture = r'C:\Users\dr_dn\Desktop\Picture\welcome.jpg'
files_dir_cat = r'C:\Users\dr_dn\Desktop\frogs'
photo_rel_path = (os.listdir(r'C:\Users\dr_dn\Desktop\frogs'))  # list of short paths of files
# list of full paths of files
cat_photo = [os.path.join(files_dir_cat, ph) for ph in photo_rel_path]
# print(welcome_picture)
# print(random_photo)
