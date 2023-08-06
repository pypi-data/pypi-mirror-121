import logging
def prepare_data(df):
    """It is used to separate dependent and independent features        

    Args:
        df ([pd.DataFrame]): [It is a panda Dataframe]

    Returns:
        [Tuple]: [It returns the tuple of dependent and independent features ]
    """
    logging.info("Separating Dependent and Independent Features")
    X=df.drop("y",axis=1)
    y=df["y"]
    return X,y