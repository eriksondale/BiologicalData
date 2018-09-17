import ujson as json
import urllib2
import psycopg2
import psycopg2.extras
import time

# Note this will cause server to close connection if
# run for a long period of time (~ 12 hours)

studyIDs = []
with open('clinTrialIDlist.txt','r') as IDFile:
    for line in IDFile:
        studyIDs.append(line.replace("\n",""))


userName = 'mis161'
passWord = '206AACT/'

try:
    conn = psycopg2.connect(dbname="aact", host="aact-db.ctti-clinicaltrials.org", user=userName, password=passWord, port=5432)
except Exception, e:
    print "Cannot connect to database"
    print e

del userName
del passWord

cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

with open('data.json', 'w') as outfile:
    for ID in studyIDs:
                ##printID)
        ID = [ID]
        cur.execute("SELECT nct_id,name,description FROM interventions WHERE \
                            nct_id = ANY(%s)",(ID,))  # (SELECT nct_id FROM conditions WHERE downcase_name= %s )", [condition])
        drugs = cur.fetchall()
        cur.execute("SELECT nct_id,start_date, enrollment, completion_date, \
                            overall_status,phase,results_first_posted_date \
                        FROM studies WHERE nct_id = ANY(%s)",(ID,))
        studies = cur.fetchall()
                #cur.execute("SELECT nct_id,description FROM brief_summaries WHERE nct_id = ANY(%s)",(studyIDs,))
                #brief_summaries = cur.fetchall()
        cur.execute("SELECT nct_id,name FROM conditions WHERE nct_id = ANY(%s)",(ID,))
        conditions = cur.fetchall()
                #cur.execute("SELECT nct_id,agency_class,lead_or_collaborator,name FROM sponsors WHERE nct_id = ANY(%s)",(studyIDs,))
                #sponsors = cur.fetchall()
                #cur.execute("SELECT nct_id,description FROM detailed_descriptions WHERE nct_id = ANY(%s)",(studyIDs,))
                #detailed_descriptions = cur.fetchall()
                #cur.execute("SELECT nct_id,group_type,title,description FROM design_groups WHERE nct_id = ANY(%s)",(studyIDs,))
                #design_groups = cur.fetchall()
                #for i in range(0,len(interventions)):
                    #if interventions[i]['intervention_type']=='Drug':
                        #drugs.append(interventions[i])
                #cur.execute("SELECT nct_id,outcome_type,measure,time_frame,population,description \
            #                FROM design_outcomes WHERE (nct_id = ANY(%s))",(studyIDs,))
                #design_outcomes = cur.fetchall()
                #cur.execute("SELECT nct_id,gender,minimum_age,maximum_age,population,criteria FROM eligibilities WHERE \
                            #nct_id = ANY(%s)",(studyIDs,))  # (SELECT nct_id FROM conditions WHERE downcase_name= %s )", [condition])
                #eligibilities = cur.fetchall()
                #cur.execute("SELECT nct_id,url,description FROM links WHERE nct_id = ANY(%s)",(studyIDs,))
                #links = cur.fetchall()
                #cur.execute("SELECT nct_id,pmid,reference_type FROM study_references WHERE nct_id = ANY(%s)",(studyIDs,))
                #study_references = cur.fetchall()
                #cur.execute("SELECT nct_id,result_group_id,time_frame,event_type,description,event_count, \
                #            organ_system,adverse_event_term,frequency_threshold FROM reported_events WHERE nct_id = ANY(%s)",(studyIDs,))
                #reported_events = cur.fetchall()
        cur.execute("SELECT id,nct_id,result_type,title,description FROM result_groups \
                        WHERE nct_id = ANY(%s)",(ID,)) # IN (SELECT nct_id FROM conditions WHERE downcase_name= %s )", [condition])
        result_groups = cur.fetchall()
        cur.execute("SELECT nct_id,outcome_id,result_group_id,classification,category,title, \
                            description,units,param_type,param_value,param_value_num, dispersion_type, \
                            dispersion_value, dispersion_value_num, \
                            explanation_of_na FROM outcome_measurements WHERE nct_id = ANY(%s)",(ID,))
        outcome_measurements = cur.fetchall()
        cur.execute("SELECT nct_id,outcome_id,param_type,param_value,p_value_modifier,p_value, \
                            method,method_description,groups_description FROM outcome_analyses WHERE nct_id = ANY(%s)",(ID,))
        outcome_analyses = cur.fetchall()
        cur.execute("SELECT id,nct_id,outcome_type,title,description,time_frame,population,units, \
                            units_analyzed FROM outcomes WHERE nct_id = ANY(%s)",(ID,))
        cur.execute("SELECT * FROM outcomes WHERE nct_id = ANY(%s) AND outcome_type='Primary'",(ID,))
        outcomes = cur.fetchall()

        study = {#'brief_summaries': (item for item in brief_summaries if item["nct_id"] == nct_id).next(), \
                         'conditions': conditions,\
                         #rList(nct_id,conditions), \
                        # 'design_groups': rList(nct_id,design_groups), \
                        # 'design_outcomes': rList(nct_id,design_outcomes), \
                        # 'detailed_descriptions': rList(nct_id,detailed_descriptions), \
                         'drugs': drugs,\
                         #rList(nct_id,drugs), \
                        # 'eligibilities': (item for item in eligibilities if item["nct_id"] == nct_id).next(), \
                        # 'interventions': rList(nct_id,interventions), \
                        # 'links': rList(nct_id,links), \
                         'outcome_analyses': outcome_analyses, \
                         #rList(nct_id,outcome_analyses), \
                         'outcome_measurements': outcome_measurements, \
                         #rList(nct_id,outcome_measurements), \
                         'outcomes': outcomes, \
                         #rList(nct_id, outcomes), \
                        # 'reported_events': rList(nct_id,reported_events), \
                         'result_groups': result_groups, \
                         #rList(nct_id,result_groups), \
                        # 'sponsors': rList(nct_id,sponsors), \
                         'studies': studies[0], \
                         #'study_references': rList(nct_id,study_references), \
                         'nct_id': studies[0]['nct_id']
                        }
        json.dump(study, outfile)
        time.sleep(.2)
print('Done')
