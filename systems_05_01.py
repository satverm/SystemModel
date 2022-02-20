# This program is for converting the various system of the main system into and object and do various operations and also link with a database file for storing the data of many instances of the object

import sqlite3 as sq
import os

class System:

    print("The program is used to create a new system and its sub-systems as a parent child database file.\n")
    
    # class attributes , these can be made as user input later
    system_id = '0' # input("Enter the system id: ")
    
    system_code = 'TS'  # input("Enter the system name: ")
    system_name = 'TestSystem'

    # The filename code will be modified to have options to select a database file or create new one
    # This is akin to asking to create a new system or using an already created system
    filename = 'testdata.db'  # input("Enter the database filename (anyfile.db):")
    # The filename can be of the format system_code_sytem_name.db, for example uas_tapas.db
     

    # The __init__() functoin may become redundant after all tasks can be done using the UI and no database is created during creation of the new system object.
    # All tasks would be done using functions such as create database, select database, create new system etc..

# testing without an __init__ function
##    def __init__(self,path = None, filename = None):
##        
##        print("A system object has been created:{}, {}".format(self.system_id,self.system_name))
##        if filename == None:
##            filename = self.filename
##        self.create_database('blank', self.filename, self.system_id, self.system_code, self.system_name)

    # The class attributes would be removed when the program matures to create select or modify a new system by functions for these tasks.
    def create_new_system(self, filename = None, filepath = None, system_id = None, system_code = None, system_name = None):
        if system_id == None:
            #system_id = input("Enter the new system_id : ")
            system_id = '0' # '0' indicates the main system id and this is used to create all child systems
        if system_code == None:
            system_code = input("Enter the new system_code : ")
        if system_name == None:
            system_name = input("Enter the new system_name : ")
        default_filename = system_code.lower() + '_' + system_name.lower() + '.db'
        if filename == None:
            sel_file = input("Enter the new database file name or press Enter to use default ({}/anyfile.db) : ".format(default_filename))
            if sel_file == '':
                #print('sel_file:[',sel_file,']')
                filename = default_filename
                print("The filename entered by you is : {}".format(filename))
            else:
                print("The selected filename is: {}".format(sel_file))
                filename = sel_file
        if filepath == None:
            #filepath = input("Enter the database file path : ")
            filepath = '~'
        self.create_database(filepath, filename, system_id, system_code, system_name)
        # After creating a new system the Class attribute for filename should also change to new file name
        System.filename = filename

    
    # create the database and various tables 
    # we can have just one table for the parent-child data
    def create_database(self, filepath = None, filename = None, system_id = None, system_code = None, system_name = None):
        if filepath is None:
            filepath = input("Enter the file path:")
        if filename is None:
            filename = input("Enter the database file name(anysystem.db):")
        top_system = (system_id, system_code, system_name)
        print("\ntop_system: ", top_system)
        con = sq.connect(filename)
        cur = con.cursor()
        # creating master tables
        # create a parent-child table which will have all the parents and the children systems and thus it will form the
        # product breakdown structure or hierarchy.

        # we use try to check if the database exists or not
        try:
            cur.execute("SELECT * FROM parent_child")
            no_table = False     # if parent_child table is present the not table will be False and we use this to not create the database in this case.
        except Exception as e:
            #print(e)
            no_table = True      # if parent_child table is present the not_table will be True and hence we can create a new database and a table.
        if no_table:
            cur.execute('''CREATE TABLE IF NOT EXISTS parent_child(dataid integer NOT NULL primary key autoincrement, parent_code text, child_code text, child_name text)''')

            # We will insert the first record as  the Top level system where parentID is System and childId is UAS and child name is TAPAS
            # Now even the main systems can be created as child of toplevel system without having a seperate function for creating main systems
            cur.execute('INSERT INTO parent_child(parent_code, child_code, child_name) VALUES(?,?,?)',top_system)
            #if self.select_parent_sys(1)== None:  # This is creating problem for creating new system as it evaluates to False and commit is not done.
            # This check can be removed if we don't create a  database every time a new instance of the System class is created. Hence the new system would not have first record.
            con.commit()
            print("\nNew database created: {}".format(filename))
            print("The Top Level System is : {} ".format(top_system[2]))
        else:
            # filename already exists
            print("New database NOT created!!")
            
        con.close()

    # Here we are changing the class attribute filename to select a different database after running the program. This can be run as the first function in the UI.
    def select_database(self,filename = None):
        if filename == None:
            list_files = input("\nPress Y to see the list of database files in the current directory: ")
            if list_files.lower() == 'y':
                all_files_list = os.listdir('.')
                i = 0
                for file in all_files_list:
                    
                    if file[-3:] == '.db':
                        i += 1
                        print("{}: {}".format(i,file))
            
            filename = input("\nEnter the database filename: ")
        # now we should check this file for presence of any system data(parent_child table) and also if the file is present or not(can be a seperate function)
        file_present = self.file_check(filename)
        if file_present:
            #print("The database is present..")
            # we also need to test if the parent_child table is present or not and the top level record (recordID= 1) is present or not
            try:
                test_top_record = (self.print_record(1,filename))
                # this can be further tested for record filds to be in correct format
                #print(test_top_record)
                record_test = True
            except Exception as e:
                print(e)
                record_test = False
                
            if record_test:
                System.filename = filename
                print("\nNew database {} selected\n".format(filename))
            else:
                print("The file is not suitable!!, select a different file!!\n")
                self.create_new_system()
        else:
            print("\nThe entered file is not present !!")
            new_system_db = input("Enter Y to create a new database file and System: ")
            if new_system_db.lower() == 'y':
                self.create_new_system()
            
        
        
  

    def file_check(self, filename = None):
        if filename == None:
            filename = input("Enter the file name to test: ")
        try:
            with open(filename, 'rb') as fr:
                test = fr.readline()
                return(True)
        except Exception as e:
            print(e)
            return(False)
            
    

    def add_record(self, filepath = None, filename = None, new_record = None):
        if filepath is None:
            filepath = input("Enter the file path:")
        if filename is None:
            filename = input("Enter the database file name(anysystem.db):")
        if new_record is None:
            new_record = self.create_child_systems()
        con = sq.connect(filename)
        cur = con.cursor()
        # write the record in the parent_child table:
        cur.execute('INSERT INTO parent_child(parent_code, child_code, child_name) VALUES(?,?,?)',new_record)
        con.commit()
        print("New record added: ",new_record)
        con.close()

    def del_record(self, filepath = None, filename = None, record_id = None):
        if filepath is None:
            filepath = input("Enter the file path:")
        if filename is None:
            filename = input("Enter the database file name(anysystem.db):")
        if record_id is None:
            record_id = int(self.select_parent_sys())
        con = sq.connect(filename)
        cur = con.cursor()
        # delete the record from the parent_child table:
        cur.execute('DELETE FROM parent_child WHERE dataid = (?) ',(record_id,))
        confirm = input("Enter Y to confirm deleting the record !!")
        if confirm.lower() == 'y':
            con.commit()
            print("Record deleted!!: ",record_id)
        else:
            print("Record NOT deleted !!")
            
        con.close()
        

    # for making the pbs or the system hierarchy we can call create_child_systems() fun as many times
    def create_child_systems(self ,parent_system_id = None):
        print("Add a child system:")
        # we need to select the parent sys using a function select_parent_sys()
        if parent_system_id == None:
            parent_system_id = self.select_parent_sys()
            # Here we cna have a while loop to enter many child systems of a parent system
        while True:
            child_system_id = input("Enter the new child system code:")
            child_system_name = input("Enter the child system name:")
            new_record = (parent_system_id, child_system_id,child_system_name)
            self.add_record('blank',self.filename,new_record)
            more_records = input("Press Y to add more child systems: ")
            if more_records.lower() != 'y':
                print("Done adding child systems")
                break
            print("Adding more child systems for the selected Parent..")
            
    
    def add_main_systems(self):
        print("Add the main systems of a system which will be at the top most level:\n")
        # since we are using the create_child_system function to add main systems and it contains while loop,
        # here while loop is not requried
        #while True:
            # here the parent system id will be the system_id(1) since we are creating the main systems
            
        new_record = self.create_child_systems(1)
        #self.add_record('',self.filename, new_record)
        #more_records = input("press Y or Enter for adding more systems:(Y/N) ")
        #if more_records.lower() == 'n':
            #print("Main systems added !!")
            #break
    
      
    # This can be modified to first select the main system and then the child systems for the selected main system and so on
    def view_hierarchy(self):  
        print("The System Hierarchy")
        print(self.print_record(1,self.filename))
        con = sq.connect(self.filename)
        cur = con.cursor()
        # write the record in the parent_child table:
        cur.execute("SELECT * FROM parent_child")
        sel_record = cur.fetchall()
        temp_parent = True
        for item in sorted(sel_record):

            if temp_parent != item[1]:
                #print("System code: {} System Name: {}".format(item[1], item[3])) # modify to show correct name
                self.view_child_systems(item[1])
                temp_parent = item[1]
        con.close()
        
 
    def select_parent_sys(self,selected_id = None):
        if selected_id == None:
            sel_parent = str(input("Press Y or y to see all the parent child systems:"))
            if sel_parent.lower() == 'y':
                self.view_hierarchy()
                selected_id = input("Enter the record id for the parent system: ")
        con = sq.connect(self.filename)
        cur = con.cursor()
        cur.execute("SELECT * FROM parent_child WHERE dataid = (?) ",(selected_id,))
        sel_record = cur.fetchone()
        print("The selected Parent system is: ",sel_record)
        if sel_record != None:
            new_parent = sel_record[0]
            print(new_parent, sel_record[3])
            con.close()
            return(str(new_parent))
        else:
            print("The selected id does not exist!!")
            
            return(None)
    
    
    def view_child_systems(self, parent_id = None):
        
        if parent_id == None:
            parent_id = self.select_parent_sys()
        selected_id = parent_id  #we select system_id as the parent_code to get all the main systems
        con = sq.connect(self.filename)
        cur = con.cursor()
        cur.execute("SELECT * FROM parent_child WHERE parent_code = (?) ",(selected_id,)) # this logic can be inverted to only view child systems
        child_systems = cur.fetchall()
        if child_systems == None:  #not working for None
            print("There are no child systems of the selected parent system!!")
        else:
            print("\nThe child systems of the selected Parent system are: ")
            self.print_record(parent_id, self.filename)
            for item in child_systems:
                
                print(item)
        con.close()
        #return(child_systems)

    # print the record for the given record id(will be used to print the parent system name by int(parent_code)
    def print_record(self, parent_id = None, filename = None):  # use parent_id as record_id creates issues for record_id = 1
        if parent_id == None:
            parent_id = input("Enter the parent_id: " )
        selected_id = int(parent_id)
        if filename == None:
            filename = input("Enter the database filename: ")
        con = sq.connect(filename)
        cur = con.cursor()
        cur.execute("SELECT * FROM parent_child WHERE dataid = (?) ",(selected_id,))
        sel_record = cur.fetchone()
        print("\nThe selected Parent system is:\n",sel_record)
        con.close()
        
 
    def ui_menu(self):

        #print('The program is used to ceate systems and sub-sytems and stored in a database file.')
        self.select_database()
        menu_items = [
            '0: Exit the program!!','1: Create main systems','2: Create child systems','3: View child systems'
            , "4: View a system's hierarchy", "5: Delete Record ", "6: Create New System"
            , "7: Select different System/database"]
        while True:
            for k in menu_items:
                print(k)
            sel_opt = str(input("Enter the number for the selected option: "))
            print('The selected option is {}'.format(sel_opt))
            if sel_opt == '1':
                self.add_main_systems()
            elif sel_opt == '2':
                self.create_child_systems()
            elif sel_opt == '3':
                self.view_child_systems()
            elif sel_opt == '4':
                self.view_hierarchy() # here we should have only systems which have child systems.
            elif sel_opt == '5':
                self.del_record('blank', self.filename)
            elif sel_opt == '6':
                self.create_new_system()
            elif sel_opt == '7':
                self.select_database()
            elif sel_opt == '0':
                print("Program finished!!")
                break
            else:
                print("Not a valid input !!")

a = System()
a.ui_menu()


# Testing
# newsystem = System()
# subsystem = newsystem.create_sub_systems(newsystem.system_id)
# print("The systemid and systemname are", subsystem)
        
        
