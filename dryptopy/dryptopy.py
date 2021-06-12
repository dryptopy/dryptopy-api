def epoch2datetime(input_date, input_time):
    output = time.strptime(input_date+" "+input_time, "%d.%m.%Y %H:%M:%S")
    print(output)
    return output
