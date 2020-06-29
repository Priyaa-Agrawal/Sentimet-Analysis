import textract
import os

#extractin text from files
def all_file(src):
    text = textract.process(src, encoding='ascii')
    print(text)
    temp = str(text)
    l = len(str(text))
    temp = temp[2:l-2]
    os.remove(src)
    return temp
