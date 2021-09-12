from django.urls.base import reverse
from newsapp.forms import SettingForm
from newsapp.models import Setting
from allauth.account.decorators import verified_email_required
from bs4 import BeautifulSoup
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
import requests
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
from django.contrib import messages


# Create your views here.

#キーワード未登録者は設定に誘導
@verified_email_required
def indexfunc(request):
    if Setting.objects.filter(id=request.user).values_list('key1',flat=True).exists():
        redirect_url = reverse('list')
        param = urlencode({'key':Setting.objects.values_list('key1',flat=True).get(pk=request.user)})
        url = f'{redirect_url}?{param}'
        return redirect(url)
    else:
        return redirect('create')
        

@verified_email_required
def listfunc(request):         
    data = Setting.objects.filter(id=request.user).all()
    key = ''
    res = ''
    i = 1 #yahoo
    j = 1 #日経
    k = 1 #株探（材料）
    l = 1 #株探（決算）
    
    newsTitle=[] 
    newsLink=[]
    
    
    if 'key' in request.GET:
        key = request.GET['key']
        
    while i<=5 and j<=361 and k<=30 and l<=30:

        urls = ['https://news.yahoo.co.jp/topics/top-picks?page=' + str(i),
                'https://www.nikkei.com/news/category/?bn=' + str(j),
                'https://kabutan.jp/news/marketnews/?category=2&page=' + str(k),
                'https://kabutan.jp/news/marketnews/?category=3&page=' + str(l),
                'https://www.jiji.com/jc/list?g=news',
        ]
        
        #マルチスレッディングでrequests
        #ページ遷移でスクレイピング(ループ処理)
        with ThreadPoolExecutor(3) as executor:
            res = list(executor.map(requests.get,urls))
            
            #yahooニュース 
            if Setting.objects.filter(id=request.user).filter(site1=True):    
                soup = BeautifulSoup(res[0].content, 'lxml')
                
                elems = soup.find_all('div',class_='newsFeed_item_title', text=re.compile(key))
                for elem in elems:
                    newsTitle.append('【yahooニュース】' + ' ' + elem.text + ' ' + elem.next_sibling.text)
                    newsLink.append(elem.parent.parent.get('href'))
                
                i += 1

            #日経電子版
            if Setting.objects.filter(id=request.user).filter(site2=True):
                soup = BeautifulSoup(res[1].content, 'lxml')

                elems = soup.find_all('a',href=re.compile('/article/'),text=re.compile(key))
                
                for elem in elems:
                    newsTitle.append('【日経電子版】' + ' ' + elem.text)
                    newsLink.append('https://www.nikkei.com/' + elem.get('href'))
                
                j += 30
            
            #株探（材料）
            if Setting.objects.filter(id=request.user).filter(site3=True):
                soup = BeautifulSoup(res[2].content, 'lxml')

                elems = soup.find_all('a',href=re.compile('/news/marketnews/'),text=re.compile(key))
                
                for elem in elems:
                    newsTitle.append('【株探（材料）】' + ' ' + elem.text)
                    newsLink.append('https://kabutan.jp' + elem.get('href'))
                    
                k += 1
                
            #株探（決算）
            if Setting.objects.filter(id=request.user).filter(site4=True):
                soup = BeautifulSoup(res[3].content, 'lxml')

                elems = soup.find_all('a',href=re.compile('/news/marketnews/'),text=re.compile(key))
                
                for elem in elems:
                    newsTitle.append('【株探（決算）】' + ' ' + elem.text)
                    newsLink.append('https://kabutan.jp' + elem.get('href'))
                    
                l += 1
            
    #時事ドットコム
    if Setting.objects.filter(id=request.user).filter(site5=True):
        soup = BeautifulSoup(res[4].content, 'lxml')

        elems = soup.find_all('p',text=re.compile(key))
            
        for elem in elems:
            newsTitle.append('【時事ドットコム】' + ' ' + elem.text)
            newsLink.append('https://www.jiji.com' + elem.parent.get('href'))
    
        

    context = {
        #ログインユーザーの設定値
        'data': data,
        'titles': newsTitle,
        'links': newsLink, 
    }
        
    return render(request, 'newsapp/list.html', context,)

@verified_email_required
#設定ルート分岐
def settingConf(request):
    if Setting.objects.filter(id=request.user).exists():
        return redirect('update',pk=request.user.pk)
    else:
        return redirect('create')
        

#設定(初回登録)
class SettingCreateView(LoginRequiredMixin,CreateView):
    
    model = Setting
    form_class = SettingForm
    template_name = 'newsapp/setting.html'
    
    def get_success_url(self):
        return reverse('update', kwargs={'pk':self.object.pk})
    
    def form_valid(self, form):
        qryset =  form.save(commit=False)
        qryset.id = self.request.user
        if qryset.key2 == '':
            qryset.key2 = '未登録'
        if qryset.key3 == '':
            qryset.key3 = '未登録'
        qryset.save()
        messages.success(self.request, '登録完了しました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '登録完了できません。')
        return super().form_invalid(form)
    
    
#設定（更新）
class SettingUpdateView(LoginRequiredMixin,UpdateView):
    model = Setting
    form_class = SettingForm
    template_name ='newsapp/setting.html'
    
    
    def get_success_url(self):
        return reverse('update',kwargs={'pk':self.object.pk})
    
    def form_valid(self, form):
        qryset = form.save(commit=False)
        qryset.id = self.request.user
        if qryset.key2 == '':
            qryset.key2 = '未登録'
        if qryset.key3 == '':
            qryset.key3 = '未登録'
        qryset.save()
        messages.success(self.request, '設定を更新しました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '設定を更新できません。')
        return super().form_invalid(form)