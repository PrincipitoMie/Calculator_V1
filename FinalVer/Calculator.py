from database import technical_Data_Table, material_Data_Table
import numpy as np
import math

#Ingreso de datos
geometry = input("Ingrese la geometria C u O: ")
technology = input("ingrese la tecnologia: ")
material = input("ingrese material: ")
weight = float(input("ingrese el peso: "))

if geometry == "C":
    diameter = float(input("ingrese el diametro: "))
else:
    largo = float(input("ingrese el largo: "))
    alto = float(input("ingrese el alto: "))

pi = 3.14159265358979


if geometry == "C":
    perimeter = 2*pi*(diameter/2)
else: 
    perimeter = 2*largo+2*alto

if geometry == "C":
    area_T = pi*(diameter/2)**2
else: 
    area_T = (largo*alto)

print(perimeter)

equivalent = ((4*area_T)/pi)**0.5
print(equivalent)



#Tratamiento de datos 1, busqueda de contracción del material
density_Looking = material_Data_Table.loc[material_Data_Table["Material"]==material]
if not density_Looking.empty:
    material_Density = density_Looking["Densidad"].values[0]

#Tratamiento de datos 2, busqueda de densidad del material
contraction_Looking = material_Data_Table.loc[material_Data_Table["Material"]==material]

if not contraction_Looking.empty:
    material_Contraction = contraction_Looking["Contracción"].values[0]

#Tratamiento de datos 3, busqueda de longitud de corte por material y tecnologia
looking = technical_Data_Table.loc[technical_Data_Table["Tecnología"]==technology]

if not looking.empty:
    if material == "PP":
        cutting_Lenght_Man = looking["Longitud de corte PP"].values[0] 
    elif material == "PLA":
        cutting_Lenght_Man = looking["Longitud de corte PLA"].values[0]
    elif material == "PET":
        cutting_Lenght_Man = looking["Longitud de corte PET"].values[0]
    elif material == "HIPS":
        cutting_Lenght_Man = looking["Longitud de corte HIPS"].values[0]

#Cálculo del calibre
if geometry == "C":
    thick = (4*weight)/((material_Density*pi)*(diameter*(1-(material_Contraction/100)))**2)
else:
    thick = (4*weight)/((material_Density*pi)*(equivalent*(1-(material_Contraction/100)))**2)

print(material, "Tiene densidad", material_Density)
print(material, "Tiene contracción", material_Contraction)
print(technology, "Tiene LongCor", cutting_Lenght_Man)  
print(thick)

#Longitud de corte según material

if thick < 0.8:
    cutting_Lenght_Material = (technical_Data_Table[["Longitud de corte PP" , "Longitud de corte PLA", "Longitud de corte PET", "Longitud de corte HIPS"]]*0.8/thick)
else: 
    cutting_Lenght_Material =technical_Data_Table[["Longitud de corte PP" , "Longitud de corte PLA", "Longitud de corte PET", "Longitud de corte HIPS"]]


print(cutting_Lenght_Material)

#Calculo del número de cavidades máximo permitido por longitud de corte
if material == "PP":
     technical_Data_Table["Max number of cavities"]=np.int64(technical_Data_Table["Longitud de corte PP"]/perimeter)
elif material == "PLA":
     technical_Data_Table["Max number of cavities"]=np.int64(technical_Data_Table["Longitud de corte PLA"]/perimeter)
elif material == "PET":
     technical_Data_Table["Max number of cavities"]=np.int64(technical_Data_Table["Longitud de corte PET"]/perimeter)
elif material == "HIPS":
     technical_Data_Table["Max number of cavities"]=np.int64(technical_Data_Table["Longitud de corte HIPS"]/perimeter)

print(technical_Data_Table["Max number of cavities"])

#Calculo del número de cavidades máximo permitido por Área

x_30 = math.cos(math.radians(30))
y_60 = math.sin(math.radians(60))

if geometry == "C":
    y_Config_60 = (diameter+12)*y_60
    x_Congig_30 = (diameter+12)*x_30
    technical_Data_Table["Cavs H"] = np.int64(technical_Data_Table["Horizontal"]/(diameter+6.5))
    technical_Data_Table["Cavs V"] = np.int64(technical_Data_Table["Vertical"]/(diameter+6.5))
    technical_Data_Table["Cavs H30"] = np.int64(technical_Data_Table["Horizontal"]/(diameter+6.5))
    technical_Data_Table["Cavs V30"] = np.int64(technical_Data_Table["Vertical"]/(x_Congig_30))
    technical_Data_Table["Cavs H60"] = np.int64(technical_Data_Table["Horizontal"]/(y_Config_60))
    technical_Data_Table["Cavs V60"] = np.int64(technical_Data_Table["Vertical"]/(diameter+6.5))
    print(technical_Data_Table[["Cavs H30", "Cavs V30", "Cavs H60", "Cavs V60"]])

else:
    technical_Data_Table["Cavs H"] = np.int64(technical_Data_Table["Horizontal"]/(largo+6.5))
    technical_Data_Table["Cavs V"] = np.int64(technical_Data_Table["Vertical"]/(alto+6.5))
    print(technical_Data_Table[["Cavs H", "Cavs V"]])

if geometry == "C":
#Cavs area arreglo 90
    technical_Data_Table["Max cavs area"] = np.int64(technical_Data_Table["Cavs H"]*technical_Data_Table["Cavs V"])

#Cavs area arreglo 30
    technical_Data_Table["Max cavs area 30"] = np.int64(technical_Data_Table["Cavs H30"]*technical_Data_Table["Cavs V30"])

#Cavs area arreglo 60
    technical_Data_Table["Max cavs area 60"] = np.int64(technical_Data_Table["Cavs H60"]*technical_Data_Table["Cavs V60"])

else: 
     technical_Data_Table["Max cavs area"] = np.int64(technical_Data_Table["Cavs H"]*technical_Data_Table["Cavs V"])
#Número máximo de cavidades permitido

if geometry == "C":
    technical_Data_Table["Max number of cavities"] = np.where(technical_Data_Table["Max number of cavities"]>technical_Data_Table["Max cavs area"],
    technical_Data_Table["Max cavs area"],technical_Data_Table["Max number of cavities"] )
    technical_Data_Table["Max number of cavities 30"] = np.where(technical_Data_Table["Max number of cavities"]>technical_Data_Table["Max cavs area 30"],
    technical_Data_Table["Max cavs area 30"],technical_Data_Table["Max number of cavities"] )
    technical_Data_Table["Max number of cavities 60"] = np.where(technical_Data_Table["Max number of cavities"]>technical_Data_Table["Max cavs area 60"],
    technical_Data_Table["Max cavs area 60"],technical_Data_Table["Max number of cavities"] )
    print(technical_Data_Table[["Max number of cavities", "Max number of cavities 30", "Max number of cavities 30"]])
else:
    technical_Data_Table["Max number of cavities"] = np.where(technical_Data_Table["Max number of cavities"]>technical_Data_Table["Max cavs area"],
    technical_Data_Table["Max cavs area"],technical_Data_Table["Max number of cavities"] )

#Arreglo

if geometry == "C":
    technical_Data_Table["Arrangement"] = np.int64(technical_Data_Table["Max number of cavities"]/technical_Data_Table["Cavs V"])
    technical_Data_Table["Arrangement 30"] = np.int64(technical_Data_Table["Max number of cavities"]/technical_Data_Table["Cavs V30"])
    technical_Data_Table["Arrangement 60"] = np.int64(technical_Data_Table["Max number of cavities"]/technical_Data_Table["Cavs V30"])
    print(technical_Data_Table[["Arrangement","Arrangement 30", "Arrangement 60"]])
else:
    technical_Data_Table["Arrangement"] = np.int64(technical_Data_Table["Max number of cavities"]/technical_Data_Table["Cavs V"])

#Determinación del arreglo horizontal y vertical

technical_Data_Table["Horizontal"]= np.where(technical_Data_Table["Cavs V"]>technical_Data_Table["Arrangement"], technical_Data_Table["Cavs V"],
technical_Data_Table["Arrangement"])

technical_Data_Table["Vertical"]= np.where(technical_Data_Table["Arrangement"]<technical_Data_Table["Cavs V"], technical_Data_Table["Arrangement"],
technical_Data_Table["Cavs V"])


#print(technical_Data_Table[["Horizontal","Vertical"]])

#Cavidades totales

technical_Data_Table["Total cavities"]= np.int64(technical_Data_Table["Horizontal"]*technical_Data_Table["Vertical"])
#print(technical_Data_Table[["Horizontal","Vertical", "Total cavities"]])

technical_Data_Table["Total area"] = (technical_Data_Table["Total cavities"]*area_T)
#print(technical_Data_Table[["Horizontal","Vertical", "Total cavities", "Total area"]])


if geometry == "C":
    #Index Lenght
    technical_Data_Table["Index lenght"]= np.int64(technical_Data_Table["Vertical"]*diameter+(6.5*technical_Data_Table["Vertical"])+25)
    #Foil width
    technical_Data_Table ["Foil width"] = np.int64(technical_Data_Table["Horizontal"]*diameter+(6.5*technical_Data_Table["Horizontal"]+25))
else: 
        #Index Lenght
    technical_Data_Table["Index lenght"]= np.int64(technical_Data_Table["Vertical"]*alto+(6.5*technical_Data_Table["Vertical"])+25)
    #Foil width
    technical_Data_Table ["Foil width"] = np.int64(technical_Data_Table["Horizontal"]*largo+(6.5*technical_Data_Table["Horizontal"]+25))

print(technical_Data_Table[["Horizontal","Vertical", "Total cavities", "Total area", "Index lenght", "Foil width"]])


#Área de uso
technical_Data_Table ["Use area"]= (technical_Data_Table["Index lenght"] * technical_Data_Table["Foil width"])

#Desperdicio 
technical_Data_Table ["Rest material"]= (1-(technical_Data_Table["Total area"]/technical_Data_Table["Use area"]))
print(technical_Data_Table[["Horizontal","Vertical", "Total cavities", "Total area", "Index lenght", "Foil width", "Use area", "Rest material"]])

#Resultado final
result = technical_Data_Table.loc[technical_Data_Table["Tecnología"] == technology]
result = result.drop(["Longitud de corte PP", "Longitud de corte PLA", "Longitud de corte PET", "Longitud de corte HIPS", "Horizontal", "Vertical"], axis = 1)
print(result)