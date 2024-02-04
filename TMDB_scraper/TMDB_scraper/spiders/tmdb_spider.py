# to run
# scrapy crawl tmdb_spider -o movies.csv -a subdir=671-harry-potter-and-the-philosopher-s-stone
import scrapy


class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'

    def __init__(self, subdir=None, *args, **kwargs):
        self.start_urls = [f"https://www.themoviedb.org/movie/{subdir}/"]

    def parse(self, response):
        yield scrapy.Request("https://www.themoviedb.org/movie/475303-a-rainy-day-in-new-york/cast",
                             callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        actors = response.css('ol.people.credits li')  # Select the <li> elements containing actor information
        for actor in actors:
            actor_link = actor.css('a::attr(href)').get()  # Extract the href attribute of the <a> tag
            if actor_link:
                yield scrapy.Request(response.urljoin(actor_link), callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        actor_name = response.css('title::text').get().split(' — ')[0]
        known_for_section = response.css('#known_for')
        titles = known_for_section.css('.title bdi::text').getall()
        for title in titles:
            yield {"actor": actor_name, 'movie_or_TV_name': title}