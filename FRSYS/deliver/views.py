import django
from django.db import reset_queries
from django.shortcuts import redirect, render
from django.shortcuts import HttpResponseRedirect,HttpResponse
from sympy import det, re
from django.contrib import messages
from deliver import models
from personnel.models import Staff
import datetime
import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from df_user import user_decorator


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
    sid=request.session['staff_id']
    s=Staff.objects.filter(staff_id=sid).values('position').last()
    if s['position']=="管理员":
        messages.add_message(request,messages.SUCCESS,"干活吧打工人 ╰（‵□′）╯")
        print(s['position'])
        return redirect('/work/delivery/glc/xqgl/')
    elif s['position']=="配送员":
        messages.add_message(request,messages.SUCCESS,"干活吧打工人 ╰（‵□′）╯")
        return redirect('/work/delivery/psc/'+sid+'/dqrw/')
    else:
        messages.add_message(request,messages.ERROR,"部门验证失败")
        return redirect('/innerlogin/')
    #return render(request,'delivery/homepage.html')

### 已经无用
def deliver_glc_sfyz(request):
    '''if request.method=='POST':
        sid=request.POST.get('sid')
        s=Staff.objects.filter(staff_id=sid).values('position').last()
        if not s:
            messages.add_message(request,messages.ERROR,"部门验证失败")
            return redirect('/work/delivery/glc/sfyz/')
        elif s['position']=="管理员":
            messages.add_message(request,messages.SUCCESS,"干活吧打工人 ╰（‵□′）╯")
            print(s['position'])
            return redirect('/work/delivery/glc/xqgl/')
        else:
            messages.add_message(request,messages.ERROR,"部门验证失败")
            return redirect('/work/delivery/glc/sfyz/')
    else:    
        return render(request,'delivery/glc/glc_sfyz.html')'''
    sid=request.session['staff_id']
    s=Staff.objects.filter(staff_id=sid).values('position').last()
    if s['position']=="管理员":
        messages.add_message(request,messages.SUCCESS,"干活吧打工人 ╰（‵□′）╯")
        print(s['position'])
        return redirect('/work/delivery/glc/xqgl/')
    else:
        messages.add_message(request,messages.ERROR,"部门验证失败")
        return redirect('/work/delivery/glc/sfyz/')
    # return render(request,'delivery/glc/glc_sfyz.html')

@user_decorator.worker
def deliver_glc_xqgl(request):
    '''update deliver_deliver set status=0 where status!=0;'''
    if request.method == 'POST':
        request.session['did'] = request.POST.get('deliver_id')
        return redirect('/work/delivery/glc/rwfp/')
        
    else:
        deliverinfo=models.Deliver.objects.all().order_by('apply_time').values(
            'deliver_id','aim_add','start_add','apply_time'
        )
        wclxq=deliverinfo.filter(status=0)
        for xq in wclxq:
            if xq['deliver_id'][0:2]=='XS':
                xq['depart']='销售部'
            elif xq['deliver_id'][0:2]=='CG':
                xq['depart']='采购部'
        context={'wclxq':wclxq}
        return render(request,'delivery/glc/glc_xqgl.html',context=context)

@user_decorator.worker
def deliver_glc_rwfp(request):
    '''update deliver_car set status=0 where status=1;'''
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        did=request.POST.get('deliver_id')
        models.Deliver.objects.filter(deliver_id=did).update(status=1)
        #models.Car.objects.filter(car_id=car_id).update(status=1)
        models.CarForDeliver.objects.create(
            deliver_id=models.Deliver.objects.filter(deliver_id=did).first(),
            car_id=models.Car.objects.filter(car_id=car_id).first()
        )
        context = get_car_info(did)

        messages.add_message(request, messages.SUCCESS, '分配成功')
        return redirect('/work/delivery/glc/xqgl/')
    else:
        did = request.session.get('did')
        context = get_car_info(did)
        return render(request,'delivery/glc/glc_rwfp.html',context=context)

@user_decorator.worker
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
        xq['use_time']=datetime.datetime.now().replace(microsecond=0)-xq['apply_time'].replace(tzinfo=None).replace(microsecond=0)
        detail=dd.filter(deliver_id=xq['deliver_id']).last()
        xq['place']=detail['province']+'省'+detail['city']+'市'
    context={'jxzxq':jxzxq}
    return render(request,'delivery/glc/glc_jxz.html',context=context)

@user_decorator.worker
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
        xq['use_time']=xq['arrival_time'].replace(microsecond=0)-xq['apply_time'].replace(microsecond=0)
    context={'ywcxq':ywcxq}
    return render(request,'delivery/glc/glc_ywc.html',context=context)


#### 已经无用
@user_decorator.worker
def deliver_psc_sfyz(request):
    if request.method=='POST':
        sid=request.POST.get('sid')
        s=Staff.objects.filter(staff_id=sid).values('position').last()
        if not s:
            messages.add_message(request,messages.ERROR,"部门验证失败")
            return redirect('/work/delivery/psc/sfyz/')
        elif s['position']=="配送员":
            messages.add_message(request,messages.SUCCESS,"干活吧打工人 ╰（‵□′）╯")
            return redirect('/work/delivery/psc/'+sid+'/dqrw/')
        else:
            messages.add_message(request,messages.ERROR,"部门验证失败")
            return redirect('/work/delivery/psc/sfyz/')
    else:
        return render(request,'delivery/psc/psc_sfyz.html')

@user_decorator.worker
def deliver_psc_dqrw(request,staff_id):
    car_id=models.Car.objects.filter(staff_id=staff_id).values('car_id').last()['car_id']
    dqrws=models.CarForDeliver.objects.filter(car_id=car_id).order_by('id').values('deliver_id')
    if len(dqrws)==0:
        messages.add_message(request,messages.SUCCESS,"当前无任务\n请好好休息！\n╰（‵□′）╯")
        return redirect('/work/delivery/psc/'+staff_id+'/ywc/')
    for dqrw in dqrws:
        aim_deliver=dqrw['deliver_id']
        deliver=models.Deliver.objects.filter(deliver_id=aim_deliver).filter(status__in=[1,2])
        if len(deliver)==0:
            messages.add_message(request,messages.SUCCESS,"当前无任务\n请好好休息！\n╰（‵□′）╯")
            return redirect('/work/delivery/psc/'+staff_id+'/ywc/')
        deliver_info=deliver.values('deliver_id','start_add','aim_add','apply_time','departure_time','status').last()
        dqrw.update(deliver_info)
        dqrw['dd']=models.DeliverDetail.objects.filter(deliver_id=aim_deliver).order_by('detail_time')

    if request.method=='POST':
        if deliver_info['status']==1:
            for dqrw in dqrws:
                aim_deliver=dqrw['deliver_id']
                models.Deliver.objects.filter(deliver_id=aim_deliver).update(departure_time=datetime.datetime.now(),status=2)
            models.Car.objects.filter(car_id=car_id).update(status=1)
            messages.add_message(request,messages.SUCCESS,"任务已开始\n祝您一路顺风\n╰（‵□′）╯")
            return redirect('/work/delivery/psc/'+staff_id+'/dqrw/')
        else:
            messages.add_message(request,messages.SUCCESS,"任务已领取\n请勿重复领取\n╰（‵□′）╯")
            return redirect('/work/delivery/psc/'+staff_id+'/xxsc/')

    for dqrw in dqrws:
        if dqrw['deliver_id'][0:2]=='XS':
            dqrw['depart']='销售部'
        elif dqrw['deliver_id'][0:2]=='CG':
            dqrw['depart']='采购部'

        if len(dqrw['dd'])==0:
            dqrw['place']='还未出发'
        else:
            ddinfo=dqrw['dd'].values('province','city').last()
            if ddinfo==None:
                dqrw['place']='还未到达检查点'
            else:
                dqrw['place']=ddinfo['province']+ddinfo['city']
        dqrw['use_time']=datetime.datetime.now().replace(microsecond=0)-deliver_info['apply_time'].replace(tzinfo=None).replace(microsecond=0)
        context={'dqrws':dqrws}
    return render(request,'delivery/psc/psc_dqrw.html',context=context)

@user_decorator.worker
def deliver_psc_xxsc(request,staff_id):
    context={}
    car_id=models.Car.objects.filter(staff_id=staff_id).values('car_id').last()['car_id']
    syrw=models.CarForDeliver.objects.filter(car_id=car_id).values('deliver_id')
    deliver_ls=[]
    for rw in syrw:
        deliver_id=rw['deliver_id']
        deliver=models.Deliver.objects.filter(deliver_id=deliver_id).filter(status=2)
        if len(deliver)==0:
            messages.add_message(request,messages.SUCCESS,"当前无进行中任务")
            return redirect('/work/delivery/psc/'+staff_id+'/dqrw/')
        deliver_info=deliver.values('deliver_id','start_add','aim_add','departure_time').last()
        deliver_ls.append(deliver_id)
    context.update(deliver_info)

    context['use_time']=datetime.datetime.now().replace(microsecond=0)-deliver_info['departure_time'].replace(tzinfo=None).replace(microsecond=0)

    deliverdetail=models.DeliverDetail.objects.filter(deliver_id=deliver_id).order_by('detail_time')
    detail_info=deliverdetail.values('province','city','detail_time')
    for dd in detail_info:
        dd['passadd']=dd['province']+'省'+dd['city']+'市'
        dd['use_time']=dd['detail_time'].replace(microsecond=0)-deliver_info['departure_time'].replace(microsecond=0) 
    context['detail_info']=detail_info
    
    if request.method=='POST':
        if 'sc' in request.POST:
            for deliver_id in deliver_ls:
                models.DeliverDetail.objects.create(
                    deliver_id=models.Deliver.objects.filter(deliver_id=deliver_id).first(),
                    province=request.POST.get('province'),
                    city = request.POST.get('city'),
                    detail_time = datetime.datetime.now(),
                )
            return redirect('/work/delivery/psc/'+staff_id+'/xxsc/')
        elif 'js' in request.POST:
            for deliver_id in deliver_ls:
                models.Deliver.objects.filter(deliver_id=deliver_id).update(
                    status=3,
                    arrival_time=datetime.datetime.now(),
                )
            return redirect('/work/delivery/psc/'+staff_id+'/dqrw/')
    return render(request,'delivery/psc/psc_xxsc.html',context=context)

@user_decorator.worker
def deliver_psc_ywc(request,staff_id):
    car_id=models.Car.objects.filter(staff_id=staff_id).values('car_id').last()['car_id']
    syrw=models.CarForDeliver.objects.filter(car_id=car_id).values('deliver_id')
    for rw in syrw:
        deliver_id=rw['deliver_id']
        if deliver_id[0:2]=='XS':
            rw['depart']='销售部'
        elif deliver_id[0:2]=='CG':
            rw['depart']='采购部'
        deliver=models.Deliver.objects.filter(deliver_id=deliver_id).filter(status=3)
        deliver_info=deliver.values('deliver_id','apply_time','start_add','aim_add','departure_time','arrival_time').last()
        if deliver_info is None:
            return render(request,'delivery/psc/psc_ywc.html')
        rw['use_time']=deliver_info['arrival_time']-deliver_info['departure_time']
        deliverdetail=models.DeliverDetail.objects.filter(deliver_id=deliver_id).order_by('detail_time')
        detail_info=deliverdetail.values('province','city')
        rw.update(deliver_info)
        rw['passadd']=''
        for ddinfo in detail_info:
            rw['passadd']+=(ddinfo['province']+'省'+ddinfo['city']+'市'+'、')
        rw['passadd']=rw['passadd'][0:-1]
    context={'ywcrw':syrw}
    return render(request,'delivery/psc/psc_ywc.html',context=context)

def test(request):
    return render(request,'delivery/form.html')