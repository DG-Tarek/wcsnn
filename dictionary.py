# Last edit : Friday 06/04/2021.
# Created on Python 3.8(64bit).

import re # pip install regex .
from csv import reader # pip install python-csv .
import numpy as np # already exist in library .
import pickle # already exist in library .
import time # already exist in library .


train_path="Train.csv"
roots_path = "roots.pkl"

ROOTS = []
Forbidden_roots =['lzm','5tr','3nd','m3k','chf','3lh','b3d','bch','tns','chy','3lch','bld','brb',
                  'ch3b','bld','chkn','rjl']



# Download roots from roots pickel file .
def read_roots():
    global ROOTS 
    try:
        open_file = open(roots_path, "rb")
        ROOTS = pickle.load(open_file)
        open_file.close()
        print(" roots -> The download was successful.")
    except :
        print(" roots -> Download failed!")


# Create or update roots pickel file.
def write_roots():
    try:
        #ROOTS.sort()
        open_file = open(roots_path, 'wb')
        pickle.dump(ROOTS, open_file)
        open_file.close()
        print(" roots -> Successfully Created.")
    except:
        print(" roots -> Update failed!")
    

# Ward --->>> Root .
def getRoot(word):
    if len(word)>2 and (word.isnumeric()==False):
        word = word.lower()
        """ Forbidden=['a', 'e', 'i', 'o', 'u','0','1','2','4','6','é','è','ç','@','$','€','à',None,'ù','£','&','ė'
                    'ȝ','ß','œ','ǿ','ļ','ĺ','ø',' ô','õ','į','ę','ě','ý','û','ú','û','ä','ķ','ł','ď'] """
        Permissible=['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z',
                    '3','5','6','7','8','9',]
        previousLetter =''
        root=''
        for letter in word:
            if (letter in Permissible) and (letter != previousLetter) :
                root += letter
            previousLetter = letter
        return root

# return True if the input root is a spam of any letter.
def spam(root):
    previousLetter=''
    i=0
    for letter in root:
        if i>0:
            if letter != previousLetter:
                return False
        else:
            i=1
        previousLetter = letter
    return True

# return True if root already exist in feather file .
def ifExist(root):
    return root in ROOTS

# Comment --->>> a ward list .
def getWords(text):
    return re.sub("[^\w]", " ",  text).split()

# Add root to roots
def addRoot(root):
    global ROOTS
    ROOTS.append(root)

# Comment --->>> Serial number list.
def getSerialNumber(text,roots):
    serialNumber =np.array([])
    wordList = getWords(text=text)
    for word in wordList :
        word_root=getRoot(word=word)
        serialNumber = np.append(serialNumber ,np.where(roots == word_root)[0])
    serialNumber.tolist()
    serialnumber =[]
    for number in serialNumber:
        serialnumber.append(int(number))
    return serialnumber

    

# Learn roots(wards) from csv file(Train.csv).
def learn_roots():
    print(" System -> Learning Words Started.")
    with open(train_path, 'r', encoding="utf8") as read_obj:
        csv_reader = reader(read_obj)
        for line in csv_reader:
            if line[0]!='ID':
                wordList = getWords(text=line[1])
                for word in wordList :
                    word_root=getRoot(word=word)
                    if (word_root is not None) == (len(str(word_root))>1) == (word_root not in Forbidden_roots):
                        if str(word_root).isnumeric() == spam(root=word_root) == ifExist(root=word_root):
                            addRoot(root=word_root)
    ROOTS.sort()
    print("ROOTS number : " +str(len(ROOTS)))
    print(" System -> Learning Words Finished.")
            



if __name__ == "__main__":
    if True:
        #this block is just for learning roots(word) from Train.csv file.
        start =time.time()
        learn_roots()
        end = time.time()
        print(f"Runtime for learning is {end - start}")
        write_roots()



        
        
    
    


