import pandas as pd
import numpy as np
import random
from annotationHelperLib import *
from IPython.display import clear_output
from google.cloud import bigquery # SQL table interface on Arcus


    
##
# Pull the report associated with a proc_ord_id for which the specified grader has a grade of 999, and then grade the report. Modifies lab.grader_table
# @param name A str containing the full name of the grader (to also be referenced in publications)
# @param toHighlight A dictionary with str keys specifying a color to highlight the list of str text with
def jennaRegradeOneTrainingReportSQL(name, toHighlight = {}):

    # Initialize the client service
    client = bigquery.Client()
    
    # Get a row from the grader table for the specified rater that has not been graded yet
    getSingleRowQuery = 'SELECT * FROM lab.training_examples WHERE grade = 999 LIMIT 1'

    df = client.query(getSingleRowQuery).to_dataframe()
    
    if len(df) == 0:
        print("There are currently no ungraded training reports.")
        return
    
    # Combine the narrative and impression text
    reportText = df['narrative_text'].values[0] 
    if df['impression_text'].values[0] != 'nan':
        reportText += ' IMPRESSION:' + str(df['impression_text'].values[0])
    
    # If the user passed a dictionary of lists to highlight
    if len(toHighlight.keys()) > 0:
        for key in toHighlight.keys():
            reportText = markTextColor(reportText, toHighlight[key], key)
            
    # Print the report and ask for a grade
    print(reportText)
    print()
    grade = str(input('Assign a SLIP rating to this report (0 do not use/1 maybe use/2 definitely use): '))
    while grade != "0" and grade != "1" and grade != "2":
        grade = str(input('Invalid input. Assign a SLIP rating to this report (0 do not use/1 maybe use/2 definitely use): '))
    print()
    
    # Update the grader table with the new grade
    updateQuery = 'UPDATE lab.training_examples set grade = '+str(grade)
    updateQuery += ' WHERE report_id like "'+str(df['report_id'].values[0]) + '"'

    updateJob = client.query(updateQuery)
    updateJob.result()

    # Ask for a reason the report was given the grade it was
    reason = str(input('Why does this report get that grade? '))
    print()

    # Update the grader table with the new grade
    updateQuery = 'UPDATE lab.training_examples set reason="'+ reason + '"'
    updateQuery += ' WHERE report_id like "'+str(df['report_id'].values[0]) + '"'

    updateJob = client.query(updateQuery)
    updateJob.result()
    print("Grade saved. Run the cell again to grade another report.")
    
    
##
# Iteratively show the user all of the SLIP/non SLIP example reports in a random order (training step 1)
# @param toHighlight A dictionary with str keys specifying a color to highlight the list of str text with
def readSampleReports(toHighlight = {}):

    # Initialize the client service
    client = bigquery.Client()
    
    # Get the SLIP and non-SLIP example reports
    getSlipExamples = 'SELECT * FROM lab.training_examples;'

    slipDf = client.query(getSlipExamples).to_dataframe()

    slipReportsList = [ row['narrative_text'] + '\n\nIMPRESSION: ' + str(row['impression_text']) + '\n\nReport given grade of ' + str(row['grade']) for i, row in slipDf.iterrows()]
        
    # Shuffle the list of all reports
    random.shuffle(slipReportsList)
    
    # Iteratively print each report
    for report in slipReportsList:
        # If the user passed a dictionary of lists to highlight
        if len(toHighlight.keys()) > 0:
            reportText = report
            for key in toHighlight.keys():
                reportText = markTextColor(reportText, toHighlight[key], key)
            
            # Print the report and ask for a grade
            print(reportText)
        else:
            print(report)
    
        print()
    
        confirm = str(input('After you read the report and understand its grade, press ENTER to continue to the next report.'))
        clear_output()
        
    print('You have finished reading the example reports. Rerun this cell to read them again or proceed to the next section.')
    
    
##
# Pull the report associated with a proc_ord_id for which the specified grader has a grade of 999, and then grade the report. Modifies lab.grader_table
# @param name A str containing the full name of the grader (to also be referenced in publications)
# @param toHighlight A dictionary with str keys specifying a color to highlight the list of str text with
def markSelfEvalReportSQL(name, toHighlight = {}):

    # Initialize the client service
    client = bigquery.Client()
    
    # Get a row from the grader table for the specified rater that has not been graded yet
    getSingleRowQuery = 'SELECT * FROM lab.training_selfeval WHERE grader_name like "' + name + '" and grade = 999 LIMIT 1'

    df = client.query(getSingleRowQuery).to_dataframe()
    
    if len(df) == 0:
        print("There are currently no reports to grade for", name, " in the table. You have completed the self-evaluation.")
        return
    
    # Get the report for that proc_ord_id from the primary report table
    getReportRow = 'SELECT * FROM arcus.training_examples_selfeval where combo_id like "'+str(df['report_id'].values[0])+'"'
    reportDf = client.query(getReportRow).to_dataframe()
    
    # Combine the narrative and impression text
    reportText = reportDf['narrative_text'].values[0] 
    if reportDf['impression_text'].values[0] != 'nan':
        reportText += ' IMPRESSION:' + reportDf['impression_text'].values[0]
    
    # If the user passed a dictionary of lists to highlight
    if len(toHighlight.keys()) > 0:
        for key in toHighlight.keys():
            reportText = markTextColor(reportText, toHighlight[key], key)
            
    # Print the report and ask for a grade
    print(reportText)
    print()
    grade = str(input('Assign a SLIP rating to this report (0 do not use/1 maybe use/2 definitely use): '))
    while grade != "0" and grade != "1" and grade != "2":
        grade = str(input('Invalid input. Assign a SLIP rating to this report (0 do not use/1 maybe use/2 definitely use): '))
    print()
    
    # Update the grader table with the new grade
    updateQuery = 'UPDATE lab.training_selfeval set grade = '+str(grade)
    updateQuery += ' WHERE report_id like "'+str(df['report_id'].values[0])+'"'
    updateQuery += ' and grader_name like "' + name + '"'

    updateJob = client.query(updateQuery)
    updateJob.result()
    
    # Ask for a reason the report was given the grade it was
    reason = str(input('Why does this report get that grade? '))
    print()

    # Update the grader table with the new grade
    updateQuery = 'UPDATE lab.training_selfeval set reason="'+ reason + '"'
    updateQuery += ' WHERE report_id like "'+str(df['report_id'].values[0]) + '"'
    updateQuery += ' and grader_name like "' + name + '"'

    updateJob = client.query(updateQuery)
    updateJob.result()
    
    # Print out the grade and reason Jenna gave the report
    print()
    truthQuery = 'SELECT grade, reason from lab.training_selfeval WHERE report_id like "'+str(df['report_id'].values[0])
    truthQuery += '" and grader_name not like "'+name+'"'
    
    truthDf = client.query(truthQuery).to_dataframe()
    print("For reference, other graders have given this report the following grades for the specified reasons:")
    print()
    for idx, row in truthDf.iterrows():
        if int(row['grade']) != 999:
            print("Grade:", row['grade'], "For reason:", row['reason'])
    
    print()
    confirmContinue = str(input('Press enter to continue'))
          
    print("Grade saved. Run the cell again to grade another report.")
    
##
# Pull the report associated with a proc_ord_id for which the specified grader has a grade of 999, and then grade the report. Modifies lab.grader_table
# @param name A str containing the full name of the grader (to also be referenced in publications)
# @param toHighlight A dictionary with str keys specifying a color to highlight the list of str text with
def markOneReportSQL(name, toHighlight = {}):

    # Initialize the client service
    client = bigquery.Client()
    
    # Get a row from the grader table for the specified rater that has not been graded yet
    getSingleRowQuery = 'SELECT * FROM lab.grader_table WHERE grader_name like "' + name + '" and grade = 999 LIMIT 1'

    df = client.query(getSingleRowQuery).to_dataframe()
    
    if len(df) == 0:
        print("There are currently no reports to grade for", name, " in the table. Please add more to continue.")
        return
    
    # Get the report for that proc_ord_id from the primary report table
    getReportRow = 'SELECT * FROM arcus.reports_annotations_master where proc_ord_id like "'+str(df['proc_ord_id'].values[0])+'"'
    reportDf = client.query(getReportRow).to_dataframe()
    
    # If the id was in the original table:
    if len(reportDf) == 1:
        # Combine the narrative and impression text
        reportText = reportDf['narrative_text'].values[0] 
        if reportDf['impression_text'].values[0] != 'nan':
            reportText += '\n\nIMPRESSION: ' + reportDf['impression_text'].values[0]
            
    elif len(reportDf) == 0:
        getReportRow = 'SELECT * FROM arcus.procedure_order_narrative where proc_ord_id like "'+str(df['proc_ord_id'].values[0])+'"'
        reportText = client.query(getReportRow).to_dataframe()['narrative_text']
        
        getReportRow = 'SELECT * FROM arcus.procedure_order_impression where proc_ord_id like "'+str(df['proc_ord_id'].values[0])+'"'
        reportDf = client.query(getReportRow).to_dataframe()
        
        if len(reportDf) == 1:
            reportText += "\n\nIMPRESSION: " + reportDf['impression_text'].values[0]
        
    
    # If the user passed a dictionary of lists to highlight
    if len(toHighlight.keys()) > 0:
        for key in toHighlight.keys():
            reportText = markTextColor(reportText, toHighlight[key], key)
            
    # Print the report and ask for a grade
    print(reportText)
    print()
    grade = str(input('Assign a SLIP rating to this report (0 do not use/1 maybe use/2 definitely use): '))
    while grade != "0" and grade != "1" and grade != "2":
        grade = str(input('Invalid input. Assign a SLIP rating to this report (0 do not use/1 maybe use/2 definitely use): '))
    print()
    
    # Ask the user to confirm the grade
    confirmGrade = "999"
    while confirmGrade != grade :
        while confirmGrade != "0" and confirmGrade != "1" and confirmGrade != "2":
            confirmGrade = str(input("Please confirm your grade by reentering it OR enter a revised value to change the grade: "))
        if confirmGrade != grade:
            grade = confirmGrade
            confirmGrade = "999"
            
    print("Saving your grade of", grade, "for this report.")
    
    # Update the grader table with the new grade
    updateQuery = 'UPDATE lab.grader_table set grade = '+str(grade)
    updateQuery += ' WHERE proc_ord_id = '+str(df['proc_ord_id'].values[0])
    updateQuery += ' and grader_name like "' + name + '"'

    updateJob = client.query(updateQuery)
    updateJob.result()
    print("Grade saved. Run the cell again to grade another report.")
    
##
# Get more proc_ord_id for which no reports have been rated for the specified user to grade
# @param name A str containing the full name of the grader (to also be referenced in publications)
def getMoreReportsToGrade(name, legacy=False):
    # Initialize the client service
    client = bigquery.Client()
    
    if legacy:
        source = "arcus.reports_annotations_master"
    else:
        source = "arcus.procedure_order"
    
    # Set up the query to get more reports for the specified person to annotate
    addReportsQuery = "insert into lab.grader_table "
    
    addReportsQuery += "with CTE as (select distinct cast(source.proc_ord_id as int64) as proc_ord_id, '" + name + "' as grader_name, 'Unique' as grade_category, 999 as grade, proc_ord_year, age_in_days, from"
    addReportsQuery += source 
    addReportsQuery += """ source 
                            left outer join
                          lab.grader_table filter
                          on cast(source.proc_ord_id as int64) = filter.proc_ord_id
                          where filter.proc_ord_id is null
                          order by source.proc_ord_year desc, source.age_in_days asc
                          limit 100)
                        select proc_ord_id, grader_name, grade_category, grade from CTE"""

    # Submit the query
    supplementRaterReports = client.query(addReportsQuery)
    supplementRaterReports.result()
    
    # Check: how many reports were added for the user?
    getUserUnratedCount = 'SELECT * FROM lab.grader_table WHERE grader_name like "' + name + '" and grade = 999'

    df = client.query(getUserUnratedCount).to_dataframe()
    
    # Inform the user
    print(len(df), "reports were added for grader", name)
    
    
def welcomeUser(name):
    print("Welcome,", name)

    
    client = bigquery.Client()
    
    # POssibly pull this bit into its own function - make it user proof
    qCheckSelfEval = 'select * from lab.training_selfeval where grader_name like"'+name+'"'
    selfEvalDf = client.query(qCheckSelfEval).to_dataframe()
    
    if len(selfEvalDf) == 0:
        print("It appears you have yet to do the self-evaluation. Please grade those reports before continuing.")
        # break
        
    elif 999 in selfEvalDf['grade'].values:
        print("It appears you have started the self-evaluation but have not finished it. Please grade those reports before continuing.")
        # break
    
    
    qReliability = 'select * from lab.grader_table where grade_category = "Reliability" and grader_name like"'+name+'"'
    reliabilityDf = client.query(qReliability).to_dataframe()
           
    if len(reliabilityDf) == 0:  # to add: check if any self-eval reports have not been graded      
        print("It appears you have yet to do grade the reliability reports. They are being added to your queue now.")
        for grade in range(3):
            print("Adding for grade", grade)
            insertReliabilityQuery = "insert into lab.grader_table "
            insertReliabilityQuery += "select "
            insertReliabilityQuery += "distinct cast(proc_ord_id as int64), "
            insertReliabilityQuery += "'"+name+"' as grader_name, "
            insertReliabilityQuery += "'Reliability' as grade_category, "
            insertReliabilityQuery += "999 as grade "
            insertReliabilityQuery += "from lab.grader_table where "
            insertReliabilityQuery += "grader_name = 'Jenna Schabdach' and "
            insertReliabilityQuery += "grade_category = 'Reliability' and "
            insertReliabilityQuery += "grade = "+str(grade) + " "
            insertReliabilityQuery += "limit 50 ; "
        
            updateJob = client.query(insertReliabilityQuery)
            updateJob.result()
            
    elif 999 in reliabilityDf['grade'].values:
        reliabilityCount = len(reliabilityDf[reliabilityDf['grade'] == 999])
        print("You have", reliabilityCount, "reliability reports to grade.")
    
    else:
        
        getToRateCount = 'select * from lab.grader_table where grader_name like "'
        getToRateCount += name + '" and grade = 999'
        
        raterUnratedDf = client.query(getToRateCount).to_dataframe()
              
        if len(raterUnratedDf) == 0:
              print("You are caught up on your report ratings")
              # TODO add function here to get more reports for the user
        else:
              print("You currently have", len(raterUnratedDf), "ungraded reports to work on.")
                
    return True


##
# Add reports to grade for a user from a list of ids
# @param procIds A list of proc_ord_ids specified by the user
# @param name A string containing the identifier for the user
# @param maxToAdd An int specifying the maximum number of reports to add (default 100)
# @param verbose A boolean flag indicating how much output to print to stdout (default False)
def addReportsFromListForUser(procIds, name, maxToAdd=100, verbose=False, legacy=False):
    print("Note: this cell may take several minutes to run. This is expected behavior.")
    # Set up variables
    client = bigquery.Client()
    reportsInTableStatus = {}
    invalidIds = []
    addedReports = 0
    inTableReports = 0
    reliabilityReports = 0
    if legacy:
        source = "arcus.reports_annotations_master"
    else:
        source = "arcus.procedure_order"
        
    # Check report ids for validity 
    print("Checking the list of ids to make sure each is valid...")
    q = "SELECT * from "+source+" ;"
    procDf = client.query(q).to_dataframe()
    if verbose: print("Proc ord table:",procDf.shape)
    validIds = [i for i in procIds if str(i) in procDf['proc_ord_id'].values]
    if verbose: print("Number of valid ids:",len(validIds))
    print("Validity check completed.")
        
    # Get the list of report ids in the table
    print("Checking to see how many requested reports have been graded or are in the grading queue...")
    q = "SELECT * from lab.grader_table;"
    graderDf = client.query(q).to_dataframe()
    if verbose: print("Graded report table shape:",graderDf.shape)
    
    # Get the difference between the two lists
    graderReports = graderDf['proc_ord_id'].values
    existingReports = [i for i in validIds if i in graderReports]
    unqueuedReports = [i for i in validIds if i not in graderReports]
    if verbose: print("Graded reports:", len(existingReports))
    if verbose: print("Ungraded reports:", len(unqueuedReports))
    
    # Pull up to N reports not yet in the table
    if len(unqueuedReports) >= maxToAdd: 
        # More reports in to-add list than the max
        toAdd = unqueuedReports[:maxToAdd]
    else:
        # Fewer reports in to-add list than the max
        toAdd = unqueuedReports
        
    print("Preparing to add", len(toAdd), "reports for", name, "...")
    
    for r in toAdd:
        # Add the report
        queryInsertReport = "INSERT into lab.grader_table (proc_ord_id, grader_name, grade_category, grade)"
        queryInsertReport += " VALUES (cast('"+str(r)+"' as int64), '"+name+"', 'Unique', 999);"
        addReportJob = client.query(queryInsertReport)
        addReportJob.result()
        
    print(len(toAdd), "were added for", name)

    # For the reports already in the table: get their statuses
    if len(existingReports) > 0:
        print(len(existingReports), "reports are already in the table:")
        gradedReports = graderDf[graderDf['proc_ord_id'].isin(existingReports)]
        if verbose: print(gradedReports.shape)
        # grade values
        for g in range(3):
            print(gradedReports[gradedReports['grade'] == g].shape[0], "were graded", g)
        # graders
        for name in list(set(gradedReports['grader_name'].values)):
            numToGrade = gradedReports[(gradedReports['grade'] == 999) & (gradedReports['grader_name'] == name)].shape[0]
            if numToGrade > 0: print(numToGrade, "are already assigned to", name)
            
            
# Main
if __name__ == "__main__":

    print("Radiology Report Annotation Helper Library v 0.2")
    print("Written and maintained by Jenna Young, PhD (@jmschabdach on Github)")
    print("Tested and used by:")
    print("- Caleb Schmitt, Summer 2021")
    print("- Nadia Ngom, Fall 2021 - Spring 2022")


