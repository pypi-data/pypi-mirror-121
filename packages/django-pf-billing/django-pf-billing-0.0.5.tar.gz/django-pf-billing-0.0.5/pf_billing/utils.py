from user_agents import parse

from django.conf import settings


class ClientInfo:
    """유저 정보(ip, os, bot 여부)클래스"""

    _IS_LOCAL = settings.DEBUG

    def __init__(self, request):
        self.request = request

    def get_ip(self):
        if self._IS_LOCAL:
            client_ip = self.request.META["REMOTE_ADDR"]
            return client_ip
        else:
            if "HTTP_X_FORWARDED_FOR" in self.request.META:
                client_ip_list = self.request.META["HTTP_X_FORWARDED_FOR"]
                client_public_ip = client_ip_list.split(",")[0]
                return client_public_ip
            else:
                return f"Could not get user ip"

    def is_bot(self):
        """봇 여부 판단"""

        user_agent_string = self.request.META["HTTP_USER_AGENT"]
        user_agent = parse(user_agent_string)
        is_bot = user_agent.is_bot
        return is_bot

    def get_os(self):

        user_agent_string = self.request.META["HTTP_USER_AGENT"]
        user_agent = parse(user_agent_string)
        user_os = user_agent.os.family
        return user_os

    def is_pc(self):

        user_agent_string = self.request.META["HTTP_USER_AGENT"]
        user_agent = parse(user_agent_string)
        is_pc = user_agent.is_pc
        return is_pc 

    def get_user_environ(self):
        """유저 access 환경"""

        user_agent_string = self.request.META["HTTP_USER_AGENT"]
        user_agent = parse(user_agent_string)

        return str(user_agent)
