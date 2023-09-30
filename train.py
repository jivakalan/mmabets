#############
## Imports ##
#############
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score


###################
# Get dataset #####
###################

full_fights = pd.read_csv('full_fights.csv')

column_names = [ '','','']
train_set = pd.read_csv('', names =column_names)

test_set = pd.read_csv('',skiprows=1,names = column_names)

##get some initial info
train_set.info()
test_set.info() 
##remove whitespaces and deal with ? values
train_set.replace(' ?',np.nan,inplace=True)
test_set.replace(' ?',np.nan,inplace=True)

#remove dupes
train_set= train_set.drop_duplicates()
test_set = test_set.drop_duplicates()

##descr table will have std dev and mean values for use in extreme_cap fn 
descr_table = train_set.describe()
a= test_set.describe()

##counts/unique values
for name in column_names:
    print(train_set[name].value_counts())
##unique values
for name in column_names:
    print(name, train_set[name].unique())
 
#cols_to_filter =["age","education_num","capital_gain","hrs_per_week","fnlwgt","capital_loss"]


######################
## Helper functions ##
######################
    
#function to cap extreme values 
def extreme_cap(df, num_std_dev):
    df_capped = df
    for col in descr_table:
        v = descr_table[col]["std"]*num_std_dev
        hi = descr_table[col]["mean"]+v
        lo = descr_table[col]["mean"]-v
        df_capped[col]=df_capped[col].apply(lambda x: hi if x > hi else x)
        df_capped[col]=df_capped[col].apply(lambda x: lo if x < lo else x)
    return df_capped


def model_evaluate(predictions):
    print('AUC:', round(roc_auc_score(y_true=test_target
                                     ,y_score=predictions)*100
                        ,2))
    print('Precision:', round(precision_score(y_true=test_target
                                            , y_pred= predictions
                                            , average='weighted')*100
                            ,2))




#####################
## Pre-processing ##
####################

##run this if want to cap values
#cap values in train set
train_set = extreme_cap(train_set, 1.5)
##cap extreme values on test set 
test_set = extreme_cap(test_set, 1.5)


#convert income to binary output
train_set["income"] = train_set["income"].apply(lambda x: 0 if x==' <=50K' else 1)
test_set["income"] = test_set["income"].apply(lambda x: 0 if x==' <=50K.' else 1)


#split target from features
train_features, train_target = train_set.iloc[:,:-1], train_set.iloc[:,-1]
test_features, test_target = test_set.iloc[:,:-1], test_set.iloc[:,-1]

#one-hot encoding for categorical variables
col_cat =["workclass","education","marital_status","occupation","relationship","race","sex","native_country"] 

for name in col_cat:
    name_df = pd.DataFrame( train_features[name])
    dum_df  = pd.get_dummies(name_df, prefix=[name+'_'] )
    train_features = train_features.join(dum_df)
    
train_features.drop(col_cat, axis='columns',inplace=True)
 

##one-hot-encoding test features
for name in col_cat:
    name_df = pd.DataFrame(test_features[name])
    dum_df  = pd.get_dummies(name_df, prefix=[name+'_'] )
    test_features = test_features.join(dum_df)
    
test_features.drop(col_cat, axis='columns',inplace=True)

##add column native_country__ Holand-Netherlands so that columns are same in test and train
test_features["native_country__ Holand-Netherlands"]=0
#sorting test and train features so order is identical
test_features = test_features.reindex(sorted(test_features.columns), axis=1)
train_features = train_features.reindex(sorted(train_features.columns), axis=1)


######################
## Model 1: XGBoost ##
######################

xgb_model = xgb.XGBClassifier( objective= 'binary:logistic'
                         , colsample_bytree= 0.3
                         , learning_Rate =.1
                         , max_depth=10
                         , verbosity =0
                         )
xgb_model.fit(train_features, train_target)

#######################
## XGB Performance   ##
#######################

xgb_preds =xgb_model.predict(test_features)
model_evaluate(xgb_preds)


############################
## Model 2 - RandomForest ##
############################

model_rf = RandomForestClassifier(n_estimators= 100 ##num trees
                                 , max_depth=10     ##num levels in forest
                                 , random_state=0   
                                 , min_samples_split =2  #min num samples to split on
                                 , min_samples_leaf = 2    #min samples at each node
                                 )

model_rf.fit(train_features, train_target)


###############################
## Randomforest Performance ##
##############################

rf_preds = model_rf.predict(test_features)
model_evaluate(rf_preds)


##variable importance plot 
var_imp = model_rf.feature_importances_
feature_names = pd.DataFrame(train_features.columns)
var_imp_pd = pd.DataFrame(var_imp)

var_imp_merge = pd.concat([var_imp_pd,feature_names],axis=1)
var_imp_merge.columns =['Importance','Feature']
var_imp_merge=var_imp_merge.sort_values(by='Importance', ascending=False)


var_plot = var_imp_merge.head(10)

var_plot.plot.bar(x='Feature',y='Importance')

#################################################################################
#########################################
##  Randomforest Hyperparameter Tuning ##
#########################################


grid = { 'n_estimators': list(range(75,300, 25))
       , 'max_depth': list(range(5,50, 5))
       , 'min_samples_split': [2,4,6]
       , 'min_samples_leaf': [1,2,3,4]
       , 'bootstrap': [True,False]}

rf_tuning = RandomizedSearchCV(  estimator=model_rf
                               , param_distributions= grid
                               , n_iter = 10
                               , scoring='roc_auc'
                               , cv = 5
                               , verbose=2
                               , random_state=0
                               , return_train_score=True)

## this will take a few minutes
rf_tuning.fit(train_features, train_target)

best_params_rf= rf_tuning.best_params_
best_model = rf_tuning.best_estimator_
best_model.fit(train_features,train_target)
best_preds = best_model.predict(test_features)

best_roc = roc_auc_score(y_true=test_target, y_score=best_preds)
print('Tuned AUC:', round(best_roc*100,2))


##############################
## Model 2 - Neural Network ##
##############################

from keras.models import Sequential
from keras.layers import Dense

model_nn = Sequential()
model_nn.add(Dense(12, input_dim=105, activation='relu'))
model_nn.add(Dense(8, activation='relu'))
model_nn.add(Dense(1, activation='sigmoid'))

model_nn.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

model_nn.fit(train_features, train_target, epochs = 50, batch_size = 100)

nn_preds = model_nn.predict(test_features)
nn_preds = [round(x[0]) for x in nn_preds]
model_evaluate(nn_preds)



