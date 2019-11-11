#-*- coding: utf-8 -*-

import settings

import os
import io
import requests, json


def get_result_path(filepath):
    outfile = filepath.replace('\\data\\', '\\result\\')
    outfile = outfile + '.result'

    return outfile


def anal_face(filename, outfile):
    file = {'image' : (filename, open(filename, 'rb'), )}
    response = requests.post(settings.ANAL_FACE_SERVER_URL, files=file)

    file = io.open(outfile, "w", encoding='utf-8')
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


def anal_face_all():
    # loop for visual data
    cwd = os.path.realpath(os.path.dirname(__file__))
    data_wd = os.path.join(cwd, 'data', 'kr_celeb_crop_face_1000_testset')

    all_filepath = getListOfFiles(data_wd)

    for filepath in all_filepath:
        if filepath.split('.')[1] == 'png':
            outfile = get_result_path(filepath)
            dir = os.path.dirname(outfile)
            try:
                os.makedirs(dir)
            except OSError:
                pass
            if not os.path.exists(outfile):
                anal_face(filepath, outfile)
            else:
                print "skip exist result" + outfile


def anal_place(filename, outfile):
    file = {'image' : (filename, open(filename, 'rb'), )}
    response = requests.post(settings.ANAL_PLACE_SERVER_URL, files=file)

    file = io.open(outfile, "w", encoding='utf-8')
    file.write(response.text)
    file.close()
    print response.text


def anal_place_all():
    # loop for visual data
    cwd = os.path.realpath(os.path.dirname(__file__))
    data_wd = os.path.join(cwd, 'data', 'val_256')

    all_filepath = getListOfFiles(data_wd)

    for filepath in all_filepath:
        if filepath.split('.')[1] == 'jpg':
            outfile = get_result_path(filepath)
            dir = os.path.dirname(outfile)
            try:
                os.makedirs(dir)
            except OSError:
                pass
            if not os.path.exists(outfile):
                anal_place(filepath, outfile)
            else:
                print "skip exist result" + outfile


def is_correct_face_top1(answer_file_path, verbose=False):
    with io.open(answer_file_path, encoding='utf-8') as data_file:
        data = json.load(data_file)

        max_score = 0.0
        max_desc = 'None'
        ret = False

        try:
            labels = data['result'][0]['label']
            for label in labels:
                if max_score < label['score']:
                    max_score = label['score']
                    max_desc = label['description']

            max_desc = max_desc.replace(' ', '_')


            if answer_file_path.find(max_desc) > 0:
                ret = True
        except:
            ret = False

        if verbose:
            print ret, max_desc, max_score

        return ret


def is_correct_face_top5(answer_file_path, verbose=False):
    with io.open(answer_file_path, encoding='utf-8') as data_file:
        data = json.load(data_file)

        hit_score = 0.0
        hit_desc = 'None'
        ret = False

        try:
            labels = data['result'][0]['label']
            for label in labels:
                desc = label['description']
                desc_under = desc.replace(' ', '_')
                if answer_file_path.find(desc) > 0:
                    hit_score = label['score']
                    hit_desc = desc
                    ret = True
                elif answer_file_path.find(desc_under) > 0:
                    hit_score = label['score']
                    hit_desc = desc
                    ret = True

        except:
            ret = False

        if verbose:
            print ret, hit_desc, hit_score

        return ret


def eval_face_accuracy(verbose=False):
    cwd = os.path.realpath(os.path.dirname(__file__))
    data_wd = os.path.join(cwd, 'result', 'kr_celeb_crop_face_1000_testset')

    all_filepath = getListOfFiles(unicode(data_wd))

    face_cnt = 0
    hit_face_cnt = 0

    for filepath in all_filepath:
        face_cnt = face_cnt + 1
        if is_correct_face_top5(filepath, verbose):
            hit_face_cnt = hit_face_cnt + 1

    ret_rate = float(hit_face_cnt)/float(face_cnt)
    print "Face Recognition Accuracy : {} ({}/{})".format(ret_rate, hit_face_cnt, face_cnt)

    return ret_rate


def eval_place_accuracy():
    # Place365 실험 결과 (TOP1)

    hit_cnt = 22957
    place_cnt = 36500
    ret_rate = float(hit_cnt) / float(place_cnt)

    print "Place Recognition Accuracy : {} ({}/{})".format(ret_rate, hit_cnt, place_cnt)
    return ret_rate


def eval_object_accuracy():
    # 또 오해영 실험 결과 (실험3)
    ret_rate = 0.7043

    print "Object Recognition Accuracy : {}".format(ret_rate)
    return ret_rate


def eval_all():
    face_acc = eval_face_accuracy()
    place_acc = eval_place_accuracy()
    obj_acc = eval_object_accuracy()

    face_err = 1-face_acc
    place_err = 1-place_acc
    obj_err = 1-obj_acc

    # 1차년도 보고서에 작성한 pre defined weight
    face_weight = 0.4
    place_weight = 0.3
    obj_weight = 0.3

    # 목표 오류율
    # 1차: 36
    # 2차: 30
    # 3차: 24


    overall = face_err * face_weight + place_err * place_weight + obj_err * obj_weight

    eval_str = '(Error Rate = {} * face_err({}) + {} * place_err({}) + {} * object_err({}))'.format(
        face_weight, face_err,
        place_weight, place_err,
        obj_weight, obj_err
    )
    print
    print 'Metadata Error Rate = {}'.format(overall)
    print eval_str


