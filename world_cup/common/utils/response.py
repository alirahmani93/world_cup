from rest_framework.response import Response


def custom_response(status_code: dict, data: dict):
    return Response(
        data={
            'detail': status_code.get('detail'),
            'code': status_code.get('code', status_code.get('detail').replace(' ', '_')),
            'data': data},
        status=status_code.get('number'))
