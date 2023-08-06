from django.utils.translation import pgettext_lazy


class BillingStatus:
    READY = "READY"
    SEND_TMS = "SEND_TMS"
    OPEN_PAYMENT = "OPEN_PAYMENT"
    SELECT_METHOD = "SELECT_METHOD"
    ARS_WAITING = "ARS_WAITING"
    AUTH_PASSWORD = "AUTH_PASSWORD"
    ISSUED_SID = "ISSUED_SID"
    SUCCESS_PAYMENT = "SUCCESS_PAYMENT"
    PART_CANCEL_PAYMENT = "PART_CANCEL_PAYMENT"
    CANCEL_PAYMENT = "CANCEL_PAYMENT"
    FAIL_AUTH_PASSWORD = "FAIL_AUTH_PASSWORD"
    QUIT_PAYMENT = "QUIT_PAYMENT"
    FAIL_PAYMENT = "FAIL_PAYMENT"
    CHOICES = [
        (READY, pgettext_lazy("billing status", "결제 요청")),
        (SEND_TMS, pgettext_lazy("billing status", "결제 요청 메시지(TMS) 발송 완료")),
        (OPEN_PAYMENT, pgettext_lazy("billing status", "사용자 결제 화면 진입")),
        (SELECT_METHOD, pgettext_lazy("billing status", "결제 수단 선택 및 인증 완료")),
        (ARS_WAITING, pgettext_lazy("billing status", "ARS 인증 진행 중")),
        (AUTH_PASSWORD, pgettext_lazy("billing status", "비밀번호 인증 완료")),
        (ISSUED_SID, pgettext_lazy("billing status", "SID 발급 완료(정기 결제 시 SID만 발급 한 경우)")),
        (SUCCESS_PAYMENT, pgettext_lazy("billing status", "결제 완료")),
        (PART_CANCEL_PAYMENT, pgettext_lazy("billing status", "부분 취소")),
        (CANCEL_PAYMENT, pgettext_lazy("billing status", "결제된 금액 모두 취소")),
        (FAIL_AUTH_PASSWORD, pgettext_lazy("billing status", "사용자 비밀번호 인증 실패")),
        (QUIT_PAYMENT, pgettext_lazy("billing status", "사용자 결제 중단")),
        (FAIL_PAYMENT, pgettext_lazy("billing status", "결제 승인 실패")),
    ]


class PaymentGateway:
    KAKAO_PAY = "카카오페이"
    KG_MOBILIANS = "KG모빌리언스"
    NO_PG = "-"

    CHOICES = [
        (KAKAO_PAY, pgettext_lazy("payment gateway", "카카오페이")),
        (KG_MOBILIANS, pgettext_lazy("payment gateway", "KG모빌리언스")),
        (NO_PG, pgettext_lazy("payment gateway", "포인트/쿠폰 결제")),
    ]
