from django.db import reset_queries
from django.shortcuts import redirect, render
from django.shortcuts import HttpResponseRedirect,HttpResponse
from sympy import det
from django.contrib import messages
from deliver import models
from personnel.models import Staff
import datetime


def get_car_info(did):
        dic=dict(((0, '无冷链车辆'),(1, 'A级冷链冷藏车辆'), (2, 'B级冷链冷藏车辆'),
             (3, 'C级冷链冷藏车辆'), (4, 'D级冷链冷藏车辆'), (5, 'E级冷链冷藏车辆'), 
             (6, 'F级冷链冷藏车辆'), (7, 'G级冷链冷藏车辆'), (8, 'H级冷链冷藏车辆')))

        carinfo=models.Car.objects.all().values('car_id','status','cold_chain','load','staff_id')
        staffinfo=Staff.objects.all().values('staff_id','staff_name')
        freecar=carinfo.filter(status=0)
        for car in freecar:
            car['cold_chain_level']=dic[car['cold_chain']]
            car['driver']=staffinfo.get(staff_id=car['staff_id'])['staff_name']
        return {'freecar': freecar,'staff': staffinfo,'did':did}


def deliver_home(request):
    return render(request,'delivery/homepage.html')


def deliver_glc_sfyz(request):
    if request.method=='POST':
        sid=request.POST.get('sid')
        s=Staff.objects.filter(staff_id=sid).values('position')
        if not s:
            messages.add_message(request,messages.ERROR,"部门验证失败")
            redirect('/work/delivery/glc/sfyz/')
        elif s['position']=="管理员":
            messages.add_message(request,messages.SUCCESS,"干活吧打工人 ╰（‵□′）╯")
            redirect('/work/delivery/glc/dqrw/')
        else:
            messages.add_message(request,messages.ERROR,"部门验证失败")
            redirect('/work/delivery/glc/sfyz/')
    else:
        return render(request,'delivery/glc/glc_sfyz.html')

def deliver_glc_xqgl(request):
    '''update deliver_deliver set status=0 where status!=0;'''
    if request.method == 'POST':
        request.session['did'] = request.POST.get('deliver_id')
        return redirect('/work/delivery/glc/rwfp/')
        
    else:
        deliverinfo=models.Deliver.objects.all().order_by('apply_time').values(
            'deliver_id','departure_time','arrival_time',
            'aim_add','start_add','apply_time'
        )
        wclxq=deliverinfo.filter(status=0)
        for xq in wclxq:
            if xq['deliver_id'][0:2]=='XS':
                xq['depart']='销售部'
            elif xq['deliver_id'][0:2]=='CG':
                xq['depart']='采购部'
        context={'wclxq':wclxq}
        return render(request,'delivery/glc/glc_xqgl.html',context=context)

def deliver_glc_rwfp(request):
    '''update deliver_car set status=0 where status=1;'''
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        did=request.POST.get('deliver_id')
        models.Deliver.objects.filter(deliver_id=did).update(status=1)
        models.Car.objects.filter(car_id=car_id).update(status=1)
        models.CarForDeliver.objects.create(
            deliver_id=models.Deliver.objects.filter(deliver_id=did).first(),
            car_id=models.Car.objects.filter(car_id=car_id).first()
        )
        context = get_car_info(did)

        messages.add_message(request, messages.SUCCESS, '注册成功')
        return redirect('/work/delivery/glc/xqgl/')
    else:
        did = request.session.get('did')
        context = get_car_info(did)
        return render(request,'delivery/glc/glc_rwfp.html',context=context)

def deliver_glc_jxz(request):
    deliverinfo=models.Deliver.objects.all().order_by('apply_time').values(
        'deliver_id','departure_time','arrival_time',
        'aim_add','start_add','apply_time'
    )
    dd=models.DeliverDetail.objects.all().order_by('detail_time').values('deliver_id','province','city','detail_time')
    jxzxq=deliverinfo.filter(status=2)
    for xq in jxzxq:
        if xq['deliver_id'][0:2]=='XS':
            xq['depart']='销售部'
        elif xq['deliver_id'][0:2]=='CG':
            xq['depart']='采购部'
        xq['use_time']=(datetime.datetime.now()-xq['apply_time'].replace(tzinfo=None))
        detail=dd.filter(deliver_id=xq['deliver_id']).last()
        xq['place']=detail['province']+'省'+detail['city']+'市'
    context={'jxzxq':jxzxq}
    return render(request,'delivery/glc/glc_jxz.html',context=context)

def deliver_glc_ywc(request):
    deliverinfo=models.Deliver.objects.all().order_by('apply_time').values(
        'deliver_id','departure_time','arrival_time',
        'aim_add','start_add','apply_time'
    )
    ywcxq=deliverinfo.filter(status=3)
    for xq in ywcxq:
        if xq['deliver_id'][0:2]=='XS':
            xq['depart']='销售部'
        elif xq['deliver_id'][0:2]=='CG':
            xq['depart']='采购部'
        xq['use_time']=xq['arrival_time']-xq['apply_time']
    context={'ywcxq':ywcxq}
    return render(request,'delivery/glc/glc_ywc.html',context=context)

def deliver_psc_sfyz(request):
    if request.method=='POST':
        sid=request.POST.get('sid')
        s=Staff.objects.filter(staff_id=sid).values('position')
        if not s:
            messages.add_message(request,messages.ERROR,"部门验证失败")
            redirect('/work/delivery/psc/sfyz/')
        elif s['position']=="配送员":
            messages.add_message(request,messages.SUCCESS,"干活吧打工人 ╰（‵□′）╯")
            redirect('/work/delivery/psc/'+sid+'/dqrw/')
        else:
            messages.add_message(request,messages.ERROR,"部门验证失败")
            redirect('/work/delivery/psc/sfyz/')
    else:
        return render(request,'delivery/psc/psc_sfyz.html')

def deliver_psc_dqrw(request,staff_id):
    

    context={}
    return render(request,'delivery/psc/psc_dqrw.html',context=context)

def deliver_psc_xxsc(request,staff_id):


    context={
        
    }
    return render(request,'delivery/psc/psc_xxsc.html',context=context)

def deliver_psc_ywc(request,staff_id):


    context={
        
    }
    return render(request,'delivery/psc/psc_ywc.html',context=context)




def test(request):
    return render(request,'delivery/form.html')