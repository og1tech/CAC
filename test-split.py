from tssplit import tssplit

buffer = '2020-07-04|Guatemala|30|Link|80032502|AGENCIAS J.I.COHEN, SOCIEDAD ANONIM|COHEN|5-000202|"MAPFRE | SEGUROS GUATEMALA, S.A."|"MAPFRE | SEGUROS GUATEMALA, S.A."|NA|MABTHERA|1699326|MABTHERA VIALS 100 MG/10 ML 2|Aseguradora|N|Y|1|750'
x = tssplit(buffer, quote='"\'', delimiter='|', escape='/^', trim='')
print(len(x))
i = 0
for col in x:
    i += 1
    print(i, col)
