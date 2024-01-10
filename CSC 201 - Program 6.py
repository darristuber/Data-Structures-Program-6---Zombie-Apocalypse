#PROGRAM 6
#Darri Stuber
#Data Structures and Algorithm Analysis
#Dr. Lori Jacques

#binary search function
def binarySearch(arr, what):
    curr = 0
    last = len(arr) - 1
    while curr <= last:
        mid = (last + curr) // 2
        if arr[mid] == what:
            return mid
        elif arr[mid] < what:                                                                                                         
            curr = mid + 1
        else:
            last = mid - 1
    
    return -1

gr = [] #empty list where graph adjacency list/table is created

file = open("DataSet1.txt")
allNames = [] #empty list to store all names
for line in file: #for line in the read in file
    line = line.strip('') #remove extra characters
    splitline = line.split(',') #split line into a list based on commas (read as csv)
    allNames.append(splitline[0]) #add fist name to allNames list
    contacts = [] #empty list to store just the names that everyone had contact with
    for w in range(1,len(splitline)): #for every word in each row
        word =splitline[w].replace("\n","") # get rid of weird formatting
        if binarySearch(contacts, word) == -1: #if the word is not in contacts add to contacts
            contacts.append(word) 
            contacts.sort()
        if binarySearch(allNames, word) == -1: # add to a list with all the names for simplicity later on
            allNames.append(word)
            allNames.sort()
    gr.append([splitline[0], contacts]) #add the new information to the gr graph
    
    #Above I am creating a graph. I am choosing a graph because the each person in the data has multiple connections to one another. It does not make sense to use
    #linked list because there are multiple connections not in linear order. Also, since we are not searching a binary tree would not be useful. Since the data (names) do not
    #have any other information I used a normal list in the adjacency list rather than a linked list with object nodes. This allows me to easily access
    #each name in the file and all names they had contact with. 
    

#function to get all contacts of a given name
def getContacts(name):
    for row in gr:
        if row[0] == name:
            return row[1]
    
allNames = list(set(allNames)) #I am getting duplicates and dont know why looked up this code to remove them https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/
#I needed a list to store all names to be able to go through people who are also potential zombies
        
#PART ONE: Who did each sick person have contact with?
print('Contact records: ')
for line in gr: #using the graph
    print('\t'+'{} had contact with {}'.format(line[0],', '.join(line[1]))) #looked up join on chat GPT


#PART TWO: Who are the patient zeros?
zeroes = [] #empty list to hold zero names

for name in allNames: #for each person
    found = False
    for line in gr: #for each vertex in graph check if the name is one of their contacts
        if binarySearch(line[1], name) != -1: #if name is in that contact list
            found = True
            break
    if found == False:
        zeroes.append(name)
        zeroes.sort()
        
print('Patient zeros: {}'.format(', '.join(zeroes)))


#PART THREE:  Who are potential zombies?
potential = []
for name in allNames: #for each person
    found = False
    for line in gr: #for vertex in graph
        if name == line[0]: #if name is in that contact list
            found = True
            break
    if found == False:
        potential.append(name)
        potential.sort()

print('Potential zombies: {}'.format(', '.join(potential)))

            
def findPotential(name, contacts, count = 0):
    if binarySearch(potential, name) != -1:
        return count
    if contacts == None: #we reached a potential zombie? 
        return count+1
    count += 1
    maxCount = 0
    for contact in contacts:
        count_indiv = findPotential(contact, getContacts(contact), count)
        if count_indiv > maxCount:
            maxCount = count_indiv
    return maxCount          
            

#PART FOUR: Who are neither patient zeros nor potential zombies?
    #since we already have a list of all names and the names we do not want to include this section just uses those to create a new list
neither = []
for name in allNames:
    found = False
    if binarySearch(potential, name) != -1:
        found = True
    if binarySearch(zeroes, name) != -1:
        found = True
    if found == False:
        if binarySearch(neither, name) == -1:
            neither.append(name)
            neither.sort()
        
print('Neither patient zero nor potential zombies: {}'.format(', '.join(neither)))

#PART FIVE: Who are the most viral people?
#used https://blog.finxter.com/python-find-longest-list-in-list
maxInfo = max(gr, key = lambda x:len(x[1])) #get the max edges from vertices from graph
max_len = len(maxInfo[1])
mostViral = [] #use a list because it is simple just to be able
for row in gr:
    if len(row[1]) == max_len:
        mostViral.append(row[0])
print('Most viral people: {}'.format(', '.join(mostViral)))       

#PART SIX: Who are the most contacted people?
contacted_nums = [] #use a list because it is simple to store names after going through graph
for name in allNames: #for each person
    count = 0
    for line in gr: #for vertex in graph
        if binarySearch(line[1], name) != -1: #if name is in that contact list
            count +=1
    newRow = [name, count]
    contacted_nums.append(newRow)

maxInfo2 = max(contacted_nums, key = lambda x: x[1]) #chat gpt for how to change key
maxNum = maxInfo2[1]
mostContacted = []
for row in contacted_nums:
    if row[1] == maxNum:
        mostContacted.append(row[0])
mostContacted.sort()
print('Most contacted people: {}'.format(', '.join(mostContacted)))

#PART SEVEN: What is each person's maximum distance from a potential zombie?
distances = [] #create a new graph with a list so that we can store a name and subsequent number of connections efficently, do not need link list because we are only storing names (not a name object)
for name in allNames:
    count = findPotential(name, getContacts(name))
    NewRow = [name, count]
    distances.append(NewRow)
    
    
distances = sorted(distances, key=lambda x:(-x[1], x[0])) #chat gpt like max code above chat gpt but how to sort based on two columns
print('Maximum distance from a potential zombie:')
for row in distances:
    print('\t'+'{}: {}'.format(row[0], row[1]))

#EXTRA CREDIT:  identify the following additional categories:
        #Spreader zombies: a spreader zombie is a sick person that has only had contact with potential zombies (i.e., people who haven't yet been determined to be sick – and aren't the initial name in a line of input).
        #Regular zombies: a regular zombie is a sick person that has had contact with both potential zombies and people who are already sick.
        #Zombie predators: a zombie predator is a person that has only had contact with people who are sick (i.e., people who have been determined to be sick – and appear as the initial name in a line of input).

#using lists because it is quick to store information and we only need to store names (not connections or other features)
spreader = [] #spreader zombies = sick person that has only had contact with potential zombies
predator = [] #zombie predators = xombie predator that only had contact with people who are sick 
regular = [] #regular zombies = sick person that has had contact with 

for line in gr:
    pc = 0 #number of potential zombie contacts
    sc = 0 #number of sick zombie contacts
    for contact in line[1]: #for each contact in specified line
        if binarySearch(potential, contact) != -1:
            pc += 1
        else:
            sc += 1
    if pc == 0:
        predator.append(line[0])
    elif sc == 0:
        spreader.append(line[0])
    else:
        regular.append(line[0])
        
print('For extra credit:')
print('\t'+'Spreader zombies: {}'.format(', '.join(spreader)))
print('\t'+'Regular zombies: {}'.format(', '.join(regular)))
print('\t'+'Zombie predators: {}'.format(', '.join(predator)))

            
            
            
        



   