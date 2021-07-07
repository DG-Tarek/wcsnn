# Last edit : Friday 06/04/2021.
# Created on Python 3.8(64bit).

from csv import reader # pip install python-csv .
import numpy as np # already exist in library .
import pickle # already exist in library .
import time # already exist in library .
from dictionary import getSerialNumber as get_serial_number # from dictionary.py in Folder.

# The pickle module implements binary protocols for serializing and de-serializing a Python object structure.

# Class Comments : for classifying comments and return a pickle file.

class Comments :

    def __init__(self, train_path,roots_path,new_train,family=None):
        # train_path : (path:str) Train csv file path .
        # roots_path : (path:str) roots pickle file path .
        # new_train : (String) name for the comments pickle file will return .
        # family : (int) for find out comments class .
        if family is not None:
            self.train_path = train_path
            self.roots_path = roots_path
            self.new_train = new_train
            self.family =family
            self.ROOTS = np.array([])
            self.Train =[]
            self.read_roots()
            self.Converting_comments()
            self.write_train()

    #Read roots from roots pickle file .
    def read_roots(self):
        try:
            open_file = open(self.roots_path, "rb")
            self.ROOTS = np.array(pickle.load(open_file))
            open_file.close()
            print(" roots -> The download was successful.")
        except :
            print(" roots -> Download failed!")

    # Write the new train pickle file (list of serial numbers).
    def write_train(self):
        try:
            open_file = open(self.new_train+'.pkl', 'wb')
            pickle.dump(self.Train, open_file)
            open_file.close()
            print(" Train -> Successfully Created.")
        except:
            print(" Train -> Update failed!")

    # Converting comment from string comment to serial number comment.
    def Converting_comments(self):
        l=70000
        p=0
        k,kk=0,0
        print(" System -> Convert comments to serial number...")
        with open(self.train_path, 'r', encoding="utf8") as read_obj:
            csv_reader = reader(read_obj)
            start =time.time()
            for line in csv_reader:
                if line[2]==str(self.family):
                    serial_number=get_serial_number(text=line[1],roots=self.ROOTS)
                    self.Train+=[serial_number]
                    k=int((p*100)/l)
                    if k > kk :
                        print(" System ->  Converting  ... " + str(k)+'% ('+str(int((time.time()-start)/60))+
                                                            ' min '+str(int((time.time()-start)%60))+' s).')
                        kk=k
                p+=1
        print("Comments number : " +str(len(self.Train)))
        print(" System -> Converting Finished.")

if __name__ == "__main__":
    # Creating a pickle file for normal comments .
    normal_comments =Comments(train_path="Train.csv",
                              roots_path="roots.pkl",
                              new_train='normal_comments',
                              family=0)

    # Creating a pickle file for positive comments .
    positive_comments =Comments(train_path="Train.csv",
                                roots_path="roots.pkl",
                                new_train='positive_comments',
                                family=1)

    # Creating a pickle file for negative comments .
    negative_comments =Comments(train_path="Train.csv",
                                roots_path="roots.pkl",
                                new_train='negative_comments',
                                family=-1)