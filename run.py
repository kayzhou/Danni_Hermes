from email.mime import text
import requests
from bs4 import BeautifulSoup
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import time
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(text, link):
    print("send_email()", text, link)
    print(text)
    # 输入Email地址和口令:
    config = [line.strip() for line in open("email_config")]
    from_addr = config[0]
    password = config[1]

    msg = MIMEText(
        f"吴博士，您好！\n\nAI坤坤子监测到您关注的爱马仕商品有上新！\n详细信息：{text}\n商品链接：{link} \n\n 祝好，\n振坤",
        'plain', 'utf-8')
    msg["From"] = "爱你的坤坤子~"
    msg['To'] = "妮妮子"
    msg['Subject'] = Header('爱马仕上新！').encode()

    # 输入收件人地址:
    to_addr = config[2]

    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'
    server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    # server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


def crawl_item(url):
    # 商品关注列表
    r = requests.get(url)
    if r.status_code == 403:
        return -1

    content = r.content
    soup = BeautifulSoup(content, 'lxml')
    # print(soup.title.text)
    txt = soup.find_all("form", {"class": "simple-product-selector"})[0].text.split()
    info = soup.title.text
    color = [t for t in txt if t.endswith("色")][1]

    # sorry = soup.find_all("span", {"class": "message-error"})[0].text.startswith("抱歉！")
    error_info = soup.find_all("span", {"class": "message-error"})
    if len(error_info) > 0:
        if "抱歉" in error_info[0].text:
            return 0
    else:
        send_email(info + " " + color, url)
        return 1

    
def crawl(url, type):
    # 项链
    # 商品关注列表
    I_want_them = {
        "项链": ["pop"]
    }

    r = requests.get(url)
    content = r.content
    soup = BeautifulSoup(content, 'lxml')

    for li in soup.find_all('a'):
        # print(li)
        text = li.text.lower()
        if "¥" in text:
            for th in I_want_them[type]:
                print("监测内容：", type, th)
                if th in text:
                    print(li.text)
                    link = li.get("href")
                    link = "https://www.hermes.cn" + link

                    for c in ["浅褐色"]:
                        if c in li.text:
                            send_email(li.text, link)
                            time.sleep(10)
                    # break
    time.sleep(1)


if __name__ == "__main__":
    # cnt = 0
    # while True:
    #     crawl("https://www.hermes.cn/cn/zh/category/%E5%A5%B3%E5%A3%AB/%E6%97%B6%E5%B0%9A%E9%A6%96%E9%A5%B0/%E9%A1%B9%E9%93%BE%E5%9D%A0%E9%A5%B0/#||%E7%B1%BB%E5%88%AB", "项链")
    #     # crawl("https://www.hermes.cn/cn/zh/category/%E5%A5%B3%E5%A3%AB/%E6%97%B6%E5%B0%9A%E9%A6%96%E9%A5%B0/%E8%80%B3%E7%8E%AF/#||%E6%9D%90%E8%B4%A8", "耳钉")
    #     cnt += 1
    #     print(f"执行中 ... 循环爬取{cnt}次 ...")
    #     time.sleep(20)
    urls = [
        "https://www.hermes.cn/cn/zh/product/pop-h%E8%80%B3%E7%8E%AF-H608001FO55/",
        "https://www.hermes.cn/cn/zh/product/mini-pop-h%E8%80%B3%E7%8E%AF-H608001FO55/",
        "https://www.hermes.cn/cn/zh/product/pop-h%E8%80%B3%E7%8E%AF-H608002FP49/",
        "https://www.hermes.cn/cn/zh/product/mini-pop-h%E8%80%B3%E7%8E%AF-H608002FP49/",
        "https://www.hermes.cn/cn/zh/product/pop-h%E9%A1%B9%E9%93%BE-H147992FO55/",
        "https://www.hermes.cn/cn/zh/product/mini-pop-h%E9%A1%B9%E9%93%BE-H147991FO94/",
        "https://www.hermes.cn/cn/zh/product/pop-h%E9%A1%B9%E9%93%BE-H147991FO55/",
        "https://www.hermes.cn/cn/zh/product/mini-pop-h%E9%A1%B9%E9%93%BE-H147991FO55/",
        "https://www.hermes.cn/cn/zh/product/pop-h%E9%A1%B9%E9%93%BE-H147991F55/",
        "https://www.hermes.cn/cn/zh/product/mini-pop-h%E9%A1%B9%E9%93%BE-H147991F55/",
        # "https://www.hermes.cn/cn/zh/product/mini-pop-h%E8%80%B3%E7%8E%AF-H608002FPS7/"
    ]
    cnt = 0
    while True:
        for url in urls:
            print(url)
            crawl_item(url)
            time.sleep(3)
        cnt += 1
        print(f"执行中 ... 循环爬取{cnt}次 ...")

# https://www.hermes.cn/cn/zh/product/mini-pop-h%E8%80%B3%E7%8E%AF-H608002FP49/
# https://www.hermes.cn/cn/zh/product/pop-h%E9%A1%B9%E9%93%BE-H147992FO55/