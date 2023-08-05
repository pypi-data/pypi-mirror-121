#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def clay_minerals(DATA):
    import plotly.express as px
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    global minerals
    title=[0]
    global slope
    slope=[]
    minerals =pd.DataFrame({"chlorite_1":[],"chlorite_2":[],"smectite":[],"illite":[],"mica":[],"glautonic":[],"feldspar":[]})
    minerals_name=["chlorite_1","chlorite_2","smectite","illite","mica","glautonic","feldspar"]
    minerals_data = [[[0,1],[0,30]],[[0,2.5],[0,30]],[[0,7],[0,25]],[[0,2.5],[0,5]],[[0,6.5],[0,10]],[[0,7.5],[0,5]],[[0,4.5],[0,2.5]]]
    for i in range(len(minerals_data)):
        data = pd.DataFrame({"x":minerals_data[i][0],"y":minerals_data[i][1]})
        y1 = data.y.min()
        x1 = data["x"][data["y"]==y1].values
        y2 = data.y.max()
        x2 = data["x"][data["y"]==y2].values
        first_term = y2-y1
        second_term = x2-x1
        m = first_term/second_term
        intercept = y1-m*x1
        x=np.arange(0,10)
        line = m*x + intercept
        slope.append(m)
        minerals[minerals_name[i]]=line
    DATA["POTA(%)/THOR(PPM)"]= (DATA["POTA"]*100)/DATA["THOR"]
    clay=["chlorite","smectite","illite","mica","glauconite","feldspar"]
    DATA["mineral"]=0
    for i,z in zip(range(len(slope)-1),clay):
        x = np.arange(0.1,1,0.3)
        y = slope[i]*x
        a=x/y
        a=a[0]
        x1 = np.arange(0.1,1,0.3)
        y1 = slope[i+1]*x
        b=x1/y1
        b=b[0]
        c =DATA[(DATA["POTA(%)/THOR(PPM)"]>a) & (DATA["POTA(%)/THOR(PPM)"]<b)]
        DATA.loc[list(c.index),"mineral"]=z
        
    x = np.arange(1.5,2.5,0.3)
    y = slope[1]*x
    a=x/y
    a=a[0]
    x1 = np.arange(1.5,2.5,0.3)
    y1 = slope[2]*x
    b=x1/y1
    b=b[0]
    c = DATA[(DATA["POTA(%)/THOR(PPM)"]>a) & (DATA["POTA(%)/THOR(PPM)"]<b) & (DATA["POTA"]*100>1.5)]
    d = DATA[(DATA["POTA(%)/THOR(PPM)"]>a) & (DATA["POTA(%)/THOR(PPM)"]<b) & (DATA["POTA"]*100<1.5)]
    DATA.loc[list(c.index),"mineral"]="clay"
    DATA.loc[list(d.index),"mineral"]="smectite" 
        
      

        
    y = slope[0]*x
    a=x/y
    a=a[0]
    y1 = slope[1]*x 
    b=x1/y1
    b=b[0]
    c = DATA[(DATA["POTA(%)/THOR(PPM)"]>a) & (DATA["POTA(%)/THOR(PPM)"]<b) & (DATA["POTA"]*100>0.7)]
    d = DATA[(DATA["POTA(%)/THOR(PPM)"]>a) & (DATA["POTA(%)/THOR(PPM)"]<b) & (DATA["POTA"]*100<=0.7)]
    DATA.loc[list(c.index),"mineral"]="kaolinite"
    DATA.loc[list(d.index),"mineral"]="chlorite"
        
       
    plt.figure(figsize=(10,10))
    for i in range(len(minerals.columns)):
        plt.plot(np.arange(0,10),minerals.iloc[:,i])
        plt.ylim(0,30)
        plt.xlim(0,9)
    plt.scatter(DATA["POTA"][DATA["mineral"]=="smectite"]*100,DATA["THOR"][DATA["mineral"]=="smectite"],edgecolor="red",s=20,label="Smectite")
    plt.scatter(DATA["POTA"][DATA["mineral"]=="illite"]*100,DATA["THOR"][DATA["mineral"]=="illite"],edgecolor="green",s=20,label="Illite")
    plt.scatter(DATA["POTA"][DATA["mineral"]=="mica"]*100,DATA["THOR"][DATA["mineral"]=="mica"],edgecolor="brown",s=20,label="Mica")
    plt.scatter(DATA["POTA"][DATA["mineral"]=="glauconite"]*100,DATA["THOR"][DATA["mineral"]=="glauconite"],edgecolor="purple",s=20,label="Glauconite")
    plt.scatter(DATA["POTA"][DATA["mineral"]=="feldspar"]*100,DATA["THOR"][DATA["mineral"]=="feldspar"],edgecolor="red",s=20,label="Feldspar")
    plt.scatter(DATA[DATA["mineral"]=="clay"]["POTA"]*100,DATA[DATA["mineral"]=="clay"]["THOR"],edgecolor="black",s=20,color="gray",label="Clay")
    plt.scatter(DATA[DATA["mineral"]=="kaolinite"]["POTA"]*100,DATA[DATA["mineral"]=="kaolinite"]["THOR"],edgecolor="black",s=20,color="purple",label="Kaolinite")
    plt.scatter(DATA[DATA["mineral"]=="chlorite"]["POTA"]*100,DATA[DATA["mineral"]=="chlorite"]["THOR"],edgecolor="black",s=20,color="pink",label="Chlorite")
    plt.legend()
    plt.xlabel("POTA %")
    plt.ylabel("THOR PPM")
    plt.grid()
    plt.show()
    plt.figure(figsize=(10,10))
    well = input("Title : ")
    plt.title(well)
    sns.histplot(data=DATA, x="POTA(%)/THOR(PPM)", bins=30,hue="mineral",multiple="stack")
    plt.show()
    mineral_data0=[]
    pie_data0=[]
    for z in list(DATA["mineral"].value_counts().index):
        a = DATA[DATA["mineral"]==z]["mineral"]
        b = a.replace([z],1)
        total =  (b.sum())/(DATA.index.max()-DATA.index.min())
        mineral_data0.append(z)
        pie_data0.append(total)
    mineral_data0=pd.DataFrame({"mineral":mineral_data0,"quantity":pie_data0})
    fig = px.pie(mineral_data0,  values="quantity", names="mineral",title = well)
    fig.show()
    plt.figure(figsize=((7,77.6)))
    plt.subplot(1, 2, 1)
    ax = sns.scatterplot(data=DATA,x="GR",y="DEPT",color="black")
    ax.invert_yaxis()
    ax.legend(fontsize=19)
    plt.subplot(1, 2, 2)
    ax = sns.scatterplot(data=DATA,x="GR",y="DEPT",hue="mineral")
    ax.invert_yaxis()
    ax.legend(fontsize=19)
    plt.show()

