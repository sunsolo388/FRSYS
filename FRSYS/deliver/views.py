from django.db import reset_queries
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect,HttpResponse
from deliver import models
from personnel.models import Staff


def deliver_home(request):
    return render(request,'delivery/homepage.html')

def deliver_glc_rwfp(request):
    ColdChain_ITEMS = (
        (0, '无冷链车辆'),
        (1, 'A级冷链冷藏车辆'), (2, 'B级冷链冷藏车辆'),
        (3, 'C级冷链冷藏车辆'), (4, 'D级冷链冷藏车辆'),
        (5, 'E级冷链冷藏车辆'), (6, 'F级冷链冷藏车辆'),
        (7, 'G级冷链冷藏车辆'), (8, 'H级冷链冷藏车辆'),
    )
    dic=dict(ColdChain_ITEMS)

    carinfo=models.Car.objects.all().values('car_id','status','cold_chain','load','staff_id')
    staffinfo=Staff.objects.all().values('staff_id','staff_name')
    
    freecar=carinfo.filter(status=0)
    for car in freecar:
        car['cold_chain_level']=dic[car['cold_chain']]
        car['driver']=staffinfo.get(staff_id=car['staff_id'])['staff_name']
    context = {
        'freecar': freecar,
        'staff': staffinfo,
    }
    return render(request,'delivery/glc/glc_rwfp.html',context=context)

def deliver_glc_xqgl(request):
    deliverinfo=models.Deliver.objects.all().values('deliver_id','departure_time','arrival_time')
    wclxq=deliverinfo.filter(departure_time__isnull=True)
    wclxq=wclxq.filter(arrival_time__isnull=True)

    print(wclxq)
    for xq in wclxq:
        print(xq)
        if xq['deliver_id'][0:2]=='XS':
            xq['depart']='销售部'
        elif xq['deliver_id'][0:2]=='CG':
            xq['depart']='采购部'

    print(wclxq)
    for xq in wclxq:
        print(xq)
    context={
        'wclxq':wclxq,
    }

    return render(request,'delivery/glc/glc_xqgl.html',context=context)


def deliver_psc_dqrw(request):
    return render(request,'delivery/psc/psc_dqrw.html')

def test(request):
    return render(request,'delivery/table.html')