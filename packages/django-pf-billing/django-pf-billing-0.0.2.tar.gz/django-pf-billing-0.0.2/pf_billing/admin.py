from django.contrib import admin
from django.utils import timezone 

from .models import Billing
from .interface import BillingAction


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    """billing admin"""

    list_display = [
        'item_name',
        'convert_to_kor_money',
        'get_pg_name',
        'billing_username', 'get_kst',
        'customer_access_env',
        'get_payment_status',
        'cancel_payment',
    ]
    fields = [
        'captured_amount',  # 확정 금액
        'request_amount',  # 요청 금액
        'vat',  # 부가세
        'tax',  # 면세액
        'billing_username',  # 구매자 이름
        'billing_email',  # 구매자 이메일 
        'billing_phone_number',  # 구매자 연락처 
        'message',  # PG 리턴 메시지
        'transaction_id',  # 트랜잭션 ID
        'pg_token',  # PG 토큰 
    ]
    readonly_fields = [
        'captured_amount',  # 확정 금액
        'request_amount',  # 요청 금액
        'vat',  # 부가세
        'tax',  # 면세액
        'billing_username',  # 구매자 이름
        'billing_email',  # 구매자 이메일 
        'billing_phone_number',  # 구매자 연락처 
        'message',  # PG 리턴 메시지
        'transaction_id',  # 트랜잭션 ID
        'pg_token',  # PG 토큰 
    ]

    def get_pg_name(self, obj):
        return obj.get_pg_name_display()
    get_pg_name.short_description = 'PG'

    def get_payment_status(self, obj):
        if obj.pg_name == 'KakaoPay':
            payment = BillingAction.set_pg("KakaoPay")
            status = payment.track(obj.transaction_id).json()['status']
            obj.status = status
            obj.save()
            return obj.get_status_display()
    get_payment_status.short_description = '요청일'

    def get_kst(self, obj):
        kst = timezone.localtime(obj.created_at)
        return kst.strftime("%Y-%m-%d %H:%M:%S")
    get_kst.short_description = '요청일'


    def convert_to_kor_money(self, obj):
        kor_money = int(obj.captured_amount) 
        return f"{kor_money} 원"
    convert_to_kor_money.short_description = '금액'

    def cancel_payment(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        if obj.status == "SUCCESS_PAYMENT":
            billing_id = obj.id
            kwargs = {
                'billing_id': billing_id,
            }
            url = reverse('pf_billing:admin_cancel_payment', kwargs=kwargs)
            a_tag = format_html(f'<a href={url} target="_blank">🔒</a>')
            return a_tag
        else:
            return "🚫" 
    cancel_payment.short_description = '환불'
