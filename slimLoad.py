import pandas as pd

def slimload(args, path):
    df = pd.DataFrame()
    load = pd.read_csv(path, iterator=True, chunksize=1000)
    for i in load:
        table = i.dropna(subset=args)
        df = pd.concat([df, table])
    df = df.dropna(axis=1, how='all')
    return df


if __name__ == "__main__":
    #get all rows where this column is not NaN
    out = slimload(['avatar_gender'], 'data/logs.csv')
    #save to output
    out.to_csv("big_avatar_gender_output.csv")
