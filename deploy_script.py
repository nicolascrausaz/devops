#!/usr/bin/python

import os
import sys
import getopt
import shutil


def main(argv):
    clientDirectory = ''
    serverDirectory = ''
    try:
        opts, args = getopt.getopt(
            argv, "hc:s:", ["cdirectory=", "sdirectory="])
    except getopt.GetoptError:
        print('deploy_script.py -c <clientDirectory> -s <serverDirectory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('deploy_script.py -c <clientDirectory> -s <serverDirectory>')
            sys.exit()
        elif opt in ("-c", "--cdirectory"):
            clientDirectory = arg
        elif opt in ("-s", "--sdirectory"):
            serverDirectory = arg
    print('Client Directory is ', clientDirectory)
    print('Server Directory is ', serverDirectory)

    if len(clientDirectory) > 0 and len(serverDirectory) > 0:
        # 1) Build angular app
        print('---------- STEP 1 : BUILD ANGULAR APP ----------')
        os.chdir(clientDirectory)
        os.system("ng build")
        # 2) Copy build in springboot app
        print('---------- STEP 2 : COPY BUILD -----------------')
        path = os.path.join(clientDirectory, 'dist')
        os.chdir(path)
        applicationName = os.listdir(path)[0]
        # HINT : MAC as a file .DS_Store that we don't want
        if applicationName == ".DS_Store":
            applicationName = os.listdir(path)[1]
        src_path = os.path.join(clientDirectory, 'dist', applicationName)
        dst_path = os.path.join(serverDirectory, 'src', 'main', 'resources', 'static')
        # Check if dest directory exist, if not create it
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        # Remove all file in dest directory
        shutil.rmtree(dst_path)
        # Copy angular app
        shutil.copytree(src_path, dst_path)
        # 3) Build springboot app
        print('---------- STEP 3 : BUILD SPRINGBOOT APP -------')
        os.chdir(serverDirectory)
        os.system("mvn clean install -DskipTests")
        # 4) Deploy full application
        print('---------- STEP 4 : DEPLOY ON AWS --------------')
        os.system("eb deploy --staged")
        print('--------------------- DONE ---------------------')

    else:
        print('you must give 2 parameters deploy_script.py -c <clientDirectory> -s <serverDirectory>')


if __name__ == "__main__":
    main(sys.argv[1:])
