import re
import math


class NumToUyghur:
    '''
    阿拉伯数字转拉丁维语
    '''

    def __init__(self):
        self.num_units = ['', 'bir', 'vikki', 'vUc', 'tOt', 'bAx', 'valtA', 'yAttA', 'sAkkiz', 'toqquz']
        self.num_tens = ['', 'von', 'yigirmA', 'vottuz', 'qiriq', 'vAllik', 'vatmix', 'yAtmix', 'sAksAn', 'toksan']
        self.num_hundreds = ['', 'bir yUz', 'vikki yUz', 'vUc yUz', 'tOt yUz', 'bAx yUz', 'valtA yUz', 'yAttA yUz', 'sAkkiz yUz', 'toqquz yUz']
        self.thousand_level = 'miN'
        self.million_level = 'milyon'
        self.percent = 'pirsAnt'
        self.single_year = 'yili'
        self.single_month = 'vay'
        self.single_day = 'cesla'
        self.inner_list = [self.num_units, self.num_tens, self.num_hundreds]

    def numToUyghurCardinal(self, num_string):
        '''
        基数数字转换
        '''
        latin_num_string = ''

        for i in range(math.ceil(len(num_string)/3)):
            if i % 3 == 1:
                latin_num_string = self.thousand_level + ' ' + latin_num_string
            if i % 3 == 2:
                latin_num_string = self.million_level + ' ' + latin_num_string
            for inter_serial, num in enumerate(num_string[::-1][i*3:(i+1)*3]):
                num = int(num)
                if num != 0:
                    latin_num_string = self.inner_list[inter_serial][num] + ' ' + latin_num_string

        return latin_num_string.strip()

    def numToUyghurOrdinal(self, num_string):
        '''
        序数数字转换
        '''
        ordinal_result = self.numToUyghurCardinal(num_string)
        if ordinal_result[-1] in ['i', 'A']:
            return ordinal_result[:-1] + 'inci'
        else:
            return ordinal_result + 'inci'

    def percentToUyghur(self, num_string):
        '''
        百分数转换
        '''
        return self.numToUyghurCardinal(num_string) + ' ' + self.percent

    def yearToUyghur(self, num_string):
        '''
        单年份转换
        '''
        return self.numToUyghurOrdinal(num_string) + ' ' + self.single_year

    def monthToUyghur(self, num_string):
        '''
        单月份转换
        '''
        return self.numToUyghurOrdinal(num_string) + ' ' + self.single_month

    def dayToUyghur(self, num_string):
        '''
        单日天转换
        '''
        return self.numToUyghurOrdinal(num_string) + ' ' + self.single_day

    def monthWithDayToUyghur(self, num_string):
        '''
        月份带日转换
        '''
        return 'vayniN {} kUni'.format(self.numToUyghurOrdinal(num_string))


if __name__ == "__main__":
    n_trans = NumToUyghur()

    test_list = ['10']
    for i in test_list:
        print('基数', n_trans.numToUyghurCardinal(i))
    for i in test_list:
        print('序数', n_trans.numToUyghurOrdinal(i))
    for i in test_list:
        print('百分数', n_trans.percentToUyghur(i))
    for i in test_list:
        print('单年', n_trans.yearToUyghur(i))
    for i in test_list:
        print('单月', n_trans.monthToUyghur(i))
    for i in test_list:
        print('单天', n_trans.dayToUyghur(i))
    for i in test_list:
        print('月份带日', n_trans.monthWithDayToUyghur(i))
