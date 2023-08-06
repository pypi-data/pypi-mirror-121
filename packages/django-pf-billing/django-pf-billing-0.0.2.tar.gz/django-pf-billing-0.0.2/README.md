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

===== example ====
HOST_DOMAIN = "www.example.com"
HOST_APPROVAL_URLNAME = "kakao_success"
HOST_CANCEL_URLNAME = "kakao_cancel"
HOST_FAIL_URLNAME = "kakao_fail"
```

<br>

#### 3. Include the `pf_billing` URLconf in your project urls.py like this

```python
from django.conf import settings
path('pf_billing/', include(f'{settings.APP_NAME}.urls')),
```

<br>

#### 4. Run `python manage.py migrate` to create a Billing model.

<br>

#### 5. Start the development server

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

### 1. Must implement following API

#### 1) PG calls your success view when PG determines the billing is successful.

- HOST_APPROVAL_URLNAME you wrote in settings.py

#### 2) PG calls your cancel view when PG determines the billing is canceled.

- HOST_CANCEL_URLNAME you wrote in settings.py

#### 3) PG calls your fail view when PG determines the billing is failed.

- HOST_FAIl_URLNAME you wrote in settings.py

<br>

### 2. Register your domain in Kakao developers.

- https://developers.kakao.com/console/app/364537/config/platform
