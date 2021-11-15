import os
import discord
import json
import requests
from requests.exceptions import HTTPError

from price import fetch_price_to, fetch_price_cg
from network import fetch_net_stats
from web_server import keep_run

with open('config.json') as f:
    config = json.load(f)

TOKEN = os.environ['TOKEN']
# GUILD = config['guild']

url_xwp = config['url_xwp']
url_btc = config['url_btc']

cg = config['url_gecko']

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    page_price_to = discord.Embed(
        title = '',
        description = '',
        colour = discord.Colour.green()
    )
    page_price_cg = discord.Embed(
        title = '',
        description = '',
        colour = discord.Colour.green()
    )
    page_network = discord.Embed(
        title = '',
        description = '',
        colour = discord.Colour.blue()
    )
    page_intro =  discord.Embed(
        title = 'Swap is the first CryptoNote coin securing the network with Cuckoo.',
        description = '',
        colour = discord.Colour.blue())

    text_1 = 'Swap is keeping CryptoNote for transactions with anonymity features and user friendliness. Meanwhile, for mining, adopting Cuckaroo with superior network protection and stability.\n\nCryptoNight mining is vulnerable to FPGA and ASIC network attacking.'
    text_2 = 'With a 42-line complete specification, Cuckatoo Cycle is less than half the size of either SHA256 or Blake2b. While trivially verifiable, finding a 42-cycle, on the other hand, is far from trivial, requiring considerable resources.\n-John Tromp'
    text_3 = 'Step one is removing edges that are not part of a cycle (99.9%). Step two is a backtracking graph traversal to find all cycles.\n\nSwap uses 32 edge trimming cycles.'
    text_4 = 'Cuckaroo29s uses 32-cycles while Cuckaroo29 uses 42-cycles. Both cycling ratios produce similar performances.\n\nFor more details read the Cuckoo Whitepaper on Github.'
    text_5 = 'Miners use 1 bit per edge and 1 bit per node. Finding node bits in random sequence causes a bottleneck which makes mining memory latency bound.\n\nThe majority of this form of mining is done in a very simple way.'

    text_6 = 'Find an improvement in mining and receive a bounty reward.\n\nCPU speedup bounty $10,000, linear time-memory trade-off bounty $10,000, GPU speedup bounty $5,000, and Siphash bounty $5,000.'

    text_7 = 'Less server overhead making processing more efficient.'

    page_intro.add_field(name='CryptoNote and Cuckaroo hybrid monster', value = text_1)
    page_intro.add_field(name='Simplest PoW algorithm', value = text_2)
    page_intro.add_field(name='The most efficient way to find cycles', value = text_3)
    page_intro.add_field(name='Cuckaroo29s vs Cuckaroo29', value = text_4)
    page_intro.add_field(name='Lean and mean mining', value = text_5)
    page_intro.add_field(name='Graph cycle performance', value = text_6)
    page_intro.add_field(name='Decreased hash confirmation time', value = text_7)
    
    help_text = 'Swap price bot commands\n```!xwp intro: display how swap works\n!xwp to: swap price on tradeogre\n!xwp cg: fetch price data from coingecko\n!xwp info: swap network stats\n!xwp commands: this page```'

    if message.author == client.user:
        return
    if message.content.lower().strip().startswith('!xwp intro'):
        await message.channel.send(embed=page_intro)
    elif message.content.lower().strip().startswith('!xwp commands'):
         await message.channel.send(help_text)
    elif message.content.lower().strip().startswith('!xwp to'):
        price_to = fetch_price_to(url_xwp, url_btc)
        page_price_to.add_field(name='**Swap**', value=price_to)
        await message.channel.send(embed=page_price_to)
    elif message.content.lower().strip().startswith('!xwp info'):
        net_data = fetch_net_stats()
        page_network.add_field(name='**swap netwrok info**', value=net_data)
        await message.channel.send(embed=page_network)
    elif message.content.lower().strip().startswith('!xwp cg'):
        price_cg = fetch_price_cg(cg)
        page_price_cg.add_field(name='**Swap**', value=price_cg)
        await message.channel.send(embed=page_price_cg)
keep_run()
client.run(TOKEN)