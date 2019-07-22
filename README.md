# EDGAR-Automation
Python Web Scraping program that parses fund holdings pulled from EDGAR.


## Requirements and Installation
In order to run these files, your will need...
* Python >= 3
* install selenium==3.141.0
* install bs4==4.7.1
* install urllib3==1.23
* Webdriver from selenium website (must be in the same folder as the program.)

#### Note: I have an install function that auto install all the modules.


## What the program does...
This Python program that parses fund holdings pulled from EDGAR, given...
* A CIK number
* A value of which most recent document to go over.

And then it will take those two inputs, find the information table, and write it to a .tsv file.

## Usage
Run the main.py Python file to use it.

In terminal or command prompt...

```
python3 main.py
```

### Feature TODO
* Auto install modules.
* Ability to review previous reports. (Well, only up to previous 40 reports right now, explained more below.)

## Fetching previous reports...
So in the email, it was mentioned that to consider how to get the previous reports.

My solution to that is to ask for an extra input value, i-th, if i = 1 that means the first most recent report, i = 2 means the second most recent report, and so on.

And my tsv file name will label the date, so user knows which version the report is.

My solution currently does have a fault though, I can get the previous records but only up to the ones on the same page, so 40 reports, I haven't implement the functionality to get the next 40, but I believe I can easily implement it by using selenium to click to the next page until the next page no longer exists.

## Dealing with different formats...
I noticed for some tickers would have the other manger column completely empty and some tickers would have that column partially filled.

If a row has an empty value for the other manger column, it won't show the other manger tag in the xml file, so to make sure I don't miss out this column for the tsv file, I went over every single infoTable in xml, and save the one that includes all the columns.

Initially this is what I did...

colNames = []
maxLen = -1
for i in range(numOfComp):
       temp = []
       for child in root[i]:
           temp.append(child.tag.replace('{http://www.sec.gov/edgar/document/thirteenf/informationtable}', ''))
           for gChild in child:
               temp.append(gChild.tag.replace('{http://www.sec.gov/edgar/document/thirteenf/informationtable}', ''))
       if len(temp) > maxLen:
           maxLs = temp
           maxLen = len(temp)

for col in maxLs:
       colNames.append(col)

But this looks kinda gross, and a lot of repeating work, like most of the time temp is the same list, so I'm repeating the appending process, forming the same list, then check does it include every column, if not I toss it away, and might end up checking exact list again for the next loop. And that bothers me, so I changed it a bit.

So I ended up using dictionary, that way I don't keep appending the same list, and just forming the dictionary, but it still uses nested for loops.


## What can be improved...

* The format of the tsv file.
So unfortunately, the text format in the tsv file is tab-spaced, but the entries don't line up with the column names, so they look messy. I tried looking for ways to make them line up, but I couldn't find one.

Another problem with the format is the column names, so some columns have sub-columns, for example voting authority has sole, shared and None. So that makes it really confusing to read and to match entries, I thought about writing those sub-columns to the second row under the main columns, then I remember I don't know how to line them up, so that will probably make things worse.

So I just end up grouping those columns together, so if a column has sub-columns, I put them in a tuple, but the user will have to know the entries are suppose to be under the sub-columns not the main column, if a column has sub-columns.

* More try & excepts for catching errors.
* Optimize the code.
* Maybe also save the tsv file in Excel for better reading.
* Asks for extra input for the filling type, then no longer limits to 13F files.
* Perhaps a user interface for the program (like doing GUI in Python).


## What I learned
* BeautifulSoup4
* urllib.request
