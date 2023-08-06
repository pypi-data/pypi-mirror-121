from scipy.stats import pearsonr, pointbiserialr, chi2_contingency
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# from statistics import mean
# from sklearn.impute import SimpleImputer
# from sklearn.preprocessing import MinMaxScaler, StandardScaler
# from sklearn.decomposition import PCA
# from lightgbm import LGBMClassifier
# from catboost import CatBoostClassifier
# from xgboost import XGBClassifier
# from sklearn.ensemble import VotingClassifier
# from sklearn.model_selection import GridSearchCV
# from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from math import ceil

def univar_analysis(df):
    for i in df:
        if df[i].dtype == 'object': 
            sns.barplot(df[i].value_counts().index,df[i].value_counts())
            plt.title(i)
            plt.show()
        else:
            fig, ax = plt.subplots(1,2,figsize=(10,4))
            fig.tight_layout()
            ax[0].hist(df[i])
            ax[0].set_title(i)
            ax[1].boxplot(df[i])
            ax[1].set_title(i)
            plt.show()

def dichotomous_categorical_visual(df,target):
    if len(df[target].unique()) == 2:
        df_0 = df[df[target] == 0]
        df_1 = df[df[target] == 1]
        for i in df:
            if df[i].dtype == 'object':
                fig, axes = plt.subplots(1,2,figsize=(16,6))
                pd.crosstab(df_0[target],df_0[i]).plot(kind='bar',ax=axes[0])
                pd.crosstab(df_1[target],df_1[i]).plot(kind='bar',ax=axes[1])
    else:
        print("Your target variable is not dichotomous!")

def categorical_visual(x,y,kind,data):
    sns.catplot(x=x, y=y, kind=kind, data=tips)

def categorical_multivariate_visual(x,y,hue,kind,data):
    sns.catplot(x=x, y=y, hue=hue, kind=kind, data=tips)

def continuous_visual(df,target):
    rows = math.ceil(len(train.select_dtypes('float').columns-1)/2)
    cols = 2
    # fig, axes = plt.subplots(rows,cols,figsize=(16,6))
    df_float = train.select_dtypes('float')
    for i in df_float:
        # axes[0] = 
        plt.subplot(rows,cols,i+1)
        plt.imshow(df_float[i])
        plt.show()


def chi2_test():
    pass


def pbs_test():
    num_summary = []
    for i in df_num:
        pbs = pointbiserialr(df_num[i],df_num[target])
        score_to_add = {}
        score_to_add['var'] = i
        score_to_add['pbs corr'] = pbs[0]
        score_to_add['pbs p-value'] = pbs[1]
        num_summary.append(score_to_add)
    df_num = pd.DataFrame(num_summary)
    df_num

def pearson_test():
    pass

def outlier_treatment(): #maybe don't need this
    pass

def fill_null():
    pass

def normalisation():
    pass

def standardisation():
    pass

def one_hot_encoding():
    pass

def label_encoding():
    pass

def ordinal_encoding():
    pass

def pca():
    pass

#addigional boosted trees models and classifiers?
#gridsearch?