import pandas as pd

def main():
    """This Program loads .csv exports saved from Barclays online banking"""
    """Supported formats: statements saved after Year 2021"""
    """Returns a Pandas DataFrame object in ascending Date order"""

    source='C:/Barclays/'
    scope=['2022','2023','2024']
    for year in scope:
        df = load_csv_as_df(source,year)
        if not df.empty:
            print('Year',year+': loaded',df.shape[0],'records')
            # print(df.to_csv(index=False))
    return(df)

def load_csv_as_df(path:str,year:str) -> pd.DataFrame:
    """This function loads barclays .csv format statements, cleans them and returns a DataFrame"""

    barclays=pd.DataFrame
    #set desired columns & datatypes to read from .csv file
    try:
        barclays = pd.read_csv(path+year+'.csv', sep=',', usecols=['Date','Subcategory','Memo','Amount'], dtype={'Date':str,'Subcategory':str,'Memo':str,'Amount':float})

        #set formats and clean data
        barclays = barclays.round({'Amount':2})
        barclays['Date'] = barclays['Date'].str.replace('/','-')
        barclays.replace(',','', regex=True, inplace=True)
        barclays['Memo']=barclays['Memo'].str.replace(' BGC','').str.replace(' FT','').str.replace(' ASD','').str.replace(' BBP','').str.replace('C T','').str.replace(' CB','').str.replace(' BCC','').str.replace(' CLP','').str.replace(' CLR','').str.replace(' TFR','').str.replace(' UNP','').str.replace('FIRST DDR','').str.replace(' DDR','').str.replace(' DD','')
    
        #remove whitespaces from columns
        df_obj = barclays.select_dtypes(['object'])
        barclays[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    
        #split Memo column to extract Payee and Reference information
        barclays[['Payee','Reference']] = barclays.Memo.str.split('\t', expand = True)
        barclays.Payee = barclays.Payee.replace(r'\s+', ' ', regex=True)
        barclays.Reference = barclays.Reference.replace(r'\s+', ' ', regex=True)
        barclays = barclays.drop(['Memo'], axis=1)
    
        #remove whitespaces from columns
        df_obj = barclays.select_dtypes(['object'])
        barclays[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    
        #reverse dataframe to get records in ascending date order, choose specific columns to be returned
        barclays = barclays.iloc[::-1,[0,2,3,4,1]]
    except:
        print('ERROR: Input file',path+year+'.csv','not found!')

    return(barclays)

if __name__ == "__main__":
    main()
