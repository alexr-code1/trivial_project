#
# Class name: Db_Interation
#
# Purpose: This class will be used in the back end to interact with the database
# Attributes: database path, table name, number of records
# Opertaions performed: setters & getters for attributes, db insertion using file, db insertion using manual entry
#

#importing required libraries:
import os
import os.path
import pyodbc
import pandas as pd


class Db_Interation:


    def __init__(self):

        self.db_path = ""
        self.table_name = "Q_SET"
        self.num_records = 0
    
    def __init__(self, path):

        self.db_path = path
        self.table_name = "Q_SET"

        #to get the number of records, we will opent the db and count records in the table:
        #connecting to database:
        conn = pyodbc.connect('driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(self.db_path))
        #conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Umar files\PYTOHN PROJECT WORK\TR_CMP_DB1.accdb;')
        cursor = conn.cursor()
        count_qry = "SELECT *  FROM Q_SET;"
        print(cursor.execute(count_qry))
        self.num_records = len(cursor.fetchall())
        
        #self.num_records = cursor.execute(count_qry).rowcount #updating number of records in the object
        print ("row count is: " + str(self.num_records))
        conn.commit()


    def set_dbpath(self, path):

        #check if file exitsts
        #if no - give error message
        if os.path.isfile(path):
            #if yes, assign it to attribute:
            self.db_path = path
        else:
            print("Sorry. There is an issue with the file path provided. Please review: ", path)


    def get_dbpath(self):

        return self.db_path
    

    def get_tblname(self):

        return self.table_name
    

    def update_rcrds(self, rcrd_delta):

        self.num_records = rcrd_delta


    def get_rcrds(self):

        return self.num_records
    

    def insrt_file(self, file_path):

        # This method will be used to upload a file to the database
        # we will update the num_recrods variable in this as well

        #check if file exists
        # if no - give error message
        # if yes - proceed
        if not os.path.isfile(file_path):

            print("No file found. Input provided is: ", file_path)
            print("Quitting program now.")
            quit()

        else:

            #in this case, we will read the file and use it for upload
            #reading file
            data_read = pd.read_excel(file_path)
            
            print("number of records in file: ", len(data_read.index))

            #connecting to database:
            conn = pyodbc.connect('driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(self.db_path))
            #conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Umar files\PYTOHN PROJECT WORK\TR_CMP_DB1.accdb;')
            cursor = conn.cursor()

                
            # Looping through file and uploading each row
            i = 0
            while (i < len(data_read.index)):

                #creating query for insert
                print(i)
                data_comp = str(data_read['Q_Num'][i]) + ", '" + data_read['CATEGORY'][i] + "', '" + data_read['QUESTION'][i]+ "', '" + data_read['ANSWER'][i] + "', " + data_read['USED'][i] + ", " + data_read['NOT_USE'][i]
                insrt_qry = "INSERT INTO Q_SET (Q_Num, CATEGORY, QUESTION, ANSWER, USED, NOT_USE) VALUES ( " + data_comp + " )"
                print(insrt_qry)
                #executing insert query
                cursor.execute(insrt_qry)
                conn.commit()
                i += 1 #increment for while loop


            #at this point, we have inserted the records
            #we update the rcrd_delta variable to show updated number of records:
            self.update_rcrds(i)




    #Here, we assume that rcrd is a dataframe with all the rquired columns
    #rcrds: this will have key as question number and value will be a list of remaining attributes
    # example rcrd format: rcrd = {15: ["Category", "Quesiton", "ANSWER", USED, NOT_USE]}
    def insrt_row(self, rcrd):

        # This method will be used to upload a record to the database
        # we will update num_recorcds variable in this as well


        #Connecting to database:
        conn = pyodbc.connect('driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(self.db_path))
        cursor = conn.cursor()
        
        #Creating query to add:
        data_comp = str(self.num_records + 1) + "'" + rcrd.value[1] + "', '" + rcrd.value[2]+ "', '" + rcrd.value[3] + "', " + rcrd.value[4] + ", " + rcrd.value[5]
        insrt_qry = "INSERT INTO Q_SET (Q_Num, CATEGORY, QUESTION, ANSWER, USED, NOT_USE) VALUES ( " + data_comp + " )"
        cursor.execute(insrt_qry)
        conn.commit()

        print("record has been added.")

    def delete_data(self):

        #Connecting to database:
        conn = pyodbc.connect('driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(self.db_path))
        cursor = conn.cursor()
        
        del_qry = "DELETE * FROM Q_SET;"
        cursor.execute(del_qry)
        conn.commit()

    def delete_data_category(self, category_str):

        #Connecting to database:
        conn = pyodbc.connect('driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(self.db_path))
        cursor = conn.cursor()
        
        del_qry = "DELETE * FROM Q_SET WHERE CATEGORY = ' + category_str +';"
        cursor.execute(del_qry)
        conn.commit()

    def flag_category(self, category_str):

        #Connecting to database:
        conn = pyodbc.connect('driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(self.db_path))
        cursor = conn.cursor()

        #creating query to execute
        upd_qry = "UPDATE Q_SET SET NOT_USE = Yes WHERE CATEGORY = '" + category_str + "';"
        
        # executing query
        cursor.execute(upd_qry)
        conn.commit()

    def get_Question (self, category_str):

        #Connecting to database:
        conn = pyodbc.connect('driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(self.db_path))
        cursor = conn.cursor()

        #get question query:
        get_Q_qry = "SELECT TOP 1 * FROM Q_SET WHERE USED = No AND CATEGORY = '" + category_str + "' ORDER BY RND()"
        Q_to_Ask = cursor.execute(get_Q_qry).fetchall()
        conn.commit()

        #As the question is going to be asked, we will update the used flag from No to Yes:
        Q_num_extrctd = Q_to_Ask[0][0]
        #print(Q_num_extrctd)
        upd_flag = "UPDATE Q_SET SET USED = Yes WHERE Q_Num = " + str(Q_num_extrctd) + ";"
        print("upd_flag " + upd_flag)
        cursor.execute(upd_flag)
        conn.commit()

        #taking the first question from the list of questions extracted
        Q_to_return = Q_to_Ask[0]

        return Q_to_return #This will return the quesiton extracted




    
