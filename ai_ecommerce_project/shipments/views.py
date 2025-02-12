from urllib import request
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from orders.models import Order, OrderItem
from orders.serializers import OrderItemSerializer, OrderSerializer
from orders.views import OrderViewSet
from orders.utils import get_latest_order_for_user

from .models import Shipments
from .serializers import ShipmentSerializer

import logging 

logger = logging.getLogger(__name__)

class ShipmentViewSet(viewsets.ModelViewSet): 
    queryset = Shipments.objects.filter(order__status='shipped')
    serializer_class = ShipmentSerializer