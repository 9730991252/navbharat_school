from django.shortcuts import render, redirect
from home.models import *
from sunil.models import *
from teacher.models import *
from school.models import *
from school_admin.models import *
from django.contrib import messages
import time
import io
import os
import base64
import math
from datetime import date
from django.db.models import *
from django.template.loader import render_to_string
from django.db.models import Avg, Sum, Min, Max
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.files.base import ContentFile