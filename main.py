import os
import os
import sys
import time
import warnings

from colorama import Fore

from lib.OneForAll.test import oneforall
from func import getsubdata, get_fofa, add2list, run_subdomains_brute, dnsx, 删除换行符, asset

warnings.filterwarnings("ignore")

def merge_and_deduplicate_lists(a, b):
    merged_set = set(a + b)  # 合并并去重
    merged_list = list(merged_set)  # 转换回列表
    return merged_list
def extract_subdomain_value(data):
    if 'subdomain' in data:
        return data['subdomain']
    else:
        return None
# 定义一个函数来处理单个域名的操作
def process_domain(domain):

    # sub
    contont = []
    doif = run_subdomains_brute(domain)

    if doif:
        file = open(f'.\\out\\{doif}', 'r')
        if os.path.isfile(f'./out/{doif}'):
            contont = file.readlines()
            contont = getsubdata(contont)
    else:
        print('[+]读取失败')



    # dnsx
    contont_dnx = []
    # domain = 'baidu.com'
    dnsx_file = dnsx(domain)
    if dnsx_file:
        file = open(f'.\\out\\{dnsx_file}', 'r')
        if os.path.isfile(f'.\\out\\{dnsx_file}'):
            contont_dnx = file.readlines()
            contont_dnx = 删除换行符(contont_dnx)
    else:
        print('[+]读取失败')
    domain_list = add2list(contont_dnx, contont)


    # asset
    contont = []
    # domain = 'baidu.com'
    ass_file = asset(domain)
    if ass_file:
        file = open(f'.\\out\\{ass_file}', 'r')
        if os.path.isfile(f'.\\out\\{ass_file}'):
            contont = file.readlines()
            contont = 删除换行符(contont)
    else:
        print('[+]读取失败')
    domain_list = add2list(contont, domain_list)

    # one
    domains_ones = []
    print('[+]oneforall')
    one = oneforall(domain)
    for one_l in one:
        domains_ones.append(extract_subdomain_value(one_l))
    domain_list = merge_and_deduplicate_lists(domains_ones,domain_list)



    # 深度挖掘
    # domainnew2 = []
    # num = 0
    # for i in domain_list:
    #     if 'http://' not in i and 'https://' not in i:
    #         num += 1
    #         url = 'https://' + i
    #         urls = find_by_url(url)
    #         print('\r\rurl深度挖掘:{:.0f}%'.format(num / len(domain_list) * 100), end='')
    #         sys.stdout.flush()
    #         if urls is not None:
    #             subdomains = find_subdomain(urls, domain)
    #             domainnew2.append(subdomains)
    # print()
    #
    # for a in domainnew2:
    #     for b in a:
    #         if b not in domain_list:
    #             domain_list.append(b)

    with open(f'./re/{domain}-{time.time()}.txt', 'w+') as fff:
        for domain_list_i in domain_list:
            fff.write(domain_list_i + '\n')
            fff.flush()
    try:
        os.remove(f'.\\out\\{doif}')
    except:
        pass

if __name__ == '__main__':
    if not os.path.exists('.\\out\\'):
        os.makedirs('.\\out\\')
    if not os.path.exists('.\\re\\'):
        os.makedirs('.\\re\\')
    print(f'''[+] {Fore.YELLOW}注意!{Fore.RESET}
[+] oneforall的配置文件在{Fore.RED}.\\lib\\OneForAll\\config\\api.py{Fore.RESET}
[+] {Fore.YELLOW}该工具由EX & 面包狗共同制作开发{Fore.RESET}
    ''')
    domainl = input(f"{Fore.GREEN}请输入扫描的子域名列表: {Fore.RESET}")
    domainl = open(domainl, 'r')
    domains = [domain.replace('\n', '') for domain in domainl.readlines()]
    for domain in domains:
        process_domain(domain)

    print("扫描完成")


