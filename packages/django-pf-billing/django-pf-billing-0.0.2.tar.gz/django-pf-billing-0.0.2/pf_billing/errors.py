"""PG 에러 처리"""


class PGException(Exception):
    def __init__(self, response):
        super(PGException, self).__init__(response)
        self.response = response

    @property
    def text(self):
        return self.response.text

    @property
    def status_code(self):
        return self.response.status_code


class KakaoPayAPIException(PGException):
    pass

class KGMobiliansAPIException(PGException):
    pass
