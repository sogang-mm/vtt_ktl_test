
import settings
import requests
import os


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
            outfile = filepath.replace('\\data\\', '\\result\\')
            outfile = outfile + '.result'
            dir = os.path.dirname(outfile)
            try:
                os.makedirs(dir)
            except OSError:
                pass
            if not os.path.exists(outfile):
                anal(filepath, outfile)
            else:
                print "skip exist result" + outfile
