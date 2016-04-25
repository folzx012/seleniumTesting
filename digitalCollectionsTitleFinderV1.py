from selenium import webdriver
#from unidecode import unidecode

import time
import csv
import re

            
            
#d#ef remove_non_ascii(text):
    #return unidecode(unicode(text, encoding = "utf-8"))
    
    
#initailizes where the browser is run from and sets it up for use
path_toChromeDriver = '/Users/Folz/Desktop/chromedriver'
browser = webdriver.Chrome(executable_path = path_toChromeDriver)

#access the historical collections site
url = 'http://digitalcollections.pacific.edu/cdm/search/collection/muirletters'
browser.get(url)

#get the list of letters on the webpage
#myClickables = browser.find_elements_by_class_name('listContentTopBottomAlign')
time.sleep(10)
myImgs = browser.find_elements_by_class_name('body_link_11')

#variable to keep track of letter count
letterCount = 0

#initialize textFile for CSV format
tf = '/Users/Folz/Desktop/textfileTitle.csv'

#initialize logText file
logFile = '/Users/Folz/Desktop/log.txt'

#add title + text columns in csv
f2 = csv.writer(open(tf, 'w'), delimiter=',', quoting=csv.QUOTE_ALL)
firstRow = ['Date', 'Creator', 'Recipient']
f2.writerow(firstRow)


#loop through all letters on the website
for z in range(1, 68):
    imgCount = 0
    if z > 1:
        browser.find_element_by_id('pagination_button_next').click()
        time.sleep(10)
        while len(myImgs < 154):
            myImgs = browser.find_elements_by_class_name('body_link_11')
                
        #time.sleep(10)
    for item in myImgs:
        if imgCount < 55:
            imgCount += 1
        else:
            if imgCount > 154:
                imgCount += 1
            else:
                imgCount += 1
                #time.sleep(1)
                #variable resetting when accessing new letter
                #myImgs = ""
                myLetterTitle = ""
                myText = ""
                temp = ""
                tempText = []
                creator = ""
                recipient = ""
                #started = 0 #reset to 0 for initial run in myText loop for change in id
                #get Title text and use regular expression to filter out what we want
                while True:
                    try:
                        myLetterTitle = item.get_attribute('innerHTML')
                        break
                    except Exception:
                        pass
                    
                #myLetterTitle = remove_non_ascii(myLetterTitle)
                
                myLetterTitle = str(myLetterTitle)
                myLetterTitle.rstrip()
                myLetterTitle = re.sub('[ ]{2,}', '', myLetterTitle)
                
                #myLetterTitle = str(myLetterTitle)
                #print "original title text:  " + str(myLetterTitle)
                print "@Letter count= " + str((z-1)*100+(imgCount - 55))
                
                date = re.match('(,.+)$', str(myLetterTitle))
                date = re.sub('^(, )', '', str(date))
                #use reg expressions to access creator and recipient
                myLetterTitle = re.sub('(Letter from )', '', myLetterTitle)
                #myLetterTitle = re.sub('to', '\n', myLetterTitle)
                myLetterTitle = re.sub('(\,.+)$', '', myLetterTitle)
                
                
               
                #print myLetterTitle
                
                #firstRegex = re.compile('^(.+to)')
                #secRegex = re.compile('(to.+)$')
                
                creator = re.sub('(to.+)$', '', myLetterTitle)
                creator = re.sub('[ ]{2,}', '', creator)
                #firstRegex.match(myLetterTitle)
                #creator = re.sub(' to', ' ', str(creator))
                creator.rstrip()
                #print str(creator)
                
                recipient = re.sub('(.+to )', '', myLetterTitle)
                recipient = re.sub('[ ]{2,}', '', recipient)
                recipient.rstrip()
                #secRegex.match(myLetterTitle)
                #recipient = re.sub('to ', ' ', str(recipient))
                #print str(recipient)
                
                #creator = re.sub('to', '', str(creator))
                #recipient = re.sub('to', '', str(recipient))
                
                nextRow = [str(date), str(creator), str(recipient)]
                f2.writerow(nextRow)
            
        

        
