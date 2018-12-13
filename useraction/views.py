#coding:utf-8
from django.shortcuts import render,get_object_or_404,render_to_response
from .models import *
# from errbotui.views import pagination
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
# from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import views,authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from errbotui.views import pagination
from django.contrib.auth.models import User
import json,time
from urllib.parse import unquote

# Create your views here.



def hello(request):
    return render(request,'errbot/hello.html',{"hello":"hello"})

def registeruser(request):
    curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if request.method == 'POST':  # 提交数据的方式POST，并且POST有数据

        username = request.POST.get('name', '')
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('repassword', '')
        email = request.POST.get('email', '')
        errors = []

        registerForm = RegistForm(
            {'username': username, 'password1': password1, 'password2': password2, 'email': email})  # b********
        if not registerForm.is_valid():
            errors.extend(registerForm.errors.values())
            return render_to_response("blog/userregister.html", context={'curtime': curtime,
                                                                                         'username': username,
                                                                                         'email': email,
                                                                                         'errors': errors})
        if password1 != password2:
            errors.append("两次输入的密码不一致!")
            return render_to_response("blog/userregister.html", context={'curtime': curtime,
                                                                                         'username': username,
                                                                                         'email': email,
                                                                                         'errors': errors})

        filterResult = User.objects.filter(username=username)  # c************
        if len(filterResult) > 0:
            errors.append("用户名已存在")
            return render_to_response("blog/userregister.html", context={'curtime': curtime,
                                                                                         'username': username,
                                                                                         'email': email,
                                                                                         'errors': errors})

        user = User()  # d************************
        user.username = username
        user.set_password(password1)
        user.email = email
        user.save()
        # 登录前需要先验证
        newUser = auth.authenticate(username=username, password=password1)  # f***************
        if newUser is not None:
            auth.login(request, newUser)  # g*******************
            return HttpResponseRedirect("/user")
    else:
        sForm = RegistForm()
    return render_to_response('index.html', locals())

    pass
def login(request):
    #extra_context是一个字典，它将作为context传递给template，这里告诉template成功后跳转的页面将是/hello
    template_response = views.login(request, extra_context={'next': '/errbot/rulelist/rule/'})
    return template_response

#用户退出
def logout(request):
    #logout_then_login表示退出即跳转至登陆页面，login_url为登陆页面的url地址
    template_response = views.logout_then_login(request,login_url='/login')
    return template_response

#密码更改
@login_required
def password_change(request):
    #post_change_redirect表示密码成功修改后将跳转的页面.
    template_response = views.password_change(request,post_change_redirect='/hello')
    return template_response

def registuser(request):
    if request.method == 'POST':
        form = RegistForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repassword = form.cleaned_data['repassword']
            email = form.cleaned_data['email']

            if password==repassword:
                exuser = User.objects.filter(username = username)
                if len(exuser) > 0:
                    err = '用户名已存在'
                    return render(request, 'user/useradd.html', {'form': form,'error':err,'page_title':"用户管理",'sub_title':"用户",})
            else:
                err='密码不匹配'
                return render(request, 'user/useradd.html',{'form': form, 'error': err, 'page_title': "用户管理", 'sub_title': "用户", })

            user = User.objects.create_user(username=username,password=password,email=email)
            user.save()

            return HttpResponseRedirect('/lists/user',)
    else:
        form = RegistForm()
    return render(request,'user/useradd.html',{'form':form,'page_title':"用户管理",'sub_title':"用户",})
@login_required
def changepwd(request):
    if request.method == 'GET':
        form = ChangepwdForm()
        return render(request,'user/changepwd.html', {'form': form, 'page_title':"用户管理",'sub_title':"用户",})
    else:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                return render(request,'user/afterchangepwd.html',  {'changepwd_success': True,'page_title':"用户管理",'sub_title':"用户", })
            else:
                return render(request,'user/changepwd.html',  {'form': form, 'oldpassword_is_wrong': True, 'page_title':"用户管理",'sub_title':"用户",})
        else:
            return render(request,'user/changepwd.html', {'form': form, 'page_title':"用户管理",'sub_title':"用户", })

@login_required
def qunpermis(request):
    query=""
    qunlist=qun.objects.order_by('id')
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
        data = qunlist.filter(**kwargs)
    else:
        data = qunlist
    print (qunlist)
    data_list, page_range, count, page_nums = pagination(request, data)
    context = {
        'data':data_list,
        'query':query,
        'page_range':page_range,
        'count': count,
        'page_nums':page_nums,
        'page_title':"",
    }
    return render(request,'user/qunlist.html',context)
@login_required
def userpermis(request):
    query=""
    perlist=person.objects.order_by('id')
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
        data = perlist.filter(**kwargs)
    else:
        data = perlist
    data_list, page_range, count, page_nums = pagination(request, data)
    context = {
        'data':data_list,
        'query':query,
        'page_range':page_range,
        'count': count,
        'page_nums':page_nums,
        'page_title':"",
    }
    return render(request,'user/perlist.html',context)
@login_required
def lqunper(request,table,pk):
    # if request.method=="GET":
    global name,perqun
    if table=='qun':
        name=get_object_or_404(qun,pk=pk)
        perqun = QunPer.objects.filter(qunname=name.name)
        typeid='qun'
    else:
        name=get_object_or_404(person,pk=pk)
        perqun = SinPer.objects.filter(Sinname=name.descname)
        name=name.descname
        typeid='person'
    # perqun=QunPer.objects.get(pk=pk)
    try:
        rulelists = perqun[0].qunrulename.all()
    except:
        rulelists=""
    data_list, page_range, count, page_nums = pagination(request, rulelists)
    content = {
        "name": name,
        "typeid": typeid,
        'data': data_list,
        # 'query': query,
        'page_range': page_range,
        'count': count,
        'page_nums': page_nums,
        # 'page_title': "规则列表",
    }
    # context={"name":name,"rulelists":rulelists,"typeid":typeid}
    return render(request,"user/confqun.html",context=content)
# return render(request, "user/confqun.html", context)
@login_required
def qunper(request,name):
    rulelists = QunPer.objects.filter(qunrulename=name)
    context={"name":name,"rulelists":rulelists}
    return render(request,"user/confqun.html",context)
@login_required
def perrulelist(request,type,name,pk):
    global query,allrules
    if type=='qun':
        try:
            qun=QunPer.objects.get(qunname=name)
            qunrules=qun.qunrulename.all()
            allrules=rulelistmodel.objects.exclude(pk__in=qunrules)
        except:
            allrules=rulelistmodel.objects.order_by('id')
    else:
        try:
            qun=SinPer.objects.get(Sinname=name)
            qunrules=qun.qunrulename.all()
            allrules=rulelistmodel.objects.exclude(pk__in=qunrules)
        except:
            allrules=rulelistmodel.objects.order_by('id')
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
        'pk':pk,
        'type':type
    }
    return render(request,'user/rules_list.html',context)
@login_required
def confqunper(request):
    if request.is_ajax():
        lists = request.POST.get("data")
        lists=json.loads(lists)
        listqun = request.POST.get("qun")
        ruleid = request.POST.get("ruleid")
        mytype = request.POST.get("mytype")
        ruleid=int(ruleid)
        if mytype=='qun':
            qunid=qun.objects.get(name=unquote(listqun))
            QunPer.objects.update_or_create(qunname=unquote(listqun))
            qunper =QunPer.objects.get(qunname=unquote(listqun))
            myty='qun'
        else:
            qunid=person.objects.get(descname=unquote(listqun))
            SinPer.objects.update_or_create(Sinname=unquote(listqun))
            qunper = SinPer.objects.get(Sinname=unquote(listqun))
            myty='person'
        if ruleid!=0:
            rule = rulelistmodel.objects.get(pk=ruleid)
            print (rule)
            qunper.qunrulename.remove(rule)
        for i in lists:
            rulei = rulelistmodel.objects.get(rulename=i)
            qunper.qunrulename.add(rulei)
            # QunPer.objects.update_or_create(qunname=unquote(listqun),qunrulename=rulei,ctime=rulei.ctime,cuser=rulei.cuser)
        return HttpResponse(json.dumps({"qun":unquote(listqun),"qunid":qunid.id,"myty":myty}), content_type='application/json')
@login_required
def removerule(request,type,pk1,pk2):
    rule=rulelistmodel.objects.get(pk=pk1)
    if type=='qun':
        qun=QunPer.objects.get(qunname=pk2)
    else:
        qun=SinPer.objects.get(Sinname=pk2)
    try:
        qun.qunrulename.remove(rule)
        data="success"
    except:
        data="error"
    return JsonResponse(data, safe=False)
