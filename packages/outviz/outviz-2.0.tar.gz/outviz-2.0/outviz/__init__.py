#Univariate Visualization
def univariate_viz(data_frame):
  import matplotlib.pyplot as plt
  import seaborn as sns
  import warnings
  #Separating Categorical & Numerical columns in a list for the ease of visualising.
  categoricals = []
  numericals = []
  for i in data_frame.columns:
    if data_frame.dtypes[i] == 'object' or data_frame.dtypes[i] == 'datetime64':
      categoricals.append(i)
    else:
      numericals.append(i)
  print("\n","Type Visualizing: Numerical Data","\n") 
  for i in numericals:
    warnings.filterwarnings("ignore")
    plt.figure(figsize=(32,4))
    plt.tight_layout(pad=1.0)
    #BoxPLot
    plt.subplot(1,3,1)
    sns.boxplot(data=data_frame, x=data_frame[i])
    
    #Histogram
    plt.subplot(1,3,2)
    sns.histplot(data=data_frame, x=data_frame[i], kde=True)

    #Distribution plot: In future updates "Distplot" will be "Displot"
    plt.subplot(1,3,3)
    sns.distplot(x=data_frame[i], kde=True, rug=True)

    plt.show()

  print("\n","Type Visualizing: Categorical Data","\n") 
  for i in categoricals:
    warnings.filterwarnings("ignore")
    plt.figure(figsize=(32,4))
    plt.tight_layout(pad=1.0)
    #CountPlot
    plt.subplot(1,3,1)
    sns.countplot(data=data_frame, x=data_frame[i])

    plt.show()

#Multivariate Visualization
def multivariate_viz(data_frame, hue=""):
  import matplotlib.pyplot as plt
  import seaborn as sns
  import warnings
  #Separating Categorical & Numerical columns in a list for the ease of visualising.
  categoricals = []
  numericals = []
  for i in data_frame.columns:
    if data_frame.dtypes[i] == 'object' or data_frame.dtypes[i] == 'datetime64':
      categoricals.append(i)
    else:
      numericals.append(i)
  print("Type Visualizing: Categorical Data","\n")   
  col =len(data_frame.columns)
  for j in categoricals:
    warnings.filterwarnings("ignore")
    
    #BoxPLot
    plt.figure(figsize=(32,4))
    for index in range(1, len(numericals)+1):
      plt.subplot(1,col,index)
      plt.tight_layout(pad=1.0)
      if hue =="":
        sns.boxplot(data=data_frame, x=data_frame[j], y=data_frame[numericals[index-1]])
      else:
        sns.boxplot(data=data_frame, x=data_frame[j], y=data_frame[numericals[index-1]], hue=hue)
    plt.show()

    #Violinplot
    plt.figure(figsize=(32,4))
    for index in range(1, len(numericals)+1):
      plt.subplot(1,col,index)
      plt.tight_layout(pad=1.0)
      if hue =="":
        sns.violinplot(data=data_frame, x=data_frame[j], y=data_frame[numericals[index-1]])
      else:
        sns.violinplot(data=data_frame, x=data_frame[j], y=data_frame[numericals[index-1]], hue=hue)
    plt.show()

    #Swarmplot
    plt.figure(figsize=(32,4))
    for index in range(1, len(numericals)+1):
      plt.subplot(1,col,index)
      plt.tight_layout(pad=1.0)
      if hue =="":
        sns.swarmplot(data=data_frame, x=data_frame[j], y=data_frame[numericals[index-1]])
      else:
        sns.swarmplot(data=data_frame, x=data_frame[j], y=data_frame[numericals[index-1]], hue=hue)
    plt.show()
  
  print("\n","Type Visualizing: Numerical Data","\n") 
  for j in numericals:
    warnings.filterwarnings("ignore")
    #ScatterPlot
    plt.figure(figsize=(32,4))
    for index in range(1, len(numericals)+1):
      plt.subplot(1,col,index)
      plt.tight_layout(pad=1.0)
      if hue =="":
        sns.scatterplot(data=data_frame, x=data_frame[j], y=data_frame[numericals[index-1]])
      else:
        sns.scatterplot(data=data_frame, x=data_frame[j], y=data_frame[numericals[index-1]], hue=hue)
    plt.show()

#Zscore
def zscore_outliers(data_frame, replace_with=""):
  from scipy import stats
  import numpy as np
  import pandas as pd 
  #Separating Categorical & Numerical columns in a list for the ease of visualising.
  numericals = []
  for i in data_frame.columns:
    if data_frame.dtypes[i] == 'object' or data_frame.dtypes[i] == 'datetime64':
      pass
    else:
      numericals.append(i)

  df1 = pd.DataFrame()
  for i in numericals:
    df1[i] = data_frame[i]
  Zscore = stats.zscore(df1, ddof =1)
  Zscore = pd.DataFrame(Zscore, columns= df1.columns)

  #Filtering outliers using Zscore:
  threshold = 3
  for i in df1.columns:
    outliers = [] 
    for j in range(len(Zscore[i])):
      if (Zscore[i][j] > threshold) or (Zscore[i][j] < (-threshold)):
        outliers.append(data_frame[i][j])

    if replace_with == "":
      print("Outliers in {} are : {}".format(i, outliers))
      print("Total Outlies: ", len(outliers),"\n")

    else:
      #Removing duplicates values and recreate oulier list :
      outliers = set(outliers)
      outliers = list(outliers)

      #Getting index for outliers.
      outlier_index=[]
      for m in outliers:
        for n in range(len(data_frame[i])):
          if data_frame[i][n] == m:
            outlier_index.append(n)

      #For each of the column, the NAN value is replaced with given input method
      #inplace = True will replace the values in the dataset
      if replace_with == "mean":
        data_frame[i] = data_frame[i].replace(data_frame[i][k], np.NaN)
        data_frame[i].fillna(round(data_frame[i].mean(), 2), inplace = True)
      elif replace_with == "median":
        data_frame[i] = data_frame[i].replace(data_frame[i][k], np.NaN)
        data_frame[i].fillna(round(data_frame[i].median(), 2), inplace = True)
      elif replace_with == "mode":
        data_frame[i] = data_frame[i].replace(data_frame[i][k], np.NaN)
        data_frame[i].fillna(round(data_frame[i].mode(), 2), inplace = True)
      else:
        print(f"Replace with {replace_with} is not possible")

#Interquertile Range(IQR):
def iqr_outliers(data_frame, replace_with=""):
  import numpy as np
  import pandas as pd 
  #Separating Categorical & Numerical columns in a list for the ease of visualising.
  numericals = []
  for i in data_frame.columns:
    if data_frame.dtypes[i] == 'object' or data_frame.dtypes[i] == 'datetime64':
      pass
    else:
      numericals.append(i)

  df1 = pd.DataFrame()
  for i in numericals:
    df1[i] = data_frame[i]

  #Filtering outliers using IQR:
  for i in df1.columns:
    Q1 = np.percentile(data_frame[i], 25)
    Q2 = np.percentile(data_frame[i], 50)  
    Q3 = np.percentile(data_frame[i], 75)
    IQR = Q3 - Q1
    low_lim = Q1 - 1.5 * IQR
    up_lim = Q3 + 1.5 * IQR

  #Filtering outliers using Interquertile Range(IQR):
    outlier =[]
    for j in range(len(data_frame[i])):
      if (data_frame[i][j] > up_lim) or (data_frame[i][j] < low_lim): 
        outlier.append(data_frame[i][j])

    if replace_with == "":
      print("Outliers in {} are : {}".format(i, outlier))
      print("Total Outlies: ", len(outlier),"\n")

    else:
      #Removing duplicates values and recreate oulier list :
      outliers = set(outlier)
      outliers = list(outlier)

      #Getting index for outliers.
      outlier_index=[]
      for m in outliers:
        for n in range(len(data_frame[i])):
          if data_frame[i][n] == m:
            outlier_index.append(n)

      #Replacing Outliers with NaN at index
      if replace_with == "mean":
        data_frame[i] = data_frame[i].replace(data_frame[i][k], np.NaN)
        data_frame[i].fillna(round(data_frame[i].mean(), 2), inplace = True)
      elif replace_with == "median":
        data_frame[i] = data_frame[i].replace(data_frame[i][k], np.NaN)
        data_frame[i].fillna(round(data_frame[i].median(), 2), inplace = True)
      elif replace_with == "mode":
        data_frame[i] = data_frame[i].replace(data_frame[i][k], np.NaN)
        data_frame[i].fillna(round(data_frame[i].mode(), 2), inplace = True)
      elif replace_with == "cap":
        for j in outlier_index:
          if (data_frame[i][j] > up_lim):
            data_frame[i].replace(data_frame[i][j], round(up_lim, 2), inplace=True)
          elif (data_frame[i][j] < low_lim):
            data_frame[i].replace(data_frame[i][j], round(low_lim, 2), inplace=True)
          else:
            pass
      else:
        print(f"Replace with {replace_with} is not possible")