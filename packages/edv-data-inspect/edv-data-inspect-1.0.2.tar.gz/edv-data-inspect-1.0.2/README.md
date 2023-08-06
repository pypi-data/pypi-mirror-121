# EDV Data Inspect
A Python Package to analyze the edv data in terms of total edv applicants, the derivatives(family members) and gives only the intended data in the scrap.txt file after running this package.
For now, we have this package able to calculate those data for only KDU embassy and AS region. It helps only to those Nepalese who have won EDV and want to investigate about previous year edv data. 

# Usage
On this https://dvcharts.xarthisius.xyz/ceacFY21.html there is whole lots of data provided for each year edv lottery. The data they provided for year 2020 2021 and so on opens in excel software where we can do analyze.
But if you want to do same for year 2019, 2018, and other previous year, those data doesn't open in excel but they redirect to webpage with that data. So, we can't analyze the exact number that we want to figure out from the data.

Following query will provide you the actual data for total edv winners, total derivatives(family members) for year 2018 and 2019

'''
edv-data-inspect 
'''
Before running the above query do the following:
1. Go to https://dvcharts.xarthisius.xyz/ceacFY21.html here.
2. In the left side of this webpage, there is a sidebar with [ DV-(year) CEAC Data ] format.
3. Click on either [ DV-2018 CEAC Data ] or [ DV-2019 CEAC Data ].
4. On click, The central content changes and new information are shown in the page.
5. There are .csv file with Heading [ DV(year) Raw CEAC Data ]
6. Click on any .csv file there.
7. It opens the whole plethora of data, containing in that .csv file
8. Now, use command ctl+A and ctl+C respectively
9. Now goto your terminal or command line, and type: edv-data-inspect 
10. Your terminal shows the output from the data and scrap.txt file in saved in the current directory with regexed data.