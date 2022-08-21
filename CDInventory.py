#------------------------------------------#
# Title: Assignment7_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
#------------------------------------------#

import pickle # function used to save/load binary data to files

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def load_inventory():
        """loading the inventory from your already preset text file"""
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
    
    @staticmethod
    def add_CD(newCD):
        """adds your newCD arguments by way of get_CD function to the list table"""
        lstTbl.append(newCD)
        IO.show_inventory(lstTbl)
        
    @staticmethod
    def del_CD(intIDDel):
        """deletes the specified CD by ID"""
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
    
    @staticmethod
    def save_CD(file_name, table):
        """saves CD data to default CDInventory.txt file name"""
        with open(strFileName, 'wb') as fileObj:
            pickle.dump(table, fileObj)
            """when using pickling function, data is saved properly in binary when checking the file created"""
        #objFile = open(strFileName, 'w')
        #for row in lstTbl:
            #lstValues = list(row.values())
            #lstValues[0] = str(lstValues[0])
            #objFile.write(','.join(lstValues) + '\n')
        #objFile.close()

        
        
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        #table.clear()  # this clears existing data and allows to load data from file
        with open(file_name, 'rb') as fileObj:
            lstTbl.clear() #clear the list
            freshTable = None
            try:
                freshTable = pickle.load(fileObj)    
                for i in range(0, len(freshTable)):
                    lstTbl.append(freshTable[i]) 
            except Exception as e:
                    """fixing error/issue with a blank inventory file loading in"""
                    print('\nProgram started, but nothing was loaded...\n')
                    print(type(e), e, e.__doc__, sep='\n')
            except FileNotFoundError as e:
                print("Unable to find the specified filename")
                print(type(e), e, e.__doc__, sep='\n')
            """pickled object definitely exists as a list(?) but does not display/load properly outside of this print"""
               #can keep this less formatted version and remove the original display inventory function?
        #objFile = open(file_name, 'r')
        #for line in objFile:
            #data = line.strip.split(',')
        #objFile.close()



# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def get_CD():
        """Asks for inventory specifications with the three specified parameters"""
        while True:
            try:
                strID = int(input('Enter ID: ').strip())
                break
                """requires a loop to avoid continuing asking for other inputs and restarts at asking for ID again"""
            except ValueError as e:
                print('That is not an integer!\n')
                print(type(e), e, e.__doc__, sep='\n')    
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return {'ID': strID, 'Title': strTitle, 'Artist': strArtist}

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName)

# 2. start main loop
while True:
    """after replacing all of the functions here with new ones in our classes, we add class calls into the main loop"""
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        DataProcessor.load_inventory()
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # TODO move IO code into function
        newCD = IO.get_CD()

        # 3.3.2 Add item to the table
        # TODO move processing code into function
        DataProcessor.add_CD(newCD)
        continue  
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try: 
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except ValueError as e:
            print("Please enter an ID number!")
            print(type(e), e ,e.__doc__, sep = '\n')
            continue
        # 3.5.2 search thru table and delete CD
        # TODO move processing code into function
        DataProcessor.del_CD(intIDDel)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TODO move processing code into function
            """modified save CD function to take arguments in order to utilize pickling the table dataset properly"""
            DataProcessor.save_CD(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')   
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




