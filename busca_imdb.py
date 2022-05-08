from lxml import html
import requests

def buscar_peli(peli):
    url_buscar = 'https://www.imdb.com/find?q={}&ref_=nv_sr_sm'.format(peli)
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
    result = requests.get(url_buscar, headers=headers)
    parse = html.fromstring(result.content)

    text_res1 = parse.xpath('//div[@class="article"]/h1/text()')[0]
    text_res2 = parse.xpath('//h1[@class="findHeader"]/span/text()')[0]

    if not 'No results found' in text_res1:
        tabla_titles = parse.xpath('//div[@class="article"]')
        for tb_t in tabla_titles:
            div_findsection = tb_t.xpath('./div[@class="findSection"]')
            for dv in div_findsection:
                div_titul = dv.xpath('./h3[@class="findSectionHeader"]/text()')[0]
                if 'Titles' in div_titul:
                    tabla = dv.xpath('./table/tr')
                    num_resultados = len(tabla)

                    titol = str(num_resultados)+ ' Resultats per ' + text_res2 + '  en IMDB:'
                    pelis = titol + '\n\n'
                    if num_resultados >= 0:
                        for tb in tabla:
                            tb_imatge= tb.xpath('./td[1]/a/img/@src')[0]
                            tb_nom = tb.xpath('./td[2]/a/text()')[0]
                            tb_link = 'https://www.imdb.com'+tb.xpath('./td[2]/a/@href')[0]
                            tb_any = tb.xpath('./td[2]/text()')[1].strip()
                            pelis = pelis +tb_nom+' '+tb_any + '\n' + tb_link + '\n\n'
                        return pelis
                      
    else:
        return 'No hay resultados, busca el nombre en google XD'
