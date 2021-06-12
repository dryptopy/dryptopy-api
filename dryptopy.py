def get_volume_data_1m(client, pair, starttime_ms):
    volume_date = []
    volume_data = []
    epoch_1h = 60 * 60 * 1000
    epoch_8h = 8 * 60 * 60 * 1000
    epoch_1m = 60 * 1000
    y = 0
    errcnt = 0
    for x in range (0, 42):
        kline_start = int(starttime_ms+(epoch_8h*x))
        candles = client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1HOUR, limit=480, startTime=(kline_start))
        while y < 480:
    
            #check if the candle time reported matches the expected time to ensure we havent lost data due to binance shutdown
            if int(candles[y-errcnt][0]) != starttime_ms + (y * epoch_1m) + (x * epoch_8h):
            
                #if the times dont match increment error counter            
                errcnt += 1
                #convert candle date to readable date
                candle_date = str(datetime.datetime.fromtimestamp(((int(candles[y][0]))/1000)))
                #convert expected date to readable date
                expected_date = str(datetime.datetime.fromtimestamp((((starttime_ms + (y * (1000 * 60 * 60))))/1000)))
            
                #we found an error e.g. got 5am when expected to get 4am data
                #need to create missing data
                volume_date.append(expected_date)
                volume_data.append(0)
            
                #add data for current set we did find
                volume_date.append(str(datetime.datetime.fromtimestamp(((candles[y][0])/1000))))
                volume_data.append(candles[y][5])            
                y += 1              
            elif y + errcnt >= 480:
                print("end of valid records to read")
                y += 1  
            else:
                volume_date.append(str(datetime.datetime.fromtimestamp(((candles[y][0])/1000))))
                volume_data.append(candles[y][5])
                y += 1 
    pair_data = list(zip(volume_date, volume_data))  
    return pair_data  
    
    
    def calc_start_time_user_1m(user_time):
    get_int_epoch_to_floor = math.floor(user_time / 1000 / 60) * 60 * 1000 #round time down to minute
    one_min_epoch_ms = 60 * 1000 #milliseconds in 1 minute
    two_weeks_epoch = 14 * 24 * 60 * 60 * 1000 #milliseconds in 2 weeks
    one_hour_epoch = 60 * 60 * 1000 #milliseconds in 1 hour
    starttime_ms = get_int_epoch_to_floor - two_weeks_epoch - one_hour_epoch #set start time to be time now rounded down to minute minus 2 weeks minus 1 minute  minus 1 hour
    start_date = str(datetime.datetime.fromtimestamp(((starttime_ms)/1000))) #get starting capture date/time in normal form 
    print(start_date)  
    return starttime_ms
    
    def calc_start_time_1m():
    timenow_ms = time.time()*1000 #get current time in milliseconds
    get_int_epoch_to_floor = math.floor(timenow_ms / 1000 / 60) * 60 * 1000 #round time down to minute
    one_min_epoch_ms = 60 * 1000 #milliseconds in 1 minute
    two_weeks_epoch = 14 * 24 * 60 * 60 * 1000 #milliseconds in 2 weeks
    one_hour_epoch = 60 * 60 * 1000 #milliseconds in 1 hour
    starttime_ms = get_int_epoch_to_floor - two_weeks_epoch - one_min_epoch_ms - one_hour_epoch #set start time to be time now rounded down to minute minus 2 weeks minus 1 minute  minus 1 hour
    start_date = str(datetime.datetime.fromtimestamp(((starttime_ms)/1000))) #get starting capture date/time in normal form  
    print(start_date) 
    return starttime_ms
    
    
    def show_volume_avg_1m(volume_data):
    volume_2w = 0
    volume_1w = 0
    volume_2d = 0
    volume_1d = 0
    volume_8h = 0
    volume_1h = 0  
    for x in range (0, len(volume_data)):
        volume_2w += float(volume_data[x][1])
    avg_volume_2w = volume_2w / (len(volume_data)/60)
    for x in range (len(volume_data)-(168*60), len(volume_data)):
        volume_1w += float(volume_data[x][1])
    avg_volume_1w = volume_1w / (168 / 60)
    for x in range (len(volume_data)-(48*60), len(volume_data)):
        volume_2d += float(volume_data[x][1])
    avg_volume_2d = volume_2d / (48 / 60)
    for x in range (len(volume_data)-(24*60), len(volume_data)):
        volume_1d += float(volume_data[x][1])
    avg_volume_1d = volume_1d / (24 / 60)
    for x in range (len(volume_data)-(8*60), len(volume_data)):
        volume_8h += float(volume_data[x][1])
    avg_volume_8h = volume_8h / (8 / 60)
    for x in range (len(volume_data)-(1*60), len(volume_data)):
        volume_1h += float(volume_data[x][1])
    avg_volume_1h = volume_1h / (1 / 60)

    
    print("2 Week Volume: ", volume_2w, " Size of Volume Data: ", len(volume_data), " 2 Week Average Volume: ", avg_volume_2w)
    print("1 Week Volume: ", volume_1w, " Size of Volume Data: ", len(volume_data), " 1 Week Average Volume: ", avg_volume_1w, " % Change on 2 Week Average: ", (avg_volume_1w/avg_volume_2w)*100)
    print("2 Day Volume: ", volume_2d, " Size of Volume Data: ", len(volume_data), " 2 Day Average Volume: ", avg_volume_2d, " % Change on 2 Week Average: ", (avg_volume_2d/avg_volume_2w)*100)
    print("1 Day Volume: ", volume_1d, " Size of Volume Data: ", len(volume_data), " 1 Day Average Volume: ", avg_volume_1d, " % Change on 2 Week Average: ", (avg_volume_1d/avg_volume_2w)*100)
    print("8 Hour Volume: ", volume_8h, " Size of Volume Data: ", len(volume_data), " 8 Hour Average Volume: ", avg_volume_8h, " % Change on 2 Week Average: ", (avg_volume_8h/avg_volume_2w)*100)
    print("1 Hour Volume: ", volume_1h, " Size of Volume Data: ", len(volume_data), " 1 Hour Average Volume: ", avg_volume_1h, " % Change on 2 Week Average: ", (avg_volume_1h/avg_volume_2w)*100)
