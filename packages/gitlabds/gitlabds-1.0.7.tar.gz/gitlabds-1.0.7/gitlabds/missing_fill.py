def missing_fill(df=None, columns='all', method='zero', inplace=False):
    
    import pandas as pd
    import numpy as np
    
    if inplace == True:
        df2 = df
        
    else:
        df2 = df.copy(deep=True)
        
    #Get all columns with missing values
    missing_cols = set(df.columns[df.isnull().any()].tolist())

    if columns == 'all':
        #Pull all numeric columns to miss fill
        all_numeric = set(df.select_dtypes(include=['number']).columns.tolist())
        #print(all_numeric)
        
        #Remove columns that have no missing values
        var_list = list(all_numeric & missing_cols)
        
    else:
        var_list = columns
    
    print(f'\nMissing Fill')
    print(f'Columns selected for {method} filling: {columns}\n')
    print(f'Actual columns with missing values that will be {method} filled: {var_list}\n')
            
    if method == 'zero':
        df[var_list] = df[var_list].fillna(0)

    if method == 'mean':
        for v in var_list:
            fill_value = df[v].mean()
            df[v] = df[v].fillna(fill_value)

    if method == 'median':
        for v in var_list:
            fill_value = df[v].median()
            df[v] = df[v].fillna(fill_value)

    if method == 'drop_row':
        print('drop row...nothing will happen. This is future functionality.')

    if method == 'drop_column':
        print('drop column...nothing will happen. This is future functionality')
     
    return df2
