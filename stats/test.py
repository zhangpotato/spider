# url = 'https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html'
url = 'https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/13.html'
print(url.rindex("/"))    #52
print(url[0:url.rindex("/") + 1])


