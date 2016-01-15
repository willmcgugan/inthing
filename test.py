from inthing import stream, events
import sys

stream = stream.Stream(id="test", password="password")

print(stream)

import datetime

stream.add_text('Hello, World!', title="New Text Event")
stream.add_image('bear.jpg', title="Bear", text="A bear I shot in Finland")
