from .models import Loan

def calc_installment(data):
    ''' calculates loan installment '''
    r = data['rate'] / 12.0
    installment = ((r + r / ((1 + r) ** data['term'] - 1)) * data['amount'])
    installment = round(installment, 2)
    data.update({'installment':installment})
    return data
