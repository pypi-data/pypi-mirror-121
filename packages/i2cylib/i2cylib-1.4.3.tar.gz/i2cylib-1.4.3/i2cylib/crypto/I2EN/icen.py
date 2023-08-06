#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Icy(enderman1024@foxmail.com)
# OS: ALL
# Name: Simple File encoder/decoder
##VERSION: 3.1


import os
import sys
import time
from ..iccode import Iccode


def action_bar(prt, maxlen):  # Action bar generator
    bar = "[" + "#" * int(prt * maxlen) + " " * (maxlen - int(prt * maxlen)) + "]"
    return bar


def round(data, num):  # float rounder
    data = str(data)
    n = 0
    for i in data:
        if i == ".":
            break
        else:
            n += 1
    try:
        data = data[:n + num]
    except:
        data = data
    return data


def get_args():  # read command shell's argument(s)
    opts = sys.argv[1:]
    argv = ""
    res = {}
    for i in opts:
        if len(argv) > 0 and "-" != i[0]:
            res.update({argv: i})
            argv = ""
        if "-" == i[0]:
            argv = i
            res.update({argv: ""})
    return res


def trf_time(data):  # Time transformer
    time_data = data
    hour = int(time_data / 3600)
    time_data = time_data - hour * 3600
    mins = int(time_data / 60)
    time_data = time_data - mins * 60
    sec = time_data
    return (hour, mins, sec)


def usage():
    print("""IcCode File Encrypter (by Icy)

Usage: icen.py -f <Target_File> -d/-e -k <Key> -t <File_to_Save>

Options:
 -h --help                           - display this page
 -f --file <File_Path>               - target file to be encode
                                       or decoder
 -d --decode                         - decode mode
 -e --encode                         - encode mode(default)
 -l --level                          - fingerprint level (3 default, >=1)
 -k --key <Key>                      - the key which is used for
                                       enctypter to encrypt
 -t --to <File_Path>                 - file to save to(default: %filename%.enc)

Example:
 $ icen.py -f "test.jpg" -e -k "test" -t "res.jpg"
""")
    sys.exit(1)


def main():
    global FILE, ENCODE, KEY, TO
    FILE = None
    ENCODE = True
    KEY = None
    TO = None
    level = 3
    opts = get_args()
    if opts == {}:
        MODE = input("Mode(\"e\"--encode, \"d\"--decode): ")
        if MODE == "e":
            ENCODE = True
        elif MODE == "d":
            ENCODE = False
        else:
            print("please input correct words")
            sys.exit(1)

        FILE = input("Target file path: ")

        if not os.path.exists(FILE):
            print("Can not find file \"" + FILE + "\"")
            sys.exit(1)

        TO = input("Finnal encripted(decripted) file path: ")

        KEY = input("key: ")
        level = input("fingerprint level(>=1): ")

    for i in opts:
        if i in ("-h", "--help"):
            usage()
        elif i in ("-f", "--file"):
            FILE = opts[i]
            if not os.path.exists(FILE):
                print("Can not find file \"" + FILE + "\"")
                sys.exit(1)
        elif i in ("-e", "--encode"):
            ENCODE = True
        elif i in ("-d", "--decode"):
            ENCODE = False
        elif i in ("-k", "--key"):
            KEY = opts[i]
        elif i in ("-t", "--to"):
            TO = opts[i]
        elif i in ("-l", "--level"):
            level = opts[i]
        else:
            print("Unhandled option: \"" + i + "\", try \"-h\" for help")
            sys.exit(1)
    try:
        level = int(level)
        if level < 1:
            raise Exception()
    except Exception:
        print("finger print level must be int type and bigger than 0")

    if KEY == None:
        KEY = input("key:")

    if None == FILE:
        print("syntax error, please check your command")
        sys.exit(1)

    if not len(TO):
        TO = FILE + ".enc"
    print("File Name  : " + FILE)
    if ENCODE:
        mode = "Encode"
    else:
        mode = "Decode"
    print("MODE       : " + mode)
    print("Level      : " + str(level))
    print("Destination: " + TO)
    print("Key        : " + KEY)
    file_a = open(FILE, "rb")
    try:
        file_to = open(TO, "wb")
    except Exception as err:
        print("Failed to open file: \"" + TO + "\", result: " + str(err))
        return
    clk = 0
    lt = time.time()
    st = lt
    file_size = os.path.getsize(FILE)
    doed = 0
    coder = Iccode(KEY, fingerprint_level=level)
    ui = ""
    while True:
        data = file_a.read(2048)
        #print(len(data))
        doed = doed + len(data)
        if ENCODE:
            data = coder.encode(data)
        else:
            data = coder.decode(data)
        if len(data) == 0:
            break
        try:
            file_to.write(data)
        except Exception as err:
            print("Failed to write data to file: \"" + TO + "\", result: " + str(err))
            sys.exit(1)
        if time.time() - lt >= 1:
            speed = 1 / (time.time() - lt)
            lt = time.time()
            clk = 0
            eta = trf_time((file_size - doed) / (speed * 1024 * 1024))
            if eta[0] != 0:
                eta = ("0" + str(eta[0]))[-2:] + ":" + ("0" + str(eta[1]))[-2:] + ":" + ("0" + str(int(eta[2])))[-2:]
            else:
                eta = ("0" + str(eta[1]))[-2:] + ":" + ("0" + str(int(eta[2])))[-2:]
            sys.stdout.write("\r" + " " * len(ui) + "\r")
            ui = action_bar(doed / file_size, 25) + " " + str(round(100 * doed / file_size, 2)) + "% " + str(
                round(speed, 2)) + "MB/s " + eta + " ETA"
            sys.stdout.write("\r" + ui)
            sys.stdout.flush()
        clk += 1
    file_a.close()
    file_to.close()
    eta = trf_time(time.time() - st)
    sys.stdout.write("\r" + " " * len(ui))
    if eta[0] != 0:
        eta = ("0" + str(eta[0]))[-2:] + ":" + ("0" + str(eta[1]))[-2:] + ":" + ("0" + str(int(eta[2])))[-2:]
    else:
        eta = ("0" + str(eta[1]))[-2:] + ":" + ("0" + str(int(eta[2])))[-2:]
    ui = action_bar(1, 25) + " 100%  PT: " + eta + " AS: " + str(
        round(file_size / ((time.time() - st) * 1024 * 1024), 2)) + "MB/s"
    sys.stdout.write("\r" + ui + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
