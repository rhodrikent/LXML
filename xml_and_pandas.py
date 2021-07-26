import pandas as pd
from lxml import etree as ET
import numpy as np

Metals = pd.read_excel('NXMaterialData.xls',sheet_name='Combined',skiprows=3,usecols="A:AN",nrows=150)
Plastics_to_misc = pd.read_excel('NXMaterialData.xls',sheet_name='Combined',skiprows=409,usecols="A:AN",nrows=148)
Hoses = pd.read_excel('NXMaterialData.xls',sheet_name='Combined',skiprows=559,usecols="A:AN",nrows=51)
Others = pd.read_excel('NXMaterialData.xls',sheet_name='Combined',skiprows=611,usecols="A:AN",nrows=100)
Tables = pd.read_excel('NXMaterialData.xls',sheet_name='Tables',skiprows=4,usecols="A:AN",nrows=100)
Tables.columns = list(range(0,Tables.shape[1]))
Tables.set_index(0,inplace = True)
## use this to find stress strain:
## Tables.loc[test]

Metals = Metals.append(Plastics_to_misc).append(Hoses).append(Others)


root = ET.Element("MatML_Doc")

##start of metals section

def Metallics (prop1,format1,data1):
    stress = []
    strain = []
    
    if prop1 == "Stress-Strain (H)_1":
        if data1 == 'EMPTY':
            #print("is empty")
            pass
        else:
            
            table = Tables.loc[data1]
            for i in range(2,Tables.shape[1]+1):
                if pd.isna(table[i]):
                    pass
                else:
                    if (i % 2) == 0:  
                        strain.append(table[i])
                    else:
                        stress.append(table[i])
            stress = [str(x) for x in stress]
            strain = [str(y) for y in strain]
            stress = ' , '.join(stress)
            strain = ' , '.join(strain)

            #print(stress)
            #print(strain)
              


            
            PropertyData = ET.SubElement(BulkDetails, "PropertyData",property=prop1)
            Data = ET.SubElement(PropertyData, "Data",format=format1)
            Data.text = strain

            Qualifier = ET.SubElement(PropertyData, "Qualifier")
            Qualifier.text = "strain"

            ParameterValue = ET.SubElement(PropertyData, "ParameterValue",parameter=prop1,format=format1)
            Data1 = ET.SubElement(ParameterValue, "Data")
            Data1.text = stress
        
    else:
        PropertyData = ET.SubElement(BulkDetails, "PropertyData",property=prop1)
        Data = ET.SubElement(PropertyData, "Data",format=format1)
        Data.text = data1

props = ["Material Type","Version","Category","MassDensity","YoungsModulus","PoissonsRatio","Stress-Strain (H)_1","MatlNonlinearityType",
         "YieldFunctionCriterion","HardeningRule","CSYSOption","Yield","UltTensile","RefTemp","ThermalExpansion"]
formats = ["string","string","string","exponential","exponential","exponential","exponential","integer","integer",
           "integer","integer","exponential","exponential","exponential","exponential"]

Metals.Type.replace('ISO','IsotropicMaterial', inplace=True)

for i in range(0,len(Metals["#libref"])):
    if pd.isna(Metals["#libref"].iloc[i]) == True:
        pass
    else:
        #print(str(i) + str(type(Metals["#libref"].iloc[i])))
        Material = ET.SubElement(root, "Material")
        BulkDetails = ET.SubElement(Material, "BulkDetails")
        Name = ET.SubElement(BulkDetails, "Name")
        Name.text = Metals['Name'].iloc[i]

        Class1 = ET.SubElement(BulkDetails, "Class")
        Name1 = ET.SubElement(Class1, "Name")
        Name1.text = Metals.Cat.iloc[i]
        #Name1.text = S99G[2]

        Source = ET.SubElement(BulkDetails, "Source",source="")
        
        datas = [Metals.Type.iloc[i],"1.0",Metals.Cat.iloc[i],Metals.Density.iloc[i],Metals.Youngs.iloc[i],Metals.Poissons.iloc[i],Metals['Stress-Strain'].iloc[i],"1","1","1","0",
                 Metals.Yield.iloc[i],Metals['Ult Stress'].iloc[i],Metals['R Temp'].iloc[i],Metals['Thermal Coeff'].iloc[i]]
        datas = [str(j) for j in datas]
        zipped = list(zip(props,formats,datas))
        
        for x,y,z in zipped:
            Metallics(x,y,z)#,stress_strains)

##end of metals section

##start of composties section

props1 = ['Material Type','Version','YoungsModulus','YoungsModulus2','YoungsModulus3','PoissonsRatio','PoissonsRatio2',
          'PoissonsRatio3','MassDensity','ShearModulus','ShearModulus2','ShearModulus3',
            'ThermalCoeff','ThermalCoeff2','ThermalCoeff3','RefTemp','ThermalConduct','ThermalConduct2','ThermalConduct3',
          'MaxStressTension','MaxStressTension2','MaxStressTension3','MaxStressCompress','MaxStressCompress2',
            'MaxStressCompress3','MaxInPlaneShearStress','TsaiWuInteraction']
formats1 = ['string','string'] + ['exponential'] * (len(props1)-2)

Laminates = pd.read_excel('NXMaterialData.xls',sheet_name='Combined',skiprows=154,usecols="A:AV",nrows=250)
Cores1 = pd.read_excel('NXMaterialData.xls',sheet_name='Combined',skiprows=712,usecols="A:AV",nrows=22)
Cores2 = pd.read_excel('NXMaterialData.xls',sheet_name='Combined',skiprows=735,usecols="A:AV",nrows=16)
Laminates = Laminates.append(Cores1).append(Cores2)

Laminates.Type.replace('ORTHO','OrthotropicMaterial', inplace=True)

def Lams (prop2,format2,data2):
    PropertyData = ET.SubElement(BulkDetails, "PropertyData",property=prop2)
    Data = ET.SubElement(PropertyData, "Data",format=format2)
    Data.text = data2

for i in range(0,len(Laminates["#libref"])):
    if pd.isna(Laminates["#libref"].iloc[i]) == True:
        pass
    else:
        #print(str(i) + str(type(Metals["#libref"].iloc[i])))
        Material = ET.SubElement(root, "Material")
        BulkDetails = ET.SubElement(Material, "BulkDetails")
        Name = ET.SubElement(BulkDetails, "Name")
        Name.text = Laminates['Name'].iloc[i]
        Class1 = ET.SubElement(BulkDetails, "Class")
        Name1 = ET.SubElement(Class1, "Name")
        Name1.text = "COMPOSITES"
        Source = ET.SubElement(BulkDetails, "Source",source="")
        
        datas1 = [Laminates.Type.iloc[i],"1.0",Laminates['Youngs Modulus X'].iloc[i],Laminates['Youngs Modulus Y'].iloc[i],Laminates['Youngs Modulus Z'].iloc[i],Laminates['Poissons Ratio XY'].iloc[i],
                  Laminates['Poissons Ratio YZ'].iloc[i],Laminates['Poissons Ratio XZ'].iloc[i],Laminates['Mass Density'].iloc[i],Laminates['Shear Modulus XY'].iloc[i],Laminates['Shear Modulus XZ'].iloc[i],
                  Laminates['Shear Modulus YZ'].iloc[i],Laminates['Thermal Exp Coeff X'].iloc[i],Laminates['Thermal Exp Coeff Y'].iloc[i],Laminates['Thermal Exp Coeff Z'].iloc[i],
                  Laminates['R Temp'].iloc[i],Laminates['Thermal Cond X'].iloc[i],Laminates['Thermal Cond Y'].iloc[i],Laminates['Thermal Cond Z'].iloc[i],
                  Laminates['Max Stress Tension X'].iloc[i],Laminates['Max Stress Tension Y'].iloc[i],Laminates['Max Stress Tension Z'].iloc[i],
                  Laminates['Max Stress Compression X'].iloc[i],Laminates['Max Stress Compression Y'].iloc[i],Laminates['Max Stress Compression Z'].iloc[i],Laminates['Max Shear Stress 12'].iloc[i],Laminates['Tsai Wu'].iloc[i]]
        datas1 = [str(j) for j in datas1]
        zipped1 = list(zip(props1,formats1,datas1))

        for x,y,z in zipped1:
            Lams(x,y,z)
        

##end of comps

##start of fluids

props2 = ['Material Type','Version','Category','MassDensity','MolarMass']
formats2 = ['string','string','string'] + ['exponential'] * (len(props2)-3)

Fluids = pd.read_excel('NXMaterialData.xls',sheet_name='Combined',skiprows=752,usecols="A:AN",nrows=40)

Fluids.Type.replace('FLUID','FluidMaterial', inplace=True)
Fluids.Molar_Mass.replace('EMPTY','0.0', inplace=True)

def Flu (prop2,format2,data2):
    PropertyData = ET.SubElement(BulkDetails, "PropertyData",property=prop2)
    Data = ET.SubElement(PropertyData, "Data",format=format2)
    Data.text = data2

for i in range(0,len(Fluids["#libref"])):
    if pd.isna(Fluids["#libref"].iloc[i]) == True:
        pass
    else:
        #print(str(i) + str(type(Metals["#libref"].iloc[i])))
        Material = ET.SubElement(root, "Material")
        BulkDetails = ET.SubElement(Material, "BulkDetails")
        Name = ET.SubElement(BulkDetails, "Name")
        Name.text = Fluids['Name'].iloc[i]
        Class1 = ET.SubElement(BulkDetails, "Class")
        Name1 = ET.SubElement(Class1, "Name")
        Name1.text = Fluids.Cat.iloc[i]
        Source = ET.SubElement(BulkDetails, "Source",source="")
        
        datas2 = [Fluids.Type.iloc[i],'1',Fluids.Cat.iloc[i],Fluids['Mass_Density'].iloc[i],Fluids['Molar_Mass'].iloc[i]]
        datas2 = [str(j) for j in datas2]
        zipped1 = list(zip(props2,formats2,datas2))

        for x,y,z in zipped1:
            Flu(x,y,z)
        

##end of fluids

##importing metadata

tree1 = ET.parse('metadata.xml')
root1 = tree1.getroot()
root.append(root1)



##write out

tree = ET.ElementTree(root)

tree.write('output1.xml', pretty_print=True)


