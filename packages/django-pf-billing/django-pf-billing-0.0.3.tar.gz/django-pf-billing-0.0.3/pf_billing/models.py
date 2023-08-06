
from django.db import models

from . import BillingStatus, PaymentGateway


class Billing(models.Model):

    status = models.CharField(max_length=50, choices=BillingStatus.CHOICES, default=BillingStatus.READY, verbose_name="결제상태")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="요청일")
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=255, blank=True, verbose_name="트랜잭션ID")
    api_id = models.CharField(max_length=255, blank=True, verbose_name="API ID")
    request_amount = models.DecimalField(max_digits=9, decimal_places=2, default="0.0", verbose_name="요청금액")
    tax = models.DecimalField(max_digits=9, decimal_places=2, default="0.0", verbose_name="면세금액")
    vat = models.DecimalField(max_digits=9, decimal_places=2, default="0.0", verbose_name="부가가치세")
    item_name = models.CharField(max_length=255, blank=True, verbose_name="상품명")
    billing_username = models.CharField(max_length=255, blank=True, verbose_name="구매자명")
    billing_email = models.EmailField(blank=True, verbose_name="구매자 이메일")
    billing_phone_number = models.CharField(max_length=255, blank=True, verbose_name="구매자 연락처")
    customer_ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="구매자IP")
    customer_access_env = models.CharField(max_length=255, blank=True, null=True, verbose_name="구매환경") 
    admin_memo = models.TextField(blank=True, default="", verbose_name="관리자 메모")
    message = models.TextField(blank=True, default="", verbose_name="결제 상세 내역")
    pg_token = models.CharField(max_length=50, blank=True, default="", verbose_name="PG토큰")
    captured_amount = models.DecimalField(max_digits=9, decimal_places=2, default="0.0", verbose_name="확정금액")
    pg_name = models.CharField(max_length=12, choices=PaymentGateway.CHOICES, default=PaymentGateway.KAKAO_PAY)

    class Meta:
        db_table = "billing"
        verbose_name = "결제"
        verbose_name_plural = "결제"

    def __str__(self):
        return f"트랜잭션ID : {self.transaction_id}"
