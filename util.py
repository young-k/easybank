
f = open("./data/data.csv", "r+")

lines = []
import numpy
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from itertools import groupby

for line in f:
    lines.append(line.strip().split(","))
    
"""
parses into separate lists 
"""
descriptions= [line[0] for line in lines if line[0] != ""]
withdrawals = [float(line[1]) for line in lines if line[1] != ""]
dates=[line[2] for line in lines if line[2] != ""]
cities= [line[3] for line in lines if line[3] != ""]
states= [line[4] for line in lines if line[4] != ""]
location=[]

for x in range(0, len(cities)):
    location.append(cities[x]+states[x])
    
transaction= []

def createTransaction(descriptions):
    counter =0
    for desc in descriptions:
        transaction.append(desc +"+" + str(withdrawals[counter])+"+" +dates[counter] +"+" + location[counter])
        counter+=1

createTransaction(descriptions)

homeLoc = "Kearny NJ"
geolocator= Nominatim()
myloc =  geolocator.geocode(homeLoc)
myHome= (myloc.latitude, myloc.longitude)

def median(lst):
    return numpy.median(numpy.array(lst))

def mean(lst):
    return numpy.mean(numpy.array(lst))
    
def std(lst):
    return numpy.mean(numpy.array(lst))
"""
different lists
"""
statStrange=[]
locStrange=[]
categoryStrange=[]
locList=[]
uniqueLocation=[]
categoryStrange=[]
"""
finds quantatitive oddities in withdrawals
"""
def withdrawal_strange(lst):
    for trans in lst:
        desc, withd, dates, loc= trans.split("+")
        if (-1*float(withd)+median(withdrawals) > abs(std(withdrawals))):
            statStrange.append(trans)
"""
find location oddities
"""
def distanceList(lst):
    for loc in lst:
        geolocator= Nominatim()
        transLoc= geolocator.geocode(loc)
        coord=(transLoc.latitude, transLoc.longitude)
        locList.append(vincenty(coord, myHome).miles)


def loc_strange(lst):
    distanceList(location)
    for trans in lst:
        desc, withd, dates,loc= trans.split("+")
        geolocator= Nominatim()
        transLoc= geolocator.geocode(loc)
        coord=(transLoc.latitude, transLoc.longitude)
        distance= vincenty(coord, myHome).miles
        if (abs(distance - median(locList) > std(locList))):
            locStrange.append(trans)


"""
Finds strange locations based on frequency of transaction
"""
def frequency(lst):
    uniqueLocations= set(location)
    for loc in uniqueLocations:
        if (location.count(loc)==1):
            for trans in lst:
                desc, withd, dates,loc2= trans.split("+")
                if loc==loc2:
                    uniqueLocation.append(trans)

"""
Finds strange categories based on profile
"""
def categories(lst):
    transportation=["Plane", "Air","Car","Train","Subway","Airpot","Airlines","Station","Cruise","Boat","Ship"]
    for trans in lst:
        desc, withd, dates,loc2=trans.split("+")
        splitDesc= desc.split(" ")
        for buzzword in transportation:
            if buzzword in splitDesc:
                categoryStrange.append(trans)

        
transactionDictionary=[]
"""
All the algo calls and consolidation
"""
uniqueTransactions=[]
def consolidate(lst):
    transactionDictionary= []
    withdrawal_strange(lst)
    loc_strange(lst)
    frequency(lst)
    categories(lst)
    consolidatedList= statStrange+locStrange+categoryStrange+uniqueLocation+categoryStrange
    uniqueTransactions= list(set(consolidatedList))
    for trans in uniqueTransactions:
            desc, withd, dates,loc=trans.split("+")
            dict={'description': desc, 'withdrawal': withd, 'date': dates, 'location':loc}
            transactionDictionary.append(dict)
    return transactionDictionary

def account(name):
    if name=="Don":
        dict1={'name': '360 CHECKING', 'balance': 300.86, 'account_number': 4512}
        dict2={'name': '360 SAVINGS', 'balance': 3124.86, 'account_number': 8512}
        return [dict1, dict2]
    if name=="Agnes":
        dict1={'name': 'CHECKING', 'balance': 3892.86, 'account_number': 4982}
        dict2={'name': 'SAVINGS', 'balance': 890.86, 'account_number': 1212}
        return [dict1,dict2]

def transactionHistory(name):
    transactionDict=[]
    if name=="Don" or name=="Agnes":
        for trans in transaction:
            desc, withd,dates,loc=trans.split("+")
            dict={'description': desc, 'withdrawal': withd,'date': dates, 'location':loc}
            transactionDict.append(dict)
        return transactionDict

def weirdTransaction(name):
    if name=="Don" or name=="Agnes":
        return consolidate(transaction)

if __name__ == "__main__":
    print weirdTransaction("Don")