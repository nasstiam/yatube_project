from datetime import datetime, date

def year(request):
    now = datetime.today()
    return {'year': now.year}