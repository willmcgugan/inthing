from inthing import stream, events
import sys

stream = stream.Stream(id="test", password="password")

print(stream)
text = events.Text('test', sys.argv[1])
stream.add(text)
print(text)