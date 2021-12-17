import pandas

import database

con = database.DbSchedule().connection

print(pandas.read_sql('SELECT * FROM schedule', con)
      )