# Interim Status Report: College Characteristics and Graduate Earnings
## Progress on the Tasks Described in the Project Plan
As of April 14, 2026, we have completed the initial stages of the project. Using our Project Plan and the project instructions document for guidance, we have been able to stay on track. We have successfully performed data acquisiton on the two datasets we chose to use for the project. Both the College Scorecard and IPEDS datasets are public domain under the U.S. government, so we had no issues complying with licenses and terms of use. Although the datasets could have been acquired via a simple CSV download, we wanted to diversify our acquisition methods to apply what we learned in IS 477 lectures. For the College Scorecard dataset, we fetched the data using an API request. In order to do this, we needed to get an API key. For the IPEDS dataset, we downloaded the CSV. We made sure to generate SHA-256 checksums for each of the datasets to ensure data integrity.

After we acquired the data, we conducted a data quality analysis and documented our observations. This helped us identify what to focus on during data cleaning. 

... add more stuff


## Updated Timeline
The approximate timeline for the project is as follows:
+ [__April 4th - 5th__]: **Data Acquisition**, completion of acquiring the data with ethical and storage constraints in mind. Will be completed by Vicky. ✔️
+ [__April 11th - 12th__]: **Data Analysis & Cleaning**, using Python/Pandas and SQL to integrate the datasets, we will conduct an initial data analysis, documenting the quality of the data and cleaning any missing data to make it ready for investigation. Will be completed by Alex. ✔️
+ [__April 18th - 26th__]: **Data Investigation**, working with the data to solve our question while utilizing automated workflows to do so. Will be completed by Vicky.
+ [__April 28th - 30th__]: **Documentation**, preparing documentation for how we completed the project, ensuring reproducibility and adherence to FAIR principles. Will be completed by Alex.
+ [__May 1st - 2nd__]: **Final Submission**, prepare to submit prior to deadline. Will be completed by both Alex & Vicky.
## Changes Made to the Project Plan
One change we made to the Project Plan was within the timeline. We underestimated how long it would take us to complete each task, so we've adjusted the timeline to better reflect how long we'll spend on each. Another change we made was shifting some of the responsibilities and tasks assigned to each team member. Vicky expressed interest in taking over the data acquisiton part of the project while Alex wanted to do more of the data analysis, so we reassigned the roles slightly. 

... add any other changes
## Challenges or Problems Encountered
One challenge that we've ran into so far is related to storage. When we initially acquired the data, we realized that the file sizes for both the College Scorecard and IPEDS datasets were very large. Together, they took up 1.55 GB. This exceeds the Github file size limit of 50 MB and also resulted in low storage warnings on our laptops. We viewed the CSV files to find the root of the problem and noticed that it was due to an excessive number of columns, many of which we did not even need to answer our research questions. To address the storage challenge, we decided the best course of action would be to revise the data acquisition script so that we extract only the columns relevant to our project from the College Scorecard and IPEDS datasets. The fix made a substantial difference. It solved the problem as the file sizes went from a combined 1.55 GB down to 698 KB.

... add any other challenges
## Team Members Contribution Summary
Vicky Wu: I acquired the data for this project. First, I familiarized myself with the characterstics and naming conventions of the College Scorecard and IPEDS datasets using the documentation available on the respective source websites. Then, I wrote a Python script on Visual Studio Code for data acquisition, making sure I included the calculation of checksums for data integrity and labeling the steps with comments. I resolved the issue we encountered with storage by modifying the code to extract only certain columns. The `acquire_data.py` script can be found in the folder `scripts`. The script was able to successfully create the raw data files `ipeds_hd2024.csv` and `scorecard_raw.csv`. I pushed these changes to Github, and the files are available under `data/raw`.

Alex Cai:
