from gc import callbacks
import scrapy

class AosFatosSpider(scrapy.Spider):
    name = 'aos_fatos'

    start_urls = ['https://aosfatos.org/',
                  'https://www.aosfatos.org/noticias/checamos/verdadeiro/']

    def parse(self, response):
        """
        Navega pelo menu lateral do site pra pegar as categorias
        """
        links = response.xpath(
            '//nav//ul//li/a[re:test(@href,"checamos")]/@href'
            ).getall()
        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_category
            )

    def parse_category(self, response):
        """
        Dentro de cada categoria, pega todas as notícias
        """
        news = response.css('a.entry-item-card::attr(href)').getall()
        for new_url in news:
            yield scrapy.Request(
                response.urljoin(new_url),
                callback=self.parse_new
            )

    def parse_new(self, response):
        title = response.css('article h1::text').get()
        date = ' '.join(response.css('div.publish-date::text').get().split())
        # quote = 
        # statu_quote = 
        # url = 
        yield {
            'title': title,
            'date': date,
            'url': response.url
        }




    # um método de callback no scrapy retorna 
    # um novo request ou dicionário ou um item
    # se eu não definir um callback (é opcional), ele vai mandar pra def parse por padrão

    # HTTPCACHE_ENABLED=1 salva as páginas em cache no sistema de arquivos
    # isso é bom pq em dev não ficamos toda hora fazendo request pro servidor
    # e tbm dá pra controlar a qtd de requests simultâneos
    # sempre importante ter educação com o servidor alheio!
    # pra salvar os responses é com -o nome.csv
    # scrapy runspider hello-aos-fatos.py -s HTTPCACHE_ENABLED=1 -o quotes.csv