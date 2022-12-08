def page_not_found_view(request, exception):
    from django.http import HttpResponse

    return HttpResponse(f"""
    <div>
    
    <p> Dear User: {request.user}</p>
    <p> Page Not Found </p>
    
    </div>
    """)
