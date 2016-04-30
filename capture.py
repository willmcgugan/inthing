from inthing import Stream
s = Stream.new()
with Stream.new().capture('example') as capture:
    print('hello')
capture.browse()

