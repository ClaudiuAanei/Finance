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
          'SENDING MONEY INSTANTLY TO', 'DIRK P2P MOBILE','REVOLUT','KRUIDVAT', 'MARIA MIDDELARE', 'VAKANTIEGELD',
          'MUCH MORE MARKET BENEL BE BRUXELLES'
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

date_formats = {
    "dd/mm/yyyy": "%d/%m/%Y",
    "mm/dd/yyyy": "%m/%d/%Y",
    "yyyy/mm/dd": "%Y/%m/%d",
    "yyyy/dd/mm": "%Y/%d/%m",
    "dd-mm-yyyy": "%d-%m-%Y",
    "mm-dd-yyyy": "%m-%d-%Y",
    "yyyy-mm-dd": "%Y-%m-%d",
    "yyyy-dd-mm": "%Y-%d-%m"
}


class ProcessFile:
    def __init__(self, file, name: str= 'No_Name', date_format: str= 'dd/mm/yyyy' ,sep:str= ','):
        """
        Initializes the ProcessFile object.

        Args:
            file (str): The string content of the CSV file.
            name (str, optional): The name of the account holder. Defaults to 'No_Name'.
            date_format (str, optional): The format of the dates in the file.
                                         Defaults to 'dd/mm/yyyy'.
            sep (str, optional): The separator used in the CSV file. Defaults to ','.
        """
        self.name = name
        self.file = file
        self.sep = sep
        self.date_format = date_formats[date_format]


    def process_file(self):
        """
        Reads and corrects the CSV file content.

        This method splits the input string into lines and handles cases where
        the header has fewer columns than the data rows by padding it.

        Returns:
            io.StringIO or None: A file-like object containing the corrected
                                 CSV content, or None if the input file is empty.
        """
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


    def convert_tabel(self, corrected_file):
        """
        Converts the corrected CSV content into a pandas DataFrame.

        It reads the CSV data, selects a subset of columns, sets a default
        'uncategorized' value, and standardizes the data types for 'Amount'
        and 'Date' columns.

        Args:
            corrected_file (io.StringIO): A file-like object with the CSV data.

        Returns:
            pd.DataFrame or None: A cleaned and formatted DataFrame, or None
                                  if the input is empty.
        """
        if corrected_file:
            df = pd.read_csv(corrected_file, sep= self.sep)
            columns_to_keep = ["Name", "Date", "Description", "Amount", "Currency"]

            new_df = df[columns_to_keep].copy()
            new_df['Category'] = "uncategorized"
            if new_df['Amount'].dtype == object:
                new_df['Amount'] = new_df['Amount'].str.replace(',', '.')
            new_df['Date'] = pd.to_datetime(new_df['Date'], format= self.date_format, dayfirst=True)

            new_df['Amount'] = new_df['Amount'].astype(float)
            return new_df

        else:
            return None

    def change_description(self, df_filtrat):
        """
        Standardizes transaction descriptions for easier reading and categorization.

        This method iterates through a predefined list of store names and keywords.
        If a keyword is found in a transaction's description, the description is
        replaced with the standardized keyword.

        Args:
            df_filtrat (pd.DataFrame): The DataFrame whose descriptions are to be changed.

        Returns:
            pd.DataFrame: The DataFrame with updated descriptions.
        """

        df_filtrat = df_filtrat.copy()
        df_filtrat['Name'] = self.name
        df_filtrat.loc[df_filtrat['Description'].str.contains(from_saving_account, case=False, na=False), 'Description'] = str(categories['own accounts'][0])
        df_filtrat.loc[df_filtrat['Description'].str.contains(to_saving_account, case=False, na=False), 'Description'] = str(categories['own accounts'][1])

        for store in stores:
            df_filtrat.loc[df_filtrat['Description'].str.contains(store, case=False, na=False), 'Description'] = str(store)

        return df_filtrat


    def get_tabel(self, first_date: str= None, last_date: str = None):
        """
        Processes the file and returns a complete, filtered DataFrame.

        This is the main method that orchestrates the file processing, conversion
        to a DataFrame, and description standardization. It can also filter the
        transactions based on a start and end date.

        Args:
            first_date (str, optional): The start date for filtering (in the specified format).
                                        Defaults to the earliest date in the file.
            last_date (str, optional): The end date for filtering. Defaults to today.

        Returns:
            pd.DataFrame or None: The final, processed (and possibly filtered)
                                  DataFrame, or None if the initial file is empty.
        """
        data = self.process_file()
        df = self.convert_tabel(data)

        if df.empty:
            return None

        df['Date'] = pd.to_datetime(df['Date'], format=self.date_format)

        if first_date:
            first_date = pd.to_datetime(first_date, format= self.date_format)
        else:
            first_date = pd.to_datetime(df['Date'].min(), format= self.date_format)

        if last_date:
            last_date = pd.to_datetime(last_date, format= self.date_format, dayfirst= True)
        else:
            last_date = str(pd.to_datetime('today', format= self.date_format, dayfirst= True))


        df = df[(df['Date'] >= first_date) & (df['Date'] <= last_date)]

        new_df = self.change_description(df)

        return new_df


    def get_last_month_tabel(self):
        """
         Retrieves all transactions from the previous calendar month.

         This method processes the file and filters the resulting DataFrame to
         include only the transactions that occurred in the month prior to the
         current one.

         Returns:
             pd.DataFrame or None: A DataFrame containing last month's data,
                                   or None if the file is empty.
        """

        data = self.process_file()
        df = self.convert_tabel(data)


        if df.empty:
            return None

        current_date = pd.to_datetime('today')

        first_day_current_month = current_date.replace(day=1)
        first_day_last_month = (first_day_current_month - pd.DateOffset(days=1)).replace(day=1)

        first_day_of_last_month = pd.Timestamp(first_day_last_month).normalize()
        last_month_data = df[(df['Date'] >= first_day_of_last_month) & (df['Date'] < first_day_current_month)]
        new_df = self.change_description(last_month_data)

        return new_df


if __name__ == '__main__':
    with open('../FILE/transactions.csv', mode='r', encoding='utf-8') as f:
        content = f.read()

    fd = ProcessFile(file= content, name='Claudiu', sep=';', date_format= 'yyyy-mm-dd')
    mdf = fd.get_tabel()
    print(mdf )
