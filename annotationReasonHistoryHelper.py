import pandas as pd
import numpy as np
from IPython.display import clear_output

def safelySaveDf(df, fn):
    try:
        df = df.astype(str)
        df.to_csv(fn)
        return True
    except PermissionError:
        print("Error: write access to "+fn+" denied. Please check that the file is not locked by Datalad.")
        return False

def markRedText(line, toMark):
    start = '\x1b[5;30;41m' # red background, bold black text
    end = '\x1b[0m'
    
    if type(toMark) == str:
        line = line.replace(toMark, start+toMark+end)
        
    elif type(toMark) == list:
        for phrase in toMark:
            line = line.replace(str(phrase), start+str(phrase)+end)
    
    else:
        print("Error: the second argument must be either a string or a list of strings")
        
    return line

        
def markGreenText(line, toMark):    
    start = '\x1b[5;30;42m' # green background, bold black text
    end = '\x1b[0m'
    
    if type(toMark) == str:
        line = line.replace(toMark, start+toMark+end)
        
    elif type(toMark) == list:
        for phrase in toMark:
            line = line.replace(str(phrase), start+str(phrase).upper()+end)
    
    else:
        print("Error: the second argument must be either a string or a list of strings")
        
    return line


def markYellowText(line, toMark):
    start = '\x1b[5;30;43m' # yellow background, bold black text
    end = '\x1b[0m'
    
    if type(toMark) == str:
        line = line.replace(toMark, start+toMark+end)
        
    elif type(toMark) == list:
        for phrase in toMark:
            line = line.replace(str(phrase), start+str(phrase)+end)
    
    else:
        print("Error: the second argument must be either a string or a list of strings")
        
    return line


def markReasonAndHistory(fn):

    # Load the dataframe
    df = pd.read_csv(fn)
    # If these two columns are not in the dataframe, add them
    if 'scan_reason' not in list(df):
        df['scan_reason'] = np.nan
    if 'pat_history' not in list(df):
        df['pat_history'] = np.nan

    # Initialize variables
    count = 0
    indicators = ['CLINICAL', 'INDICATION', 'HISTORY', 'REASON']

    for idx, row in df.iterrows():
        # if the row doesn't have scan reason and doesn't have history
        if (row['scan_reason'] == '' or type(row['scan_reason']) == float) and (row['pat_history'] == '' or type(row['pat_history'] == float)):
            # Get the text to print
            narr = row['narrative_text']
            if not type(row['impression_text']) is float:
                narr += "\n\n"+ row['impression_text']
    
            # Format the text - green, yellow, then red
            narr = markYellowText(narr, indicators)

            # Print the text
            print(narr)
            print()

            # Get input from the user
            scan_reason = input("Why was this scan was performed? (type 'skip' to skip this narrative, 'missing' if no reason found) ")
            pat_history = input("What is the patient's clinical history? (type 'skip' to skip this narrative, 'missing' if no history found) ")
            print()

            if scan_reason != "skip" and pat_history != "skip" and scan_reason != "" and pat_history != "":

                # Add the input to the dataframe
                df.loc[idx, 'scan_reason'] = scan_reason
                df.loc[idx, 'pat_history'] = pat_history
    
                # Increment the counter
                count += 1
    
                if count % 10 == 0:
                    print("Total annotated scans this round:", count)
                    print()

                    done = input("Would you like to stop for now? (y/n) ")

                    if done == 'y':
                        safelySaveDf(df, fn)
                        print()
                        return

                    else:
                        save = input("Would you like to save your progress? (y/n) ")
        
                        if save == 'y':
                            safelySaveDf(df, fn)
                            print()
                        else:
                            print("Continuing without saving")
                            print()




    print("You have gone through all of the sessions!")
    safelySaveDf(df, fn)


# Main
if __name__ == "__main__":

    fn = "/Users/schabdachj/Data/clip/tables/rawdata/caleb_start.csv"
    markReasonAndHistory(fn)

