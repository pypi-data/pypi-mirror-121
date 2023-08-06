# pf_billing

> **pf_billing** is a django-based billing module, which covers KakaoPay and KGMobilians.<br>
> (`pf` stands for plabfootball)<br>

<br>

## 🚀 Quick start

#### 1. install django-pf-billing

```python
pip install django-pf-billing
```

#### It will install following dependencies if not installed

- requests<br>
- user-agent<br>

<br>

#### 2. Add "pf_billing" to your INSTALLED_APPS setting like this

```python
# settings.py
INSTALLED_APPS = [
    ...
    'pf_billing',
]

KAKAOPAY_CID = "Your kakaopay cid"
KAKAOPAY_APP_ADMIN_KEY = "Your kakao app admin key"

```

<br>

#### 3. Run `python manage.py migrate` to create a Billing model.

<br>

#### 4. Start the development server

- need the Admin app enabled
- visit http://127.0.0.1:8000/admin/ to see billing admin

<br><br>

## 🛠 How to use

```python
from pf_billing.interface import BillingAction

# 1) KakaoPay
billing = BillingAction.set_pg("KakaoPay")

# 2) KGMobilians
billing = BillingAction.set_pg("KGMobilians")


# ready
response = billing.ready(
    partner_user_id  = "190324",
    partner_order_id = "K202109301340",
    item_name        = "테스트 상품",
    total_amount     = 10000,
    quantity         = 1,
    # 결제 성공 시, 카카오페이 서버에서 운영 중인 서버로 콜백 가능한 엔드포인트
    approval_url     = "http://example.com/billing/result/success",
    # 결제 취소 시, 카카오페이 서버에서 운영 중인 서버로 콜백 가능한 엔드포인트
    cancel_url       = "http://example.com/billing/result/cancel",
    # 결제 실패 시, 카카오페이 서버에서 운영 중인 서버로 콜백 가능한 엔드포인트
    fail_url         = "http://example.com/billing/result/fail",
)

# approve
response = billing.approve(
    partner_user_id  = "190324",
    partner_order_id = "K202109301340",
    pg_token         = "YKDOEKCDKSLKNF",
    transaction_id   = "TID-n3jdks2lajs",
)

# cancel(partial/all)
response = billing.cancel(
    transaction_id = "n3jdks2lajs",
    cancel_amount  = 10000,
)

# track status
response = billing.track(
    transaction_id = "n3jdks2lajs",
)
```

<br><br>

## ⭐️ Note

### 1. Billing Model will be created in your database. Keep in mind that model or db_table name conflict.

### 2. Register your domain in Kakao developers.

- https://developers.kakao.com/console/app/364537/config/platform
