import pickle
import json
# import glob
# import os

def load_json(filename):
    with open(filename,'r') as fp:
        file = json.load(fp)
    return file
    
def save_json(filename, yourdict):
    with open(filename,'w') as fp:
        json.dump(yourdict,fp)
    return

def load_pickle(filename):
    with open(filename,'rb') as handle:
        yourdict= pickle.load(handle)
    return yourdict


# `
# def load_latest_pickle():
#     list_of_files = glob.glob('extract\data\*.pickle') # * means all if need specific format then *.csv
#     latest_file = max(list_of_files, key=os.path.getctime)
#     print(latest_file)
#     ufcfightdata = load_pickle(latest_file)
#
#     return ufcfightdata
#
#
# def save_pickle(filename, file):
#     with open(filename,'wb') as handle:
#         pickle.dump(file, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
# #define function to split up table data to represent just one fighter
# def pd_df_spltr(df):
#
#     for column in df.columns:
#
#         if column =='Fighter':
#             continue #don't split fighter name
#         elif column =='Round':
#             continue
#         else:
#             df[['%s_0' %column,'%s_1' %column]] = df[column].str.split("  ", expand=True)
#
#     return df`