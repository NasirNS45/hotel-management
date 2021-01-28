from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url

# Create your views here.
from passlib.handlers.sha2_crypt import sha256_crypt

from HMS import settings
from app.fusioncharts import FusionCharts
from app.models import BookingHistory
from app.views import get_rooms
from signup.models import CustomUser


def adminlogin(request):
    try:
        if 'admin' in request.session:
            return HttpResponseRedirect('/adminh4u')
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            login_cred = CustomUser.objects.filter(email=email, password=password, is_superuser=True)
            if login_cred:
                det = User.objects.filter(email=email).values()
                details = login_cred[0]
                dets = []
                for i in det:
                    for k, v in i.items():
                        dets.append(v)
                superuser = dets[3]
                if email == details['email'] and sha256_crypt.verify(password, details['password']):
                    request.session['email'] = email
                    request.session['admin'] = True
                    if superuser:
                        return redirect('app:adminh4u')
                    else:
                        messages.warning(request, 'Not an admin, please contact administrator')
                else:
                    messages.warning(request, 'Not an admin, please contact administrator')
                    return render(request, 'app/adminlogin.html')
            else:
                return render(request, 'app/adminlogin.html')
    except:
        return render(request, 'app/adminlogin.html')


def adminh4u(request):
    if 'admin' in request.session:
        dataSource = OrderedDict()
        chartConfig = OrderedDict()
        chartConfig["caption"] = ""
        chartConfig["xAxisName"] = "Rooms"
        chartConfig["yAxisName"] = "Available"
        chartConfig["numberSuffix"] = ""
        chartConfig["theme"] = "fusion"

        chartData = OrderedDict()
        avl1 = len(get_rooms('single'))
        avl2 = len(get_rooms('double'))
        avl3 = len(get_rooms('luxury'))
        avl4 = len(get_rooms('deluxe'))
        avl5 = len(get_rooms('executive'))
        avl6 = len(get_rooms('presidential'))

        chartData["Single"] = avl1
        chartData["Double"] = avl2
        chartData["Deluxe"] = avl3
        chartData["Luxury"] = avl4
        chartData["Executive"] = avl5
        chartData["Presidential"] = avl6

        dataSource["chart"] = chartConfig
        dataSource["data"] = []

        for key, value in chartData.items():
            data = {"label": key, "value": value}
            dataSource["data"].append(data)
        column2D = FusionCharts("column2d", "ex1", "800", "400", "chart-1", "json", dataSource)
        return render(request, 'app/adminanalytics.html',
                      {'output': column2D.render(), 'chartTitle': 'Available Rooms'})
    else:
        return render(request, 'app/adminlogin.html')


def adminbooking(request):
    try:
        bhr = BookingHistory.objects.all()
        paginator = Paginator(bhr, 10)
        page = request.GET.get('page', 1)
        try:
            bookings = paginator.page(page)
            return render(request, 'app/adminbooking.html', {'bookings': bookings})
        except PageNotAnInteger:
            bookings = paginator.page(1)
        except EmptyPage:
            bookings = paginator.page(paginator.num_pages)
            return render(request, 'app/adminbooking.html')
    except:
        return render(request, 'app/adminh4u.html')


def salesanalysis(request):
    price = BookingHistory.objects.aggregate(Sum('amount'))
    amount = 0
    for k, v in price.items():
        amount = v
    chartObj = FusionCharts('angulargauge', 'ex1', '600', '400', 'chart-1', 'json', """{
    "chart": {
    "captionpadding": "0",
    "origw": "320",
    "origh": "300",
    "gaugeouterradius": "115",
    "gaugestartangle": "270",
    "gaugeendangle": "-25",
    "showvalue": "1",
    "valuefontsize": "30",
    "majortmnumber": "13",
    "majortmthickness": "2",
    "majortmheight": "13",
    "minortmheight": "7",
    "minortmthickness": "1",
    "minortmnumber": "1",
    "showgaugeborder": "0",
    "theme": "fusion"
    },
    "colorrange": {
    "color": [
      {
        "minvalue": "0",
        "maxvalue": "5000000",
        "code": "#999999"
      },
      {
        "minvalue": "1500",
        "maxvalue": "10000000",
        "code": "#F6F6F6"
      }
    ]
  },
  "dials": {
    "dial": [
      {
        "value": """ + str(amount) + """,
        "bgcolor": "#F20F2F",
        "basewidth": "8"
      }
    ]
  },
  "annotations": {
    "groups": [
      {
        "items": [
          {
            "type": "text",
            "id": "text",
            "text": "INR",
            "x": "$gaugeCenterX",
            "y": "$gaugeCenterY + 40",
            "fontsize": "20",
            "color": "#555555"
          }
        ]
      }
    ]
  }
}""")
    return render(request, 'app/salesanalysis.html', {'output': chartObj.render()})


class AdminLoginView(LoginView):
    form_class = AuthenticationForm
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'app/adminlogin.html'
    redirect_authenticated_user = False
    extra_context = None

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.ADMIN_PANEL_LOGIN_REDIRECT_URL)


class AdminLogoutView(LogoutView):
    next_page = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/logged_out.html'
    extra_context = None