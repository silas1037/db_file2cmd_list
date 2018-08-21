#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sqlite3
import os

def dirlist(path, allfile):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)

        elif filepath.endswith('db'):
            if 'Cache' in filepath:
                allfile.append(filepath)
    return allfile

filelist = dirlist("D:/tst/tst2", [])

allbat = []
pathbat = []
filebat = []
callp = []
callf = []
callall = []
for everyone in filelist:
    allbat.append(everyone[:-22]+'ru.bat')
    pathbat.append(everyone[:-22] + 'p.bat')
    filebat.append(everyone[:-22] + 'f.bat')
    callp.append(everyone[:-22] + 'pall.bat')
    callf.append(everyone[:-22] + 'fall.bat')
    callall.append(everyone[:-22] + 'call.bat')
namelist = allbat

for i in range(0,len(filelist)):
    conn = sqlite3.connect(filelist[i])
    cursor = conn.cursor()
    cursor.execute("select * from cache_file")
    while True:
        value = cursor.fetchone()
        if not value:
            break
        path = value[2]
        name = value[3]
        size = value[4]
        md5 = value[5]
        final_path = path[1:].replace("/", "\\") + str(name)
        if size!=0:
            with open(namelist[i], "a", encoding='utf-8') as fa:
               fa.write('BaiduPCS-Go ru -length='+ str(size) + ' -md5=' + str(md5) + ' "' + str(path) + str(name) +'"'+'\n')
            with open(filebat[i], "a", encoding='utf-8') as ff:
               ff.write('echo BaiduPCS-Go ru -length='+ str(size) + ' -md5=' + str(md5) + ' "' + str(path) + str(name) +'"' + '>>'+   '"' +final_path + ".bat"+'"'+'\n')
        if size == 0:
            with open(pathbat[i], "a", encoding='utf-8') as fp:
                fp.write('md ' + '"' + str(final_path) + '"' + '\n')
    with open(callall[i],"a") as fcallall:
        fcallall.write('chcp 65001\nru.bat')
        fcallall.close()
    with open(callp[i],"a") as fcallp:
        fcallp.write('chcp 65001\np.bat')
        fcallp.close()
    with open(callf[i],"a") as fcallf:
        fcallf.write('chcp 65001\nf.bat')
        fcallf.close()

    for endbat in [namelist[i],pathbat[i],filebat[i],]:
        with open(endbat, "a", encoding='utf-8') as eendbat:
            eendbat.write('pause')
            eendbat.close()
