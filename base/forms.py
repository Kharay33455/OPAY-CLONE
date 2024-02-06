from django import forms

class AccountNumberForm(forms.Form):
    account_number = forms.IntegerField(label='' , min_value=10000000000, max_value = 99999999999, widget= forms.NumberInput(attrs={"placeholder" : "Phone No.Opay Account No./Name"}))
    


class AmountForm(forms.Form):
    amount = forms.IntegerField(label='Amount', min_value= 10, max_value=5000000)
    remark = forms.CharField(label='Remark', max_length=200, required=False)

class TFpassForm(forms.Form):
    pin = forms.IntegerField(label='', min_value=1000, max_value=9999)