class GetIp:
    def getip(self,request=None):
        if not request:
            raise Exception("缺少一个必传参数：request")
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        return ip