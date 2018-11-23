# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
NullVal = 'null'

class coords():
    
    def __init__(self):
        self.arr = []
        
    def add_row(self,info):
        self.arr.append(info)
        
    def del_row(self,no):
        self.arr.pop(no)
        
class ind(coords):
    
    def __init__(self):
        coords.__init__()
        
class col(coords):
    def __init__(self):
        coords.__init__()
        

class data_frame():
    # klasa data_frame sluzy do wczytywania danych ....dalszy opis...
    #poczytaj tez o dokumentacji wczytywaniu metod itd
    #pierwsza linia ewentulanie druga jezeli pierwsza to nazyw kolumn ustala
    #typy
    #problem z "" trzeba jakos rozwiazac
    #dopisac klase do wczytywania pliku?
    #dodawanie indeksów
    #indeksy i kolumny jako nowe type? uporządkowany dictionary
    #sprawdzanie długosci kolejnych wersów
    #ustalanie offsetu przy wczytywaniu
    #dodanie czytania czegos innego niz array

    
    def __init__(self):
        self.columns = []
        self.datatypes = []
        self.index = []
        self.tabela = []
        
        
    def read_line(self,file,separator):
        line = file.readline().rstrip('\n').split(separator)
        if line == ['']:
            return None
        else:
            return line
        
    def save_row(self,line):
        row = []
        if line != None:
            for i,x in enumerate(line):
                try:
                    row.append(self.datatypes[i](x))
                except ValueError:
                    row.append(NullVal)
            self.tabela.append(row)
        else:
            pass
        
    def check_data_type(self,f,colfilin,separator):
        if colfilin == True:
            line1 = self.read_line(f,separator)
            line2 = self.read_line(f,separator)
        else:
            line2 = self.read_line(f,separator)
            line1 = [str(i) for i in range(len(line2))]
        print(line2)
        for x,y in zip(line1,line2):
            try:
                int(y)
                self.columns.append(x)
                self.datatypes.append(int)
            except ValueError:
                try:
                    float(y)
                    self.columns.append(x)
                    self.datatypes.append(float)
                except ValueError:
                    self.columns.append(x)
                    self.datatypes.append(str)
        return line2
    def read_csv(self,path,separator=',',colfilin=True):
        with open(path,'r') as f:
            line = self.check_data_type(f,colfilin,separator)
            while line:
                self.save_row(line)
                line = self.read_line(f,separator)
            print('table loaded')
            
            

df = data_frame()
df.read_csv('próbny.csv')
df.tabela