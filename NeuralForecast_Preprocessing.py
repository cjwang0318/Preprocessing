import pandas as pd

def insert_ds(df):
    uids = df['unique_id'].unique()  # Select ids
    df_return = pd.DataFrame()
    for id in uids:
        df_temp = df.query('unique_id in @id').reset_index(drop=True)
        start = 1
        df_temp.insert(2, 'ds', range(start, start + df_temp.shape[0]))
        #print(Y_df.shape)
        #print(Y_df.head(20))
        df_return = pd.concat([df_return, df_temp], axis=0, ignore_index=True)
    #print(df_return.tail())
    return df_return

if __name__ == '__main__':
    df = pd.read_csv('./dataset/test.csv', header=None, names=["unique_id", "datetime", "y"])
    #print(df.head())
    df_return=insert_ds(df)
    df_return.to_csv("./dataset/result.csv", index=False)

