import datetime
current_date = datetime.date.today().isoformat()
from datetime import datetime, timedelta

# текущая дата
date = datetime.now()

# вычитание одного дня
new_date = date + timedelta(days=90)
print(new_date)