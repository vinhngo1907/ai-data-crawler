import os, requests, re, random, datetime as dt
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from dotenv import load_dotenv, dotenv_values

# from twitterscraper import query_tweets
# from ast import literal_eval

config = dotenv_values(".env")

api_key = config["API_KEY"]
cse_id = config["CSE_ID"]


def google_query(query, **kwargs):
    """
    :param query:
    :param kwargs:
    :return: scrape data
    """
    query_service = build("customsearch", "v1", developerKey=api_key)
    query_results = query_service.cse().list(q=query, cx=cse_id, **kwargs).execute()

    try:
        return query_results["items"]
    except:
        return dict()


keywords = ["Crime", "Child Abuse", "Women Abuse", "Cyber Bullying"]


def crawling(query, keywords):
    """
    :param query:
    :param keywords:
    :return: crawled links, scrape data
    """
    general = list()
    crime = list()
    child_abuse = list()
    women_abuse = list()
    pornography = list()
    rape = list()
    cyber_bullying = list()
    general_scrape = list()
    crime_scrape = list()
    child_abuse_scrape = list()
    women_abuse_scrape = list()
    pornography_scrape = list()
    rape_scrape = list()
    cyber_bullying_scrape = list()

    lists = [
        general,
        crime,
        child_abuse,
        women_abuse,
        pornography,
        rape,
        cyber_bullying,
    ]

    scrape_lists = [
        general_scrape,
        crime_scrape,
        child_abuse_scrape,
        women_abuse_scrape,
        pornography_scrape,
        rape_scrape,
        cyber_bullying_scrape,
    ]

    base_search_url = "https://www.google.co.in/search?q="

    for keyword, list_update, list_update2 in zip(keywords, lists, scrape_lists):
        try:
            num = random.randint(7, 10)
            pages = google_query(f"{query} {keyword}", num=num)
            for result in pages:
                list_update.append((result["link"], result))
                list_update2.append(result["link"])
        except:
            print("bs4 algo running...")
            empty = dict()
            page = requests.get(base_search_url + query + keyword)
            soup = BeautifulSoup(page.content, "html.parser")
            links = soup.findAll("a")
            result_div = soup.find_all(
                "a", href=re.compile("(?<=/url\?q=)(htt.*://.*)")
            )
            for link in result_div:
                print("here")
                link = re.split(":(?=http)", link["href"].replace("/url?q=", ""))
                x = str(link).split("&")
                empty = scraper(x[0].replace("['", ""))
                list_update.append((x[0].replace("['", ""), empty))
                list_update2.append(x[0].replace("['", ""))

    context = {
        "general": general,
        "crime": crime,
        "child abuse": child_abuse,
        "woman abuse": women_abuse,
        "cyber bullying": cyber_bullying,
    }

    reduced = [
        general[:4],
        crime[:4],
        child_abuse[:4],
        women_abuse[:4],
        cyber_bullying[:4],
    ]

    reduced2 = [
        general_scrape[:4],
        crime_scrape[:4],
        child_abuse_scrape[:4],
        women_abuse_scrape[:4],
        cyber_bullying_scrape[:4],
    ]

    return context, reduced, reduced2, lists


def count_items(context):
    list_count_dict = dict()
    temp = list()
    for key, value in context.items():
        for key2, value2 in value.items():
            temp.append(len(value2))
        list_count_dict[key] = temp
        temp = []
    return list_count_dict


def wiki_scraping(link):
    print("scraping")
    page = requests.get(str(link.split("%")[0]))
    infobox = dict()
    empty = True
    if page.status_code is 200:
        print("first success")
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            empty = False
            table = soup.select(".infobox")[0]
            rows = table.find_all("tr")
            flag = 1
            i = 0
            length = len(rows)
            for i in range(length):
                try:
                    if i == 0:
                        infobox["name"] = str(rows[i].th.text)
                        flag = 0
                    else:
                        infobox[str(rows[i].th.text)] = str(rows[i].td.text)
                except:
                    pass
        except:
            empty = True
    else:
        print("Can't reach to servers")
    return infobox, empty


def wiki_data(lists):
    """

    :param lists:
    :return: dictionary of meta data
    """
    context = dict()
    temp = list()

    for i in lists:
        temp.append(i.split("%")[0])
    for link in temp:
        context[str(link)] = wiki_scraping(link)
    return context


def scraper(link):
    """

    :param link:
    :return: scrape data
    """
    print(f"scraping {link}")
    if "youtube" in str(link):
        return {}
    else:
        page = requests.get(str(link))
        soup = BeautifulSoup(page.content, "html.parser")
        metadata = dict()
        for tag in soup.find_all("meta"):
            name = tag.attrs.get("name")
            property = tag.attrs.get("property")
            content = tag.attrs.get("content")
            if name or property:
                if name:
                    if ":":
                        names = name.split(":")
                        name = names[1]
                    metadata[name] = content
                else:
                    if ":" in property:
                        props = property.split(":")
                        property = props[1]
                    metadata[property] = content
        print(metadata)
        return metadata


def social_media_scrape(keyword):
    result = {}
    temp = {}
    base_url = "twitter.com"
    query = str(keyword) + " " + keywords[0]
    # tweets = query_tweets(query, limit=1, begindate=dt.date(2023, 6, 21), proxy=None)
    # return tweets
    return True


def extract_images(data):
    print("exttracting images", data)
    try:
        image = data["pagemap"]["metatags"][0]["og:image"]
        return image
    except:
        pass


def create_predict_image(images, images_list):
    context = dict()
    for image in images:
        for image_list in images_list:
            context[image] = image_list

    return context
