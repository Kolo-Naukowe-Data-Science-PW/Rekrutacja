# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
"""
Poniższy skrypt służy do stworzenia klasy data_frame opisanej poniżej,
oprócz niej znajdują się w nim także klasy pomocnicze : cell,vector,column,row
"""



class cell():
    """
    klasa reprezentująca pojedyączą komórkę w datafrejmie zawierającą
    pojedyńczą wartość, funkcja inicjalizująca przypisuje wartosc komórce
    """
    def __init__(self,val):
        self.value = val

        
class vector():
    """
    klasa reprezentująca jednowymiarowy wektor w datafrejmie, przetrzymująca
    instancje klasy cell,
    funkcja inizjalizująca tworzy listę w której następnie będą przetrzymywane 
    adresy komórek
    funkcja _add_cell służy do stworzenia nowej komórki i dodania jej do listy
    funkcja _append dodaje już istniejąca komórki do listy
    """
    def __init__(self):
        self.list = list()
        
    def _add_cell(self,val):
        self.list.append(cell(val))
    
    def _append(self,cell):
        self.list.append(cell)
    
class row(vector):
    """
    klasa pochadząca od klasy vektor, reprezentuje pojedyńczy rząd wartości w
    datafrejmie, 
    funkcja inicjalizująca jest taka sama jak dla klasy vector
    funkcja _add_cell oprócz stworzenia i dodania nowej komórki do swojej listy
    dodaje ta komórke do instancji klasy column
    """
    def __init__(self,frame):
        vector.__init__(self)
    
    def _add_cell(self,val,frame,col_no):
        vector._add_cell(self,val)
        frame._columns_index[col_no]._append(self.list[-1])
    
    
class column(vector):
    """
    klasa pochadząca od klasy vektor, reprezentująca pojedyńczą kolumnę
    w datafrejmie, wyrożnia sie posiadaniem niepowtarzalnej nazwy, 
    funkcja inicjalizująca sprawdza unikalność nazwy, ewentualnie przypisuje 
    string zawierający pierwszą nieużytą wcześniej liczbę,
    funkcja _add_cell oprócz stworzenia i dodania nowej komórki do swojej listy
    dodaje ta komórke do instancji klasy column
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
    '''
    klasa data frame służaca do wczytania pliku csv i przetrzymywania danych,
    nowe dane mogą być pózniej dodawane za pomocą odpowiednich funkcji   
    '''
    _NullVal='Null'
    
    """
    funkcja inicjalizująca tworzy wewnątrz instancji klasy dwie listy do
    których dodawane będą instancje klas column i row
    """
    def __init__(self):
        self._columns_index = []
        self._rows_index = []
    """
    _read_columns służy do utworzenia nowych kolumn i przypisania im typów
    danych z uzyciem dwoch wektorow:pierwszy reprezentuje nazwy kolumn
    drugi reprezentuje pierwszy rząd danych i jest użyty do sprecyzowania typów
    drugi rząd jest przycinanny do długosci wektora zawierajacego nazwy kolumn
    """
    def _read_columns(self,names,line):
        line = line[:len(names)]
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
    '''
    funkcja zwracajaca typ i-tej kolumny
    '''
    def _type(self,i):
        return self._columns_index[i].type
    """
    funkcja służy do stworzenia nowego rzędu w datafrejmie z podanego wektora
    odpowiednie pozycje są zapełniane od pierwszej kolumny i zostaje
    wykorzystanych nie więcej wartosci niz liczba kolumn w datafrejmie
    """
    def add_row(self,line):
        line = self._przycinacz(line)
        self._rows_index.append(row(self))
        for i,x in enumerate(line):
            try:
                self._rows_index[-1]._add_cell(self._type(i)(x),self,i)
            except ValueError:
                self._rows_index[-1]._add_cell(data_frame._NullVal,self,i)
    """
    funkcja służy do stworzenia nowego rzędu w datafrejmie z podanego wektora
    odpowiednie pozycje są zapełniane od pierwszego rzędu i zostaje
    wykorzystanych nie więcej wartosci niz liczba wierszy w datafrejmie
    możliwe jest sprecyzowanie nazwy kolumny za pomocą argumentu 'name'
    """           
    def add_column(self,line,**keywords):
        line = self._przycinacz(line,row=False)
        try:
            proba = float(line[0])
        except ValueError:
            self._columns_index.append(column(self,str,**keywords))
            typ = str
        else:
            if proba.is_integer() == True:
                self._columns_index.append(column(self,int,**keywords))
                typ = int
            else:
                self._columns_index.append(column(self,float,**keywords))
                typ = float
        for i,x in enumerate(line):
            try:
                self._columns_index[-1]._add_cell(typ(x),self,i)
            except ValueError:
                self._columns_index[-1]._add_cell(data_frame._NullVal,self,i)
    """
    funkcja sluzaca do wyświetlenia datafrejmu
    przyjmuje dodatkowe argumenty:
    cslice - obiekt typu slice precyzujacy indeksy kolumn do wyświetlenia
    rslice - obiekt typu slice precyzujacy indeksy wierszy do wyświetlenia
    """
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
            print(self._rows_index.index(x),[y.value for y in x.list[cslice]])
    """
    fukcja przycinająca wektor do długości wynoszącej liczbę kolumn, lub
    wierszy jeśli argument row == False
    """
    def _przycinacz(self,vec,row=True):
        if row == True:
            leng = len(self._columns_index)
        else:
            leng = len(self._rows_index)
        return vec[:leng]
    """
    funkcja służąca do wczytywania pliku csv z podanej lokalizacji, możliwe
    jest podanie separatora danych w argumencie separator, oraz czy pierwszy
    rzad w pliku reprezentuje nazwy kolumn. Niestety jest ona bardzo wrazliwa
    na format pliku(rozpoznaje ona tylko podany separator)
    """
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
    """
    funkcja pomocnicza usuwająca niepotrzebne wartości zwracane podczas
    czytania pliku csv
    """
    def _readline(self,file,separator):
        line = [x for x in file.readline().rstrip('\n').split(separator) 
                if x != '']
        if line == ['']:
            return None
        else:
            return line
    """
    funkcja usuwająca wiersz o podanym indeksie
    """
    def del_row(self,no):
        self._rows_index.pop(no)
        for x in self._columns_index:
            x.list.pop(no)
    """
    funkcja usuwająca kolumnę o podanym indeksie
    """
    def del_column(self,no):
        self._columns_index.pop(no)
        for x in self._rows_index:
            x.list.pop(no)
    """
    funkcja zamieniąjaca miejscami wiersze o podanych indeksach
    """
    def change_row(self,no1,no2):
        self._rows_index[no1],self._rows_index[no2] = \
            self._rows_index[no2],self._rows_index[no1]
        for x in self._columns_index:
            x.list[no1], x.list[no2] = x.list[no2], x.list[no1]
    """
    funkcja sortująca datafrejm ze względu na kolumnę o podanym indeksie
    możliwe sprecyzowanie kolejności rosnącej lub malejącej w argumencie desc
    sortowanie może być numeryczne lub alfabetyczne i zależy od typu danych
    """
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
    """
    funkcja szukająca maksymalnej wartości w wierszu numerycznym o podanym
    indeksie
    """
    def maximum(self,col_no):
        if self._columns_index[col_no].type == str:
            print("\n!!Not a numerical columns!!")
            print("!!!!!!Can't calculate!!!!!!")
        else:
            col = [x.value for x in self._columns_index[col_no].list 
                   if x.value != data_frame._NullVal]
            return max(col)
    """
    funkcja szukająca minimalnej wartości w wierszu numerycznym o podanym
    indeksie
    """ 
    def minimum(self,col_no):
        if self._columns_index[col_no].type == str:
            print("\n!!Not a numerical columns!!")
            print("!!!!!!Can't calculate!!!!!!")
        else:
            col = [x.value for x in self._columns_index[col_no].list 
                   if x.value != data_frame._NullVal]
            return min(col)
    """
    funkcja szukająca średniej wartości w wierszu numerycznym o podanym
    indeksie
    """
    def average(self,col_no):
        if self._columns_index[col_no].type == str:
            print("\n!!Not a numerical columns!!")
            print("!!!!!!Can't calculate!!!!!!")
        else:
            col = [x.value for x in self._columns_index[col_no].list 
                   if x.value != data_frame._NullVal]
            return sum(col)/len(col)
    """
    funkcja szukająca mediany w wierszu numerycznym o podanym indeksie
    """
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
    """
    funkcja szukająca odchylenia standardowego w wierszu numerycznym o podanym 
    indeksie
    """
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
    """
    funkcja służy do zmiany wartości pozycji o podanych koordynatach
    """
    def change_value(self,val,row_no,col_no):
        self._rows_index[row_no].list[col_no].value = val
    """
    funkcja wypełnia wartości nan w kolumnie o podanym indeksie za 
    pomocą wartości określonej w zmiennej approach
    """
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