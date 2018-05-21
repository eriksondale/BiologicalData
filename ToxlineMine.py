import urllib2
import math
from sys  import argv as argument
from docx import Document

def expandResults(hits, tempFile): # Helper method meant to increase results size upon user request
    returnIDs = []
    for x in range(0, int(hits)):
        contents = urllib2.urlopen("https://toxgate.nlm.nih.gov/cgi-bin/sis/search2/g?" + tempFile + ":" +str(x)).read()
        IDStr = contents[contents.find("<Id>")+4:contents.find("</Id>")+(-1)]
        IDsTemp = IDStr.split(" ")
        for label in IDsTemp:
            returnIDs.append(label)
    #remove duplicates from list
    finalIDs = []
    for label in returnIDs:
        if label not in finalIDs:
            finalIDs.append(label)
    #return statement
    #returnIDs.sort()
    return finalIDs

print('This script will query and return based on keywords entered....')
keyword = raw_input("Enter search words: ")

# Making list of keywords in order to bold in results later
keywordTemp = keyword
keywordTemp = keywordTemp.replace("(","")
keywordTemp = keywordTemp.replace(")","")
keywordTemp = keywordTemp.replace("AND","")
keywordTemp = keywordTemp.replace("OR","")
keywordTemp = keywordTemp.replace("NOT","")
keyList = keywordTemp.split(" ")
while '' in keyList:
    keyList.remove('')

document = Document()

p = document.add_paragraph('')
p.add_run('Toxline Search Query: ').bold = True
p.add_run(keyword)

keyword = keyword.replace(" ","+")
contents = urllib2.urlopen("https://toxgate.nlm.nih.gov/cgi-bin/sis/search2/x?dbs+toxline:" + keyword).read()

hits = contents[contents.find("<Count>")+7:contents.find("</Count>")]
p = document.add_paragraph('')
p.add_run('Hits: ').bold = True
p.add_run(hits)

tempFile = contents[contents.find("<TemporaryFile>")+15:contents.find("</TemporaryFile>")]
#print(tempFile + " TempLink")

pageNum = int(math.ceil(int(hits)/ 10.0))
#print(str(pageNum) + ' Pages')
#print(' ')

answer = raw_input(hits + ' results were found. Do you want to list them all? (y/n)')
if(answer == "y"):
    IDs = expandResults(hits, tempFile)
else:
    IDStr = contents[contents.find("<Id>")+4:contents.find("</Id>")+(-1)]
    IDs = IDStr.split(" ")
#print(IDs)

drugName = raw_input("What drug did you want?: ")
count = 0

p.add_run('Drug: ').bold = True
p.add_run(drugName.capitalize())

document.add_paragraph(' ')
# Printing the desired contents of the file
for label in IDs:
    data = urllib2.urlopen("https://toxgate.nlm.nih.gov/cgi-bin/sis/search2/z?dbs+toxline:@term+@DOCNO+" + label).read()
    # Insert confirming keywords present here
    if(drugName in data or drugName.capitalize() in data):
        count = count + 1
        title = data[data.find("<na>")+4:data.find("</na>")]
        authors = data[data.find("<au>")+4:data.find("</au>")]
        source =  data[data.find("<so>")+4:data.find("</so>")]
        abstract = data[data.find("<ab>")+4:data.find("</ab>")]
        p = document.add_paragraph(' ')
        p = document.add_paragraph()
        p.add_run(title).bold = True
        p = document.add_paragraph()
        p.add_run(authors)
        p = document.add_paragraph()
        p.add_run(source)
        p = document.add_paragraph()
        p.add_run(abstract)
document.save(drugName.capitalize() + 'ToxlineSearch.docx')
print(str(count) + " articles were found with the drug. See created document..." )
