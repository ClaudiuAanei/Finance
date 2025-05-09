import pandas as pd
import io


from_saving_account = "INSTANT CREDIT TRANSFER FROM BE49 7430 7777 0671"
to_saving_account = "SENDING MONEY INSTANTLY TO BE49 7430 7777 0671"

stores = ['DEPOSIT ATM', 'A-PACK BV /A/', 'KBC BANK NV CASHBACK KATE COINS', 'COLRUYT', 'ALDI', 'LIDL', 'ALBERT HEIJN',
          'BAKKERIJ', 'HEDIYE', 'TAKEAWAY.COM', 'JOHAN P2P MOBILE', 'DECATHLON', 'IKEA', 'PRIMARK', 'ACTION', 'WOONBUREAU',
          'FLIBTRAVEL', 'MAES ', 'DATS 24', 'AVIA', 'PROXIMUS', 'LUMINUS SA', 'EDF LUMINUS', 'WATERGROEP',
          'ARGENTA ASSURANTIES', 'BUY WAY', 'REPAYMENT INSTALMENT LOAN', 'HELAN', 'SETTLEMENT MASTERCARD SILVER',
          'PRAKTIJKCENTRUM', 'APOTEEK', 'KINE VAN DUYSEN', 'MEDISCH LABO', 'AZ SINT-LUCAS', 'AZ MIDDELARES',
          'DIRK DE WITTE KAPPERS', 'KINESIST', 'TIME DE JAEGER MARC & VAN T', 'TRANSFER FROM SAVINGS ACCOUNT',
          'SENDING MONEY TO SAVINGS ACCOUNT', 'STAD LOKEREN', 'APB-GEZINNEN', 'CVO FOCUS', 'STD BH', 'BOOKING.COM',
          'NAPOLEON GAMES NV', 'SONY INTERACTIVE', 'ACV OOST-VLAANDEREN LEDENBIJDRAGEN', 'KBC PLUS ACCOUNT',
          'CASH WITHDRAWAL', 'MEDIA MARKT', 'KREFEL', 'DE KEUKELAERE', 'SPORTCENTRUM DE DAM',
          'SENDING MONEY INSTANTLY TO', 'DIRK P2P MOBILE','REVOLUT','KRUIDVAT', 'MARIA MIDDELARE'
          ]

categories = {
    'income': ['DEPOSIT ATM', 'A-PACK BV /A/', 'KBC BANK NV CASHBACK KATE COINS'],
    'groceries': ['COLRUYT', 'ALDI', 'LIDL', 'ALBERT HEIJN', 'BAKKERIJ', 'HEDIYE'],
    'bars & restaurants': ['TAKEAWAY.COM', 'JOHAN P2P MOBILE'],
    'shopping': ['DECATHLON', 'IKEA', 'PRIMARK', 'ACTION'],
    'housing': ['WOONBUREAU'],
    'mobility': ['FLIBTRAVEL', 'DATS 24', 'AVIA'],
    'utilities & telecom': ['PROXIMUS', 'LUMINUS SA', 'EDF LUMINUS', 'WATERGROEP'],
    'finance & insurances': ['ARGENTA ASSURANTIES', 'BUY WAY', 'REPAYMENT INSTALMENT LOAN', 'HELAN', 'SETTLEMENT MASTERCARD SILVER'],
    'personal care': ['PRAKTIJKCENTRUM', 'APOTEEK', 'KINE VAN DUYSEN', 'MEDISCH LABO','AZ SINT-LUCAS' ,'AZ MIDDELARES', 'DIRK DE WITTE KAPPERS', 'KINESIST', 'TIME DE JAEGER MARC & VAN T'],
    'savings': [],
    'own accounts': ['TRANSFER FROM SAVINGS ACCOUNT', 'SENDING MONEY TO SAVINGS ACCOUNT'],
    'governament': ['STAD LOKEREN', 'APB-GEZINNEN'],
    'education': ['CVO FOCUS', 'STD BH'],
    'leisure & entertainment': ['BOOKING.COM', 'NAPOLEON GAMES NV', 'SONY INTERACTIVE'],
    'services': ['ACV OOST-VLAANDEREN LEDENBIJDRAGEN', 'KBC PLUS ACCOUNT'],
    'atm withdraw' : ['CASH WITHDRAWAL'],
    'others': ['MEDIA MARKT', 'KREFEL','DE KEUKELAERE', 'SPORTCENTRUM DE DAM', 'SENDING MONEY INSTANTLY TO', 'DIRK P2P MOBILE']
}

class ProcessFile:
    def __init__(self,name= 'No_Name', file= None, sep= ','):
        self.name = name
        self.file = file
        self.sep = sep


    def process_file(self):

        if self.file:
            lines = self.file.splitlines()

            line_1, line_2 = lines[0].strip().split(self.sep), lines[1].strip().split(self.sep)

            len1, len2 = len(line_1), len(line_2)

            if len1 < len2:
                line_1 += [''] * (len2 - len1)
                lines[0] = self.sep.join(line_1)

            corrected_content = '\n'.join(lines)
            corrected_file = io.StringIO(corrected_content)
            return corrected_file

        else:
            return None

    @staticmethod
    def convert_tabel(corrected_file):
        if corrected_file:
            df = pd.read_csv(corrected_file, sep= ';')
            columns_to_keep = ["Name", "Date", "Description", "Amount", "Currency"]

            new_df = df[columns_to_keep].copy()
            new_df['Category'] = "uncategorized"
            new_df['Amount'] = new_df['Amount'].str.replace(',', '.')
            new_df['Date'] = pd.to_datetime(new_df['Date'], dayfirst= True, errors='coerce')
            new_df['Amount'] = new_df['Amount'].astype(float)

            return new_df

        else:
            return None

    def change_description(self,df_filtrat):

        """Modifica descrierea pentru o citire mai usoara."""
        df_filtrat.loc[df_filtrat['Description'].str.contains(from_saving_account, case=False, na=False), 'Description'] = str(categories['own accounts'][0])
        df_filtrat.loc[df_filtrat['Description'].str.contains(to_saving_account, case=False, na=False), 'Description'] = str(categories['own accounts'][1])
        df_filtrat.loc[df_filtrat['Name'].str.contains('AANEI-AANEI', case=False, na=False), 'Name'] = str(self.name)

        for store in stores:
            df_filtrat.loc[df_filtrat['Description'].str.contains(store, case=False, na=False), 'Description'] = str(store)

        return df_filtrat


    def get_tabel(self):
        """Afiseaza tot tabelul procesat."""
        df = self.convert_tabel(self.process_file())

        if df.empty:
            return None

        new_df = self.change_description(df)

        return new_df


    def get_last_month_tabel(self):
        """Afiseaza doar ultima luna din tabelul procesat."""
        df = self.convert_tabel(self.process_file())

        if df.empty:
            return None

        current_date = pd.to_datetime('today')

        first_day_current_month = current_date.replace(day=1)
        first_day_last_month = (first_day_current_month - pd.DateOffset(days=1)).replace(day=1)

        first_day_of_last_month = pd.Timestamp(first_day_last_month).normalize()

        last_month_data = df[(df['Date'] >= first_day_of_last_month) & (df['Date'] < first_day_current_month)]
        new_df = self.change_description(last_month_data)

        return new_df