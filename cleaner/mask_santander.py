def main():
    """This Program loads .csv files saved from Santander online banking"""
    """Masks sensitive data and replaces it with xxxxxx"""

    #set run parameters
    source='C:/Py/data/sensitive/'
    output='C:/Py/data/masked/'
    scope=['2023','2024']

    for year in scope:
        #load contents of the file into a string
        text = open(source+'santander_'+year+'.txt', 'r')
        text = ''.join([i for i in text])

        # search and replace the contents
        text = text.replace('20-00-00', '00-00-00')
        text = text.replace('12345678', '00000001')
        text = text.replace('200000 12345678', '00-00-00 00000001')
        text = text.replace('Alex', 'Self')
        text = text.replace('Becky', 'Spouse')
        text = text.replace('James', 'Son')
        text = text.replace('Rachel', 'Daughter')
        text = text.replace('Barclays', 'Employer')
        text = text.replace('Nick', 'Friend')
        text = text.replace('Tony', 'Friend')
        text = text.replace('Olivia', 'Friend')
        text = text.replace('LB OF BARNET', 'Council')
        text = text.replace('LDN BORO REDBRIDGE', 'Council')

        # open file year.csv in write modea and write to it
        x = open(output+'santander_'+year+'.txt','w')
        x.writelines(text)
        x.close()

        print('Year',year+': saved',len(text),'characters to output .csv file')
        del text,x
    return()

if __name__ == "__main__":
    main()
