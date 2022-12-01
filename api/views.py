from django.http import JsonResponse

def getRoutes(request):

    route = [
        {'GET':'api/projects'},
        {'GET':'api/projects/id'},
        {'POST':'api/projects/vote'},

        {'POST':'api/users/token'},
        {'POST':'api/users/token/refresh'},
    ]

    return JsonResponse(route, safe=False)