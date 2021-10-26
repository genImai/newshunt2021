from django.urls.base import reverse, reverse_lazy
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
    if Setting.objects.filter(id=request.user.id).values_list('key1',flat=True).exists():
        redirect_url = reverse('list')
        param = urlencode({'key':Setting.objects.values_list('key1',flat=True).get(id=request.user.id)})
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
    k = 1 #ORICON
    
    newsTitle1=[] 
    newsLink1=[]
    newsTime1=[]
    newsData1=[]
    
    newsTitle2=[] 
    newsLink2=[]
    newsTime2=[]
    newsData2=[]
    
    newsTitle3=[] 
    newsLink3=[]
    newsTime3=[]
    newsData3=[]
    
    newsTitle4=[] 
    newsLink4=[]
    newsTime4=[]
    newsData4=[]
    
    newsTitle5=[] 
    newsLink5=[]
    newsTime5=[]
    newsData5=[]
    
    if 'key' in request.GET:
        key = request.GET['key']
        
    while i<=5 and j<=421 and k<=5:
        
        urls1 = ['https://news.yahoo.co.jp/topics/top-picks?page=' + str(i),    #site1
                'https://www.nikkei.com/news/category/?bn=' + str(j),           #site3
                'https://www.oricon.co.jp/category/interest/p/' + str(k) + '/', #site4
        ]
        
        #マルチスレッディングでrequests
        #ページ遷移でスクレイピング(ループ処理)
        with ThreadPoolExecutor(2) as executor:
            res = list(executor.map(requests.get,urls1))
            
            #yahooニュース(site1)
            if Setting.objects.filter(id=request.user.id).values_list('site1',flat=True):    
                soup = BeautifulSoup(res[0].content, 'lxml')
                
                elems = soup.find_all('div',class_='newsFeed_item_title', text=re.compile(key))
                for elem in elems:
                    newsTitle1.append(elem.text)
                    newsLink1.append(elem.parent.parent.get('href'))
                    newsTime1.append(elem.next_sibling.text)
                
                i += 1
                
            #日経電子版(site3)
            if Setting.objects.filter(id=request.user.id).values_list('site3',flat=True):
                soup = BeautifulSoup(res[1].content, 'lxml')

                elems = soup.find_all('a',href=re.compile('/article/'),text=re.compile(key))
                
                for elem in elems:
                    if elem.find_parent('span'):
                        newsTitle3.append(elem.text)
                        newsLink3.append('https://www.nikkei.com/' + elem.get('href'))
                        newsTime3.append(elem.find_parent().find_next_sibling().findChild('span').text)
                
                j += 30    
        

            #ORICON NEWS(site4)
            if Setting.objects.filter(id=request.user.id).values_list('site4',flat=True):
                soup = BeautifulSoup(res[2].content, 'lxml')

                elems = soup.find_all('h2',class_='title',text=re.compile(key))
                
                for elem in elems:
                    newsTitle4.append(elem.text)
                    newsLink4.append('https://www.oricon.co.jp' + elem.find_parent('a').get('href'))
                    newsTime4.append(elem.find_parent(class_='card-body').find_next_sibling(class_='card-footer').find(class_='en').text)
                
                k += 1
                
        urls2 = ['https://www.jiji.com/jc/list?g=news',#site2
                'https://www.nikkansports.com/news/',  #site5
        ]
            
    #時事ドットコム(site2)
    if Setting.objects.filter(id=request.user.id).values_list('site2',flat=True):
        res = requests.get(urls2[0])
        soup = BeautifulSoup(res.content, 'lxml')

        elems = soup.find_all('p',text=re.compile(key))
            
        for elem in elems:
            if elem.find_next_sibling(): 
                newsTitle2.append(elem.text)
                newsLink2.append('https://www.jiji.com' + elem.parent.get('href'))
                newsTime2.append(elem.find_next_sibling().text)
            else:
                pass
            
    #日刊スポーツ(site5)
    if Setting.objects.filter(id=request.user.id).values_list('site5',flat=True):
        res = requests.get(urls2[1])
        soup = BeautifulSoup(res.content, 'lxml')

        elems = soup.find_all('a',href=re.compile('https://www.nikkansports.com/'),text=re.compile(key))
        for elem in elems:
            if elem.find_next_sibling():
                newsTitle5.append(elem.text)
                newsLink5.append(elem.get('href'))
                newsTime5.append(elem.find_next_sibling().text)
            else:
                pass
    
    for i,_ in enumerate(newsTitle1):
        newsData1.append({
            'newsTitle1': newsTitle1[i],
            'newsLink1': newsLink1[i],
            'newsTime1': newsTime1[i],
        })
    for i,_ in enumerate(newsTitle2):
        newsData2.append({
            'newsTitle2': newsTitle2[i],
            'newsLink2': newsLink2[i],
            'newsTime2': newsTime2[i],
        })
    for i,_ in enumerate(newsTitle3):
        newsData3.append({
            'newsTitle3': newsTitle3[i],
            'newsLink3': newsLink3[i],
            'newsTime3': newsTime3[i],
        })
    for i,_ in enumerate(newsTitle4):
        newsData4.append({
            'newsTitle4': newsTitle4[i],
            'newsLink4': newsLink4[i],
            'newsTime4': newsTime4[i],
        })
    for i,_ in enumerate(newsTitle5):
        newsData5.append({
            'newsTitle5': newsTitle5[i],
            'newsLink5': newsLink5[i],
            'newsTime5': newsTime5[i],
        })
        
    newsCount1 = len(newsTitle1)
    newsCount2 = len(newsTitle2)
    newsCount3 = len(newsTitle3)
    newsCount4 = len(newsTitle4)
    newsCount5 = len(newsTitle5)
    
    context = {
        #ログインユーザーの設定値
        'data': data,
        #ニュースデータ
        'newsData1': newsData1,
        'newsData2': newsData2,
        'newsData3': newsData3,
        'newsData4': newsData4,
        'newsData5': newsData5,
        'newsCount1': newsCount1,
        'newsCount2': newsCount2,
        'newsCount3': newsCount3,
        'newsCount4': newsCount4,
        'newsCount5': newsCount5,
    }
        
    return render(request, 'newsapp/list.html', context,)

@verified_email_required
#設定ルート分岐
def settingConf(request):
    if Setting.objects.filter(id=request.user.id).exists():
        return redirect('update',pk=request.user.pk)
    else:
        return redirect('create')
        

#設定(初回登録)
class SettingCreateView(LoginRequiredMixin,CreateView):
    model = Setting
    form_class = SettingForm
    template_name = 'newsapp/setting.html'
    success_url = reverse_lazy('index')
    
    # def get_success_url(self):
    #     return reverse('update', kwargs={'pk':self.object.pk})
    
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
    success_url = reverse_lazy('index')
    
    # def get_success_url(self):
    #     return reverse('update',kwargs={'pk':self.object.pk})
    
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