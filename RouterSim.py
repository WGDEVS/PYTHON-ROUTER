'''
Router Sim v1.0
Program description: This program simulates a network consisting of routers. 
It will be displayed in a command line interface and feature controls 
to build and maintain the network by modifying routers, save/load the 
network to external files, display information about the routers in
the network and, use pathfinding algorithms to find routes within the 
network.

Made by WGDEV, some rights reserved, see license.txt for more info
'''

Main = list() #the database of all routers, keeps track of links to other routers, looks like [[router #,[[other router #, bandwidth],...]]...]

'''
Description: Implements dijkstra's algorithim to find the best path to a target router from an inital router
Parameters:
	Router: The initial router's number
	Target: The target router's number
Returns:
	A string representation of the path to the target from the initial router or an error message
'''
def findPath(Router, Target):
    global Main
    q = [[0,Router,str(Router)]] #q is short for the queue, looks like [[delay,router #,path so far]...]
    mapy = [q[0]] #Keeps track of the best path to a router so far, sorted based on router #,uses the same format as que
    
    q.insert(0,[False,False])
    
    if not binSearch(0,Main,Router)[1]:
        return("Initial router not found!")
    
    while (q[0][1] != Target):
        q.pop(0)
        if len(q) <= 0:
            return("No path found!")
        
        ln = binSearch(1,mapy,q[0][1])
        if ln[1] and mapy[ln[0]][0] < q[0][0]:
            continue
        
        ln = binSearch(0,Main, q[0][1])
        for i in Main[ln[0]][1]:
            ln2 = binSearch(1,mapy,i[0])
            nc = q[0][0] + i[1]
            if not ln2[1]:
                mapy.insert(ln2[0],[nc,i[0],q[0][2]+"->" +str(i[0])])
            else:
                if mapy[ln2[0]][0] > nc:
                    mapy[ln2[0]][0] = nc
                else:
                    continue
            ln3 = binSearch(0,q,nc)
            if ln3[0] <= 0:
                ln3[0] = 1
            q.insert(ln3[0],[nc,i[0],q[0][2]+"->" +str(i[0])])  
    
    return("Delay is " + str(q[0][0]) + " with a path of " + q[0][2])

'''
Description: Implements a binary search algorithim to find the index of a list with an item at a specified index in a jagged list
Parameters:
	Index: The index of the value in each list in the jagged list to compare
	List: The jagged list
	Value: The value to find
Returns:
	A list with two items, the first is the index of the list with the value, the second is if the list is actually in the list
'''
def binSearch(Index,List,Value):
    if len(List) == 0:
        return [0,False]
    if len(List) == 1:
        if List[0][Index] == Value:
            return [0,True]
        elif List[0][Index] > Value:
            return [0,False]
        else:
            return [1,False]
    
    mini = 0
    maxi = len(List)-1
    while(maxi-mini>1):
        mid = (int)((mini+maxi)/2)
        if(List[mid][Index]== Value):
            return [mid,True]
        elif(List[mid][Index] > Value):
            maxi = mid
        else:
            mini = mid
    if (List[mini][Index] == Value):
        return [mini,True]
    elif (List[maxi][Index] == Value):
        return [maxi,True]
    elif (List[mini][Index] > Value):
        return [mini,False]       
    elif (List[maxi][Index] > Value):
        return [maxi,False]
    else:
        return [maxi+1,False]
    
        
'''
    Description: Prints all the availabe commands
    '''
def showOptions():    
    print("Command -> Effect:")
    print("save [filename] -> saves the network to the file")
    print("load [filename] -> loads the network from the file")
    print("tracert [router 1] [router 2] -> finds the path between two routers")
    
    print("link [router 1] [router 2] [delay] -> adds/updates a link between two routers")
    print("remove [router 1] [router 2] -> removes the link between two routers")
    print("delete [router] -> deletes the router")
    print("neighbour [router] -> lists all routers directly linked to the specified router")
    print("topology -> lists all routers in the network")
    
'''
      Description: Prints all the routers in the network
      '''    
def showRouters():
    print("Showing all routers in the network:")
    for i in Main:
        print("Router " + str(i[0]) + " has " + str(len(i[1])) + " link(s) to other routers")

'''
        Description: Prints all the routers that are directly linked to a router
        Parameters:
        Router1: The specified router's number
        '''
def showRoutes(Router1):
    ln = binSearch(0,Main,Router1)
    if (not ln[1]):
        print ("Router does not exist!")
        return
    print("Showing neighbour(s) for router "+str(Router1)+":")
    
    for i in Main[ln[0]][1]:
        print("Other router is " + str(i[0]) + " with a delay of " + str(i[1]) + ".")
    
        '''
          Description: Takes two routers, creates them if they do not exist and, links them or changes the cost if the link already exists
          Parameters:
          Router1: The first router's number
          Router2: The second router's number
          Cost: The new cost of the link
          Returns: An string represening the number of routers that were created by the function
          '''    
def addRoute(Router1,Router2,Cost):
    if Cost < 1:
        return "Delay must be at least 1!"
    if Router1 == Router2:
        return "Links cannot loop!"
    
    global Main
    outp = 0
    
    ln = binSearch(0,Main,Router1)
    if ln[1] == False:
        Main.insert(ln[0],[Router1,[]])
        outp +=1        
        
    ln2 = binSearch(0,Main[ln[0]][1],Router2)
    if ln2[1] == False:
        Main[ln[0]][1].insert(ln2[0],[Router2,Cost])
    else:
        Main[ln[0]][1][ln2[0]][1] = Cost
   
    ln = binSearch(0,Main,Router2)
    if ln[1] == False:
        Main.insert(ln[0],[Router2,[]])
        outp +=1        
        
    ln2 = binSearch(0,Main[ln[0]][1],Router1)
    if ln2[1] == False:
        Main[ln[0]][1].insert(ln2[0],[Router1,Cost])
    else:
        Main[ln[0]][1][ln2[0]][1] = Cost    
    
    return "Link sucessfully added, with " + str(outp) + " router(s) automatically installed."

'''
          Description: Takes two routers, deletes the link between them and, deletes them if they do not have any links left afterwards
          Parameters:
          Router1: The first router's number
          Router2: The second router's number
          Returns: An string represening the number of routers that were deleted by the function
          '''      
def removeRoute(Router1,Router2):    
    global Main    
    outp = 0
    
    ln1 = binSearch(0,Main,Router1)
    if (not (ln1[1])):
        return "One or more specified router(s) do not exist!"
    
    ln = binSearch(0,Main[ln1[0]][1],Router2)
    if (not ln[1]):
        return "The link does not exist!"
    
    Main[ln1[0]][1].pop(ln[0])
    if len(Main[ln1[0]][1]) <= 0:
        Main.pop(ln1[0])
        outp += 1
    
    ln1 = binSearch(0,Main,Router2)    
    if (not (ln1[1])):
        return "One or more specified router(s) do not exist!"    
    
    ln = binSearch(0,Main[ln1[0]][1],Router1)
    if (not ln[1]):
        return "The link does not exist!"
    
    Main[ln1[0]][1].pop(ln[0])
    if len(Main[ln1[0]][1]) <= 0:
        Main.pop(ln1[0])
        outp += 1    
    
    return "Link sucessfully deleted, with " + str(outp) + " router(s) automatically removed."

'''
          Description: Deletes a router and any links associated with the router, also automatically deletes any routers with no links
          Parameters:
          Router1: The specified router's number
          Returns: An string represening the number of routers that were deleted by the function
          '''      
def deleteRoute(Router1):
    global Main
    outp = 0
    ln = binSearch(0,Main,Router1)
    if (not ln[1]):
        return "Router does not exist!"
    
    while (len(Main[ln[0]][1]) > 0):
        ln1 = binSearch(0,Main,Main[ln[0]][1][0][0])
        ln2 = binSearch(0,Main[ln1[0]][1],Router1)
        Main[ln1[0]][1].pop(ln2[0])
        if len(Main[ln1[0]][1]) <= 0:
            Main.pop(ln1[0])
            if (ln1[0] < ln[0]):
                ln[0] -= 1
            outp += 1
        Main[ln[0]][1].pop(0)
    Main.pop(ln[0])
    return "Router sucessfully deleted, with " + str(outp) + " other router(s) automatically removed."
        
'''
          Description: Saves the network to a text document
          Parameters:
          Name: The text document's name
          Returns: An string represening if the network was successfully saved
          '''              
def save(Name):
    try:
        File = open(Name, "w")
        File.write(str(len(Main)))
        for i in Main:
            File.write(" " + str(i[0]) + " " + str(len(i[1])))
            for j in i[1]:
                File.write(" " + str(j[0]) + " " + str(j[1]))
        File.close()
        return "Network saved."
    except:
        return "Error saving network!"

'''
              Description: Loads the network from a text document
              Parameters:
              Name: The text document's name
              Returns: An string represening if the network was successfully loaded
              '''    
def load(Name):
    try:
        File = open(Name, "r")
        inp = File.read().split(" ")
        File.close()
        cur = 1
        global Main
        Main = list()
        while (cur<len(inp)):
            t1 = list()
            t1.append(int(inp[cur]))
            t1.append(list())
            cur += 1
            tSize = int(inp[cur])
            cur += 1
            for i in range(tSize):
                t1[1].append([int(inp[cur]),int(inp[cur+1])])
                cur += 2
            Main.append(t1)
        return "Network loaded."
    except:
        return "Error loading network!"
        
#The  actual program starts here
print("Welcome to RouterSim v1.0 made by WGDEV, some rights reserved see license.txt for more info, enter \"?\" for a list of commands.")
while (True):
    i = raw_input().lower().split(' ')
    if (i[0] == "?"):
        showOptions()
    elif (i[0] == "link"):
        print(addRoute(int(i[1]),int(i[2]),int(i[3])))
    elif (i[0] == "remove"):
        print(removeRoute(int(i[1]),int(i[2])))
    elif (i[0] == "delete"):
        print(deleteRoute(int(i[1])))
    elif (i[0] == "neighbour"):
        showRoutes(int(i[1]))
    elif (i[0] == "topology"):
        showRouters()
    elif (i[0] == "tracert"):
        print(findPath(int(i[1]),int(i[2])))
    elif(i[0] == "save"):
        print(save(i[1]))
    elif(i[0] == "load"):
        print(load(i[1]))
    else:
        print("Command invalid, enter \"?\" for a list of commands!")