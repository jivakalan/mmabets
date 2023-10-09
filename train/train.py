####################################################################
##                          Imports                             ###
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.metrics import confusion_matrix
from train.tools.helper import *
import pickle
# from train.tools.evaluator import *
# todo update yml file conda env update
####################################################################

###################
# Get dataset #####
###################

df_ds_dataset = pd.read_csv('train/data/ds_dataset.csv', index_col = False)
print(df_ds_dataset.shape)
df_ds_dataset =df_ds_dataset.drop_duplicates()
print(df_ds_dataset.shape)
df_ds_dataset['Fight_ID'] = df_ds_dataset['Fight_ID'].astype('category')
df_ds_dataset['Fighter_ID_0'] = df_ds_dataset['Fighter_ID_0'].astype('category')
df_ds_dataset['Fighter_ID_1'] = df_ds_dataset['Fighter_ID_1'].astype('category')


X = df_ds_dataset.drop(columns=['Fighter_0_Outcome','Fight_ID','Fighter_ID_0','Fighter_ID_1'])  # Features
y = df_ds_dataset['Fighter_0_Outcome']  # Target

# split train + temp set (80-20 train-temp)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)

# split test + validation ste (
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.75, random_state=42)

del X_temp, y_temp

##get some initial info
X_train.info()
X_test.info()

# descr table will have std dev and mean values for use in extreme_cap fn
descr_table = X_train.describe()
a= X_test.describe()

column_names =  X_train.columns.tolist()
# counts/unique values
for name in column_names:
    print(X_train[name].value_counts())
##unique values
for name in column_names:
    print(name, X_train[name].unique())
 



#####################
## Pre-process ##
####################

##run this if want to cap values
#cap values in train set
# X_train = extreme_cap(X_train, 1.5)
##cap extreme values on test set 
# X_test = extreme_cap(X_test, 1.5)


######################
## Model 1: XGBoost ##
######################

xgb_model = xgb.XGBClassifier( objective= 'binary:logistic'
                         , colsample_bytree= 0.3
                         , learning_Rate =.1
                         , max_depth=10
                         , verbosity =0
                         )
xgb_model.fit(X_train, y_train)

#######################
## XGB Performance   ##
#######################
def get_performance(model, X_test, X_val, y_test, y_val, dataset='test'):
    if dataset == 'test':
        prediction_set =X_test
        ground_truth = y_test
    if dataset == 'validation':
        prediction_set =X_val
        ground_truth = y_val

    predictions = model.predict(prediction_set)
    predictions = pd.Series(predictions)

    classes_to_include =[0,1]
    filtered_indices = [i for i,label in enumerate(ground_truth) if label in classes_to_include]

    y_test_array = np.array(ground_truth)

    y_test_filtered = y_test_array[filtered_indices]
    xgb_preds_filtered = predictions[filtered_indices]

    # Calculate accuracy for the filtered classes: 60%
    accuracy = accuracy_score(y_test_filtered, xgb_preds_filtered)
    print("Accuracy for classes 1 and 2:", round(accuracy * 100, 2))

    # Calculate the confusion matrix for the filtered classes
    cm = confusion_matrix(y_test_filtered, xgb_preds_filtered, labels=classes_to_include)
    print("Confusion Matrix for classes 1 and 2:\n", cm)

    return


get_performance(xgb_model, X_test, X_val, y_test, y_val,dataset = 'test') #86.56
get_performance(xgb_model, X_test, X_val, y_test, y_val,dataset = 'validation') #90.8

with open('train/model/xgb_model.pkl','wb') as model_file:
    pickle.dump(xgb_model,model_file)
with open('score/model/xgb_model.pkl','wb') as model_file:
    pickle.dump(xgb_model,model_file)

############################
## Model 2 - RandomForest ##
############################

model_rf = RandomForestClassifier(n_estimators= 30 ##num trees
                                 , max_depth=10     ##num levels in forest
                                 , random_state=0   
                                 , min_samples_split =2  #min num samples to split on
                                 , min_samples_leaf = 2    #min samples at each node
                                 )
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=0)),  # Replace missing values with 0s
    ('classifier', model_rf)  # Your RandomForestClassifier
])
pipeline.fit(X_train, y_train)


###############################
## Randomforest Performance ##
##############################
# Make predictions
rf_preds = pipeline.predict(X_test)

#get_performance
get_performance(pipeline, X_test, X_val, y_test, y_val,dataset = 'test')  # 84.05
get_performance(pipeline,X_test, X_val, y_test, y_val,dataset = 'validation') #86.22


# Get variable importances
var_imp = pipeline.named_steps['classifier'].feature_importances_
feature_names = X_train.columns

var_imp_merge = pd.DataFrame({'Importance': var_imp, 'Feature': feature_names})
var_imp_merge = var_imp_merge.sort_values(by='Importance', ascending=False)

# Check out the top 10 most important features
var_plot = var_imp_merge.head(10)
print(var_plot)

#################################################################################
#########################################
##  Randomforest Hyperparameter Tuning ##
#########################################


grid = { 'n_estimators': list(range(15,50, 5))
       , 'max_depth': list(range(5,50, 5))
       , 'min_samples_split': [2,4,6]
       , 'min_samples_leaf': [1,2,3,4]
       , 'bootstrap': [True,False]}

rf_tuning = RandomizedSearchCV(  estimator=model_rf
                               , param_distributions= grid
                               , n_iter = 10
                               , scoring='neg_log_loss'  #for multiclass scoring...hm
                               , cv = 5
                               , verbose=2
                               , random_state=0
                               , return_train_score=True)

tuning_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=0)),  # Replace missing values with 0s
    ('classifier', rf_tuning)  # Your RandomForestClassifier
])
## this will take a few minutes
tuning_pipeline.fit(X_train, y_train)

best_params_rf = rf_tuning.best_params_
best_model = rf_tuning.best_estimator_

best_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=0)),  # Replace missing values with 0s
    ('classifier', best_model)  # Your RandomForestClassifier
])

best_pipeline.fit(X_train,y_train)
get_performance(best_pipeline,X_test,X_val,y_test,y_val,dataset='test')  # 83.98
get_performance(best_pipeline,X_test,X_val,y_test,y_val,dataset='validation') #86.85

##############################
## Model 2 - Neural Network ##
##############################

from keras.models import Sequential
from keras.layers import Dense


df_ds_dataset_nn = df_ds_dataset[df_ds_dataset.Fighter_0_Outcome.isin([0,1])]

X = df_ds_dataset_nn.drop(columns=['Fighter_0_Outcome','Fight_ID','Fighter_ID_0','Fighter_ID_1'])  # Features
y = df_ds_dataset_nn['Fighter_0_Outcome']  # Target

# split train + temp set (80-20 train-temp)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)

# split test + validation ste (
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.75, random_state=42)

del X_temp, y_temp

model_nn = Sequential()
model_nn.add(Dense(12, input_dim=68, activation='relu'))
model_nn.add(Dense(8, activation='relu'))
model_nn.add(Dense(1, activation='sigmoid'))



model_nn.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

model_nn.fit(X_train, y_train, epochs = 50, batch_size = 100)

nn_preds = model_nn.predict(X_test)
nn_preds = [round(x[0]) for x in nn_preds]





