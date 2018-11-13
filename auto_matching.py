
import settings
import requests
import os
import json


def get_result_path(filepath):
    outfile = filepath.replace('\\data\\', '\\result\\')
    obj_outfile = outfile + '.obj_result'
    outfile = outfile + '.result'

    return outfile, obj_outfile


def anal(filename, outfile):
    param = {
        'modules' : 'friends'
    }

    file = {'image' : (filename, open(filename, 'rb'), )}
    response = requests.post(settings.ANAL_SERVER_URL, files=file, data=param)

    file = open(outfile, "w")
    file.write(response.text)
    file.close()
    print response.text


def anal_obj(filename, outfile):
    file = {'image' : (filename, open(filename, 'rb'), )}
    response = requests.post(settings.ANAL_OBJ_SERVER_URL, files=file)

    file = open(outfile, "w")
    file.write(response.text)
    file.close()
    print response.text


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def anal_all():
    # loop for visual data
    cwd = os.path.realpath(os.path.dirname(__file__))
    data_wd = os.path.join(cwd, 'data', 'S01_EP11_23_Friends_Images')

    all_filepath = getListOfFiles(data_wd)

    for filepath in all_filepath:
        if filepath.split('.')[1] == 'jpg':
            outfile, obj_outfile = get_result_path(filepath)
            dir = os.path.dirname(outfile)
            try:
                os.makedirs(dir)
            except OSError:
                pass
            if not os.path.exists(outfile):
                anal(filepath, outfile)
            else:
                print "skip exist result" + outfile

            if not os.path.exists(obj_outfile):
                anal_obj(filepath, obj_outfile)
            else:
                print "skip exist obj result" + obj_outfile


def get_person(person_data):
    name_list = ['monica', 'ross', 'rachel', 'joey', 'chandler', 'phoebe']
    face_list = list()
    body_list = list()
    for name in name_list:
        if person_data[name][0]['face_rect']['min_x'] != 'none':
            face = person_data[name][0]['face_rect']
            face[u'name'] = unicode(name)
            face_list.append(face)
        if person_data[name][0]['full_rect']['min_x'] != 'none':
            body = dict()
            body[u'object_name'] = u'person'
            body[u'object_rect'] = person_data[name][0]['full_rect']

            body_list.append(body)

    return face_list, body_list


def find_face(face_list):
    return 1


def find_object(obj_list):
    return 1


def eval(answer_file_path):
    with open(answer_file_path) as data_file:
        data = json.load(data_file)

    hit_cnt = 0
    object_cnt = 0

    #print data['visual_results']
    for image_result in data['visual_results']:
        print '------------------------'
        print image_result['image']
        face_list, body_list = get_person(image_result['person'][0])
        obj_list = image_result['object']
        object_cnt = object_cnt + len(face_list)
        hit_cnt = hit_cnt + find_face(face_list)
        object_cnt = object_cnt + len(body_list)
        hit_cnt = hit_cnt + find_object(body_list)
        object_cnt = object_cnt + len(obj_list)
        hit_cnt = hit_cnt + find_object(obj_list)
        print face_list
        print body_list
        print obj_list

    return hit_cnt, object_cnt


def eval_all():
    cwd = os.path.realpath(os.path.dirname(__file__))
    data_wd = os.path.join(cwd, 'data', 'S01_EP11_23_Visual_final')

    all_hit_cnt = 0
    all_obj_cnt = 0

    all_filepath = getListOfFiles(data_wd)
    for filepath in all_filepath:
        if filepath.split('.')[1] == 'json':
            hit_cnt, obj_cnt = eval(filepath)
            all_hit_cnt = all_hit_cnt + hit_cnt
            all_obj_cnt = all_obj_cnt + obj_cnt

    print
    print "(hit) {} / {} (all)".format(all_hit_cnt, all_obj_cnt)
    print "Auto Matching Success Rate : {}".format(float(all_hit_cnt)/float(all_obj_cnt))
