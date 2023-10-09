######################
## Helper functions ##
######################

# function to cap extreme values
def extreme_cap(df, num_std_dev):
    df_capped = df
    for col in descr_table:
        v = descr_table[col]["std"] * num_std_dev
        hi = descr_table[col]["mean"] + v
        lo = descr_table[col]["mean"] - v
        df_capped[col] = df_capped[col].apply(lambda x: hi if x > hi else x)
        df_capped[col] = df_capped[col].apply(lambda x: lo if x < lo else x)
    return df_capped
