from tkinter import *
from tkinter.filedialog import *
import pickle

word = {
    'a' : [
        'a',
        'able',
        'ability',
        'achivement',
        'again',
        'all',
        'alpha',
        'alphabet'
        'am',
        'an',
        'ant',
        'any',
        'angry',
        'anyone',
        'anybody',
        'anywhere',
        'apple',
        'apply',
        'application',
        'April',
        'are',
        'as',
        'aunt',
        'August',
        'awful',
        ''
        ],
    'b' : [
        'b',
        'bank',
        'base',
        'basic',
        'banana',
        'basket',
        'baseball',
        'basketball',
        'beach',
        'bit',
        'bin',
        'boom',
        'bring',
        'bridge',
        'bright',
        ''
        ],
    'c' : [
        'c',
        'car',
        'cake',
        'case',
        'cash',
        'caugh',
        'canvas',
        'cabbage',
        'celebrate',
        'cell',
        'cute',
        ],
    'd' : [
        'd',
        'data',
        'date',
        'dance',
        'dancer',
        'danger',
        'dangeons',
        'desktop',
        'December',
        'dist',
        'dictionary'
        'document',
        'duck',
        ],
    'e' : [
        'e',
        'egg',
        'else',
        'entry',
        'entrance',
        'explore',
        'explorer',
        ],
    'f' : [
        'f',
        'float',
        'flow',
        'fade',
        'fuck',
        'fucking',
        'find',
        'found',
        'founder',
        'fix',
        'fat'
        ],
    'g' : [
        'g'
        ],
    'h' : [
        'h'
        ],
    'i' : [
        'i'
        ],
    'j' : [
        'j'
        ],
    'k' : [
        'k'
        ],
    'l' : [
        'l'
        ],
    'm' : [
        'm'
        ],
    'n' : [
        'n'
        ],
    'o' : [
        'o'
        ],
    'p' : [
        'p'
        ],
    'q' : [
        'q'
        ],
    'r' : [
        'r'
        ],
    's' : [
        's'
        ],
    't' : [
        't'
        ],
    'u' : [
        'u'
        ],
    'v' : [
        'v'
        ],
    'w' : [
        'w'
        ],
    'x' : [
        'x'
        ],
    'y' : [
        'y'
        ],
    'z' : [
        'z'
        ]
    }

def install():
    file = open('word bank.dat', 'wb')
    pickle.dump(word, file)
    file.close()

class Word():
    def __init__(self, value=None):
        if value == None:
            file = open('word bank.dat', 'rb')
            self.dic = pickle.load(file)
            file.close()
        elif type(value) == type({}):
            self.dic = value
        else:
            raise TypeError('value must be a dictionary type')
    def search(self, key):
        return self.dic[key]
    def get(self):
        return self.dic
    def insert(self, key, item=[], save=False):
        for x in item:
            self.dic[key] = self.dic[key].append(x)
        if save == True:
            file = open('word bank.dat', 'wb')
            pickle.dump(self.dic, file)
            file.close()
        return self.dic
    def change(self, key, item, save=False):
        if type(item) == type([]):
            self.dic[key] = item
        else:
            raise TypeError('Argument \'item\' must be list type')
        if save == True:
            file = open('word bank.dat', 'wb')
            pickle.dump(self.dic, file)
            file.close()
        return self.dic
    def delete(self, key, item, save=False):
        if type(item) == type(1):
            del self.dic[key][item]
        elif type(item) == type(''):
            times = 0
            try:
                while True:
                    if self.dic[key][times] == item:
                        del self.dic[key][times]
                        break
                    times += 1
            except IndexError:
                raise ValueError('No item \'%s\' in word bank.dat[%s]' % (item, key))
            return dic
        elif type(item) == type([]):
            for x in item:
                if type(x) == type(0):
                    del self.dic[key][x]
                elif type(x) == type(''):
                    times = 0
                    try:
                        while True:
                            if self.dic[key][times] == x:
                                del self.dic[key][times]
                                break
                            times += 1
                    except IndexError:
                        raise ValueError('No item \'%s\' in word bank.dat[%s]' % (x, key))
        else:
            raise TypeError('type \'item\' must be string or int')
        # Delete
        if save == True:
            file = open('word bank.dat', 'wb')
            pickle.dump(self.dic, file)
            file.close()
        return self.dic
    def save(self, location=None):
        if location == None:
            location = asksaveasfilename(filetypes=[('DAT', '.dat')])
        if location[-4] + location[-3] + location[-2] + location[-1] != '.dat':
            location = location + '.dat'
            print('Warning : Your location is not a dat file, we turned it to a dat file, please check the file if it not the shape you want.')
        file = open(location, 'wb')
        pickle.dump(self.dic, file)
        file.close()
