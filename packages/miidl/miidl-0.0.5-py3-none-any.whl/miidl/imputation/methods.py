def knn(df):
    import pandas as pd
    try:
        from sklearn.impute import KNNImputer
    except:
        import sys
        print("The module 'scikit-learn' is not found, please install first.")
        print("\tconda install -c conda-forge scikit-learn")
        sys.exit(0)
    imputer = KNNImputer()
    data = imputer.fit_transform(df.to_numpy())
    return pd.DataFrame(data, index=df.index, columns=df.columns)

def minimum(df):
    df = df.T
    mins = df.min().to_dict()
    return df.fillna(mins).T

def median(df):
    df = df.T
    medians = df.median().to_dict()
    return df.fillna(medians).T

def mean(df):
    df = df.T
    means = df.mean().to_dict()
    return df.fillna(means).T

def none(df):
    return df