from rest_framework import views, response

class SubscribeView(views.APIView):
    http_method_names = ('post', )

    def post(self, request, *args, **kwargs):
        print(kwargs)
        return response.Response({"ok": True})