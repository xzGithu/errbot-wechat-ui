#coding:utf8
from django.shortcuts import render,redirect,get_object_or_404
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse,HttpResponse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from useraction.models import *
from django.contrib.auth.decorators import login_required,permission_required
from suds.client import Client
import cx_Oracle
import os,re,json
from urllib.parse import unquote
from useraction.models import commands,rulelistmodel
from .forms import ruleform,commform
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
# Create your views here.

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


#分页函数
def pagination(request, queryset, display_amount=10, after_range_num = 5,before_range_num = 4):
    #按参数分页
    try:
        #从提交来的页面获得page的值
        page = int(request.GET.get("page", 1))
        #如果page值小于1，那么默认为第一页
        if page < 1:
            page = 1
    #若报异常，则page为第一页
    except ValueError:
            page = 1
    #引用Paginator类
    paginator = Paginator(queryset, display_amount)
    #总计的数据条目
    count = paginator.count
    #合计页数
    num_pages = paginator.num_pages
    try:
        #尝试获得分页列表
        objects = paginator.page(page)
    #如果页数不存在
    except EmptyPage:
        #获得最后一页
        objects = paginator.page(paginator.num_pages)
    #如果不是一个整数
    except PageNotAnInteger:
        #获得第一页
        objects = paginator.page(1)
    #根据参数配置导航显示范围
    temp_range = paginator.page_range

    #如果页面很小
    if (page - before_range_num) <= 0:
        #如果总页面比after_range_num大，那么显示到after_range_num
        if temp_range[-1] > after_range_num:
            page_range = range(1, after_range_num+1)
        #否则显示当前页
        else:
            page_range = range(1, temp_range[-1]+1)
    #如果页面比较大
    elif (page + after_range_num) > temp_range[-1]:
        #显示到最大页
        page_range = range(page-before_range_num,temp_range[-1]+1)
    #否则在before_range_num和after_range_num之间显示
    else:
        page_range = range(page-before_range_num+1, page+after_range_num)
    #返回分页相关参数
    return objects, page_range, count, num_pages

@login_required()
def rulelist(request,table):
    global query,allrules
    if table=='rule':
        allrules=rulelistmodel.objects.order_by('id')
        # allrules=model_to_dict(allrules)
    if request.method == 'GET':
        kwargs = {}
        query = ''
        for key, value in request.GET.items():
            if key != 'csrfmiddlewaretoken' and key != 'page':
                if key == 'node':
                    kwargs['node__node_name__contains'] = value
                    query += '&' + key + '=' + value
                else:
                    kwargs[key + '__contains'] = value
                    query += '&' + key + '=' + value
        data = allrules.filter(**kwargs)
    else:
        data = allrules

    data_list, page_range, count, page_nums = pagination(request, data)
    context = {
        'data':data_list,
        'query':query,
        'page_range':page_range,
        'count': count,
        'page_nums':page_nums,
        'page_title':"规则列表",
    }
    return render(request,'errbot/rules_list.html',context)
@login_required()
def getfang(request):
    datas=[]
    if request.method=="GET":
        connect=cx_Oracle.connect('ultraoas/oas_123@192.168.180.156:1521/zzxnms')
        cursor=connect.cursor()
        cursor.execute("select a.BUSINESS_TYPE_NAME ,a.DESCP,b.name from OAS_OPSCENARIO a,IASE_CATEGORY b where a.IASE_CATEGORY_ID=b.id")
        fang=cursor.fetchall()
        # fang={}
        m=1
        for i in fang:
        #     datas.append(QueryDict('name='+i[0]+'&desc='+i[1]+'&cate='+i[2]))
            data={}
            data["id"]=m
            data["name"]=i[0]
            data["desc"]=i[1]
            data["cate"]=i[2]
            datas.append(data)
            m+=1
        cursor.close()
        connect.close()
        data_list, page_range, count, page_nums = pagination(request, datas)
        context = {
            'data': data_list,
            'page_range': page_range,
            'count': count,
            'page_nums': page_nums,
        }
        return render(request,'errbot/fang.html',context)
@login_required()
def newrule(request,fangan):
    if request.method == "POST":
        name = request.POST.get('name', None)

        try:
            rulelistmodel.objects.get(rulename=name)
            alertdata="存在同名规则"
            context = {"alertdata": alertdata, "sub_title": '输入指令', "fangan": fangan, "commands": "","rulesnames":name}
            return render(request, 'errbot/ruleadd.html',context=context)
        except:
            rulelistmodel.objects.update_or_create(rulename=name,cuser=request.user)
            return redirect('rulelist', table="rule")
    else:
        name = request.GET.get('name', None)
        try:
            rulename = rulelistmodel.objects.get(rulename=name)
            commlists = ""
            # commlists=commands.objects.filter(rulename=rulename)
        except:
            commlists=""
        context = {"page_title": '', "sub_title": '输入指令',"fangan":fangan,"commands":commlists,"rulesnames":name }
        return render(request, 'errbot/ruleadd.html',context=context)
@login_required()
def newcommand(request,fangan,rule):
    global msg
    oasurl = "http://192.168.180.73:59999/oas/services/UCWS?wsdl"
    client = Client(oasurl)
    requxml = "<request><opscenarioName>" + fangan + "</opscenarioName></request>"
    parmlist = client.service.getOpscenarioParamByOpsName(
        requestXML=requxml)
    pars = re.findall("<identity>(.*?)</identity>", parmlist)
    try:
        relname = rulelistmodel.objects.get(rulename=rule)
        if relname:
            msg="已存在同名规则"
    except:
        msg="新规则"
    if request.method=="POST":
        try:
            relname = rulelistmodel.objects.get(rulename=rule)
        except:
            rulelistmodel.objects.create(rulename=rule,cuser=request.user)
        relname = rulelistmodel.objects.get(rulename=rule)
        print (relname)
        rulekey = relname
        command=request.POST.get('name',None)
        status=request.POST.get('tool_run_type',None)
        orders=request.POST.getlist('inputvalue',None)
        dictorders=dict(zip(pars,orders))
        dictorders=sorted(dictorders.keys(),key=lambda x:x[1])
        # obj = commands(fanan=fangan, zhiling=command, cuser=request.user,status=status,params=','.join(dictorders),)
        # obj.save()
        obj = commands.objects.create(rulename=rulekey, fanan=fangan, zhiling=command, cuser=request.user,status=status,params=','.join(dictorders),)
        # rulelistmodel.objects.create(rulename=rule, cuser=request.user)
        return HttpResponseRedirect(reverse('getrule',args=(fangan,rule)))
    content={"data":pars,"sub_title": '输入指令',"msg":msg}
    return render(request,'errbot/newcommand.html',context=content)
@login_required()
def modrenew(request,rulename):
    datas=[]
    if request.method=="GET":
        connect=cx_Oracle.connect('ultraoas/oas_123@192.168.180.156:1521/zzxnms')
        cursor=connect.cursor()
        cursor.execute("select a.BUSINESS_TYPE_NAME ,a.DESCP,b.name from OAS_OPSCENARIO a,IASE_CATEGORY b where a.IASE_CATEGORY_ID=b.id")
        fang=cursor.fetchall()
        # fang={}
        m=1
        for i in fang:
        #     datas.append(QueryDict('name='+i[0]+'&desc='+i[1]+'&cate='+i[2]))
            data={}
            data["id"]=m
            data["name"]=i[0]
            data["desc"]=i[1]
            data["cate"]=i[2]
            datas.append(data)
            m+=1
        cursor.close()
        connect.close()
        data_list, page_range, count, page_nums = pagination(request, datas)
        context = {
            'data': data_list,
            'page_range': page_range,
            'count': count,
            'page_nums': page_nums,
        }
        return render(request, 'errbot/renew_fang.html', context)

@login_required()
def commadd(request,fangan,rule):
    global msg
    oasurl = "http://192.168.180.73:59999/oas/services/UCWS?wsdl"
    client = Client(oasurl)
    requxml = "<request><opscenarioName>" + fangan + "</opscenarioName></request>"
    parmlist = client.service.getOpscenarioParamByOpsName(
        requestXML=requxml)
    pars = re.findall("<identity>(.*?)</identity>", parmlist)
    # try:
    #     relname = rulelistmodel.objects.get(rulename=rule)
    #     if relname:
    #         msg="已存在同名规则"
    # except:
    #     msg="新规则"
    if request.method=="POST":
        try:
            relname = rulelistmodel.objects.get(rulename=rule)
        except:
            rulelistmodel.objects.create(rulename=rule,cuser=request.user)
        relname = rulelistmodel.objects.get(rulename=rule)
        print (relname)
        rulekey = relname
        command=request.POST.get('name',None)
        status=request.POST.get('tool_run_type',None)
        orders=request.POST.getlist('inputvalue',None)
        dictorders=dict(zip(pars,orders))
        dictorders=sorted(dictorders.keys(),key=lambda x:x[1])
        # obj = commands(fanan=fangan, zhiling=command, cuser=request.user,status=status,params=','.join(dictorders),)
        # obj.save()
        obj = commands.objects.create(rulename=rulekey, fanan=fangan, zhiling=command, cuser=request.user,status=status,params=','.join(dictorders),)
        # rulelistmodel.objects.create(rulename=rule, cuser=request.user)
        return HttpResponseRedirect(reverse('getrule',args=(fangan,rule)))
    content={"data":pars,"sub_title": '输入指令',"msg":msg}
    return render(request,'errbot/newcommand.html',context=content)
@login_required()
def modrenewcommand(request,rule,fangan):
    oasurl = "http://192.168.180.73:59999/oas/services/UCWS?wsdl"
    client = Client(oasurl)
    requxml = "<request><opscenarioName>" + fangan + "</opscenarioName></request>"
    parmlist = client.service.getOpscenarioParamByOpsName(
        requestXML=requxml)
    pars = re.findall("<identity>(.*?)</identity>", parmlist)
    if request.method=="POST":
        try:
            relname = rulelistmodel.objects.get(rulename=rule)
        except:
            rulelistmodel.objects.create(rulename=rule,cuser=request.user)
        relname = rulelistmodel.objects.get(rulename=rule)
        print ("############################################")
        print (relname.id)
        rulekey = relname
        command=request.POST.get('name',None)
        status=request.POST.get('tool_run_type',None)
        orders=request.POST.getlist('inputvalue',None)
        dictorders=dict(zip(pars,orders))
        dictorders=sorted(dictorders.keys(),key=lambda x:x[1])
        obj = commands.objects.create(rulename=rulekey, fanan=fangan, zhiling=command, cuser=request.user,status=status,params=','.join(dictorders),)
        return redirect('modrule',pk=relname.id)
        # return JsonResponse("yes")
    content={"data":pars,"sub_title": '输入指令',}
    return render(request,'errbot/renewcommand.html',context=content)

@login_required()
def getrule(request,fangan,rule):
    if request.method=="GET":
        try:
            rulename=rulelistmodel.objects.get(rulename=rule)
            commandlists=commands.objects.filter(rulename=rulename)
        except:
            commandlists=""
        content={"rulename":rule,"commlist":commandlists,"fangan":fangan}
        return render(request,'errbot/rulecomm.html',context=content)
    else:
        relname=request.POST.get('morenrule',None)
        print (relname)
        newname = request.POST.get('confname', None)
        print (newname)
        try:
            rulelistmodel.objects.filter(rulename=unquote(relname)).update(rulename=unquote(newname))
        except:
            rulelistmodel.objects.update_or_create(rulename=unquote(newname),cuser=request.user)
        return redirect('rulelist', table="rule")

@login_required()
def modrule(request,pk):
    if request.method=="GET":
        table_ins = get_object_or_404(rulelistmodel, pk=pk)
        commandlists = commands.objects.filter(rulename=table_ins)
        # content={"rulename":table_ins.rulename,"commlist":commandlists,}
        data_list, page_range, count, page_nums = pagination(request, commandlists)
        content = {
            "rulename": table_ins.rulename,
            # "commlist": commandlists,
            'data': data_list,
            # 'query': query,
            'page_range': page_range,
            'count': count,
            'page_nums': page_nums,
            # 'page_title': "规则列表",
        }
        return render(request,'errbot/modrule.html',context=content)
    else:
        rulename = request.POST.get("confname", None)
        rulelistmodel.objects.filter(id=pk).update(rulename=rulename,)
        return redirect('rulelist', table="rule")

@login_required()
def modcomm(request,pk,):
    table_ins=get_object_or_404(commands,pk=pk)
    print (table_ins.status)
    form=commform(request.POST or None, instance=table_ins)
    ruleid=get_object_or_404(rulelistmodel,rulename=table_ins.rulename)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.cuser=str(request.user)
        instance.save()
        return redirect('modrule', pk=ruleid.id)
    context = {
        'form': form,
    }
    return render(request, 'errbot/comminfo.html', context)
    # return render(request, 'errbot/modModal.html', context)

@login_required()
def delcomm(request,pk):
    table_ins = get_object_or_404(commands, pk=pk)
    if request.method == 'POST':
        #删除该条目
        try:
            table_ins.delete()
            #删除成功,则data信息为success
            data = 'success'
        except IntegrityError:
            #如因外键问题，或其他问题，删除失败，则报error
            data = 'error'
        #将最后的data值传递至JS页面，进行后续处理
        return JsonResponse(data,safe=False)
@login_required()
def delrule(request,pk):
    table_ins = get_object_or_404(rulelistmodel, pk=pk)
    if request.method == 'POST':
        #删除该条目
        try:
            table_ins.delete()
            #删除成功,则data信息为success
            data = 'success'
        except IntegrityError:
            #如因外键问题，或其他问题，删除失败，则报error
            data = 'error'
        #将最后的data值传递至JS页面，进行后续处理
        return JsonResponse(data,safe=False)


@login_required
def postrule(request):
    if request.is_ajax():
        rulename=request.POST.get("data")
        return HttpResponse(json.dumps({"rulename":rulename}), content_type='application/json')

@login_required
def queryrule(request,rulename):
    if request.method=="GET":
        rulename=str(rulename.strip('"'))
        table_ins = rulelistmodel.objects.filter(rulename=rulename)
        commandlists = commands.objects.filter(rulename=table_ins)
        return render(request,'errbot/queryrule.html',{"rulename":rulename,"commands":commandlists})

@login_required
def alldel(request):
    if request.is_ajax():
        ruleids=request.POST.get("data")
        lists = json.loads(ruleids)
        for i in lists:
            rulelistmodel.objects.filter(pk=i).delete()
        return HttpResponse(json.dumps({"data":"success"}),content_type='application/json')
