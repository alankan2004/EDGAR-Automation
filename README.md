# EDGAR-Automation
Python Web Scraping program that parses fund holdings pulled from EDGAR.


## Usage

## Prerequisites

* Python 3


## What the program does...
This Python program that parses fund holdings pulled from EDGAR, given...
* A CIK number
* A value of which most recent document to go over.

And then it will take those two inputs, find the information table, and write it to a .tsv file.

### Feature
I also added a function for auto install modules, just to make life slightly easier for users.

And being able to access previous reports too.

## Fetching previous reports...
So in the email, it was mentioned that to consider how to get the previous reports.

TO-DO talk more aobut the brute force solution
My solution to that is to ask for an extra input value, i-th, if i = 1 that means the first most recent report, i = 2 means the second most recent report, and so on.

And my tsv file name will label the date, so user knows which version the report is.

My solution currently does have a fault though, I can get the previous records but only up to the ones on the same page, so 40 reports, I haven't implement the functionality to get the next 40, but I believe I can easily implement it by using selenium to click to the next page until the next page no longer exists.

## Dealing with different formats...

## What can be improved...

* The format of the tsv file.
So unfortunately, the text format in the tsv file is tab-spaced, but the entries don't line up with the column names, so they look messy. I tried looking for ways to make them line up, but I couldn't find one.

Another problem with the format is the column names, so some columns have sub-columns, for example voting authority has sole, shared and None. So that makes it really confusing to read and to match entries, I thought about writing those sub-columns to the second row under the main columns, then I remember I don't know how to line them up, so that will probably make things worse.

So I just end up grouping those columns together, so if a column has sub-columns, I put them in a tuple, but the user will have to know the entries are suppose to be under the sub-columns not the main column, if a column has sub-columns.

* More try & excepts for catching errors.
* Maybe also save the tsv file in Excel for better reading.
* Asks for extra input for the filling type, then no longer limits to 13F files.
* Perhaps a user interface for the program.

## Challenges
* The current challenge is the readability of the output file.
* Previous challenge would probably be trying to remember what I deleted the night before, when I was super tired, that's causing everything to not work anymore.
      * After that I uploaded the project to Github like a normal human being.

## What I learned and Used

## Conclusion
