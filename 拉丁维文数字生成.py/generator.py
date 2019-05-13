import re
import math


class NumToUyghur:
    '''
    阿拉伯数字转拉丁维语
    '''

    def __init__(self):
        self.cardinal_num_units = ['', 'bir', 'vikki', 'vUc', 'tOt', 'bAx', 'valtA', 'yAttA', 'sAkkiz', 'toqquz']
        self.ordinal_num_units = ['', 'birinci', 'vikkinci', 'vUcinci', 'tOtinci', 'bAxinci', 'valtinci', 'yAttinci', 'sAkkizinci', 'toqquzinci', 'voninci']
        self.cardinal_num_tens = ['', 'von', 'yigirmA', 'vottuz', 'qiriq', 'vAllik', 'vatmix', 'yAtmix', 'sAksAn', 'toksan']
        self.ordinal_num_tens = ['', 'voninci', 'yigirmA', 'vottuz', 'qiriq', 'vAllik', 'vatmix', 'yAtmix', 'sAksAn', 'toksan']
        self.num_hundreds = ['', 'bir yUz', 'vikki yUz', 'vUc yUz', 'tOt yUz', 'bAx yUz', 'valtA yUz', 'yAttA yUz', 'sAkkiz yUz', 'toqquz yUz']
        self.thousand_level = 'miN'
        self.percent = 'pirsAnt'
        self.cardinal_inner_list = [self.cardinal_num_units, self.cardinal_num_tens, self.num_hundreds]
        self.ordinal_inner_list = [self.ordinal_num_units, self.ordinal_num_tens, self.num_hundreds]

    def numToUyghurCardinal(self, num_string):
        '''
        基数数字转换
        '''
        latin_num_string = ''

        for i in range(math.ceil(len(num_string)/3)):
            if i > 0:
                latin_num_string = self.thousand_level + ' ' + latin_num_string
            for inter_serial, num in enumerate(num_string[::-1][i*3:(i+1)*3]):
                num = int(num)
                if num != 0:
                    latin_num_string = self.cardinal_inner_list[inter_serial][num] + ' ' + latin_num_string

        return latin_num_string.strip()

    def numToUyghurOrdinal(self, num_string):
        '''
        序数数字转换
        '''
        latin_num_string = ''

        for i in range(math.ceil(len(num_string)/3)):
            if i > 0:
                latin_num_string = self.thousand_level + ' ' + latin_num_string
            for inter_serial, num in enumerate(num_string[::-1][i*3:(i+1)*3]):
                num = int(num)
                if num != 0:
                    if i == 0:  # 只有第一个个位数用序数数字
                        latin_num_string = self.ordinal_inner_list[inter_serial][num] + ' ' + latin_num_string
                    else:  # 其他权节的第一位用基数数字
                        latin_num_string = self.cardinal_inner_list[inter_serial][num] + ' ' + latin_num_string

        return latin_num_string.strip()

    def percentToUyghur(self, num_string):
        return self.numToUyghurCardinal(num_string) + ' ' + self.percent


if __name__ == "__main__":
    n_trans = NumToUyghur()

    test_list = ['12']
    for i in test_list:
        print(n_trans.numToUyghurCardinal(i))
    for i in test_list:
        print(n_trans.numToUyghurOrdinal(i))
    for i in test_list:
        print(n_trans.percentToUyghur(i))
