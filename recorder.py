import pandas



class Recorder:
    """Класс-сохранялка для датафреймов"""
    def __init__(self, record: pandas.DataFrame):
        self.record = record
        self.name = 'Выгрузка'

    def save_html(self):
        with open(self.name+".html", 'w') as f:
            f.write(self.record.to_html(index=False))

    def save_json(self):
        with open(self.name+".json", 'w') as f:
            f.write(self.record.to_json(orient='records'))

    def save_xml(self):
        with open(self.name+'.xml', 'w') as f:
            f.write(self.record.to_xml())

    def save_excel(self):
        with pandas.ExcelWriter("Лист замен.xlsx", mode='w') as write:
            for date in list(self.record['day'].drop_duplicates().sort_values().values):
                df: pandas.DataFrame = self.record[self.record['day'] == date].copy()
                df.to_excel(write, sheet_name=date, index=False)
