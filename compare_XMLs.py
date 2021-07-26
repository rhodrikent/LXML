import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('wf1_material_data.xml')
tree2 = ET.parse('C:\delete\LinkedInLearning\Learn_pandas\output1.xml')

root = tree.getroot()
root2 = tree2.getroot()

Names1 = []
Names2 = []

zipped = []
zipped2 = []



for materials in root.findall('Material'):
    for BulkDetails in materials.findall('BulkDetails'):
        values = []
        for Name in BulkDetails.findall('Name'):
                
            Names1.append(Name.text)

##        for PropertyData in BulkDetails.findall('PropertyData'):
##            for prop in PropertyData:
##                
##                for value in PropertyData.findall('Data'):
##                    values.append(value.text)
##        zipped.append(values)

for materials in root2.findall('Material'):
    for BulkDetails in materials.findall('BulkDetails'):
        values2 = []
        for Name in BulkDetails.findall('Name'):
                
            Names2.append(Name.text)

#Names2.append("test mat")

if len(Names2) > len(Names1):
    for i in Names1:
        try:
            Names2.remove(i)
        except:
            pass
    [print("Additional Materials: "+m) for m in Names2]
elif len(Names2) < len(Names1):
    for i in Names2:
        try:
            Names1.remove(i)
        except:
            pass
    [print("Additional Materials: "+m) for m in Names1]
else:
    print("No additional materials")

##        for PropertyData in BulkDetails.findall('PropertyData'):
##            for prop in PropertyData:
##                
##                for value in PropertyData.findall('Data'):
##                    values2.append(value.text)
##        zipped2.append(values2)        

##df = pd.DataFrame()
##df2 = pd.DataFrame()
##
##for i,j in enumerate(Names1):
##	zipped[i].insert(0,j)
##	df.loc[:,i] = pd.Series(zipped[i])
##
##for i,j in enumerate(Names2):
##	zipped2[i].insert(0,j)
##	df2.loc[:,i] = pd.Series(zipped2[i])
##
##n = 30
##df.append([None]*(n-df.shape[0]),ignore_index=True)
##df2.append([None]*(n-df2.shape[0]),ignore_index=True)
##
##if df.equals(df2) == True:
##    print("the two xml files are an exact match")
##
##else:
##    print("the two xml files are not exact match")
##    diff = df.compare(df2)



    

    
                    
                        
            
            
