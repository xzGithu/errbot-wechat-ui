#coding:utf-8
from django.db import models

# Create your models here.

class qun(models.Model):
    name=models.CharField(max_length=200,verbose_name="群名称")
    class Meta:
        db_table = 'ui_qun'
        permissions = (
            ("can_read_qun", "读取群权限"),
            ("can_change_qun", "更改群权限"),
            ("can_add_qun", "添加群权限"),
            ("can_delete_qun", "删除群权限"),
        )
        verbose_name = '群表'
        verbose_name_plural = '群表'
    def __str__(self):
        return self.name

class person(models.Model):
    descname=models.CharField(max_length=200,verbose_name="备注名")
    nickname=models.CharField(max_length=200,verbose_name="昵称",blank=True,null=True)
    group=models.CharField(max_length=1000,verbose_name="所属群组",blank=True,null=True)
    isfriend=models.IntegerField(verbose_name="是否好友",blank=True,null=True)
    class Meta:
        db_table = 'ui_person'
        permissions = (
            ("can_read_person", "读取好友权限"),
            ("can_change_person", "更改好友权限"),
            ("can_add_person", "添加好友权限"),
            ("can_delete_person", "删除好友权限"),
        )
        verbose_name = '好友表'
        verbose_name_plural = '好友表'
    def __str__(self):
        return self.descname

class permis(models.Model):
    rulename=models.CharField(max_length=200,verbose_name="规则名称")
    opername=models.CharField(max_length=200,verbose_name="对应的函数名")
    chengyuan=models.CharField(max_length=1000,verbose_name="允许列表")
    class Meta:
        db_table="ui_permis"
        permissions = (
            ("can_read_permis", "读取acl权限"),
            ("can_change_permis", "更改acl权限"),
            ("can_add_permis", "添加acl权限"),
            ("can_delete_permis", "删除acl权限"),
        )
        verbose_name = 'acl表'
        verbose_name_plural = 'acl表'
class rulelistmodel(models.Model):
    status_choice=(
        ('0',u'启用'),
        ('1',u'禁用'),
    )
    rulename=models.CharField(max_length=200,verbose_name="规则名称")
    cuser=models.CharField(max_length=100,verbose_name="创建人")
    ctime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    class Meta:
        db_table="ui_rulelist"
        permissions = (
            ("can_read_rule", "读取规则权限"),
            ("can_change_rule", "更改规则权限"),
            ("can_add_rule", "添加规则权限"),
            ("can_delete_rule", "删除规则权限"),
        )
        verbose_name = '规则表'
        verbose_name_plural = '规则表'
    def __str__(self):
        return self.rulename

class QunPer(models.Model):
    qunname = models.CharField(max_length=400, verbose_name="群名称")
    qunrulename = models.ManyToManyField(rulelistmodel, related_name='rusper', max_length=400, verbose_name="规则名称")
    class Meta:
        db_table = 'ui_qunper'

    def grouprule_list(self):
        return ','.join([i.rulename for i in self.qunrulename.all()])

class SinPer(models.Model):
    Sinname = models.CharField(max_length=400, verbose_name="备注名")
    qunrulename = models.ManyToManyField(rulelistmodel, related_name='sinper', max_length=400, verbose_name="规则名称")
    class Meta:
        db_table = 'ui_sinper'

    def sinrule_list(self):
        return ','.join([i.rulename for i in self.qunrulename.all()])
    # ctime = models.DateTimeField(verbose_name="创建时间")
    # cuser = models.CharField(max_length=100, verbose_name="创建人")
class commands(models.Model):
    status_choice=(
        ('0',u'启用'),
        ('1',u'禁用'),
    )
    rulename = models.ForeignKey(rulelistmodel,max_length=200, related_name='rus',verbose_name="规则名称")
    fanan=models.CharField(max_length=200,verbose_name="方案名称")
    zhiling=models.CharField(max_length=400,verbose_name="指令用例")
    status=models.CharField(choices=status_choice,max_length=50,verbose_name="状态")
    params=models.CharField(max_length=300,verbose_name="参数顺序")
    ctime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    cuser=models.CharField(max_length=100,verbose_name="创建人")
    class Meta:
        db_table="ui_command"
        permissions = (
            ("can_read_command", "读取指令权限"),
            ("can_change_command", "更改指令权限"),
            ("can_add_command", "添加指令权限"),
            ("can_delete_command", "删除指令权限"),
        )
        verbose_name = '指令表'
        verbose_name_plural = '指令表'
    def __str__(self):
        return self.zhiling


