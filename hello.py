class Programmer(object):
	def __init__(self, name, age):
		self.name = name		
		self.age = age
		print("创建了一个类!")
if __name__ == '__main__':
	p = Programmer('albert', 25)
	print(p)
