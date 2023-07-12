from datetime import datetime

def year(request):
    now = datetime.today()
    return {'year': now.year}