from django.utils.deprecation import MiddlewareMixin


class MobileCheckMiddleware(MiddlewareMixin):
    MOBILE_APPS_UA = ("AdinusaAndroid", "AdinusaIos")

    def process_request(self, request):
        request.is_mobile = False
        request.mobile_app = None
        request.mobile_version = None

        if 'User-Agent' in request.headers:
            user_agent = request.headers['User-Agent']
            ua_splits = user_agent.split("/")

            if len(ua_splits) != 2:
                return

            app, version = ua_splits
            if app in self.MOBILE_APPS_UA:
                request.is_mobile = True
                request.mobile_app = app
                request.mobile_version = version
