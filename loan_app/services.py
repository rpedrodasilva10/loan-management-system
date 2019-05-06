"""Missing: DOCSTRING"""

def calc_installment(data):
    """Missing: DOCSTRING"""
    r_value = data['rate'] / 12.0
    installment = (
        (r_value + r_value / ((1 + r_value) ** data['term'] - 1))
        * data['amount'])
    installment = round(installment, 2)
    data.update({'installment':installment})
    return data
