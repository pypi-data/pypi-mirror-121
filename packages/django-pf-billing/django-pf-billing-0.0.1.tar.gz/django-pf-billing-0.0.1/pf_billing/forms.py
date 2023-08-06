from django import forms


class PaymentMethodForm(forms.Form):
    """결제 수단 form"""

    PG_LIST = (
        ('KAKAO_PAY', '카카오페이',),
        ('RED_BANKING', '계좌 이체')
    )
    pg_name = forms.ChoiceField(choices=PG_LIST) 
