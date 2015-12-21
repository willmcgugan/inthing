from inthing import stream, events
import sys

stream = stream.Stream(id="test", password="password")

print(stream)

import datetime

for _ in range(3):
	text = events.Text('test', datetime.datetime.now().ctime())
	stream.add(text)
	print(text)