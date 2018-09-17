import ujson as json

# build study ID list
idFile = open("clinTrialIDlist.txt","r")
ids = []
count = 0
for line in idFile:
    ids.append(line.strip("\n"))
    count += 1
idFile.close()
for id in ids:
    with

    # interventions, studies, conditions, result_groups, outcome_measurements,
    # outcome_analyses, outcomes (type needs to be Primary)


    study = None # set value to dictionary of dictionaries listed above
    outfile = open('trialData','a')
    json.dump(study,outfile)
    outfile.close()
