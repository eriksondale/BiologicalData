import ujson as json

def getDictFromFile(fileName, clinID):
    studyFile = open(fileName, 'r')
    firstLine = studyFile.readline()
    firstLine = firstLine.split('|')
    for line in studyFile:
        if id in line:
            line =  line.split('|')
            studyInfo = {}
            for x in range(0,len(line)):
                print(firstLine[x] + ": " + line[x])
                studyInfo[firstLine[x]] = line[x]
            break
    studyFile.close()
    return dict

# build study ID list
idFile = open("clinTrialIDlist.txt","r")
ids = []
count = 0
for line in idFile:
    ids.append(line.strip("\n"))
    count += 1
idFile.close()
infoCount = 0
for id in ids:
    # Study
    studyDict = getDictFromFile('FullClinTrial1Sept2018/conditions.txt', id)
    # Conditions
    conditionDict = getDictFromFile('FullClinTrial1Sept2018/conditions.txt',id)
    # Interventions
    interventionDict = getDictFromFile('FullClinTrial1Sept2018/interventions.txt',id)
    # Outcome (Make sure only primary!!!!!)
    outcomeDict = getDictFromFile('FullClinTrial1Sept2018/outcomes.txt',id)
    # Outcome Measures
    outcomeMeasureDict = getDictFromFile('FullClinTrial1Sept2018/outcome_measurements.txt',id)
    # Outcome Analyses
    outcomeAnalDict = getDictFromFile('FullClinTrial1Sept2018/outcome_analyses.txt',id)
    # Result Groups
    resultGroupDict = getDictFromFile('FullClinTrial1Sept2018/result_groups.txt',id)

    # Build study dict and dump with json

    study = {'nct_id':id,'studies':studyDict,'drugs':interventionDict,'conditions':conditionDict\
            ,'outcomes':outcomeDict,'outcome_measurements':outcomeMeasureDict,'outcome_analyses':outcomeAnalDict,\
            'result_groups':resultGroupDict}
    outfile = open('trialData.json','a')
    json.dump(study,outfile)
    outfile.close()
