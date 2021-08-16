#!/usr/bin/env python

import os
import csv
from copy import deepcopy


class CsvFile():

    def __init__(self):
        self.data = list()
        self.fieldnames = list()
        
    def read(self, filename):
        self.read_filename = filename
        
        with open(self.read_filename, 'r+', encoding='GBK') as f:
            csv_reader = csv.DictReader(f)
            
            save_fieldnames = True
            for row in csv_reader:
                self.data.append(row)
                
                if save_fieldnames is True:
                    save_fieldnames = False
                    self.fieldnames = list(row.keys())
       
    
    def print_data(self):
        for row in self.data:
            print(row)
    
    @staticmethod
    def split_by_size(line_dict):
        template = deepcopy(line_dict)
                
        del template['size']
        del template['id']
        
        id_suffix = 1
        for size in line_dict['size'].split('|'):
            template['new_size'] = size
            template['code'] = line_dict['id'] + '_' + str(id_suffix)
            yield template
            id_suffix += 1

    def write(self, filename):
        self.write_filename = filename
        
        self.fieldnames[0] = 'code'
        self.fieldnames[1] = 'new_size'
        
        with open(self.write_filename, 'w+', encoding='GBK') as f:
            w = csv.DictWriter(f, fieldnames = self.fieldnames)
            w.writeheader()
            
            row_number = 1
            for row in self.data:
                print("[%3d]Processing ID: %s" % (row_number, row['id']))
                
                # only one size in this line
                if '|' not in row['size']:
                    row['code'] = row['id']
                    row['new_size'] = row['size']
                    del row['id']
                    del row['size']
                    w.writerow(row)
                else:
                    for line in CsvFile.split_by_size(row):
                        w.writerow(line)
                row_number += 1

            
if __name__ == '__main__':
    origin_filename = input("请将待处理的csv文件拖动到窗口内，然后按回车键")

    if len(origin_filename) == 0:
        origin_filename = './test/product_data.csv'
        print("使用默认测试文件进行测试")
    filename, ext = os.path.splitext(origin_filename)
    write_filename = filename + '_new' + ext
    
    csv_file = CsvFile()
    csv_file.read(origin_filename)
    csv_file.write(write_filename)
