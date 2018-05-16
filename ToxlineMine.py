import urllib2

print('This script will query and return based on keywords entered....')
keyword = raw_input("Enter keyword: ")
keyword = keyword.replace(" ","+")

contents = urllib2.urlopen("https://toxgate.nlm.nih.gov/cgi-bin/sis/search2/x?dbs+toxline:" + keyword).read()

IDStr = contents[contents.find("<Id>")+4:contents.find("</Id>")+(-1)]
IDs = IDStr.split(" ")

print(' ')
print(contents)
print(' ')
for label in IDs:
    print(label)
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
