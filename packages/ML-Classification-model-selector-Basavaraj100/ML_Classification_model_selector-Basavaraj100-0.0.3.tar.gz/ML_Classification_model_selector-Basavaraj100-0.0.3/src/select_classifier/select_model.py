
# importing libraries related to data manipulation
import pandas as pd
import numpy as np 
import klib
#  for visualization
import matplotlib.pyplot as plt 
import seaborn as sns 

# importing libraries related to classification models
from scipy.stats import zscore
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier


# metrics related packages
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score



# for data preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

#  ignore warmings
import warnings
warnings.filterwarnings('ignore')

#  to indicate progress
from tqdm import tqdm

#  for logging
import logging

logging_str="[%(asctime)s:%(levelname)s:%(model)s]%(message)s"
logging.basicConfig(filename='activity.log',level=logging.INFO,format=logging_str)


# ===================================================================================




class Model_Selector:
    '''this class help to select
    suitable model for given data frame.
    the models used are
    a) Logistic regression
    b)KNN classifier
    c)Decision tree
    d)Random forest
    e)Adaboostclassifier
    f)gradient boost classifier
    g)xgboost classifier
    h) Lighgbm
    i)catboost'''

    def __init__(self):
        self.model_used=[LogisticRegression,KNeighborsClassifier,DecisionTreeClassifier,RandomForestClassifier,
        AdaBoostClassifier,GradientBoostingClassifier,XGBClassifier,LGBMClassifier,CatBoostClassifier]
        self.model_names=['LogisticRegression','KNeighborsClassifier','DecisionTreeClassifier','RandomForestClassifier',
                         'AdaBoostClassifier','GradientBoostingClassifier','XGBClassifier','LGBMClassifier','CatBoostClassifier']
    
    
    def model_performances(self,dataframe,label,normalize=False):    
       #------Defining X and y------
        logging.info('Defining X and y')
        x=dataframe.drop(label,axis=1)
        y=dataframe[label]
        
        
       # -------splitting data-------
        logging.info('Splitting data into train and test')
        x_train,x_test,y_train,y_test=train_test_split(x,y,stratify=y,test_size=0.3,random_state=42)
       
    #  scaling the data if normalize=True 
        if normalize==True:
            logging.info('Normalizing the data')
            scale=StandardScaler()
            scale.fit(x_train)
            x_train_scaled=scale.transform(x_train)
            x_test_scaled=scale.transform(x_test)
        
        else:
            pass
        print(x_train.shape,x_test.shape) 
       #------- Data frmale of model performance---------
        model_performance=pd.DataFrame({'model_name':[],'accuracy':[],'Precision score':[],'Recall score':[],'f1_score':[]})
        
       #--------- fitting different models---------
        ind=0
        for Model in tqdm(self.model_used):
            model=Model()
            model.fit(x_train.values,y_train)
            logging.info(f'{self.model_names[ind]} model fitted')
            y_pred=model.predict(x_test.values)
            if y.nunique()==2:

                
                y_test=np.array(y_test).reshape(-1,1)
                y_pred=y_pred.reshape(-1,1)
                accuracy=accuracy_score(y_test,y_pred)
                precision=precision_score(y_test,y_pred)
                recall=recall_score(y_test,y_pred)
                f1=f1_score(y_test,y_pred)
            elif y.nunique()>2:
                accuracy=accuracy_score(y_test,y_pred)
                precision=precision_score(y_test,y_pred,average='weighted')
                recall=recall_score(y_test,y_pred,average='weighted')
                f1=f1_score(y_test,y_pred,average='weighted')
                
            model_performance.loc[ind]=[self.model_names[ind],accuracy,precision,recall,f1]
            print(self.model_names[ind],'model fitted')
            ind+=1
        logging.info('All models fitted')
        self.model_performance=model_performance
        return model_performance.style.highlight_max(subset = model_performance.columns[1:],
                       color = 'lightgreen', axis = 0)
    
    
    def select_best_model(self,based_on='accuracy'):
        '''based_on=['accuracy','Precision score','Recall score','f1_score']'''
        logging.info(f'selecting best model based on {based_on}')
        self.best_model_ind=self.model_performance[self.model_performance[based_on]==self.model_performance[based_on].max()].index[0]
        return self.model_names[self.best_model_ind]
            
        
    def plot_model_performance(self):
        logging.info('Plotting model performances')
        self.model_performance.plot(figsize=(20,8),marker='o')
        plt.xticks(range(len(self.model_performance)),self.model_performance['model_name'].values)
        plt.xticks(rotation=45)
        plt.show()
