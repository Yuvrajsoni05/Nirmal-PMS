import logging
import os

from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from ..models import (
    Job_detail,
    Jobimage,
    JobHistory,
    CDRDetail,
    CylinderMadeIn,
    CDRImage,
    Party,
    PartyContact,
    BankDetails,
    PartyEmail,
    PouchQuotation,
    PurchaseOrder,
    ProformaJob,
    ProformaInvoice,
    PartyBillingAddress,
    PouchQuotationJob,
)

from ..decorators import custom_login_required
from .. import utils

logger = logging.getLogger(__name__)
