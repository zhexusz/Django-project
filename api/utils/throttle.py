from rest_framework.throttling import BaseThrottle, SimpleRateThrottle

class VisitThrottle(object):
    
    def allow_request(self,request,view): # check if the request is allowed
        remote_addr = request.META.get('REMOTE_ADDR') # get the ip address of the request
        print(remote_addr)
        return True #False拒绝访问，True则放行

    def wait(self):
        pass

# 写法2
class TestThrottle(BaseThrottle): # extends from BaseThrottle

    def allow_request(self, request, view):
        remote_addr = self.get_ident(request) # use get_ident from BaseThrottle
        return remote_addr 

# 写法3
class NewThrottle(SimpleRateThrottle):
    scope = "keynamehere" # This is used as the key, and you can do global configuration in settings.py
    
    def get_cache_key(self, request, view):
        return self.get_ident(request)