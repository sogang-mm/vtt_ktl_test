
import os
import wget
import zipfile


# data path
cwd = os.path.realpath(os.path.dirname(__file__))
data_wd = os.path.join(cwd, 'result')

# download url
friends_s1_image_result_url = "ftp://mldisk.sogang.ac.kr/data/vtt/S01_EP11_23_Friends_Images.zip"



def check_and_downlaod(url, filename, unzip=False):
    file_path = os.path.join(data_wd, filename)
    unzip_dir = filename.split(".")[0]
    print "Check " + filename
    if not os.path.exists(file_path):
        print "...... Start Download " + filename
        wget.download(url, out=data_wd)
        if unzip:
            print "...... Start Unzip " + filename
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(data_wd)



# check
#check_and_downlaod(friends_s1_visual_url, 'S01_EP11_23_Visual_final.zip', unzip=True)
check_and_downlaod(friends_s1_image_result_url, 'S01_EP11_23_Friends_Images.zip', unzip=True)
#check_and_downlaod(k_celeb_face1000_url, 'kr_celeb_crop_face_1000.zip', unzip=True)
#check_and_downlaod(friends_s1_scene_place, 'Friends_S01_place.xlsx')

print 'Done.'