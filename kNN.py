from numpy import * #导入科学计算包Numpy
import operator   #导入运算符包

# 创建数据集和标签
def createDataSet():
	group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
	labels = ['A', 'A', 'B', 'B']
	return group, labels

'''
	(1)计算已知类别数据集中的点与当前点的距离
	(2)按照距离递增次序排列
	(3)选取与当前点距离最小的k个点
	(4)确定前k个点所属类别出现的频率
	(5)返回频率最高的类别，作为当前点的预测分类
'''
def classify0(inX, dataSet, labels, k):
	#set.shape[0] 求数组的行数。 set.shape[1]求数组的列数。求出源数据的行数
	dataSetSize = dataSet.shape[0]
	#tile(inX,(dataSetSize,1))将inX复制成一个dataSetSize行的数列， inX用于分类的向量，dataSet用于训练的向量，diffMat,用于分类的点，到各个点的向量
	diffMat = tile(inX, (dataSetSize, 1)) - dataSet

	sqDiffMat = diffMat**2
	#.sum(axis=1)矩阵的每一行相加的和
	sqDistances = sqDiffMat.sum(axis=1)
	distances = sqDistances**0.5
	#argsort()将数组排序之后的下标，由大到小返回
	sortedDistIndicies = distances.argsort()
	classCount = {}
	for i in range(k):
		#从1到k读取第一到第k元素的标签
		voteIlabel = labels[sortedDistIndicies[i]]
		#对读取到的标签加一
		classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
		#排序后输出标签数最大的那个	
	sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1), reverse = True)
	return sortedClassCount[0][0]

#创建file2matrix讲txt文件中的数据转化为矩阵的形式，并返回
def file2matrix(filename):
#打开filename文件，并返回文件指针
	fr = open(filename)
	#读取文件的所有行并作为一个列表放回，包含所有的行结束符
	arrayOLines = fr.readlines()
#获取文件的行数
	numberOfLines = len(arrayOLines)
#创建一个列为3，行为数据行数的矩阵，用于储存数据
	returnMat = zeros((numberOfLines,3))
	classLabelVector = []
	index = 0
	for line in arrayOLines:
		#line.strip()删除行中的空白字符
		line = line.strip()
		#通过制表字符\t对line切片
		listFromLine = line.split('\t')
#将数据读取到returnMat矩阵中
		returnMat[index,:] = listFromLine[0:3]
#将标签读取到classLabelVecor矩阵中
		classLabelVector.append(int(listFromLine[-1]))
		index += 1
	return returnMat,classLabelVector
#将数据归一化
def autoNorm(dataSet):
	minVals = dataSet.min(0)
	maxVals = dataSet.max(0)

	ranges = maxVals - minVals

	normDataSet = zeros(shape(dataSet))

	m = dataSet.shape[0]

	normDataSet = dataSet - tile(minVals,(m,1))

	normDataSet = dataSet/tile(ranges,(m,1))

	return normDataSet, ranges, minVals

#test
def datingClassTest():
	hoRatio = 0.10

	datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')

	normMat, ranges, minVals = autoNorm(datingDataMat)

	m = normMat.shape[0]

	numTestVecs = int(m*hoRatio)

	errorCount = 0.0

	for i in range(numTestVecs):
		classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:], datingLabels[numTestVecs:m],3)
		
		print("The classifier came back with: %d, the real answer is: %d" %(classifierResult, datingLabels[i]))

		if(classifierResult != datingLabels[i]): errorCount += 1.0

	print("The total error rate is :%f" %(errorCount/float(numTestVecs)))

#预测函数
def classifyPerson():
	
	resultList = ['not at all', 'in small does', 'in large doess']

	percentTats = float(input("percenttage of time spent playing video games?"))

	ffMiles = float(input("frequent flier miles earned per year?"))
	
	iceCream = float(input("liters of ice cream consumed per year?"))

	datingDataMat, datingLabels = file2matrix("datingTestSet2.txt")

	normMat, ranges, minVals = autoNorm(datingDataMat)

	inArr = array([ffMiles, percentTats, iceCream])

	classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)

	print("you will probably like this man:%s" %(resultList[classifierResult-1]))
