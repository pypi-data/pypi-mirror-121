import requests

from django.conf import settings

from .errors import KakaoPayAPIException


class BillingAction:
    _available_pg = ["KakaoPay", "KGMobilians"]
    host_approval_endpoint = None
    host_cancel_endpoint = None
    host_fail_endpoint = None

    def __init__(self, *args, **kwargs):
        from django.urls import reverse
        HOST_DOMAIN = settings.HOST_DOMAIN
        APP_NAME = settings.APP_NAME
        HOST_APPROVAL_URLNAME = reverse(f'{APP_NAME}:{settings.HOST_APPROVAL_URLNAME}') 
        HOST_CANCEL_URLNAME = reverse(f'{APP_NAME}:{settings.HOST_CANCEL_URLNAME}') 
        HOST_FAIL_URLNAME = reverse(f'{APP_NAME}:{settings.HOST_FAIL_URLNAME}') 
        if "/" in HOST_DOMAIN[-1]:
            raise ValueError(f"Need to delete ending slash in 'settings.py' HOST_DOMAIN: {HOST_DOMAIN}")

        self.host_approval_endpoint = f"{HOST_DOMAIN}{HOST_APPROVAL_URLNAME}"
        self.host_cancel_endpoint = f"{HOST_DOMAIN}{HOST_CANCEL_URLNAME}"
        self.host_fail_endpoint = f"{HOST_DOMAIN}{HOST_FAIL_URLNAME}"

    @classmethod
    def set_pg(cls, pg_name):
        if pg_name not in cls._available_pg:
            raise ValueError(f"Available PGs: {', '.join(cls._available_pg)}")
        if pg_name == 'KakaoPay':
            return KakaoPay()
        else:
            return KGMobilians()
    
    def ready(self, *args, **kwargs):
        raise NotImplementedError()

    def approve(self, *args, **kwargs):
        raise NotImplementedError()

    def cancel(self, *args, **kwargs):
        raise NotImplementedError()


class KakaoPay(BillingAction):
    # 고유번호
    PG_NAME = "KakaoPay"
    CID = settings.KAKAOPAY_CID
    APP_ADMIN_KEY = settings.KAKAOPAY_APP_ADMIN_KEY

    # 카카오페이 URL
    BASE_URL = "https://kapi.kakao.com"
    READY_URL = "/v1/payment/ready"
    APPROVE_URL = "/v1/payment/approve"
    TRACK_URL = "/v1/payment/order"
    CANCEL_URL = "/v1/payment/cancel"

    headers = {
        'Authorization': f"KakaoAK {APP_ADMIN_KEY}",
        'Content-type': "application/x-www-form-urlencoded;charset=utf-8",
        }

    def ready(
        self,
        partner_user_id,
        partner_order_id,
        item_name,
        total_amount,
        quantity,
        approval_url,
        cancel_url,
        fail_url,
        tax=0,
    ):
        """결제 대기 API"""

        try:
            data = {
                "partner_user_id": partner_user_id,
                "partner_order_id": partner_order_id, 
                "item_name": item_name,
                "total_amount": total_amount,

                "cid": self.CID,
                "quantity": quantity,
                "tax_free_amount": tax,
                "approval_url": approval_url,
                "cancel_url": cancel_url,
                "fail_url": fail_url,
            }
            response = requests.post(
                self.BASE_URL + self.READY_URL,
                headers=self.headers,
                data=data,
            )
            return response
        except Exception as e:
            raise KakaoPayAPIException(e) 

    def approve(self, partner_user_id, partner_order_id, pg_token, transaction_id):
        """결제 승인 API"""

        try:
            data = {
                "partner_user_id": partner_user_id,
                "partner_order_id": partner_order_id, 
                "pg_token": pg_token,
                "cid": self.CID,
                "tid": transaction_id,
            }
            response = requests.post(
                self.BASE_URL + self.APPROVE_URL,
                headers=self.headers,
                data=data,
            )
            return response
        except Exception as e:
            raise KakaoPayAPIException(e)

    def track(self, transaction_id):
        """주문 조회 API"""

        try:
            data = {
                "cid": self.CID,
                "tid": transaction_id,
            }
            response = requests.post(
                    self.BASE_URL + self.TRACK_URL,
                    headers=self.headers,
                    data=data,
                )
            return response
        except Exception as e:
            raise KakaoPayAPIException(e)
            
    def cancel(self, transaction_id, cancel_amount):
        """주문 (전체/부분) 취소 API"""

        try:
            data = {
                "cid": self.CID,
                "tid": transaction_id,
                "cancel_amount": cancel_amount,
                "cancel_tax_free_amount": 0,
            }

            response = requests.post(
                    self.BASE_URL + self.CANCEL_URL,
                    headers=self.headers,
                    data=data,
                )
            return response
        except Exception as e:
            raise KakaoPayAPIException(e)


class KGMobilians(BillingAction):
    """KG 모빌리언스(일반 결제) 도입 예정"""

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Will be implemented")

    def ready(self, *args, **kwargs):
        pass

    def approve(self, *args, **kwargs):
        pass

    def cancel(self, *args, **kwargs):
        pass
