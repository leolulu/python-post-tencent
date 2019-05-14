# -*- coding:utf-8 -*-
from __future__ import unicode_literals
'''
Created on 2019年4月26日

@author: Jinghao Yan
#Code transfer between Uyghur and Latin 
#usage:
#From ugyhur to latin
#python ug_coding.py need 'auyghur.code' and 'ug.sed' file 
'''
import sys
import re
import argparse
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

#load code mapping and re file 
def cmap_file(filename, ug_refile):
    ug_sed_temp = {}
    ucodedict_temp = {}
    acode = ""
    ucode = ""
 
    with codecs.open (filename, 'r', encoding='UTF-8') as user_cmapfile:
        for codeline in user_cmapfile:
            codeline = codeline.strip()
            codeline = re.sub('\s+', '', codeline, re.M)
            if not (codeline):
                continue
            ucode = codeline.split('=', 3)[0]
            if (len(codeline.split('=', 3)) == 3):
                acode = codeline.split('=', 3)[2]
            if (bool(acode and ucode)):
                ucode_split_var = ucode.split(',')
                for i in range(len(ucode_split_var)):
                    wild_temp = ucode_split_var[i]
                    if (wild_temp):
                        if (wild_temp.isdigit()):
                            wild_temp = unichr(int(wild_temp))
                        if not (bool(ucodedict_temp.get(wild_temp))):
                            ucodedict_temp[wild_temp] = acode   # a character should be unique, but unfortunately many codes are used in various systems.
                        else:
                            sys.stderr.write('There are ambiguous codes for character: {0}.\n'.format(wild_temp))
                            sys.exit(0)
            acode = ""
            ucode = ""
    with codecs.open (ug_refile, 'r', encoding='UTF-8') as ug_re:
        ug_count = 0
        for single_sed in ug_re:
            single_sed = single_sed.strip().encode('utf-8')
            if not len(single_sed):
                continue
            patten_1 = re.match(r'^s\/(.+)\/(.+)\/g', single_sed).group(1)
            sub_1 = re.match(r'^s\/(.+)\/(.+)\/g', single_sed).group(2)
            ug_sed_temp[ug_count] = [patten_1, sub_1]
            ug_count += 1
    
    return (ucodedict_temp, ug_sed_temp)

# One to one code change between two sets of characters. 
# only many -> one code converting.....                        
def code_file(ucodedict2, ug_sed_dict, inputstr):
    linecount = 0
    outputstr = ''
    for sourceline in inputstr.split('\n'):
        sourceline = sourceline.strip()
        # add a final indicator, never get to this one.
        sourceline = sourceline + "!"
        linecount += 1
        destline = ""
        codeindex = 0
        token = ""
        linelen = len(sourceline) - 1
        while(linelen > codeindex):
            char = sourceline[codeindex : codeindex + 1]
            codeindex += 1
            if ((linelen - codeindex) > 2):
                double = sourceline[codeindex - 1 : codeindex + 1]
                if (bool(ucodedict2.get(double))):
                    char = double
                    codeindex += 1
            if (bool(ucodedict2.get(char))):
                token = token + ucodedict2[char]
            else:
                if (token != ""):
                    destline = destline + token + char
                    token = ""
                else:
                    destline = destline + char
        
        if (token != ""):
            destline = destline + token
            token = ""
        end_destline = ""
        for unchar in destline.encode('utf-8'):
            if re.match('-', unchar):
                end_destline += " "
            elif re.match('[0-9a-zA-Z,\.?!%%\s]', unchar):
                end_destline += unchar
            else:
                end_destline += ","
        end_destline =  re.sub(',+', ",", end_destline)
        end_destline = re.sub(r'([0-9]+)',' \g<1> ' , end_destline)
        for ug_count in range(len(ug_sed_dict)):
            patten_1 = ug_sed_dict[ug_count][0]
            sub_1 = ug_sed_dict[ug_count][1]
            end_destline = re.sub(patten_1, sub_1, end_destline)
        
        end_destline = re.sub('\s+', ' ', end_destline)
        outputstr += end_destline + '\n'
        return outputstr 


        
def main():
    (ucodedict, ug_seddict)= cmap_file('auyghur.code', 'ug.sed')
    inputstr = 'بۇ يەردە ئومۇمىي ئۇقۇم مۈجمەل  '
    outputstr = code_file(ucodedict, ug_seddict, inputstr)
    print (outputstr)

if __name__ == '__main__':
    main()


