import pandas as pd

#Datos técnicos de la técnología

technical_Data = {"Tecnología":["A","B","C","D","E","F","G","H","I","J","K","L","M","N"],
"Longitud de corte PP": [4000, 4600,5000, 5500, 6000, 6500, 7000,7500, 8000, 2000,2500, 3000, 3500, 4000],
"Longitud de corte PLA": [4000, 4600,5000, 5500, 6000, 6500, 7000,7500, 8000, 2000,2500, 3000, 3500, 4000],
"Longitud de corte PET": [4000, 4600,5000, 5500, 6000, 6500, 7000,7500, 8000, 2000,2500, 3000, 3500, 4000],
"Longitud de corte HIPS": [4800, 4800,6000, 7200, 6000, 6500, 7000,7500, 8000, 2000,2500, 3000, 3500, 4000],
"Horizontal":[560, 560, 680, 680, 700, 400, 500, 650, 540, 550, 600, 710, 690, 535],
"Vertical":[485, 485, 280, 280, 300, 340, 200, 370, 390, 230, 220, 300, 350, 300]}

material_Data = {"Material":["PP","PLA","APET","HIPS","PVC"], "Densidad":[0.00091,0.00127,0.00134,0.00105,0.00139],
"Contracción":[1.85, 0.50, 0.50, 0.80, 0.50]}

technical_Data_Table = pd.DataFrame(technical_Data)
material_Data_Table = pd.DataFrame(material_Data)

print(technical_Data_Table)
print(material_Data_Table)