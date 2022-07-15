## Introduction

Thank you in advance for assisting in the CLIP curation process.

CLIP is our clinical Cohort with Limited Imaging Pathology. The very first step of curating this dataset, before even looking at the images, is checking the reports written by the radiologists when the images were read clinically.

## Requirements

- Python 3.X
- `pandas`
- `numpy`

Please message your friendly lab tech support if you need help installing the requirements.

## Getting started

Contained in this directory are a Jupyter notebook, and a Python file:

- annotationHelperLib.py
- Radiology\_Report\_Onboarding.ipynb

There are also 4 .csv files associated with this repo but not included in it:

- training\_examples\_clip.csv
- training\_examples\_not\_clip.csv
- training\_examples\_selfeval.csv
- reliability\_ratings.csv


Do NOT open the reliability ratings file in Excel or Sheets, but the other 3 .csv files can be opened in your spreadsheet software of choice. 

The training examples clip/not clip files should be looked at first. They are meant to be references to 
1. Accustom you to the structure and language of radiology reports, and
2. Provide examples of reports identified as CLIP or not CLIP.

Once you have a grasp for what types of reports are assigned to the CLIP and not CLIP groups, proceed to the training examples selfeval (self-evaluation). You may also open the selfeval file in the spreadsheet software of your choice. Hide the column labelled "confirm\_healthy" and add a new column at the end for your own rating practice. For each row, read the narrative text and impression text columns and note your rating (0/1/2, see next section) in your rating column. The goal is to practice reading and rating, but you can check your ratings with the ratings in the hidden column.

## Rating System

These examples are labelled as CLIP or not CLIP (True or False in the `confirm_clip` column). We are currently in the process of migrating from a binary system to a 3 label system:

0 - NOT CLIP, pathology or conditions in the radiology report indicate the subject should not be considered for this data set
1 - mild pathology, such as slightly enlarged ventricles, etc.
2 - CLIP, the report contains an utter lack of pathology in the brain and the impression is "unremarkable"


Keywords (updated 2022-06-13):
- Special Cases:
  - Chiari malformation: is it small enough that there is no measurement, if it’s borderline, or if the brain is otherwise remarkable, the scan can be marked as CLIP. If there’s multiple things going on in addition to the Chiari malformation or the malformation has a measurement associated with it, it’s more likely a non-CLIP scan
  - Outside Scan: Go ahead and mark those reports ("This is an outside scan") as non CLIP. Chances are we wouldn’t be able to get those scans since they didn’t actually happen at CHOP and there’s no way to confirm what’s going on in them
  - Otherwise unremarkable: check for other keywords in the

- Not CLIP Keywords (Rating 0):
  - chemo
  - craniectomy
  - craniotomy
  - shunt
  - postop/post op/post-op/post surg/surgical cavity/surgical site/resection
  - glioblastoma
  - glioma
  - astrocytoma
  - Most -omas, otomy, and -ectomy
  
- Maybe CLIP Keywords (Rating 1):
  - orthodontic hardware
  - motion/patient motion/patient movement/motion degrad/degraded by motion
  - patient motion/motion artifact
  - virchow-robin
  - pineal cyst
  - pars intermedia cyst
  - enlarged ventricles
  - prominent CSF
  - "slight enlargment"
  - "mild"
  
- CLIP Keywords (Rating 2):
  - Unremarkable brain/scan/MRI
  
- Not relevant to CLIP:
  - opacification of the sinus cavities


## Reliability Ratings

When you finish the self evaluation and understand any mismatches between your ratings and the "ground truth" ratings, you will open the final spreadsheet (reliability ratings) using the .ipynb. NOTE: do not open this file in Excel, Sheets, or Numbers - this spreadsheet is used for measuring reliability between raters and must be saved in an unaltered .csv file. (Excel/Sheets/Numbers have a tendency to impose formatting on data that is then saved in its modified form. Example: a numeric session id 123456789 could be forced into scientific notation and saved as 1.23E8, which is bad for our purposes.)

To run the Jupyter notebook, open a Terminal window, navigate to the directory containing the .ipynb file (`cd`), and run the command

`jupyter notebook`

A page will open in your default internet browser. Open the .ipynb file. Follow the instructions at the top of the file, beginning with modifications to the three variables in the first cell. For the name variable, please enter the name you want used in any publications about this data set.

Run the two code cells and follow the prompts in the output portion of the second cell. You will be prompted to assign ratings to each displayed report (0/1/2, see previous section), with the options to navigate between reports, save your progress to the file, and exit (stop the code). 

It is HIGHLY recommended to save periodically and take breaks when the program prompts you to.

Customizations: You may find as you go that there are certain words that help you differentiate between different rating groups. At any point, you may use the exit command after a rating to stop the program, then modify the list of terms in the first code cell that are highlighted during the rating process. This feature is meant as an aid, but entering too many common terms may make the highlighted reports visually overwhelming.  

## Next Steps

Contact the project maintainer to return the updated reliability ratings file and obtain more reports to grade.
