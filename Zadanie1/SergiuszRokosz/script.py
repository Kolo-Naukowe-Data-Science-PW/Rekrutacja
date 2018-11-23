# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class cell():
    """
    klasa reprezentujaca pojedyncza komorke w datafrejmie zawierajaca
    pojedyncza wartosc, funkcja inicjalizujaca przypisuje wartosc komorce
    """
    def __init__(self,val):
        self.value = val

        
class vector():
    """
    klasa reprezentujaca jednowymiarowy wektor w datafrejmie, przetrzymujaca
    instancje klasy cell, oprocz funkcji inicjalizujacej zawiera takze funkcje
    sluzace do dodawania nowych komorek z danymi
    """
    def __init__(self):
        self.list = list()
        
    def _add_cell(self,val):
        self.list.append(cell(val))
    
    def _append(self,cell):
        self.list.append(cell)
    
class row(vector):
    """
    klasa pochadzaca od klasy wektor, reprezentuje pojedynczy rzad wartosci w
    datafrejmie, funkcja przypisujaca nowa wartosc do rzedu dopisuje ta wartosc
    rowniez do odpowiedniej kolumny
    """
    def __init__(self,frame):
        vector.__init__(self)
    
    def _add_cell(self,val,frame,col_no):
        vector._add_cell(self,val)
        frame._columns_index[col_no]._append(self.list[-1])
    
    
class column(vector):
    """
    klasa pochadzaca od klasy wektor, reprezentujaca pojedyncza kolumne
    w datafrejmie, wyroznia sie posiadaniem niepowtarzalnej nazwy, funkcja
    inicjalizujaca sprawdza unikalnosc nazwy, ewentulanie przypisuje string
    zawierajacy liczbe, funkcja dodajaca komorke do kolumny dodaje ja takze
    do odpowiedniego rzedu
    """
    def __init__(self,frame,type_,**keywords):
        try:
            Name = keywords['name']
        except KeyError:
            Name = len(frame._columns_index)
        vector.__init__(self)
        if Name not in [x.name for x in frame._columns_index]:
            self.name = Name
        else:
            i = 0
            while str(i) in [x.name for x in frame._columns_index]:
                i += 1
            self.name = str(i)
        self.type = type_
        
    def _add_cell(self,val,frame,row_no):
        vector._add_cell(self,val)
        frame._rows_index[row_no]._append(self.list[-1])
        


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
    _NullVal='Null'
    
    def __init__(self):
        self._columns_index = []
        self._rows_index = []
        
    def _read_columns(self,names,line):
        for x,y in zip(names,line):
            try:
                int(y)
                self._columns_index.append(column(self,int,name=x))
            except ValueError:
                try:
                    float(y)
                    self._columns_index.append(column(self,float,name=x))
                except ValueError:
                    self._columns_index.append(column(self,str,name=x))
            
    def _type(self,i):
        return self._columns_index[i].type
            
    def add_row(self,line):
        line = self._przycinacz(line)
        self._rows_index.append(row(self))
        for i,x in enumerate(line):
            try:
                self._rows_index[-1]._add_cell(self._type(i)(x),self,i)
            except ValueError:
                self._rows_index[-1]._add_cell(data_frame._NullVal,self,i)
    def add_column(self,line,**keywords):#################musi sprawdzac najpierw float
        line = self._przycinacz(line,row=False)
        try:
            int(line[0])
            self._columns_index.append(column(self,int,**keywords))
            typ = int
        except ValueError:
            try:
                float(line[0])
                self._columns_index.append(column(self,float,**keywords))
                typ = float
            except ValueError:
                self._columns_index.append(column(self,str,**keywords))
                typ = str
        for i,x in enumerate(line):
            try:
                self._columns_index[-1]._add_cell(typ(x),self,i)
            except ValueError:
                self._columns_index[-1]._add_cell(data_frame._NullVal,self,i)
    def show(self,**kwargs):
        try:
            cslice = kwargs['cslice']
        except KeyError:
            cslice = slice(len(self._columns_index))
        try:
            rslice = kwargs['rslice']
        except KeyError:
            rslice = slice(len(self._rows_index))
        print('\ncolumns names')
        print([x.name for x in self._columns_index[cslice]])
        print('rows')
        for x in self._rows_index[rslice]:
            print(self._rows_index.index(x),[y.value for y in x.list])
            
    def _przycinacz(self,vec,row=True):
        if row == True:
            leng = len(self._columns_index)
        else:
            leng = len(self._rows_index)
        return vec[:leng]
    
    def read_csv(self,path,separator=',',colfilin=True):
        with open(path,'r') as f:
            if colfilin == True:
                names = self._readline(f,separator)
                line = self._readline(f,separator)
            else:
                line = self._readline(f,separator)
                names = [str(i) for i in range(len(line))]
            self._read_columns(names,line)
            while line:
                self.add_row(line)
                line = self._readline(f,separator)
            print('table loaded')
    
    
    def _readline(self,file,separator):
        line = file.readline().rstrip('\n').split(separator)
        if line == ['']:
            return None
        else:
            return line
                                 
        
    def del_row(self,no):
        self._rows_index.pop(no)
        for x in self._columns_index:
            x.list.pop(no)
        
    def del_column(self,no):
        self._columns_index.pop(no)
        for x in self._rows_index:
            x.list.pop(no)
            
    def change_row(self,no1,no2):
        self._rows_index[no1],self._rows_index[no2] = \
            self._rows_index[no2],self._rows_index[no1]
        for x in self._columns_index:
            x.list[no1], x.list[no2] = x.list[no2], x.list[no1]
    
    def sort(self,col_no,desc=True):
        col = [x.value for x in self._columns_index[col_no].list]
        if data_frame._NullVal in col:
            print('\n!!Null value in the column!!')
            print("!!!!!!!!!Can't sort!!!!!!!!!")
        else:
            if desc == False:
                col = col[::-1]
            order = [i[0] for i in sorted(enumerate(col), key=lambda x:x[1])]
            self._rows_index = [self._rows_index[i] for i in order]
            for j in self._columns_index:
                j.list = [j.list[i] for i in order]
                
                
    def maximum(self,col_no):
        if self._columns_index[col_no].type == str:
            print("\n!!Not a numerical columns!!")
            print("!!!!!!Can't calculate!!!!!!")
        else:
            col = [x.value for x in self._columns_index[col_no].list 
                   if x.value != data_frame._NullVal]
            return max(col)
        
    def minimum(self,col_no):
        if self._columns_index[col_no].type == str:
            print("\n!!Not a numerical columns!!")
            print("!!!!!!Can't calculate!!!!!!")
        else:
            col = [x.value for x in self._columns_index[col_no].list 
                   if x.value != data_frame._NullVal]
            return min(col)
        
    def average(self,col_no):
        if self._columns_index[col_no].type == str:
            print("\n!!Not a numerical columns!!")
            print("!!!!!!Can't calculate!!!!!!")
        else:
            col = [x.value for x in self._columns_index[col_no].list 
                   if x.value != data_frame._NullVal]
            return sum(col)/len(col)
        
    def median(self,col_no):
        if self._columns_index[col_no].type == str:
            print("\n!!Not a numerical columns!!")
            print("!!!!!!Can't calculate!!!!!!")
        else:
            col = [x.value for x in self._columns_index[col_no].list 
                   if x.value != data_frame._NullVal]
            if len(col)%2 == 0:
                return sum(sorted(col)[len(col)//2-1:len(col)//2+1])/2
            else:
                return sorted(col)[len(col)//2]
        
        
    def deviation(self,col_no):
        from math import sqrt
        if self._columns_index[col_no].type == str:
            print("\n!!Not a numerical columns!!")
            print("!!!!!!Can't calculate!!!!!!")
        else:
            col = [x.value for x in self._columns_index[col_no].list 
                   if x.value != data_frame._NullVal]
            av = self.average(col_no)
            col = [(x-av)**2 for x in col]
            return sqrt(sum(col)/(len(col)-1))
        
    def change_value(self,val,row_no,col_no):
        self._rows_index[row_no].list[col_no].value = val
        
        
    def fill_na(self,col_no,approach):
        dicti = {'deviation':self.deviation,
                 'median':self.median,
                 'average':self.average,
                 'minimum':self.minimum,
                 'maximum':self.maximum,
                 }
        try:
            val = dicti[approach](col_no)
        except KeyError:
            print("\n!!can't recognize approach!!")
        else:
            for x in self._columns_index[col_no].list:
                if x.value == data_frame._NullVal:
                    x.value = val
                
                
df = data_frame()
df.read_csv('próbny.csv')
df.add_column([6.1,2,'c'],name='0')
df.add_column(['y','g','d'],name='0')
df.add_row([1,2,2,5,'a'])
df.show()
df.fill_na(1,'median')
df.show()