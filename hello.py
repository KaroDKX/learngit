class Programmer(object):
	def __init__(self, name):
		self.name = name
		print("创建了一个类!")
if __name__ == '__main__':
	p = Programmer('albert')
	print(p)
