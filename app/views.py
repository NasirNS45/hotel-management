from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.base import View

from signup.models import CustomUser
from .forms import RoomBooking, Reservations
from datetime import datetime
from .models import RoomBooking, BookingHistory, Rooms
from passlib.hash import sha256_crypt
from django.db.models import Sum
import smtplib
from .fusioncharts import FusionCharts, FusionTable, TimeSeries
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import OrderedDict


def test(request):
    return render(request, 'base.html')


def home(request):
    return render(request, 'app/index.html')


def contact(request):
    return render(request, 'app/contact.html')


def about(request):
    return render(request, 'app/about.html')


def available_rooms(request):
    return render(request, 'app/available-rooms.html')


class BookingView(View):

    def get(self, request):
        return render(request, 'app/booking.html')

    def post(self, request):
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        return redirect('app:available_rooms')


def roombooking(request):
    if request.method == 'GET':
        return render(request, 'app/index.html')
    global room_details, cin, cout, rem
    monthDays = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31,
                 '11': 30, '12': 31}
    leapDays = {'01': 31, '02': 29, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31,
                '11': 30, '12': 31}
    room_details = []
    if request.method == 'POST':
        form = RoomBooking(request.POST)
        check_in = request.POST.get('checkin')
        cin = changeDateFormat(check_in)
        check_out = request.POST.get('checkout')
        if check_out == '':
            messages.warning(request, "Checkout date cannot be empty")
            return render(request, 'app/booking.html')
        cout = changeDateFormat(check_out)
        dt1 = check_in.split('/')
        dt2 = check_out.split('/')
        diff = int(dt2[1]) - int(dt1[1])
        year = int(dt1[2])
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            days_comp = leapDays[dt1[0]]
        else:
            days_comp = monthDays[dt1[0]]
        rem = days_comp
        if diff < 0:
            rem = days_comp + diff
        email = request.session['email']
        hotel_name = request.session['hotel']
        room_details = [cin, cout, email, hotel_name]
        return render(request, 'app/rooms.html')


@login_required()
def single(request):
    try:
        if request.method == 'POST':
            form = Reservations(request.POST)
            details = get_form(request, form)
            name = details[0] + " " + details[1] + " " + details[2]
            price = rem * 1000
            price = price * details[10]
            reservation('single', details, price)
            avl = get_rooms('single')
            avl = len(avl)
            rooms_details = Rooms.objects.filter(roomtype='single').values()
            det = []
            for i in rooms_details:
                for k, v in i.items():
                    det.append(v)
            rs = det[2] - details[10]
            if rs < 0:
                rs = 0
            Rooms.objects.filter(roomtype='single').update(available=rs)
            return render(request, 'app/reservation.html',
                          {'name': name, 'room': details[10], 'cin': cin, 'cout': cout, 'bid': today_date,
                           'price': price, 'roomtype': 'Single'})
        else:
            avl = get_rooms('single')
            if len(avl) != 0:
                return render(request, 'app/singlerooms.html', {'avl': avl})
            else:
                messages.warning(request, 'No rooms are available')
                return render(request, 'app/singlerooms.html', {'avl': avl})
    except:
        return render(request, 'app/booking.html')


@login_required()
def double(request):
    try:
        if request.method == 'POST':
            form = Reservations(request.POST)
            details = get_form(request, form)
            name = details[0] + " " + details[1] + " " + details[2]
            price = rem * 1500
            price = price * details[10]
            reservation('double', details, price)
            avl = get_rooms('double')
            avl = len(avl)
            rooms_details = Rooms.objects.filter(roomtype='double').values()
            det = []
            for i in rooms_details:
                for k, v in i.items():
                    det.append(v)
            rs = det[2] - details[10]
            if (rs < 0):
                rs = 0
            Rooms.objects.filter(roomtype='double').update(available=rs)
            return render(request, 'app/reservation.html',
                          {'name': name, 'room': details[10], 'cin': cin, 'cout': cout, 'bid': today_date,
                           'price': price, 'roomtype': 'Double'})
        else:
            avl = get_rooms('double')
            if len(avl) != 0:
                return render(request, 'app/doublerooms.html', {'avl': avl})
            else:
                messages.warning(request, 'No rooms are available')
                return render(request, 'app/doublerooms.html', {'avl': avl})
    except:
        return render(request, 'app/booking.html')


@login_required()
def deluxe(request):
    try:
        if request.method == 'POST':
            form = Reservations(request.POST)
            details = get_form(request, form)
            name = details[0] + " " + details[1] + " " + details[2]
            price = rem * 3500
            price = price * details[10]
            reservation('deluxe', details, price)
            avl = get_rooms('deluxe')
            avl = len(avl)
            rooms_details = Rooms.objects.filter(roomtype='deluxe').values()
            det = []
            for i in rooms_details:
                for k, v in i.items():
                    det.append(v)
            rs = det[2] - details[10]
            if (rs < 0):
                rs = 0
            Rooms.objects.filter(roomtype='deluxe').update(available=rs)
            return render(request, 'app/reservation.html',
                          {'name': name, 'room': details[10], 'cin': cin, 'cout': cout, 'bid': today_date,
                           'price': price, 'roomtype': 'Deluxe'})
        else:
            avl = get_rooms('deluxe')
            if len(avl) != 0:
                return render(request, 'app/deluxe.html', {'avl': avl})
            else:
                messages.warning(request, 'No rooms are available')
                return render(request, 'app/deluxe.html', {'avl': avl})
    except:
        return render(request, 'app/booking.html')


@login_required()
def luxury(request):
    try:
        if request.method == 'POST':
            form = Reservations(request.POST)
            details = get_form(request, form)
            name = details[0] + " " + details[1] + " " + details[2]
            price = rem * 5000
            price = price * details[10]
            reservation('luxury', details, price)
            avl = get_rooms('luxury')
            avl = len(avl)
            rooms_details = Rooms.objects.filter(roomtype='luxury').values()
            det = []
            for i in rooms_details:
                for k, v in i.items():
                    det.append(v)
            rs = det[2] - details[10]
            if (rs < 0):
                rs = 0
            Rooms.objects.filter(roomtype='luxury').update(available=rs)
            return render(request, 'app/reservation.html',
                          {'name': name, 'room': details[10], 'cin': cin, 'cout': cout, 'bid': today_date,
                           'price': price, 'roomtype': 'Luxury'})
        else:
            avl = get_rooms('luxury')
            if len(avl) != 0:
                return render(request, 'app/luxury.html', {'avl': avl})
            else:
                messages.warning(request, 'No rooms are available')
                return render(request, 'app/luxury.html', {'avl': avl})
    except:
        return render(request, 'app/booking.html')


@login_required()
def executive(request):
    try:
        if request.method == 'POST':
            form = Reservations(request.POST)
            details = get_form(request, form)
            name = details[0] + " " + details[1] + " " + details[2]
            price = rem * 6500
            price = price * details[10]
            reservation('executive', details, price)
            avl = get_rooms('executive')
            avl = len(avl)
            rooms_details = Rooms.objects.filter(roomtype='executive').values()
            det = []
            for i in rooms_details:
                for k, v in i.items():
                    det.append(v)
            rs = det[2] - details[10]
            if (rs < 0):
                rs = 0
            Rooms.objects.filter(roomtype='executive').update(available=rs)
            return render(request, 'app/reservation.html',
                          {'name': name, 'room': details[10], 'cin': cin, 'cout': cout, 'bid': today_date,
                           'price': price, 'roomtype': 'Executive'})
        else:
            avl = get_rooms('executive')
            if len(avl) != 0:
                return render(request, 'app/executive.html', {'avl': avl})
            else:
                messages.warning(request, 'No rooms are available')
                return render(request, 'app/executive.html', {'avl': avl})
    except:
        return render(request, 'app/booking.html')


@login_required()
def presidential(request):
    try:
        if request.method == 'POST':
            form = Reservations(request.POST)
            details = get_form(request, form)
            name = details[0] + " " + details[1] + " " + details[2]
            price = rem * 8000
            price = price * details[10]
            reservation('presidential', details, price)
            avl = get_rooms('presidential')
            avl = len(avl)
            rooms_details = Rooms.objects.filter(roomtype='presidential').values()
            det = []
            for i in rooms_details:
                for k, v in i.items():
                    det.append(v)
            rs = det[2] - details[10]
            if (rs < 0):
                rs = 0
            Rooms.objects.filter(roomtype='presidential').update(available=rs)
            return render(request, 'app/reservation.html',
                          {'name': name, 'room': details[10], 'cin': cin, 'cout': cout, 'bid': today_date,
                           'price': price, 'roomtype': 'Presidential'})
        else:
            avl = get_rooms('presidential')
            if len(avl) != 0:
                return render(request, 'app/presidential.html', {'avl': avl})
            else:
                messages.warning(request, 'No rooms are available')
                return render(request, 'app/presidential.html', {'avl': avl})
    except:
        return render(request, 'app/booking.html')


def reservation(room, details, price):
    try:
        global today_date
        today_date = int(datetime.now().strftime("%Y%m%d%H%M%S"))
        rb = RoomBooking(today_date, room_details[0], room_details[1], details[0], details[1], details[2], details[3],
                         details[4], details[5], details[6], details[7], details[8], details[9], details[10])
        rb.save()
        user = User.objects.get(email=room_details[2])
        arguments = [today_date, room_details[0], room_details[1], user.email, user.id, price]
        bh = BookingHistory(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5])
        bh.save()
    except:
        return HttpResponseRedirect('/booking')


def update_rooms(request, roomtype, available, no_of_rooms):
    try:
        rooms_details = Rooms.objects.filter(roomtype=roomtype).values()
        det = []
        for i in rooms_details:
            for k, v in i.items():
                det.append(v)
        rs = det[2] - det[3]
        if rs < 0:
            rs = 0
        room_details.available = rs
        room_details.save()
    except:
        return render(request, 'app/booking.html')


def changeDateFormat(date):
    d_list = date.split('/')
    modified_date = d_list[2] + '-' + d_list[0] + '-' + d_list[1]
    return modified_date


@login_required()
def bookinghistory(request):
    try:
        red = booking_hist(request)
        return render(request, 'app/booking_history.html', {'details': red})
    except:
        return render(request, 'app/booking.html')


def booking_hist(request):
    try:
        bhr = BookingHistory.objects.filter(email=request.user.email).values()
        det = []
        details = []
        for i in bhr:
            for k, v in i.items():
                det.append(v)
            details.append(det)
        return details
    except:
        return render(request, 'app/booking.html')


@login_required()
def forgotpassword(request):
    try:
        if request.method == 'POST':
            fromaddr = 'ruby.coders@gmail.com'
            toaddrs = request.POST.get('email')
            data = CustomUser.objects.filter(email=request.user.email)
            msg = 'Hello, your password is P@$sword '
            username = 'ruby.coders@gmail.com'
            password = '$uperSt@r007'
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
            return redirect('accounts:login')
        else:
            return render(request, 'app/forgotpassword.html')
    except:
        messages.warning(request, 'Invalid email please enter valid email')
        return render(request, 'app/forgotpassword.html')


def rooms(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'app/display_rooms.html')


def getusers(request):
    usr = User.objects.all()
    users = []
    list2 = []
    for i in usr:
        users.append(i)
    for u in users:
        dets = User.objects.filter(email=u).values()
        list1 = []
        for k in dets:
            list1.append(k['id'])
            list1.append(k['first_name'])
            list1.append(k['last_name'])
            list1.append(k['email'])
            list1.append(k['date_joined'])
        list2.append(list1)
    return render(request, 'app/getusers.html', {'list': list2})


def get_form(request, form):
    firstname = form['firstname'].value()
    middlename = form['middlename'].value()
    lastname = form['lastname'].value()
    email = form['email'].value()
    phone = form['phone'].value()
    address = form['address'].value()
    city = form['city'].value()
    state = form['state'].value()
    zipcode = form['zipcode'].value()
    idproof = form['idproof'].value()
    rooms = form['rooms'].value()
    no_of_rooms = int(rooms)
    list = [firstname, middlename, lastname, email, phone, address, city, state, zipcode, idproof, no_of_rooms]
    return list


def get_rooms(roomtype):
    available = Rooms.objects.filter(roomtype=roomtype).values()
    det = []
    for i in available:
        for k, v in i.items():
            det.append(v)
    avl = det[3]
    avail = []
    for i in range(1, avl + 1):
        avail.append(i)
    return avail
