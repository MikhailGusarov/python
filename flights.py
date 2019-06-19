from datetime import datetime
import pprint

def convert2ampm(time24: str) -> str:
    return datetime.strptime(time24, '%H:%M').strftime('%I:%M%p')

with open('buzzers.csv') as data:
    ignore = data.readline()
    flights = {}
    for line in data:
        k, v = line.strip().split(',')
        flights[k] = v

pprint.pprint(flights)
print()

flights2 = {convert2ampm(k): v.title()
            for k, v in flights.items()}
w = {place : [k
              for k,v in flights2.items()
              if v == place]
     for place in set(flights2.values())}
pprint.pprint(flights2)
print()
pprint.pprint(w)
