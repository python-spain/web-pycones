from django.conf.urls import url
from pycones.tshirts.views import Tshirt, Thanks, TshirtUpdate

app_name = "tshirts"

urlpatterns = [
    # Pattern tshirts:<name>
    url(r"^$", Tshirt.as_view(), name="index"),
    url(r"^thanks", Thanks.as_view(), name='thanks'),
    url(r'^update/$', TshirtUpdate.as_view(), name='update')
]
