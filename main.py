import json
import requests
from bs4 import BeautifulSoup



def get_first_news():
    headers = {
        "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5128.120 Safari/537.36"
    }
    
    url = "https://www.computerworld.com/news/"
    r = requests.get(url = url, headers = headers)
    
    soup = BeautifulSoup(r.text, "lxml")
    
    article_cards = soup.find_all("div", class_ = "river-well article")
    
    news_dict = {}
    
    for article in article_cards:
        
        article_title = article.find("h3").text.strip() #name article
        article_desc = article.find("h4").text.strip() #desc

        article_url_end = article.find("a").get("href")
        article_url = f'https://www.computerworld.com{article_url_end}'
        article_id = article_url.split("/")[-2]
    
        
        #print(f"{article_title} | {article_url} | {article_desc}")
        
        news_dict[article_id] = {
            'article_title': article_title,
            'article_desc': article_desc,
            'article_url': article_url
        }
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    # print(r)
    
    
def check_news():
    with open('news_dict.json') as file:
        news_dict = json.load(file)
        
        
    headers = {
        "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5128.120 Safari/537.36"
    }
    
    url = "https://www.computerworld.com/news/"
    r = requests.get(url = url, headers = headers)
    
    soup = BeautifulSoup(r.text, "lxml")
    
    article_cards = soup.find_all("div", class_ = "river-well article")
    
    fresh_news = {}
    
    for article in article_cards:
        article_url_end = article.find("a").get("href")
        article_url = f'https://www.computerworld.com{article_url_end}'
        article_id = article_url.split("/")[-2]
        
        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h3").text.strip() #name article
            article_desc = article.find("h4").text.strip() #desc
            
        
            news_dict[article_id] = {
                'article_title': article_title,
                'article_desc': article_desc,
                'article_url': article_url
            } 
            fresh_news[article_id] = {
                'article_title': article_title,
                'article_desc': article_desc,
                'article_url': article_url            
            }
        
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
        
    return fresh_news
          
    
def main():
    #get_first_news()
    print(check_news())
    
    
if __name__ == "__main__":
    main()
        
        
    