import pandas as pd

def main():
    """This Program loads .txt exports saved from Santander online banking"""
    """Supported formats: statements saved after Year 2023 onwards"""
    """Returns a Pandas DataFrame object in ascending Date order"""

    source='C:/Py/data/masked/'
    scope=['2023','2024']
    for year in scope:
        df = load_txt_as_df(source,year)
        if not df.empty:
            print('Year',year+': loaded',df.shape[0],'records into a dataframe')
#            print(df.to_csv(index=False))
    return(df)

def load_txt_as_df(path:str,year:str) -> pd.DataFrame:
    """This function loads santander .txt format statements, cleans them and returns a DataFrame"""

    #initialisations
    santander=pd.DataFrame(columns = ['Date','Description','Reference1','Mandate','Amount'])

    #load txt file
    try:
        with open(path+'santander_'+year+'.txt', 'r') as f:
            lines = f.readlines()
    except:
        print('ERROR: Input file',path+'santander_'+year+'.txt','not found!')

    lines.reverse()
    datex,desc,ref1,mandate,amount='','','','',0.0
    for line in lines:
        if line.find('Amount:')==0: amount=line.replace('Amount:','').strip()
        if line.find('Description:')==0:
            desc=line.replace('Description:','').strip()
            ref1=''
            if desc.find('MANDATE')!=-1: 
                mandate=desc[desc.find('MANDATE'):len(desc)].strip()
                endd=desc.find('MANDATE')
            else: endd=len(desc)
            if desc.find('REFERENCE')!=-1: ref1=desc[desc.find('REFERENCE'):endd].replace('REFERENCE','').replace(',','').strip()
            if ref1=='':
                if desc.find('REF.')!=-1: ref1=desc[desc.find('REF.'):endd].replace('REF.','').replace(',','').strip()
            if ref1=='':
                if desc.find('REF')!=-1: ref1=desc[desc.find('REF'):endd].replace('REF','').replace(',','').strip()
            desc=desc.replace(mandate,'').replace(ref1,'').strip()
            
        if line.find('Date:')==0:
            datex=line.replace('Date:','').strip()
            # print(datex,desc,ref1,mandate,amount)

            # append new row to dataframe
            new_row = pd.DataFrame([{'Date':datex,'Description':desc,'Reference1':ref1,'Mandate':mandate,'Amount':amount}])
            santander = pd.concat([santander, new_row])
            datex,desc,ref1,mandate,amount='','','','',0.0

    #set formats and clean numbers/dates
    if not santander.empty:
        santander = santander.round({'Amount':2})
        santander['Date'] = santander['Date'].str.replace('/','-')

        #remove whitespaces from columns
        df_obj = santander.select_dtypes(['object'])
        santander[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    
        # print(santander.to_csv(index=False))

    return(santander)

if __name__ == "__main__":
    main()
