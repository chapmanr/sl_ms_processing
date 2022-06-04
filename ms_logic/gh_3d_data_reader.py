
import requests
import pandas as pd
from io import StringIO
import numpy as np

def get_demo_data_gh():
    url = "https://raw.githubusercontent.com/chapmanr/ms_data/main/msi_csv/mussel.3d.csv"
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


class MSI3DXiCParser:

    def __init__(self, lines:list):
        if len(lines) > 5:
            data = []
            for line in lines:
                data.append([float(fs) for fs in line.split(",")])
            self.df = pd.DataFrame(data, index=None)
            header=["x","y", "z"]
            for i in range(3, len(self.df.columns)):
                header.append("m" + str(i-2))
            self.df.columns=header
        else:
            print("incorrect format")
    
    def Describe(self):
        print(self.df.head())

    def NumMasses(self):
        return len(self.df.columns)-3

    

if __name__ == "__main__":
   #print(get_demo_data_gh()) 
   
   rte= MSI3DXiCParser(get_defaut_data_lines())
   rte.Describe()
 