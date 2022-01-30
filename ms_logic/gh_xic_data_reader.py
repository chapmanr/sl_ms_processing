import requests
import pandas as pd
from io import StringIO
import numpy as np


def get_demo_data_gh():
    url = "https://raw.githubusercontent.com/chapmanr/ms_data/main/xyi/May4_kidney_serial_S18%20Analyte%201.raw.xyi"
    page = requests.get(url)
    return page.text



def get_defaut_data_lines():
    stringio = StringIO(get_demo_data_gh())
    lines = stringio.readlines()
    return lines

def get_data_lines_from_file_obj(file_obj):
    stringio = StringIO(file_obj.getvalue().decode("utf-8"))
    lines = stringio.readlines()
    return lines

class RTEParser:

    def __init__(self, lines:list):
        if len(lines) > 5:
            self.raw_loc = lines[0]
            self.masses = np.array([float(ms) for ms in lines[1].split(',')])
            self.mass_windows = np.array([float(mws) for mws in lines[2].split(',')])
            self.rgbf = np.array([float(rgbs) for rgbs in lines[3].split(',')]) / 255
            self.mode = lines[4]
            data = []
            for line in lines[5:]:
                data.append([float(fs) for fs in line.split(",")])
            self.df = pd.DataFrame(data, index=None)
            header=["s","x", "y"]
            for i in range(3, len(self.df.columns)):
                header.append("m" + str(i-2))
            self.df.columns=header
        else:
            print("incorrect format")
    
    def Describe(self):
        print(self.raw_loc)
        print(self.masses)
        print(self.mode)
        print(self.df.head())
    

if __name__ == "__main__":
   #print(get_demo_data_gh()) 
   
   rte= RTEParser(get_defaut_data_lines())
   rte.Describe()

