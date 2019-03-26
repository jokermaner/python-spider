# -*- coding: utf-8 -*-
import scrapy
import json
import re
from zhihu2.items import Zhihu2Item
from scrapy_redis.spiders import RedisCrawlSpider


class UserinforSpider(RedisCrawlSpider):
    name = "userinfor"
    redis_key = 'myspider:start_urls'
    allowed_domains = ["zhihu.com"]

    # start_urls = ['https://www.zhihu.com/api/v4/members/liuyu-43-97/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20']

    def parse(self, response):
        temp_data = json.loads(response.body.decode("utf-8"))["data"]

        count = len(temp_data)
        if count < 20:
            pass
        else:
            page_offset = int(re.findall("&offset=(.*?)&", response.url)[0])
            new_page_offset = page_offset + 20
            next_page_url = response.url.replace("&offset=" + str(page_offset) + "&",
                                                 "&offset=" + str(new_page_offset) + "&")
            yield scrapy.Request(url=next_page_url, callback=self.parse)

        for eve_user in temp_data:
            item = Zhihu2Item()
            item['name'] = eve_user['name']
            item['url_token'] = eve_user['url_token']
            item['headline'] = eve_user['headline']
            item['follower_count'] = eve_user['follower_count']
            item['answer_count'] = eve_user['answer_count']
            item['articles_count'] = eve_user['articles_count']
            item['uid'] = eve_user['id']
            item['gender'] = eve_user['gender']
            item['type'] = eve_user['type']

            with open("userinfor.txt") as f:
                user_list = f.read()

            if eve_user['url_token'] not in user_list:
                with open("userinfor.txt", "a") as f:
                    f.write(eve_user['url_token'] + "----")
                yield item

                new_url = "https://www.zhihu.com/api/v4/members/" + eve_user[
                    'url_token'] + "/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20"
                yield scrapy.Request(url=new_url, callback=self.parse)

# # -*- coding: utf-8 -*-
# import scrapy
# import json
# import re
# from zhihu2.items import Zhihu2Item
# class UserinfoSpider(scrapy.Spider):
#     name = 'userinfo'
#     allowed_domains = ['zhihu.com']
#     start_urls = ['https://www.zhihu.com/api/v4/members/handashu?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics']
#
#     def parse(self, response):
#         name = 'user_info'
#         allowed_domains = ['zhihu.com']
#         start_urls = [
#             'https://www.zhihu.com/api/v4/members/handashu?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics']
#
#         def parse(self, response):
#
#             temp_data = json.load(response.body.decode("utf-8"))["data"]
#             count = len(temp_data)
#             if count < 20:
#                 pass
#             else:
#                 page_offset = int(re.findall("&offset=(.*?)&",response.url)[0])
#                 new_page_offset = page_offset+ 20
#                 next_page_url = response.url.replace("&offset="+str(page_offset)+"&",
#                                                      "&offset="+str(new_page_offset+"&"))
#             # print(len(temp_data))
#             # print("*"*30)
#             for eve_user in temp_data:
#                 item = Zhihu2Item()
#                 item["name"] = eve_user["name"]
#                 item["url_token"] = eve_user["url_token"]
#                 item["headline"] = eve_user["headline"]
#                 item["follower_count"] = eve_user["follower_count"]
#                 item["answer_count"] = eve_user["answer_count"]
#                 item["articles_count"] = eve_user["articles_count"]
#                 item["uid"] = eve_user["uid"]
#                 item["gender"] = eve_user["gender"]
#                 item["type"] = eve_user["type"]
#
#                 with open("userinfor.txt")as f:
#                     user_list =f.read()
#                 if eve_user('url_token')not in user_list:
#                     with open("userinfo.txt","a")as f:
#                         f.write(eve_user['urk_token']+ "----")
#                 yield item
#                 new_url ="https://www.zhihu.com/api/v4/members/"+ eve_user['url_token']+"?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"
#                 yield scrapy.Request(url=new_url,callback=self.parse)