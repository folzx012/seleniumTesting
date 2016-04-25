from selenium import webdriver
import time
import csv
import re

#add log.txt, letterCount input, maxRunTime input

#ask user for letterCount input:
#if left blank set max letter count to a very large number or set a flag
try: 
    maxLetterCount = input("please enter a maximum letter count: ")
    #if user enters a number set the flag
    maxLetterCountFlag = 1
    maxLetterCount = int(maxLetterCount)
except SyntaxError:
    maxLetterCountFlag = 0

#ask user for max Run Time
#if left blank set a flag to ignore time as a constraint
try:
    maxRunTime = input("please enter a maximum run time(seconds): ")
    #if user enters a number set the flag
    maxRunTimeFlag = 1
    maxRunTime = int(maxRunTime)
except SyntaxError:
    maxRunTimeFlag = 0
    
#initialize time variable
startTime = time.time()
myTimeSinceStart = 0

#initailizes where the browser is run from and sets it up for use
path_toChromeDriver = '/Users/Folz/Desktop/chromedriver'
browser = webdriver.Chrome(executable_path = path_toChromeDriver)

#access the historical collections site
url = 'http://digitalcollections.pacific.edu/cdm/search/collection/muirletters'
browser.get(url)

#get the list of letters on the webpage
myClickables = browser.find_elements_by_class_name('listContentTopBottomAlign')
myImgs = browser.find_elements_by_class_name('results_tn_img')

#variable to keep track of letter count
letterCount = 0

#initialize textFile for CSV format
tf = '/Users/Folz/Desktop/textfile.csv'

#initialize logText file
logFile = '/Users/Folz/Desktop/log.txt'

#add title + text columns in csv
f2 = csv.writer(open(tf, 'w'), delimiter=',', quoting=csv.QUOTE_ALL)
firstRow = ['Title', 'Text-pt1', 'Text-pt2']
f2.writerow(firstRow)

errorCount = 0
#loop through all letters on the website
for z in range(0,len(myImgs)):
    #variable resetting when accessing new letter
    myImgs = ""
    myLetterTitle = ""
    myText = ""
    temp = ""
    tempText = []
    started = 0 #reset to 0 for initial run in myText loop for change in id
    while True:
        try:
            myImgs = browser.find_elements_by_class_name('results_tn_img')
            break
        except Exception:
            pass

    temp = letterCount
    #pop off the elements we've already accessed in the list
    #have to do it this way to keep content fresh
    while (temp > 0):
        myImgs.pop(0)
        temp -= 1
    myImgs[0].click()
    
    #successfully gets title text
    while True:
        try:
            myLetterTitle = browser.find_element_by_id('metadata_object_title')
            break
        except Exception:
            pass

    #used for debugging how many letters we have accessed
    print "Letter Count = "+str(1+letterCount) 

    #get the list containing all the pages of the letter typically 6+ pages
    temp1 = ""
    while True:
        try:
            myText = browser.find_elements_by_class_name('co-thumb-item')
            break
        except Exception:
            nothingMatter=2  
  
    #variables for use within a single letter
    outputText = ""
    outputText2 = ""
    pageCount = 1;
    lastPageText = ""
    #for all pages in the letter, click on them and add the text to the output
    for x in myText:
        #click on each page image
        while True:
            try:
                #if we are on page 6 or greater we have to wait for page to load
                if pageCount > 5:
                    x.click()
                    time.sleep(5)
                    x.click()
                else:
                    x.click()
                break
            except Exception:
                pass

        time.sleep(6)
        while True:
            #variable used to test if text is not found on page in either of the following ID's
            doesTextExist = 0

            try:
                #find text element in either object_transc or without object in the ID
                tempText = browser.find_element_by_id('metadata_object_transc')
                break
            except Exception:
                doesTextExist = 1
                pass
            try:
                tempText = browser.find_element_by_id('metadata_transc')
                break
            except Exception:
                if (doesTextExist == 1):
                    break
                else:
                    pass
        
        #loop through finding the pages text until element is loaded and found
        while True:
            try:
                #get the innerHTML of the page corresponding to the letters text
                temp1 = tempText.get_attribute('innerHTML')
                #create new column if there are more than 3 pages of letter text
                if pageCount > 3:
                    outputText2 += str(temp1)
                else:
                    outputText += str(temp1)
                break
            except Exception:
                break
            
        #check integrity of our page copying
        if lastPageText == "":
            pass
        else:
            if lastPageText == str(temp1):
                #write to log.txt about the error
                f = open('logFile', 'a')
                stringToWrite = 'Failed to write Page Number:  ' + str(pageCount) + ' in letter:  ' + str(myLetterTitle.get_attribute('innerHTML')) + '\n'
                stringToWrite = re.sub('[ ]{2,}', '', stringToWrite)                
                f.write(stringToWrite)
                errorCount += 1
        #increment our current page number
        pageCount = pageCount + 1
        lastPageText = str(temp1)

    
    #used for debuging
    #print '\n'
    #convert innerHTML to text
    outputText = str(outputText)
    
    #strip out newlines and <br>
    outputText.rstrip()
    outputText = re.sub('<br>', '', outputText)
    outputText2.rstrip()
    outputText2 = re.sub('<br>', '', outputText2)

    #create a regular expression to parse out the extra spaces and the odd numbering in the text
    #remove wierd 5 digit numbers, then also remove any '  ' aka two+ contiguous spaces
    removeFiveDigitNumbers = re.compile('[0-9]{5}')
    outputText = re.sub(removeFiveDigitNumbers, '', outputText)
    outputText2 = re.sub(removeFiveDigitNumbers, '', outputText2)
    
    #remove extra whitespace
    removeWhiteSpace = re.compile('[ ]{2,}')
    outputText = re.sub(removeWhiteSpace, '', outputText)
    outputText2 = re.sub(removeWhiteSpace, '', outputText2)
    
    #remove whitespace in title
    myLetterTitle = re.sub(removeWhiteSpace, '', str(myLetterTitle.get_attribute('innerHTML')))

    #add text to csv file
    #requires two columns of text if there are more than 3 letter pages? maybe?
    rowToAdd = [str(myLetterTitle), str(outputText), str(outputText2)]
    
    #used for debugging
    #print outputText
    #print outputText2
    
    #send row to csv file
    f2.writerow(rowToAdd)

    #return to main collections page
    browser.get(url)    
    
    #increment how many imgs we have seen so far
    letterCount += 1
    
    #give up trying content after 20 letters or based on user input if it was given
    if maxLetterCountFlag == 1:
        if letterCount >= maxLetterCount:
            print "\nYOU HAVE OBTAINED ALL THE LETTERS YOU WANTED"
            print "DO WITH THEM AS YOU WILL"
            print "Number of Errors:  " + str(errorCount)
            quit()
            exit()
        else:
            pass
    else:
        if letterCount > 20:
            #end execution      
            quit()
            exit()

    #update totalTimeElapsed        
    myTimeSinceStart = time.time() - startTime
    
    #check if time flag is set then check the maxruntime
    if maxRunTimeFlag == 1:
        if myTimeSinceStart > maxRunTime:
            print "\nYOU HAVE SURPASSED THE MAX RUN TIME"
            print "IF THIS WAS AN ERROR: RETRY WITH A LARGER MAX RUN TIME"
            print "Number of Errors:  " + str(errorCount)
            exit()
        else:
            pass
    else:
        pass