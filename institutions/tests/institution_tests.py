from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models.institution import Institution

#Placeholder list, borrar cuando se utilicen los imports
_ = [TestCase, APIClient, status, loads, Institution]