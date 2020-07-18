import mechanize
from bs4 import BeautifulSoup
import csv
from random import randint
from time import sleep

OP_csv = r'D:\dcfile793.csv'

def SaveDataInCSV(mRow):    
    with open(OP_csv, 'a', newline='') as appendFile:
        writer = csv.writer(appendFile)
        writer.writerow(mRow)
    
    appendFile.close() 
    

# Browser
br = mechanize.Browser()

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#Main page url where all brance url are listed
pageURL = "https://www.stifel.com/branch"

#Save browser data in beautifulsoup
try:
    br.open(pageURL, timeout = 20) 
    soup = BeautifulSoup(br.response().read(), "lxml")
except:
    print("Error while opening main page url! Ending macro.")
    exit()

#Get all branc urls
try:
    branch_urls = soup.select(".branch-landing-locations-list li a")
except:
    print("No branch urls are found.")
    exit()


recordCount = 0
#Open each branch url one by one and extract branch details
for bURL in branch_urls:
    if recordCount >= 2:
        break
    recordCount = recordCount+1
    
    print("Running {0} URL...".format(recordCount))
    
    tmpBranchURL = "https://www.stifel.com"+bURL['href']
    
    try:
        br.open(tmpBranchURL, timeout = 20)    
        soup = BeautifulSoup(br.response().read(), "lxml")
    except:
        print("Unable to open: ", "https://www.stifel.com"+bURL['href'])
        continue
       
    
    #Get Branch Name
    try:
        branchName = soup.find("h1", class_="bold-headline").get_text()
    except:
        branchName = ""
    
    try:
        branchManager = soup.select(".branch-landing-info-border div span a")[0].get_text()
    except:
        branchManager = ""
    
    #Get contact numbers
    try:
        branchContact = [contactNo.text for contactNo in soup.select(".branch-landing-phone-desktop a")]
    except:
        branchContact=[]
    
    #Get Address
    try:
        branchAddress = soup.find("div", class_="branch-landing-address").get_text()
        branchAddress = ",".join(branchAddress.split("\n"))
        branchAddress = branchAddress.replace(',Get Directions,', '')
        branchAddress = branchAddress[1:]        
    except:
        branchAddress = ""
        
    try:
        advisorURL = soup.select("div.branch-landing-financial-advisors-columns div.branch-landing-financial-advisors-branchFA a")
    except:
        advisorURL = []
    
    
    #Open each advisorURL and extract its details
    for aURL in advisorURL:
        print("\tOpening advisor page...")
        tmpAdvisorURL = "https://www.stifel.com"+aURL['href']
        
        try:
            br.open(tmpAdvisorURL, timeout = 20)
            soup = BeautifulSoup(br.response().read(), "lxml")
        except:
            print("Error while opening advisor url!")
            continue        
        
        #Get Advisor name
        try:
            advisorName = soup.find("span", class_="fa-landing-name").get_text()
        except:
            advisorName = ""
                        
        #Advisor Title
        try:
            advisorTitle = soup.select(".fa-landing-name-wrapper div p")[0]
            
            #Remove advisor name tag
            toRemove = advisorTitle.find("span")
            _ = toRemove.extract()
            advisorTitle = advisorTitle.get_text(strip=True)
        except:
            advisorTitle = ""
        
        SaveDataInCSV([tmpBranchURL, branchName, branchManager, branchContact, branchAddress, tmpAdvisorURL, advisorName, advisorTitle])        
        
    waitTime = randint(1, 5)
    print("Waiting for:", waitTime)
    sleep(waitTime)