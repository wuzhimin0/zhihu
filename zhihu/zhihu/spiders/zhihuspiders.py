# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from zhihu.items import ZhihuItem
# from scrapy.conf import settings
from lxml import etree
import json,re

class ZhihuspidersSpider(CrawlSpider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/api/v3/feed/topstory/hot-list-web?limit=50&desktop=true']
    """
    # 知乎推荐ajax_url（随时更新）page_number代表页数，limit代表每页数量，after_id代表（暂时不知道），他的json文件中有下一页的链接，和当前页的链接
    https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=bec70d8f50bee2ba3526b8b7a96c8938&desktop=true&page_number=2&limit=6&action=down&after_id=5
    # 知乎热榜ajax_url（网站中只有50个）
    https://www.zhihu.com/api/v3/feed/topstory/hot-list-web?limit=50&desktop=true
    # 知乎热榜详情ajax加载的答案url，questions/话题的id，offset代表从第几个开始，他是页数*每页的数量，limit代表每页的数量，他的json文件中有下一页的链接，和当前页的链接
    https://www.zhihu.com/api/v4/questions/38482426/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=5&sort_by=default
    # 知乎话题：精华ajax_url，每个话题都有不同的id值，/topics/id值；offset代表从第几个开始，他是页数*每页的数量，limit表示每页的数量，他的json文件中有下一页的链接，和当前页的链接
    https://www.zhihu.com/api/v4/topics/19673988/feeds/essence?include=data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;&limit=10&offset=10
    # 知乎话题，等待回答ajax_url，offset代表从第几个开始，他是页数*每页的数量，limit表示每页的数量，他的json文件中有下一页的链接，和当前页的链接
    https://www.zhihu.com/api/v4/topics/19673988/feeds/top_question?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.annotation_detail%2Ccomment_count%3B&offset=10&limit=20
    # 知乎话题，讨论ajax_url，limit表示每页的数量，他的json文件中有下一页的链接，和当前页的链接
    https://www.zhihu.com/api/v4/topics/19673988/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=5&after_id=4880.45638
    """
    cookies = {}
    def start_requests(self):
        yield Request(url=self.start_urls[0],cookies=self.cookies)
    def parse(self, response):
        result = json.loads(response.body)
        for info in result["data"]:
            question_heat = info["target"]["metrics_area"]["text"]
            question = info["target"]["title_area"]["text"]
            question_id = info["card_id"].split("_")[-1]
            detail_url = r"https://www.zhihu.com/api/v4/questions" + "/" + question_id + "/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=5&sort_by=default"
            # detail_url = r"https://www.zhihu.com/api/v4/questions/302478047/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=5&sort_by=default"
            yield Request(url=detail_url,cookies=self.cookies,callback=self.detail_question,meta={"question":question,"question_heat":question_heat})
    def detail_question(self,response):
        result = json.loads(response.body)
        question = response.meta["question"]
        question_heat = response.meta["question_heat"]
        for info in result["data"]:
            item = ZhihuItem()
            item["question"] = question
            item["question_heat"] = question_heat
            content = ""
            video = []
            image = []
            item["answer_token"] = info["author"]["url_token"]
            item["answer_name"] = info["author"]["name"]
            contents_info = info["content"]
            contents_result = etree.HTML(contents_info)
            contents = contents_result.xpath('//p/text()')
            # 将获取到的文字删除空格并合并成一个字符串，用逗号隔开
            for con in contents:
                if "".join(con.split()):
                    content = content + "".join(con.split()) + ","
            item["content"] = content[:-1]
            images = contents_result.xpath("//img/@src")
            re_image = re.compile(r'.*jpg|png|jpeg|gif')
            for img in images:
                # 循环用正则判断正确的图片url地址并存进item
                if re_image.findall(img):
                    image.append(img)
            item["image"] = list(set(image))
            videos = contents_result.xpath("//a/@href")
            re_video = re.compile(r".*video.*")
            for v in videos:
                # 循环用正则判断正确的视频url地址并存进item
                if re_video.findall(v):
                    video.append(v)
            item["video"] = list(set(video))
            yield item
        next_page_url = result["paging"]["next"]
        yield Request(url=next_page_url,callback=self.detail_question,meta={"question":question,"question_heat":question_heat})