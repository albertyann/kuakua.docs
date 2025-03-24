import requests
import html2text
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os

proxies = {
    "http": "http://192.168.18.54:7890",
    "https": "http://192.168.18.54:7890",
}

def url_to_markdown(url, output_file=None):
    """
    将网页URL转换为Markdown文件
    
    参数:
        url (str): 要转换的网页URL
        output_file (str, optional): 输出Markdown文件路径。如果未提供，将基于URL生成文件名
    """
    try:
        # 获取网页内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        _, path = url.split('docs/')
        print(path)
        if path != '':
            output_file = path.replace('/', '_') + '.md'

        # print(output_file)
        # exit()

        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # 检查请求是否成功
        
        # 初始化html2text转换器
        h = html2text.HTML2Text()
        h.ignore_links = False  # 保留链接
        h.ignore_images = False  # 保留图片
        h.body_width = 0  # 不自动换行
        
        soup = BeautifulSoup(response.text, 'html.parser')
        main_div = soup.find('main')
        # summary = main_div.find('h2',id='summary').next_sibling
        all_divs = soup.find_all('h4', string="Did you like it? Help us spread the word!")
        if all_divs:
            all_divs[0].find_parent('div').extract()
        markdown_text = h.handle(str(main_div))
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        
        print(f"成功将网页内容保存为Markdown文件: {output_file}")
        return output_file
    
    except requests.exceptions.RequestException as e:
        print(f"获取网页内容时出错: {e}")
    except Exception as e:
        print(f"处理过程中出错: {e}")

# 使用示例
if __name__ == "__main__":
    # 示例URL - 替换为你想要转换的网页
    urls = [
        # "https://kuakua.app/zh-Hans/docs",
        # "https://kuakua.app/zh-Hans/docs/positive-psychology",
        # "https://kuakua.app/zh-Hans/docs/positive-psychology/second-wave-positive-psychology",
        # "https://kuakua.app/zh-Hans/docs/positive-psychology/happiness-subjective-well-being",
        # "https://kuakua.app/zh-Hans/docs/positive-psychology/eudaimonia",
        # "https://kuakua.app/zh-Hans/docs/positive-psychology/character-strengths-happiness",
        # "https://kuakua.app/zh-Hans/docs/positive-psychology/emotion-feeling",
        # "https://kuakua.app/zh-Hans/docs/positive-psychology/flow-the-psychology-of-optimal-experience",
        # "https://kuakua.app/zh-Hans/docs/positive-psychology/positive-psychology-network-concept-paper",
        # "https://kuakua.app/zh-Hans/docs/humanistic-psychology",
        # "https://kuakua.app/zh-Hans/docs/humanistic-psychology/hierarchy-of-needs",
        # "https://kuakua.app/zh-Hans/docs/humanistic-psychology/intrinsic-motivation",
        # "https://kuakua.app/zh-Hans/docs/humanistic-psychology/person-centered-therapy",
        # "https://kuakua.app/zh-Hans/docs/humanistic-psychology/self-actualization",
        # "https://kuakua.app/zh-Hans/docs/feminist-psychology",
        # "https://kuakua.app/zh-Hans/docs/feminist-psychology/book",
        # "https://kuakua.app/zh-Hans/docs/feminist-psychology/relational-cultural-theory",
        # "https://kuakua.app/zh-Hans/docs/feminist-psychology/power-control-theory",
        # "https://kuakua.app/zh-Hans/docs/feminist-psychology/ambivalent-sexism",
        # "https://kuakua.app/zh-Hans/docs/feminist-psychology/feminism",
        # "https://kuakua.app/zh-Hans/docs/feminist-psychology/feminism/book",
        # "https://kuakua.app/zh-Hans/docs/family-psychology",
        # "https://kuakua.app/zh-Hans/docs/developmental-psychology",
        # "https://kuakua.app/zh-Hans/docs/behaviorism-psychology",
        # "https://kuakua.app/zh-Hans/docs/psychoanalysis",
        # "https://kuakua.app/zh-Hans/docs/social-psychology",
        # "https://kuakua.app/zh-Hans/docs/personality-psychology",
        # "https://kuakua.app/zh-Hans/docs/neuroscience",
        # "https://kuakua.app/zh-Hans/docs/psychologists",
        # "https://kuakua.app/zh-Hans/docs/product-psychology",
        # "https://kuakua.app/zh-Hans/docs/product-psychology/the-psychology-of-design",
        # "https://kuakua.app/zh-Hans/docs/product-psychology/AI-in-psychology",
        # "https://kuakua.app/zh-Hans/docs/history-of-psychology",
        # "https://kuakua.app/zh-Hans/docs/history-of-psychology/psychoanalytic",
        # "https://kuakua.app/zh-Hans/docs/history-of-psychology/behavioral-psychology",
        # "https://kuakua.app/zh-Hans/docs/history-of-psychology/cognitive-psychology",
        # "https://kuakua.app/zh-Hans/docs/history-of-psychology/humanism",
        # "https://kuakua.app/zh-Hans/docs/history-of-psychology/sociocultural-psychology",
        # "https://kuakua.app/zh-Hans/docs/history-of-psychology/biological-perspective",
        # "https://kuakua.app/zh-Hans/docs/history-of-psychology/evolutionary",
        # "https://kuakua.app/zh-Hans/docs/history-of-psychology/positive-psychology",
        # "https://kuakua.app/zh-Hans/docs/psychology-research",
        # "https://kuakua.app/zh-Hans/docs/psychology-research/cognitive-psychology-experiments",
        # "https://kuakua.app/zh-Hans/docs/psychology-research/emoji-in-psychology",
        "https://kuakua.app/zh-Hans/docs/psychology-research/addiction",
        "https://kuakua.app/zh-Hans/docs/psychology-research/cognitive-biases-codex",
        "https://kuakua.app/zh-Hans/docs/psychology-research/most-influential-values",
        "https://kuakua.app/zh-Hans/docs/psychology-research/experimental-variables-in-psychological-research",
        "https://kuakua.app/zh-Hans/docs/psychology-research/positive-psychology-and-managing-longCOVID",
        "https://kuakua.app/zh-Hans/docs/lifestyle-personal-growth",
        "https://kuakua.app/zh-Hans/docs/lifestyle-personal-growth/daoist-philosophy",
        "https://kuakua.app/zh-Hans/docs/lifestyle-personal-growth/taiji",
        "https://kuakua.app/zh-Hans/docs/lifestyle-personal-growth/the-unity-of-knowledge-and-action",
        "https://kuakua.app/zh-Hans/docs/lifestyle-personal-growth/ikigai",
        "https://kuakua.app/zh-Hans/docs/lifestyle-personal-growth/meditation",
        "https://kuakua.app/zh-Hans/docs/lifestyle-personal-growth/north-star",
        "https://kuakua.app/zh-Hans/docs/lifestyle-personal-growth/qigong",
        "https://kuakua.app/zh-Hans/docs/lifestyle-personal-growth/flow-mihaly-csikszentmihalyi",
        "https://kuakua.app/zh-Hans/docs/others/support-groups",
        "https://kuakua.app/zh-Hans/docs/others/gethelpnow",
    ]
    
    # 或者指定输出文件名
    for url in urls:
        print(url)
        url_to_markdown(url, "index.md")
        time.sleep(5)