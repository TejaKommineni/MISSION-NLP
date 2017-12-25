# MISSION-NLP
**Information extraction from text**

In this project we devised a workflow to extract information from unstructured Latin America terrorism articles. 
Detailed explanation of the project can be found in project.pdf

* The InfoExtract Python file contains the core logic for this system.
* Sample input for this system is all-input.txt which contains list of articles.
* Sample output of this system is all-input.txt.template
* Correct answer template for the given input is in all-answers.txt

Scoring for this project is done using score-ie.pl, a perl program that is invoked as: <br>
      <p align="center"> perl score-ie.pl <output_templates> <answer_templates> <br> 
                         ex: perl score-ie.pl all-input.txt.template all-answers.txt</p>

Higher the F-score achieved through above scoring function. Higher is your system's accuracy.<br>
To run our system on a linux machine run the shell script infoextract.sh passing input file as an argument.<br>
This will create a virtual environment where all the required packages are downloaded and then the execution begins. <br>
** Truecaser file needs to be in the same directory.


