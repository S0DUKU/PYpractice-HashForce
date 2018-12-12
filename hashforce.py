'''this is module used to brute force,as python practise, and soon i will append more function include threads\n use help(class) to learn more
\n -----------class hashforce
\n -----------class md5force
\n -----------class crc32force
\n -----------class dicforce
\n -----------func getType
\n -----------func addType
\n.............'''
import hashlib
from threading import *
import random
import binascii
import time

sleep = time.sleep
crc32 = binascii.crc32
random = random.random
md5 = hashlib.md5

def getNone(string):
    if not isinstance(string,str):
        raise TypeError
    return string

def getmd5(string):
    if not isinstance(string,str):
        raise TypeError
    md5_str = md5()
    md5_str.update(string)
    md5_str = md5_str.hexdigest()
    return md5_str

def getcrc32(string):
    if not isinstance(string,str):
        raise
    return str(crc32(string)&0xffffffff)

#burte type

typedic = {'md5':getmd5,'crc32':getcrc32,'noencode':getNone}




keylist = 'abcdefghijklmnopqrstuvwxyz '

force_test = md5()
force_test.update('hello')
force_test = force_test.hexdigest()


def addType(dtype,func):
    '''dtype is the key of you func to set your own brute type\n
            func is your function,it should have one arg and return a string used to compare the\n
             encode string'''
    if not isinstance(dtype,str):
        raise TypeError
    typedic[dtype] = func
    return typedic.get(dtype)
    
            
def getType(dtype):
    '''get the dtype function'''
    if not isinstance(dtype,str):
        raise TypeError
    func = typedic.get(dtype)
    if not func:
        raise TypeError
    else:
        return func




def gethash(string,flag = None):
    if not isinstance(flag,str):
        raise
    if not isinstance(string,str):
        raise
    return typedic[flag](string)
        
 
def randomsort(keylist):
    '''random sort your list'''
    if not isinstance(keylist,list): 
        raise ValueError
    exist = []
    index = 0
    temp = 0
    while(len(exist) < len(keylist)):
        index = int(random()*len(keylist))
        temp = int(random()*len(keylist))
        try:
            if exist.index(index) >= 0 and exist.index(temp) >= 0:
                continue
        except:
            temp2 = keylist[temp]
            keylist[temp] = keylist[index]
            keylist[index] = temp2
            exist.append(temp)
            exist.append(index)







            
class hashforce:
    """ md5force need a str which is the encode of\n
                origin str to init"""
    
    
    def __init__(self,value,dtype,pat = keylist):
        if not isinstance(value,str):
            raise TypeError
        if not isinstance(pat,str):
            raise TypeError
        if not isinstance(dtype,str):
            raise TypeError
        getType(dtype)
        self.encode = value
        self.pattern = pat
        self.fflag = False
        self.type = dtype
        self.decode = None

#this is the brute force func use to guess (the length of your guess is depend on the len(leylist)      

    def __thread_force(self,pattern,encode,keylist = ['0'],post = 0,fflag = False):
        if fflag:
            return -1
        key = list(keylist)
        if post == len(keylist):
            end = ''.join(key)
            dec = gethash(end,self.type)
            if dec == encode:
                self.decode = end  
                return True
            else:
                return False
        for ech in pattern:
            key[post] = ech
            if self.__thread_force(pattern,encode,key,post+1,self.fflag):
                return True
        return False   

#this the main func to force the hash,begin,end tpo depend the length of string'''
    def force(self,begin = 1,end = 8):
        '''default is 8 max length of string,change the arg end to make more'''
        if not isinstance(begin,int) or not isinstance(end,int):
            raise TypeError
        
        while begin <= end:
            force_flag = self.__thread_force(self.pattern,self.encode,begin*['0'],0,self.fflag)
            if force_flag == True:
                self.fflag = True
                sleep(1)
                return self.decode
            elif force_flag == -1:
                return self.decode
            begin = begin+1
        return False


    def randompattern(self,times = 1):
        '''random sort your pattern'''
        self.pattern = list(self.pattern)
        for i in range(times):
            randomsort(self.pattern)
        self.pattern = ''.join(self.pattern)
    
    def setpattern(self,pat = keylist):
        if isinstance(pat,list):
            pat = ''.join(pat)
        if not isinstance(pat,str):
            raise TypeError
        self.pattern = pat

    def updatestr(self,value):
        if not isinstance(value,str):
            raise TypeError
        self.encode = value
        self.fflag = false
        self.decode = None



def moddic(string,pattern,slist,keylist = [],post = 0):
    '''generate dictionary '***abc**' '''
    if post == 0:
        keylist = list(string)
    if post >= len(string):
        slist.append(''.join(keylist))
        return   
    key = list(keylist)
    for ech in range(post,len(string)):
        if string[ech] == '*':
            post = ech
            break
    for ech in pattern:
        key[post] = ech
        moddic(string,pattern,slist,key,post+1)



def defaultdic(string,slist,leng,keylist = [],post = 0):
    '''generate dictionary with length '''
    if post == 0:
        keylist = leng*['0']
    if post >= leng:
        slist.append(''.join(keylist))
        return
    key = list(keylist)
    for ech in string:
        key[post] = ech
        defaultdic(string,slist,leng,key,post+1)
    
def alldic(string,slist,begin = 1,end = 1):
    '''generate dictionary  '''
    while begin <= end:
        defaultdic(string,slist,begin)
        begin = begin+1

    return


        





class dicforce:
    '''this class used to make dictionary attack,you can create diction use this class\n help(dicforce.method) to check more'''
    def __init__(self,dtype):
        ''' init with a attack type such as 'md5' or the func you have usee addType()  '''
        if not isinstance(dtype,str):
            raise TypeError
        getType(dtype)
        self.type = dtype
        self.__dic = []
        self.decode = None

    def dicgen(self,value,*dtype):
        '''create the dic you need such as ('**ab*','123') or ('abc',4) or ('abc'),1,4) '''
        if not isinstance(value,str):
            raise TypeError
        if len(dtype) == 2 and dtype[1] >= dtype[0]:
            slist = []
            alldic(value,slist,dtype[0],dtype[1])
            self.__dic.append(slist)
            return
        
        elif len(dtype) != 0 and isinstance(dtype[0],int):
            slist = []
            defaultdic(value,slist,dtype[0])
            self.__dic.append(slist)


            return
        elif len(dtype) != 0 and isinstance(dtype[0],str):
            slist = []
            moddic(value,dtype[0],slist)
            self.__dic.append(slist)
            return
        else:
            raise TypeError

    def getdicnums(self):
        return len(self.__dic)

    def getdicitem(self,index):
        '''get the dic you want'''
        if not isinstance(index,int):
            raise TypeError
        return self.__dic[index]

    def getdic(self):
        '''get all your dic'''
        return self.__dic

    def force(self,value):
        ''' use dic you already had to brute force the string'''
        if not isinstance(value,str):
            raise TypeError
        for echdic in self.__dic:
            for ech in echdic:
                if getType(self.type)(ech) == value:
                    self.decode = ech
                    return True

        return False
            
    def getdecode(self):
        '''check your result'''
        return self.decode
            








       
class md5force(hashforce):
    '''this is md5force class'''
    def __init__(self,value,pat = keylist):
        hashforce.__init__(self,value,'md5',pat)
    


class crc32force(hashforce):
    '''this is crc32force class'''
    def __init__(self,value,pat = keylist):
        hashforce.__init__(self,value,'crc32',pat)
            

                

                             
                             
 
       
                

 

  
            
            
            
               


