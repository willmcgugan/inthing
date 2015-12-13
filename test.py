from inthing import stream, events

stream = stream.Stream(id="test", password="password")
print(stream)
text = events.Text('test', 'This is a **test**')
stream.add(text)
print(text)