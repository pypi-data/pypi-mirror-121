#!/usr/bin/env python
# coding: utf-8

# In[84]:





# In[99]:


def calcite(DATA):
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.pipeline import make_pipeline
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    global coeff
    x=np.array([-1.4,0,5,10,15,20,25,30]).reshape(-1,1)
    y=np.array([0,2,8.5,14.5,20.1,25.2,30.2,35]).reshape(-1,1)
    
    

    poly_reg = PolynomialFeatures(degree=3)
    X_poly = poly_reg.fit_transform(x)
    reg = LinearRegression()
    reg.fit(X_poly, y)
    a = reg.predict(X_poly)
    plt.figure(figsize=(10,10))
    plt.plot(x,a,color="blue",label="Calcite")
    plt.xlabel("Apparent Neutron Limestone Porosity p.u",fontsize=15)
    plt.ylabel("True Porosity p.u",fontsize=15)
    plt.plot(np.array([1,5,7,10,15,22,25,28,30,33,35,38]),
             np.array([ 0.28427032,3.68427008,5.41719822,8.05775078,12.56843258,19.11388498,22.00139953,24.93830648,26.92368466,29.94291228,31.98317091,35.08471919]),color="red",label="Dolomite")
    plt.plot(np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),color="black",label="Limestone")
    plt.legend()
    plt.grid()
    plt.show()
    question = input("Is NPHI in porosity unit  Y/N : ")
    if (question == "Y") or (question == "y"):
        NPHI = np.array(DATA["NPHI"]).reshape(-1,1)
        poly = poly_reg.transform(NPHI)
        true = reg.predict(poly)
        DATA["True Neutron Porosity"] = true
        plt.figure(figsize=(10,10))
        plt.plot(x,a,color="blue",label="Calcite")
        plt.xlabel("Apparent Neutron Limestone Porosity p.u",fontsize=15)
        plt.ylabel("True Porosity p.u",fontsize=15)
        z = DATA["NPHI"]
        z1 = DATA["True Neutron Porosity"]
        plt.scatter(z,z1,color="red")
        plt.plot(np.array([1,5,7,10,15,22,25,28,30,33,35,38]),
                 np.array([ 0.28427032,3.68427008,5.41719822,8.05775078,12.56843258,19.11388498,22.00139953,24.93830648,26.92368466,29.94291228,31.98317091,35.08471919]),color="red",label="Dolomite")
        plt.plot(np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),color="black",label="Limestone")
        plt.grid()
        message="TRUE POROSITY HAS BEEN CALCULATED. CHECK YOUR DATA"
        coeff = reg.coef_
        print(message)
        return DATA
    if (question == "N") or (question == "n"):
        NPHI = np.array(DATA["NPHI"]*100).reshape(-1,1)
        poly = poly_reg.transform(NPHI)
        true = reg.predict(poly)
        DATA["True Neutron Porosity"] = true
        plt.figure(figsize=(10,10))
        plt.plot(x,a,color="blue",label="Calcite")
        plt.xlabel("Apparent Neutron Limestone Porosity p.u",fontsize=15)
        plt.ylabel("True Porosity p.u",fontsize=15)
        z = DATA["NPHI"]*100
        z1 = DATA["True Neutron Porosity"]
        plt.scatter(z,z1,color="red")
        plt.plot(np.array([1,5,7,10,15,22,25,28,30,33,35,38]),
                 np.array([ 0.28427032,3.68427008,5.41719822,8.05775078,12.56843258,19.11388498,22.00139953,24.93830648,26.92368466,29.94291228,31.98317091,35.08471919]),color="red",label="Dolomite")
        
        plt.plot(np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),color="black",label="Limestone")
        plt.legend()
        plt.grid()
        
        message="TRUE POROSITY HAS BEEN CALCULATED. CHECK YOUR DATA"
        coeff = reg.coef_
        print(message)
        return DATA
    


# In[100]:




# In[101]:


def dolomite(DATA):
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.pipeline import make_pipeline
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    x=np.array([1,5,7,10,15,22,25,28,30,33,35,38]).reshape(-1,1)
    y=np.array([0,4.5,5,8,12.5,19,22,25,27,30,32,35]).reshape(-1,1)
    poly_reg = PolynomialFeatures(degree=2)
    X_poly = poly_reg.fit_transform(x)
    reg = LinearRegression()
    reg.fit(X_poly, y)
    a = reg.predict(X_poly)
    plt.figure(figsize=(10,10))
    plt.plot(x,a,color="red",label="Dolomite")
    plt.plot(np.array([-1.4,0,5,10,15,20,25,30]).reshape(-1,1),np.array([0,2,8.5,14.5,20.1,25.2,30.2,35]).reshape(-1,1),label="Calcite")
    plt.plot(np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),color="black",label="Limestone")
    plt.xlabel("Apparent Neutron Limestone Porosity p.u",fontsize=15)
    plt.ylabel("True Porosity p.u",fontsize=15)
  
    plt.legend()
    plt.grid()
    plt.show()
    question = input("Is NPHI in porosity unit  Y/N : ")
    if (question == "Y") or (question == "y"):
        NPHI = np.array(DATA["NPHI"]).reshape(-1,1)
        poly = poly_reg.transform(NPHI)
        true = reg.predict(poly)
        DATA["True Neutron Porosity"] = true
        plt.figure(figsize=(10,10))
        plt.plot(x,a,color="red",label="Dolomite")
        z = DATA["NPHI"]
        z1 = true
        plt.scatter(z,z1,color="black",label="Apparent versus True")
        plt.xlabel("Apparent Neutron Limestone Porosity p.u",fontsize=15)
        plt.ylabel("True Porosity p.u",fontsize=15)
        plt.plot(np.array([-1.4,0,5,10,15,20,25,30]).reshape(-1,1),np.array([0,2,8.5,14.5,20.1,25.2,30.2,35]).reshape(-1,1),label="Calcite")
        plt.plot(np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),color="black",label="Limestone")
        plt.legend()
        plt.grid()
        plt.show()
        message="TRUE POROSITY HAS BEEN CALCULATED. CHECK YOUR DATA"
        print(message)
        return DATA
    if (question == "N") or (question == "n"):
        NPHI = np.array(DATA["NPHI"]*100).reshape(-1,1)
        poly = poly_reg.transform(NPHI)
        true = reg.predict(poly)
        DATA["True Neutron Porosity"] = true
        plt.figure(figsize=(10,10))
        plt.plot(x,a,color="red",label="Dolomite")
        plt.legend()
        z = DATA["NPHI"]*100
        z1 = true
        plt.scatter(z,z1,color="black",label="Apparent versus True")
        plt.xlabel("Apparent Neutron Limestone Porosity p.u",fontsize=15)
        plt.ylabel("True Porosity p.u",fontsize=15)
        plt.plot(np.array([-1.4,0,5,10,15,20,25,30]).reshape(-1,1),np.array([0,2,8.5,14.5,20.1,25.2,30.2,35]).reshape(-1,1),label="Calcite")
        plt.plot(np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),color="black",label="Limestone")
        plt.legend()
        plt.grid()
        plt.show()
        message="TRUE POROSITY HAS BEEN CALCULATED. CHECK YOUR DATA"
        print(message)
        return DATA


# In[102]:




# In[103]:


def calc_lim(DATA):
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.pipeline import make_pipeline
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    x=np.array([0,2,8.5,14.5,20.1,25.2,30.2,35]).reshape(-1,1)
    y=np.array([[-1.4,0,5,10,15,20,25,30]]).reshape(-1,1)
    z=np.array([[-1.4,0,5,10,15,20,25,30]]).reshape(-1,1)
    poly_reg = PolynomialFeatures(degree=2)
    poly_reg.fit(x)
    X_poly = poly_reg.transform(x)
    reg=LinearRegression()
    reg.fit(X_poly,y)
    a = reg.predict(X_poly)
    plt.figure(figsize=(10,10))
    plt.plot(a,x,color="blue",label="Calcite")
    plt.legend()
    plt.plot(a,z,color="black",label="Limestone")
    plt.legend()
    plt.xlabel("Apparent Neutron Limestone Porosity p.u",fontsize=15)
    plt.ylabel("True Porosity p.u",fontsize=15)
    plt.grid()
    question = input("Is NPHI in porosity unit  Y/N : ")
    if (question == "Y") or (question == "y"):
        NPHI = np.array(DATA["NPHI"]).reshape(-1,1)
        poly = poly_reg.transform(NPHI)
        true = reg.predict(poly)
        DATA["Apparent Limestone Porosity"] = true
        message="APPARENT POROSITY HAS BEEN CALCULATED. CHECK YOUR DATA"
        print(message)
        return DATA
    if (question == "N") or (question == "n"):
        NPHI = np.array(DATA["NPHI"]*100).reshape(-1,1)
        poly = poly_reg.transform(NPHI)
        true = reg.predict(poly)
        plt.scatter(true,NPHI)
        DATA["Apparent Limestone Porosity"] = true
        message="APPARENT POROSITY HAS BEEN CALCULATED. CHECK YOUR DATA"
        print(message)
        return DATA
    
   


# In[104]:




# In[82]:


def dolo_lim(DATA):
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.pipeline import make_pipeline
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    global Z
    x=np.array([0,4.5,5,8,12.5,19,22,25,27,30,32,35]).reshape(-1,1)
    y=np.array([1,5,7,10,15,22,25,28,30,33,35,38]).reshape(-1,1)
    z=y
    poly_reg = PolynomialFeatures(degree=3)
    poly_reg.fit(x)
    X_poly = poly_reg.transform(x)
    reg=LinearRegression()
    reg.fit(X_poly,y)
    a = reg.predict(X_poly)
    Z = a
    plt.figure(figsize=(10,10))
    plt.plot(a,x,color="red",label="Dolomite")
    plt.legend()
    question = input("Is NPHI in porosity unit  Y/N : ")
    if (question == "Y") or (question == "y"):
        NPHI = poly_reg.transform(np.array(DATA["NPHI"]).reshape(-1,1))
        NPHI = reg.predict(NPHI)
        z = DATA["NPHI"]
        plt.scatter(NPHI,z)
        plt.plot(np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),color="black",label="Limestone")
        plt.legend()
        plt.grid()
        
        DATA["Apparent Limestone Porosity"]= NPHI
        message="APPARENT POROSITY HAS BEEN CALCULATED. CHECK YOUR DATA"
        print(message)
        return DATA
    if (question == "N") or (question == "n"):
        NPHI = poly_reg.transform(np.array(DATA["NPHI"]*100).reshape(-1,1))
        NPHI = reg.predict(NPHI)
        z = DATA["NPHI"]*100
        plt.scatter(NPHI,z)
        plt.plot(np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),np.array([-1.4,0,5,10,15,20,25,30,35]).reshape(-1,1),color="black",label="Limestone")
        plt.legend()
        plt.grid()
        DATA["Apparent Limestone Porosity"]= NPHI
        message="APPARENT POROSITY HAS BEEN CALCULATED. CHECK YOUR DATA"
        print(message)
        return DATA
    
   


# In[83]:



# In[91]:


get_ipython().system('pip install -e C:\\Users\\windowsChimp\\Desktop\\RUN2\\NEW')


# In[92]:


import NPHIconvert


# In[ ]:




