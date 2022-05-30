from charset_normalizer import from_path

file_path = "//RBAMVLATAMTBLP/CAC_Datos/ECAS/AWS Datalake/Auxiliary/Account_Inventory/Account_Inventory.csv"

results = from_path(file_path)

print(str(results.best()) )