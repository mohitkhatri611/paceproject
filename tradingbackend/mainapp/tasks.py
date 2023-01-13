from celery import shared_task
from yahoo_fin.stock_info import *
from threading import Thread
import queue
from channels.layers import get_channel_layer
import asyncio
from asgiref.sync import sync_to_async
import simplejson as json
from .models import *
#this file is for creating taks specific to that app
# from . import autologin
import random
#.......this task is create to do the update at periodically and setup in  consumer.py file as
# @sync_to_async
@shared_task(bind=True)
def update_stock2(self):
    # updating stock data to frontend of selected stocks
    # data = {}
    # available_stocks = tickers_nifty50()
    # for i in stockpicker:
    #     if i in available_stocks:
    #         pass
    #     else:
    #         # remove stock which are not selected
    #         stockpicker.remove(i)
    #
    # n_threads = len(stockpicker)
    # thread_list = []
    # que = queue.Queue()
    # for i in range(n_threads):
    #     # json will not accept Nan as data need to convert it
    #     thread = Thread(target=lambda q, arg1: q.put(
    #         {stockpicker[i]: json.loads(json.dumps(get_quote_table(arg1), ignore_nan=True))}),
    #                     args=(que, stockpicker[i]))
    #     thread_list.append(thread)
    #     thread_list[i].start()
    #
    # for thread in thread_list:
    #     thread.join()
    #
    # while not que.empty():
    #     result = que.get()
    #     data.update(result)

    stock_list = CoinData.objects.all()
    symbol_list_str = ""
    for i in stock_list:
        symbol_list_str += str(i.symbol + ",")

    data = {"symbols": symbol_list_str[:-1]}
    # stock_data = autologin.get_quotes(data)
    stock_data= None
    data = dict()
    # print(stock_data['d'][0]['v']['original_name'], "--->", stock_data['d'][0]['v']['cmd']['c'])
    print("asdfafda---------->",stock_list[0].symbol,stock_list[0].lp)
    a=[1,2,3,4,5,6,7,8]
    b= [5000,-10000,-3000,-45000,60000]
    for i in stock_data['d']:
        stock_detail_dict = dict()
        stock_detail_dict['price'] = i['v']['lp']  + random.choice(a)#+ stock_list[0].lp #just for testing purpose
        stock_detail_dict['volume'] = i['v']['volume'] + random.choice(b)
        stock_detail_dict['previous_close'] = i['v']['prev_close_price'] #+ random.choice(a)

        data[i['v']['symbol']] = stock_detail_dict
        # print(i['v']['original_name'], "--->", i['v']['lp'])
    # print("task---->",data)


    # send data to group...
    # the function through which we send the data is basically an asynchronous function
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    # setting the task to loop
    asyncio.set_event_loop(loop)

    loop.run_until_complete(channel_layer.group_send("stock_track", {
        'type': 'send_stock_update2',
        'message': data,
        # 'message': stock_data['d'],
    }))

    return 'Done'


# @shared_task(bind = True)
# def update_stockkk(self, stockpicker):
#     #updating stock data to frontend of selected stocks
#     data = {}
#     available_stocks = tickers_nifty50()
#     for i in stockpicker:
#         if i in available_stocks:
#             pass
#         else:
#             #remove stock which are not selected
#             stockpicker.remove(i)
#
#     n_threads = len(stockpicker)
#     thread_list = []
#     que = queue.Queue()
#     for i in range(n_threads):
#         #json will not accept Nan as data need to convert it
#         thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: json.loads(json.dumps(get_quote_table(arg1), ignore_nan = True))}), args = (que, stockpicker[i]))
#         thread_list.append(thread)
#         thread_list[i].start()
#
#     for thread in thread_list:
#         thread.join()
#
#     while not que.empty():
#         result = que.get()
#         data.update(result)
#
#     # send data to group...
#     #the function through which we send the data is basically an asynchronous function
#     channel_layer = get_channel_layer()
#     loop = asyncio.new_event_loop()
#
#     #setting the task to loop
#     asyncio.set_event_loop(loop)
#
#
#     loop.run_until_complete(channel_layer.group_send("stock_track", {
#         'type': 'send_stock_update',
#         'message': data,
#     }))
#
#
#     return 'Done'