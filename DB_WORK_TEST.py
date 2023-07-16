from DB_INTERACTION import Db_Interation



new_db_interaction = Db_Interation(r"C:\Umar files\PYTOHN PROJECT WORK\TR_CMP_DB1.accdb")

#print(new_db_interaction.get_dbpath())

#print(new_db_interaction.get_rcrds())


#now, we add records:
#new_db_interaction.insrt_file(r"C:\Users\umarz\OneDrive - Johns Hopkins\Summer 2023\PYTOHN PROJECT WORK\TEST1.xlsx")
#new_db_interaction.delete_data()

print(new_db_interaction.get_rcrds())

#new_db_interaction.flag_category("Entertainment")

test = new_db_interaction.get_Question("Arts & Literature")
print(test)

# import pandas as pd

# data = {
#   "calories": [420, 380, 390],
#   "duration": [50, 40, 45]
# }

# #load data into a DataFrame object:
# df = pd.DataFrame(data)

# print(df) 