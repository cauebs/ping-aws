#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import subprocess
import argparse


def ping_aws(count=10, interval=0.2, timeout=1):
    url = 'http://www.cloudping.info/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('td', class_='latency')
    endpoints = [(row['id'], row['endpoint']) for row in rows]

    for endpoint in endpoints:
        hostname = urlsplit(endpoint[1]).netloc
        name = endpoint[0]

        ping = subprocess.run(['ping', hostname,
                               '-c', str(count),
                               '-i', str(interval),
                               '-W', str(timeout)],
                              stdout=subprocess.PIPE)

        output = ping.stdout.decode('utf-8')
        lines = output.split('\n')
        stats = lines[-2].split('=')[-1].split('ms')[0].strip().split('/')
        stats = map(float, stats)

        print('[{}] min:{}, avg:{}, max:{}, mdev:{}'.format(name, *stats))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test latency to AWS servers')
    parser.add_argument('-c', '--count', type=int, default=10)
    parser.add_argument('-i', '--interval', type=float, default=0.2)
    parser.add_argument('-t', '--timeout', type=float, default=1)

    args = parser.parse_args()
    ping_aws(count=args.count, interval=args.interval, timeout=args.timeout)
