import logging
import os

from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from openpyxl import Workbook
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
    PurchaseOrderJob,
    PouchParty,
    PouchPartyEmail,
    PouchPartyContact,
    PouchMaster,
    PartyBillingGSTIN
    
)

from ..decorators import custom_login_required
from .. import utils
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

logger = logging.getLogger("myapp")
