import urllib2
import math
from sys  import argv as argument

def expandResulsArr(pageNum, tempFile): # Helper method meant to increase results size upon user request
    print(pageNum)
    returnIDs = []
    for x in range(0,pageNum):
        contents = urllib2.urlopen("https://toxgate.nlm.nih.gov/cgi-bin/sis/search2/g?" + tempFile + ":" +str(x)).read()
        print(contents)
        IDStr = contents[contents.find("<Id>")+4:contents.find("</Id>")+(-1)]
        IDsTemp = IDStr.split(" ")
        print(len(IDsTemp))
        for label in IDsTemp:
            returnIDs.append(label)
    #remove duplicates
    finalIDs = []
    for label in returnIDs:
        if label not in finalIDs:
            finalIDs.append(label)
    #return statement
    return finalIDs

print('This script will query and return based on keywords entered....')
keyword = argument[0]
keyword = keyword.replace(" ","+")

contents = urllib2.urlopen("https://toxgate.nlm.nih.gov/cgi-bin/sis/search2/x?dbs+toxline:" + keyword).read()

hits = contents[contents.find("<Count>")+7:contents.find("</Count>")]
tempFile = contents[contents.find("<TemporaryFile>")+15:contents.find("</TemporaryFile>")]
IDStr = contents[contents.find("<Id>")+4:contents.find("</Id>")+(-1)]
IDs = IDStr.split(" ")
pageNum = int(math.ceil(int(hits)/ 10.0))

print('There are ' + str(pageNum) + ' pages')
print(' ')
#answer = raw_input(hits + ' results were found. Do you want to list them all? (y/n)')
#if(answer == "y"):
IDs = expandResulsArr(pageNum, tempFile)
    #for label in moreIDs:
print(IDs)
#else:
    #print(IDs)

'''
for label in IDs:
    print(' ')
    print('==============================================')
    print(' ')
    data = urllib2.urlopen("https://toxgate.nlm.nih.gov/cgi-bin/sis/search2/z?dbs+toxline:@term+@DOCNO+" + label).read()
    title = data[data.find("<na>")+4:data.find("</na>")]
    abstract = data[data.find("<ab>")+4:data.find("</ab>")]
    print(title)
    print(' ')
    print(abstract)
'''
