import numpy as np

class Dataset:


    def __init__(self, filename):
        with open(filename) as f:
            content = f.readlines()
        f.close()

        n = len(content)-1
        #print(n)
        if n<=0:
            raise Exception("Raport w pliku {} nie zawiera danych".format(filename))

        cols = self.__splitfields(content[0].rstrip())
        ncols = len(cols)
        #print(cols)
        #print(ncols)

        self.data = {}

        for i in range(n):
            #print(i+1)
            #print(content[i+1])
            row = self.__splitfields(content[i+1].rstrip())
            id = int(row[0])
            #print(row)
            self.data[id] = {}
            r = 0
            for j in cols:
                
                #print(r)
                #print(j)
                
                self.data[id][j] = row[r]
                r = r + 1
            if self.data[id]['Analysis Type']!='Press':
                raise Exception("Obsługiwane tylko raporty z pomiarów ciśnienia (Analysis Type = Press)".format(filename))


            if self.data[id]['Sampling  Time'] == "1 h":
                dt = 1*60
            elif self.data[id]['Sampling  Time'] == "10 min":
                dt = 10
            else:
                raise Exception("Nieznany czas próbkowania".format(filename))

            p = []
            t = []
            k = 0
            for j in row[ncols:]:
                p.append(float(j.replace(" ","")))
                t.append(k*dt)
                k=k+1

            self.data[id]['t']=np.array(t)
            self.data[id]['p']=np.array(p)

        #print(data)


    def __splitfields(self, row):
        tmp = ""
        flag = 0
        out = []
        for s in row[:-1]:
            #print("string: {} flag: {}".format(s, flag))
            if flag == 0:
                if s != "\t":
                    tmp = tmp+s
                elif s == "\t":
                    out.append(tmp)
                    flag = 1
                    tmp = ""
            elif flag == 1:
                if s != "\t":
                    tmp = tmp + s
                    flag = 0
                elif s == "\t":
                    tmp = ""
                    out.append(tmp)
        
        s = row[-1]
        #print("last string: {} flag: {}".format(s, flag))
        if flag == 0 and s !="\t":
            tmp = tmp+s
            out.append(tmp)
        elif flag == 0 and s == "\t":
            out.append(tmp)
            tmp = ""
            out.append(tmp)
        elif flag == 1 and s == "\t":
            tmp = ""
            out.append(tmp)
            out.append(tmp)

        return out


    def ids(self):
        return list(self.data.keys())









