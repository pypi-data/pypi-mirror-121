# The MIT License (MIT)

# Copyright (c) 2016 Ahmet Aksoy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

content = """a
acaba
altı
altmış
ama
ancak
arada
artık
asla
aslında
aslında
ayrıca
az
bana
bazen
bazı
bazıları
belki
ben
benden
beni
benim
beri
beş
bile
bilhassa
bin
bir
biraz
birçoğu
birçok
biri
birisi
birkaç
birşey
biz
bizden
bize
bizi
bizim
böyle
böylece
bu
buna
bunda
bundan
bunlar
bunları
bunların
bunu
bunun
burada
bütün
çoğu
çoğunu
çok
çünkü
da
daha
dahi
dan
de
defa
değil
diğer
diğeri
diğerleri
diye
doksan
dokuz
dolayı
dolayısıyla
dört
e
edecek
eden
ederek
edilecek
ediliyor
edilmesi
ediyor
eğer
elbette
elli
en
etmesi
etti
ettiği
ettiğini
fakat
falan
filan
gene
gereği
gerek
gibi
göre
hala
halde
halen
hangi
hangisi
hani
hatta
hem
henüz
hep
hepsi
her
herhangi
herkes
herkese
herkesi
herkesin
hiç
hiçbir
hiçbiri
i
ı
için
içinde
iki
ile
ilgili
ise
işte
itibaren
itibariyle
kaç
kadar
karşın
kendi
kendilerine
kendine
kendini
kendisi
kendisine
kendisini
kez
ki
kim
kime
kimi
kimin
kimisi
kimse
kırk
madem
mi
mı
milyar
milyon
mu
mü
nasıl
ne
neden
nedenle
nerde
nerede
nereye
neyse
niçin
nin
nın
niye
nun
nün
o
öbür
olan
olarak
oldu
olduğu
olduğunu
olduklarını
olmadı
olmadığı
olmak
olması
olmayan
olmaz
olsa
olsun
olup
olur
olur
olursa
oluyor
on
ön
ona
önce
ondan
onlar
onlara
onlardan
onları
onların
onu
onun
orada
öte
ötürü
otuz
öyle
oysa
pek
rağmen
sana
sanki
sanki
şayet
şekilde
sekiz
seksen
sen
senden
seni
senin
şey
şeyden
şeye
şeyi
şeyler
şimdi
siz
siz
sizden
sizden
size
sizi
sizi
sizin
sizin
sonra
şöyle
şu
şuna
şunları
şunu
ta
tabii
tam
tamam
tamamen
tarafından
trilyon
tüm
tümü
u
ü
üç
un
ün
üzere
var
vardı
ve
veya
ya
yani
yapacak
yapılan
yapılması
yapıyor
yapmak
yaptı
yaptığı
yaptığını
yaptıkları
ye
yedi
yerine
yetmiş
yi
yı
yine
yirmi
yoksa
yu
yüz
zaten
zira"""
    
stopwordList = []

for line in content.split("\n"):
    stopwordList.append(line)

class Stopfortr:
    
    def remove_links(text):
        '''Takes a string and removes web links from it'''
        text = re.sub(r'http\S+', '', text)  # remove http links
        text = re.sub(r'bit.ly/\S+', '', text)  # remove bitly links
        text = text.strip('[link]')  # remove [links]
        text = re.sub(r'#', '', text)
        return text
    
    def remove_users(text):
        '''Takes a string and removes retweet and @user information'''
        text = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)',
                       '', text)  # remove retweet
        text = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)',
                       '', text) # remove tweeted at
        text = re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)',
                       '', text) # remove hashtags
        return text
    
    def clean_text(text):
        my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@'
        text = Stopfortr.remove_users(text)
        text = Stopfortr.remove_links(text)
        text = text.lower()  # lower case
        text = re.sub('[' + my_punctuation + ']+', ' ', text)  # strip punctuation
        text = re.sub('\s+', ' ', text)  # remove double spacing
        text = re.sub('([0-9]+)', '', text)  # remove numbers
        return text
    
    def get_stopwordList(): #Returns all the stopwords as a list
        return stopwordList
    
    def remove_stopwords(text):
        '''
        Parameters
        ----------
        text : string

        Returns
        -------
        text : string
            Removes the Turkish stop-words from given text
        '''
        text = text.lower()
        to_return = ''
        word_list = text.split()
        for i in range(0,len(word_list),1):
            if word_list[i] in stopwordList:
                word_list[i] = None
            else:
                to_return += word_list[i] + " "
        return to_return
    
    def clean_all(text): 
        '''
        Parameters
        ----------
        text : string

        Returns
        -------
        text : string
            Removes twitter punctuations such as: Retweets, Mentions, Hashtags
            Also removes short and long website links.
        '''
        text = Stopfortr.clean_text(text)
        text = Stopfortr.remove_stopwords(text)
        return text
        
    def is_stopword(word):
        #Returns a boolean if the word is in the stop-word list
        return word in stopwordList