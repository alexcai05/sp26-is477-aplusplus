# Project Plan: College Characteristics and Graduate Earnings

## Overview
The goal of this project is to examine how various characteristics of colleges affect graduate outcomes, with a focus on exploring the relationship between tuition and post-graduation earnings. Attending college can get really expensive. As the costs of post-secondary education keep increasing, knowing whether a school with higher tuition has a good return on investment could be helpful when deciding where to study.

In order to achieve our goal, we will analyze datasets from the U.S. Department of Education's College Scorecard and the Integrated Postsecondary Education Data System (IPEDS). The most recent data is from 2024. We will first clean the datasets, handling any missing values and standardizing data formats for consistency. We will also filter the datasets, retaining a subset of attributes that are relevant. Then, we will perform data integration and ultimately produce one comprehensive dataset that we can conduct exploratory data analysis on. This project will also yield statistical summaries and visualizations that can help us determine whether certain college characteristics such as tuition and institution type lead to more favorable post-graduate outcomes. Throughout the research process, we will maintain proper documentation and organization to meet IS 477 standards for transparent, ethical, and reproducible data curation.

## Team
**Alex Cai**  
Role: Data sourcing, preprocessing, and integration  
Responsibilities:
+ Acquire datasets from the Department of Education's College Scorecard and the IPEDS
+ Assess and report on the quality of the data
+ Clean the datasets and prepare them for integration
+ Merge the datasets via the common identifier

**Vicky Wu**  
Role: Data analysis, visualization design, and reporting   
Responsibilities:
+ Conduct exploratory data analysis on the merged dataset
+ Build and train machine learning models to determine the correlations between selected institutional characteristics and graduate earnings
+ Develop high-quality data visualizations to see trends
+ Interpret and summarize results clearly

Both members of the team will prepare Github deliverables together for all milestones of the project and assist each other with responsibilities as needed.

## Research Questions
+ Do universities with higher tuition result in graduates with higher post-graduation earnings?
+ Do graduates from urban universities earn more than those from rural universities?
+ Do larger universities produce higher-earning graduates?
+ Do students at universities with higher tuition graduate with more student debt?
+ Do universities with higher tuition have higher graduation rates?

## Datasets 
### Dataset 1: College Scorecard (U.S. Department of Education)
The College Scorecard is a dataset published by the U.S. Department of Education that contains detailed information about higher education institutions in the United States. 6,430 colleges are represented in the 2024 dataset. The College Scorecard provides the raw data behind some of the tools they offer to students and parents in helping them make a more informed decision on which college is best for them. This dataset is important to this project as it contains the median earnings variable will be analyzed to see how it correlates with other factors described in the research questions. It also has other measures of graduate outcomes like graduation rate and student debt.

Link to dataset source: https://collegescorecard.ed.gov/data/ 

Variables from this dataset that are relevant to the research questions include:
+ UNITID: unique identification number of the institution
+ INSTNM: institution name
+ TUITIONFEE_IN: in-state tuition and fees
+ TUITIONFEE_OUT: out-of-state tuition and fees
+ MD_EARN_WNE_P10: median earnings of students working and not enrolled 10 years after entry
+ GRAD_DEBT_MDN: median debt for students who have completed
+ C150_4: graduation rate for first time, full-time students at four-year institutions
+ UGDS: total undergraduate enrollment

Access: API or CSV  
Usage rights: Public domain under 17 U.S. Code § 105 (U.S. government work)

### Dataset 2: Integrated Postsecondary Education Data System (IPEDS)
The IPEDS is a dataset published by the National Center for Educational Statistics that synthesizes results from surveys conducted annually to collect data from educational institutions. While the College Scorecard focuses more on student outcome and financial metrics, the IPEDS looks at the structure and characteristics of colleges. Non-financial factors like location and type of institution are just as important to analyze as financial factors like tuition as they can all play a role in students' experiences. The IPEDS complements the College Scorecard well as it brings in additional information about higher education institutions, filling in gaps and allowing us to tell the full story when the two datasets are merged together.

Link to the dataset source: https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx?gotoReportId=7&fromIpeds=true&sid=43f4dc72-0e6f-445c-8481-42e2cbb69a03&rtid=7  

Variables from this dataset that are relevant to the research questions include:
+ UNITID: unique identification number of the institution
+ INSTNM: institution name
+ CONTROL: institution type (public/private not-for-profit/private for-profit)
+ LOCALE: geographic status of a school on an urban continuum ranging from "large city" to "rural"

Access: CSV  
Usage rights: Public domain under 17 U.S. Code § 105 (U.S. government work)

Both the College Scorecard and IPEDS share the UNITID identifier, which will be used to perform data integration between the two datasets for analysis.

## Timeline
The approximate timeline for the rest of the semester is as follows.
+ [__March 28th - 29th__]: **Data Acquisition**, completion of acquiring the data with ethical and storage constraints in mind. Will be completed by Alex.
+ [__April 4th - 5th__]: **Data Analysis & Cleaning**, using Python/Pandas and SQL to integrate the datasets, we will conduct an initial data analysis, documenting the quality of the data and cleaning any missing data to make it ready for investigation. Will be completed by Vicky.
+ [__April 11th - 12th__]: **Data Investigation**, working with the data to solve our question while utilizing automated workflows to do so. Will be completed by Vicky.
+ [__April 18th - 19th__]: **Documentation**, preparing documentation for how we completed the project, ensuring reproducibility and adherence to FAIR principles. Will be completed by Alex.
+ [__April 25th - 26th__]: **Final Submission**, prepare to submit prior to deadline. Will be completed by both Alex & Vicky.

## Constraints
Some constraints that might be present in our approach is the potential incompleteness of data. Not every person who graduates from these universities will provide their post-graduate outcome to their university. This might result in survivorship bias being present in our data, as only those who wish to report where they ended up will be present. If the colleges automatically record these outcomes, then that might also be an ethical violation of their data if they did not receive consent.

## Gaps
Some gaps in our project plan as of right now include how recent the data is. Although the data is collected from 2024, as we continue moving forward, that data will become more and more outdated, especially with how revolutionary AI is turning out to be. What used to be a high ROI, may no longer result in something worthwhile if it is has since been invalidated or replaced by AI.
