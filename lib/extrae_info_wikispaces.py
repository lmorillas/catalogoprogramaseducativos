# -*- coding: utf-8 -*-

import urlparse
import re
import json
from amara.bindery import html
from amara.lib import U
import shelve

catsh = shelve.open('catalogo.dat')


def quita_punto(texto):
    if texto.endswith('.'):
        return texto[:-1]
    else: return texto


def dame_texto(texto, inicio, fin):

    _ini = texto.find(inicio)
    if _ini != -1:
        i = _ini +len(inicio)
        f = texto[i:].find(fin)
        f1 = texto[i:].find('\n\n')
        _fin = min(f, f1)
        if _fin == -1:
            _fin = max(f, f1)
        texto = texto[i:i+_fin]
        texto = texto.replace (u'\u200d', '').strip()
        return texto


def parse_proyecto(url):
    item = {}
    item['url'] = url

    #doc = html.parse(url)

    #texto = U(doc.xml_select(u'//div[@class="ws-theme-content-inner"]'))
    #catsh[url.encode('utf-8')] = texto

    texto = catsh.get(url.encode('utf-8'))
    #texto = texto.decode('utf-8')

    texto = texto[texto.find("NOMBRE DE LA"):]
    nombre = dame_texto(texto, u'NOMBRE DE LA ACTUACIÓN', u'ÓRGANO GESTOR')
    item ['label'] = nombre
    gestor = dame_texto(texto, u'ÓRGANO GESTOR', u'DESCRIPCIÓN')
    if gestor:
        gestor = quita_punto(gestor)
        if '\n' in gestor:
            gestor = gestor.split('\n')
            gestor = map(quita_punto, gestor)
        item['gestor'] = gestor
    descripcion = dame_texto(texto, u'DESCRIPCIÓN', 'DESTINATARIOS')
    if descripcion:
        item['descripcion'] = descripcion
    destinatarios = dame_texto(texto, 'DESTINATARIOS', 'SOLICITUD')
    item['destinatarios'] = destinatarios
    solicitud = dame_texto(texto, 'SOLICITUD', 'FECHAS' )
    item['solicitud'] = solicitud
    fechas = dame_texto(texto, 'FECHAS' , u'FINANCIACIÓN')
    item['fechas'] = fechas
    financiacion = dame_texto(texto, u'FINANCIACIÓN', '\n\n')
    if financiacion:
        item['financiacion'] = financiacion
    masinfo = dame_texto(texto, u'MÁS INFORMACIÓN', '\n\n')
    if masinfo:
        mas_url = re.search("(?P<url>https?://[^\s]+)", masinfo)
        if mas_url:
            url = mas_url.group("url")
            masinfo = masinfo.replace(url, '<a href="{}" target="_blank">{}</a>'.format(url, url) )
        item['masinfo'] = masinfo
    return item

f = json.load(open('catacata.json'))
items = f.get('items')

nitems = []
errores = []

for it in items:
    url = it.get('url')
    if url:
        #try:
        print '-->', url
        res = parse_proyecto(url)
        nitems.append(res)
        #except:
        #    print '***', url
        #    errores.append(url)

#catsh.sync()
catsh.close()

import json
cat = json.load(open('catalogoprog.json'))
items = cat.get('items')

ld = {}
for n in nitems:
    ld[n.get('url')] = n

for it in items:
    if it.get('type') == 'ta':
        n = ld.get(it.get('url'))
        if not n:
            print '***', it
        else:
            for k in 'destinatarios fechas gestor solicitud descripcion masinfo'.split():
                it[k] = n.get(k)

json.dump(cat, open('catalogoprog.json', 'w'))


'''
    gestor = re.compile('RGANO GESTOR</h2>\W*([^<]*)', re.DOTALL)
    item['nombre'] = sel.xpath('//h1[@class="pageTitle"]//text()').extract()
    item['gestor'] = sel.re(gestor)
    item['programa'] = sel.xpath('//h1[@id="toc0"]//text()').extract()


    item['gestor'] = sel.xpath()


                item['name'] = site.xpath('a/text()').extract()
        item['url'] = site.xpath('a/@href').extract()
        item['description'] = site.xpath('text()').re('-\s([^\n]*?)\\n')
        items.append(item)
    yield item


nombre = scrapy.Field()
gestor = scrapy.Field()
descripcion = scrapy.Field()
destinatarios = scrapy.Field()
solicitud = scrapy.Field()
fechas = scrapy.Field()
financiacion = scrapy.Field()
masinfo = scrapy.Field()
apartado = scrapy.Field()

    return items

     def parse(self, response):
    for h3 in response.xpath('//h3').extract():
        yield MyItem(title=h3)

    for url in response.xpath('//a/@href').extract():
        yield scrapy.Request(url, callback=self.parse)

http://catalogo00.wikispaces.com/Reconocimiento+de+buenas+pr%C3%A1cticas+de+educaci%C3%B3n+inclusiva+y+de+convivencia.+Centros+p%C3%BAblicos+-+concertados
http://catalogo00.wikispaces.com/Reconocimiento+de+buenas+pr%C3%A1cticas+de+educaci%C3%B3n+inclusiva+y+de+convivencia.+Centros+p%C3%BAblicos+-+concertados


    "http://catalogo1.wikispaces.com/Indice+Educaci%C3%B3n+Inclusiva",
    "http://catalogo2.wikispaces.com/Indice+aprender+a+aprender",
    "http://catalogo3.wikispaces.com/Indice+Convive+y+Concilia",
    "http://catalogo4.wikispaces.com/Indice+excelencia+acad%C3%A9mica",
    "http://catalogo5.wikispaces.com/Indice+actuaciones+otros+departamentos",
    "http://catalogo6.wikispaces.com/Indice+entidades+privadas",
]


        '''
