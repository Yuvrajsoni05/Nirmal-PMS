from .common_imports import *





def master_page(request):
    return render(request, "MasterData/master_page.html")