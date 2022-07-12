import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

starterjsonfile = 'holidays.json'
newfilelocation = 'exportholidays.json'

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday: 
    name: str
    date: datetime  
    def __str__ (self):
        # String output
        # Holiday output when printed.    
        return f"{self.name} ({self.date:%Y-%m-%d})"
          
   
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
@dataclass
class HolidayList:
    innerHolidays = []

    def findHoliday(self, HolidayName, date):
        # Find Holiday in innerHolidays
        for i in self.innerHolidays:
            # Return Holiday
            if HolidayName == i.name and date == i.date: return i
        return False

    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        if type(holidayObj) is not Holiday:
            print(f"The object is not a holiday")
            return False

        else: # double check and if it is an object add it
            listedholiday = self.findHoliday(holidayObj.name, holidayObj.date)
            if listedholiday == False:
                # Use innerHolidays.append(holidayObj) to add holiday
                self.innerHolidays.append(holidayObj)
                print(f"Success:\n{holidayObj.name} on ({holidayObj.date:%Y-%m-%d} has been added to the holiday list.")
                # print to the user that you added a holiday
            else:
                print(f"Error:\n{holidayObj.name} on ({holidayObj.date:%Y-%m-%d} is already in the holiday list.")

    def removeHoliday(self, HolidayName, date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        holidaysearch = self.findHoliday(HolidayName, date)
        # innerholidays is the pair samantha; just copy and paste from find
        if holidaysearch != False:
            for i in self.innerHolidays:
                if HolidayName == i.name and date == i.date:
                    # inform user you deleted the holiday                
                    print(f"Success:\n{HolidayName} on ({date:%Y-%m-%d} has been deleted to the holiday list.")
                    # remove the Holiday from innerHolidays
                self.innerHolidays.remove(i)
                return True
        else:
            print(f"Error:\n{HolidayName} on ({date:%Y-%m-%d} is not in the holiday list.")

    def read_json(self, filelocation):
        # Read in things from json file location
        with open(filelocation, "r") as file:
            data = json.load(file)
            # Use addHoliday function to add holidays to inner list.
            for i in data["holidays"]:
                format = "%Y-%m-%d"
                date = datetime.datetime.strptime(i["date"], format)
                if self.findHoliday(i["name"], date) != False:
                    newHoliday = Holiday(i["name"], date)
                    self.innerHolidays.append(newHoliday)

    def save_to_json(self, filelocation):
            # Write out json file to selected file. frmat as list of dictionaries
            with open(filelocation, "w") as file:
                dictTemp = {}
                temp = []
                for i in self.innerHolidays:
                    hoilday = {"name":i.name, "date":i.date.strftime("%Y-%m-%d")}
                    temp.append(hoilday)
                dictTemp['holidays'] = temp
                formatJSON = json.dumps(dictTemp, indent = 1)
                file.write(formatJSON)

    def scrapeHolidays(self):
    # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
    # Remember, 2 previous years, current year, and 2  years into the future. 
    # You can scrape multiple years by adding year to the timeanddate URL. 
    # For example https://www.timeanddate.com/holidays/us/2022
            for i in range (2020,2025):
                    url = "https://www.timeanddate.com/holidays/us/{}?hol=33554809" # gets the response from the site and returns as text
                    url = url.format(i)
                    response = requests.get(url)
                    html = response.text
                    soup = BeautifulSoup(html,'html.parser') #parse
                    # print(soup.prettify())
                    table = soup.find('table', attrs = {'id':'holidays-table'}) # hoilday data is in the table"table". store it in variable
                    #innerHolidays = [] # storage for country dictionaries
                    for row in table.find_all_next('tr', class_ = "showrow"):
                            cells = row.find_all_next('td')
                            mmdd = row.find('th', class_ = "nw").text #in %b-%d format string need to convert to %Y-%m-%d
                            yyyy = f"{i} {mmdd}"
                            # final for append
                            date = datetime.datetime.strptime(yyyy, "%Y %b %d")        
                            name = cells[1].text
                            # Check to see if name and date of holiday is in innerHolidays array
                            # Add non-duplicates to innerHolidays
                            # Handle any exceptions. 
                            holidaysearch = self.findHoliday(name, date)
                            if holidaysearch == False:
                                    newHoliday = Holiday(name, date)
                                    self.innerHolidays.append(newHoliday)     

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)

    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        weekfilter = list(filter(lambda x: x.date.isocalendar()[0] == year and x.date.isocalendar()[1] == week_number, self.innerHolidays))
        return weekfilter

    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        # THIS DOES NOT MAKE SENSE TO ME
        for i in holidayList:
            print(i)

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        today = datetime.date.today()
        year = today.year
        week = today.isocalendar()[1]
        # Use your filter_holidays_by_week function to get the list of holidays
        byweek = self.filter_holidays_by_week(year, week)
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        print(f"These are the holidays for week {week}")
        self.displayHolidaysInWeek(byweek)
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

# ==============================
# User Interface
# ==============================
def AddHoliday(hlist):
    
    print('Add a Holiday')
    print('===========================')

    name_input = (input(f"Enter holiday name:"))
    date_input = str(input(f"Enter holiday date as YYYY-MM-DD:"))

    while True:
        try:
            date_input = datetime.datetime.strptime(date_input, '%Y-%m-%d')
            break
        except ValueError:
            print(f"Error:\nInvalid date. Try again.")
            date_input = str(input(f"Enter {name_input} date as YYYY-MM-DD:"))

    newholiday = Holiday(name_input, date_input)
    hlist.addHoliday = hlist.addHoliday(newholiday)
    print(f"Success:\n{newholiday} on {date_input} has been added to the holiday list.")
    savestatus = False
    return hlist, savestatus

# convert date
def convertdate(correctdate, date):
    try:
        datedatetime = datetime.datetime.strptime(date, '%Y-%m-%d')
        correctdate = True
        return datedatetime
    except:
        print(f"Error:\nInvalid date. Try again.")
        return datedatetime

def RemoveHoliday(hlist):

    print('Remove a Holiday')
    print('===========================')

    removal = False
    while removal == False:
        r_name = (input(str(f"Enter holiday name to delete:")))
        r_date = (input(str(f"Enter holiday date to delete as YYYY-MM-DD:")))
        c_date = convertdate(False, r_date)
        while c_date == False:
            yesdate = (input(str(f"Enter date for {r_name}:")))
            c_date = convertdate(c_date, yesdate)
        removal = hlist.removeHoliday(r_name, c_date)
    return removal

def SaveHoliday(madechange, hlist):
    
    print('Saving Holiday List')
    print('===========================')
    if madechange:
        while True:
            save = str(input("Are you sure you want to save your changes? [y/n] ")).lower
            if save == "y":
                hlist.save_to_json(newfilelocation)      
                print(f"\nSuccess:\nYour changes have been saved.")
                break
            elif save == "n":
                print(f"\nCancelled:\nHoliday list file save canceled.")
                break
            else:
                print("Invalid input.")


def ViewHoliday(hlist):

    print('View Holidays')
    print('===========================')
    global currentYear
    currentYear = datetime.date.today().year

    while True:
        year_input = int(input(f"Which year?:"))
        if year_input in range(currentYear-2, currentYear+3): break
        else:
            print(f"Enter a year between {currentYear-2} and {currentYear+3}")

    while True:
        week_input = str(input(f"Which week? [1-52, Leave blank for the current week]:"))
        if week_input == "": break
        elif int(week_input) in range(1,53): break
        else:
            print(f"This is not a possible calender week in a year or in the wrong format.")
            print(f"Enter a week number between 1 and 52, or leave blank for current week.")

    if week_input == "":
        hlist.viewCurrentWeek()
    else:
        print(f"These are the holidays for {year_input} week {week_input}:")
        display = hlist.filter_holidays_by_week(year_input, int(week_input))
        hlist.displayHolidaysInWeek(display)

def Exit(savestatus):
    print("Exit")
    print("===================")

    while True:
        if savestatus:
            exit = str(input("Are you sure you want to exit? [y/n] "))
        else:
            exit = str(input("Are you sure you want to exit?\nAny unsaved changes will be lost. [y/n] "))
        
        if exit == "y" or exit == "n":
            break
        else:
            print("Invalid input. Please input [y/n] ")

    if exit == "y":
        print(f"Goodbye.")
        return True


def main():
# Large Pseudo Code steps
# -------------------------------------
# 1. Initialize HolidayList Object
    holidayList = HolidayList()

# 2. Load JSON file via HolidayList read_json function
    holidayList.read_json(starterjsonfile)

# 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    holidayList.scrapeHolidays()
# 3. Create while loop for user to keep adding or working with the Calender
# 4. Display User Menu (Print the menu)
    print("Holiday Management")
    print("===================\n")
    print(f"There are currently {holidayList.numHolidays()} holidays stored in the system.")
    madechange = True

# 5. Take user input for their action based on Menu and check the user input for errors
# 6. Run appropriate method from the HolidayList object depending on what the user input is
    print('Holiday Menu')
    print('===========================')
    print(f"1. Add a Holiday\n2. Remove a Holiday\n3. Save Holiday List\n4. View Holidays\n5. Exit")

    menu_choice = int(input(f"Enter number of menu you'd like to go to: "))
    if menu_choice == 1:
        madechange = AddHoliday(holidayList)

    elif menu_choice == 2:
        RemoveHoliday(holidayList)

    elif menu_choice == 3:
        madechange = False        
        SaveHoliday(madechange, holidayList)

    elif menu_choice == 4:
        ViewHoliday(holidayList)

    elif menu_choice ==5:
        exit(madechange)

    else:
        print(f"Enter a number that corresponds to the menu item.")

# 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


if __name__ == "__main__":
    main()