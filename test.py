from inthing import stream, events

stream = stream.Stream()
print(stream)
text = events.Text('test', 'This is a **test**')
stream.add(text)
print(text)