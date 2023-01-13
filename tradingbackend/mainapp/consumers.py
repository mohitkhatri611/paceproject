import json
from mainapp.models import CoinData
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async, async_to_sync
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import copy
from .models import *
"""channel to send data to group then to user1, user 2.. using celery"""
class StockConsumer(AsyncWebsocketConsumer):
    #here we are doing the channel
    @sync_to_async
    def addToCeleryBeat(self, stockpicker):
        #task that we created for dynamic task creation
        task = PeriodicTask.objects.filter(name = "every-12-seconds")
        #checking if task is already created
        if len(task)>0:
            #now adding those stocks
            print("hello")  # testing that task.first() will work or not
            task = task.first()
            args = json.loads(task.args)
            # args = args[0]
            # for x in stockpicker:
            #     if x not in args:
            #         args.append(x)
            # task.args = json.dumps([args])
            task.save()
        else:
            #if task is not creating then creating new task
            schedule, created = IntervalSchedule.objects.get_or_create(every=30, period = IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval = schedule, name='every-12-seconds', task="mainapp.tasks.update_stock2")

    @sync_to_async    
    def addToStockDetail(self, stockpicker):
        user = self.scope["user"]
        # for i in stockpicker:
        #     stock, created = StockDetail.objects.get_or_create(stock = i)
        #     stock.user.add(user)

    @sync_to_async
    def prepare_stock_list(self):
        stock_list = CoinData.objects.all()
        symbol_list_str = ""
        stockpicker = []
        for i in stock_list:
            stockpicker.append(str(i.symbol))
        print(stockpicker)
        return stockpicker


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'stock_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Parse query_string
        #to automatically schedule celery
        query_params = parse_qs(self.scope["query_string"].decode())

        print(query_params)

        # stockpicker = query_params['stockpicker']
        stockpicker = self.prepare_stock_list()
        # data = {"symbols": symbol_list_str[:-1]}
        # stockpicker = symbol_list_str[:-1]
        # add to celery beat
        await self.addToCeleryBeat(stockpicker)

        # add user to stockdetail
        await self.addToStockDetail(stockpicker)


        await self.accept()

    @sync_to_async
    def helper_func(self):

        #removing stocks based on users selected.
        #showing only stocks to that user which are selected by particular user
        #after getting data of all the users stock data at once.
        user = self.scope["user"]
        stocks = CoinData.objects.filter(user__id = user.id)
        task = PeriodicTask.objects.get(name = "every-12-seconds")
        args = json.loads(task.args)
        # args = args[0]
        # for i in stocks:
        #     i.user.remove(user)
        #     if i.user.count() == 0:
        #         args.remove(i.stock)
        #         i.delete()
        if args == None:
            args = []

        if len(args) == 0:
            task.delete()
        else:
            task.args = json.dumps([args])
            task.save()


    async def disconnect(self, close_code):
        await self.helper_func()

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_update',
                'message': message
            }
        )
    
    @sync_to_async
    def selectUserStocks(self):
        user = self.scope["user"]
        #getting only user stocks that selected by user
        ##make below lines comment because in in react js the user is anonymous
        #solution either make the user login in react js and use that in self or either comment below 2 lines..
        if user.id != None: #if login from react and user is anonymous.
            user_stocks = user.stockdetail_set.values_list('stock', flat = True)
            return list(user_stocks)
        # return []

    # Receive message from room group
    async def send_stock_update2(self, event):
        message = event['message']
        message = copy.copy(message)
        #get user stocks
        user_stocks = await self.selectUserStocks()

        keys = message.keys()
        #removing other stocks which are not selected by user
        # for key in list(keys):
        #     if key in user_stocks:
        #         pass
        #     else:
        #         del message[key]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))