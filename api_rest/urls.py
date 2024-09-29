from rest_framework import routers
from .api import UserViewSet, RegionViewSet, AddressViewSet, HotelViewSet, RoomViewSet, ReservationViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'regions', RegionViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = router.urls