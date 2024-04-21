import scrapy


class VisasqSpider(scrapy.Spider):
    name = "visasq"
    allowed_domains = ["service.visasq.com"]
    start_urls = [
        "https://service.visasq.com/issues?keyword=&page={}&is_started_only=true".format(
            i
        )
        for i in range(1, 13)
    ]

    def clean_text(self, text):
        return text.replace("\n", "").replace("　", "").strip()

    def parse(self, response):
        for issue_item in response.css("li[qa='issue_item']"):
            yield {
                "title": self.clean_text(
                    issue_item.css("h3[qa-heading='issue_title']::text").get()
                ),
                "content": self.clean_text(
                    issue_item.css("p[qa-content='issue_description']::text").get()
                ),
                "price": self.clean_text(issue_item.css("span.text::text").get()),
                "link": f"https://service.visasq.com{issue_item.css('a::attr(href)').get()}",
            }
