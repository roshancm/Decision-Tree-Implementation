import pandas as pd

textdata = open("dt-data.txt","r")
text = textdata.read()
splitData = text.split(')')
att_name = list(splitData[0][1:].split(', '))
att_values = splitData[1].strip('\n').replace("\n","").split(";")[:-1]
i = 0

for row in att_values:
    att_values[i] = row[4:].split(", ")
    i = i+1

df = pd.DataFrame(data=att_values,columns=att_name)
from math import log2
def calculate_entropy(tempDF):
    entropy = 0;
    for value in tempDF["Enjoy"].value_counts():
        entropy = entropy + (-(float(value)/len(tempDF)) * log2((float(value)/len(tempDF))))
    return entropy

def information_gain(tempDF,att):
    tempval1 = 0
    for option in tempDF[att].unique():
        for value in tempDF[tempDF[att]==option]["Enjoy"].value_counts():
            tempval1 = tempval1 + ((value/len(tempDF)) * calculate_entropy(tempDF[tempDF[att]==option]))
    info_gained = calculate_entropy(tempDF) - tempval1
    return info_gained

def decision(df):
    if((len(df[df["Enjoy"]=="Yes"])) < (len(df[df["Enjoy"]=="No"]))):
        return "No"
    else:
        return "Yes"

def construct_tree(df):
    dtree=[]
    length = len(df)
    if(length == len(df[df["Enjoy"] == "Yes"])):
        return "Yes"
    elif (length == len(df[df["Enjoy"] == "No"])):
        return "No"
    elif (len(att_name) == 1):
        return decision(df)
    else:
         max_info=0
         for attribute in df.columns:
            if(attribute == "Enjoy"):
                continue
            else:
                info = information_gain(df[[attribute,"Enjoy"]],attribute)
                if(max_info < info):
                    max_info = info
                    splitatt = attribute
         if(max_info == 0):
            dtree.append(decision(df))
         else:
            dtree.append(splitatt)
            for option in df[splitatt].unique():
                newdtree = []
                newdtree.append(option)
                newdtree.append(construct_tree(df[df[splitatt]==option]))
                dtree.append(newdtree)
    return dtree

def print_tree(dtree,l):
        print('     ' * l,dtree[0])
        for item in dtree[1:]:
            if(type(item)==list):
                print_tree(item,l+1)
            else:
                print('     ' * (l+1),item)



def predict(dtree,df):
    if (dtree == "Yes"):
        print("Yes")
    elif (dtree =="No"):
        print("No")
    else:
        user_input = input('\nEnter Value of Attribute: '+dtree[0]+":")

        for item in dtree:
            if user_input in item[0]:
                df = df[df[dtree[0]] == user_input]
                predict(item[1],df)
                return
        print(decision(df))
        return


dtree=[]
dtree = construct_tree(df)
print(dtree)
print_tree(dtree,1)
predict(dtree,df)