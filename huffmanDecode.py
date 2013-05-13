
class TreeNode:
	def __init__(self, data=None, left=None, right=None):
		self.left = left
		self.right = right
		self.data = data

	def insertData(self, value):
		self.data = value

	def getData(self):
		return self.data

	def getLeft(self):
		return self.left

	def getRight(self):
		return self.right

	def post_traverse(self, encoding):
		if self.left != None:
			encoding += '0'
			self.left.post_traverse(encoding)
			encoding = encoding[0:-1]
		if self.right != None:
			encoding += '1'	
			self.right.post_traverse(encoding)
			encoding = encoding[0:-1]
		if self.getData()[0] != None:
			encodings[self.getData()[0]] = encoding

	def prn_traverse(self, location=''):
		print location, self.getData()
		if self.left != None:
			location += '0'
			self.left.prn_traverse(location)
			location = location[0:-1]
		if self.right != None:
			location += '1'
			self.right.prn_traverse(location)
			location = location[0:-1]

	def find_traverse(self, destination=''):
		if destination == '':
			return self.getData()
		if destination[0] == '0':
			if self.left != None:
				return self.left.find_traverse(destination[1:])
		if destination[0] == '1':
			if self.right != None:
				return self.right.find_traverse(destination[1:])

	def addNode(self, key, string):
		if string == '':
			self.insertData(key)
			return
		temp = TreeNode()
		
		if string[0] == '0':
			if self.left == None:
				self.left = temp
			self.left.addNode(key, string[1:])	
		if string[0] == '1':
			if self.right == None:
				self.right = temp
			self.right.addNode(key, string[1:])


	def hasCharacter(self):
		character = None
		if self.getData() == None:
			character = False
		if self.getData() != None:
			character = True
		return character


class Tree:
	def __init__(self, node=None):
		self.head = node

	def post_traverse(self):
		encodings = {}
		self.head.post_traverse('')

	def addNode(self, key, string):
		self.head.addNode(key, string)

	def prn(self):
		print self.head.getData()


def char_to_bit(char):
	num = ord(char)
	ans = bin(num)
	return ans[2:]


def create_eight_bit_strings(ary):
	'''(list) -> list

	This function takes a list of binary numbers, and returns a list of binary numbers where
	each binary number's length is equal to 8. This is important because we are going to takes
	the encoded characters from the file, encode them using our encode function, and then compress
	by using this function.
	'''
	temp = ''.join(ary)
	final_list = [temp[bit:bit+8] for bit in range(0, len(temp), 8)]
	return final_list


def make_eight_bit(num):
	bin_str = num
	while len(bin_str) < 8:
		bin_str = '0' + bin_str
	return bin_str


def byte_printer(string):
	'''(str) -> str

	This function takes an 8 bit string of binary numbers. It converts a base 2 number into a base
	10 number, and then returns the character associated with that base 10 number in the ASCII table
	using the chr() function.
	'''
	num = 0
	for i in range(len(string)):
		first = int(string[i])
		exponent =  7 - i
		foo = 2 ** exponent
		answer = first * foo
		num = num + answer
	return chr(num)


if __name__ == '__main__':
	#open file to extract encodings, afterwards, convert to dictionary
	f = open('huffmanTree.dat', 'r')
	encodings_str = f.readline()
	encodings_dict = eval(encodings_str)

	#recreate huffman tree using encodings and recursive function addNode
	temp = TreeNode(None)
	huffmanTree = Tree(temp)
	for k, v in encodings_dict.items():
		huffmanTree.addNode(k, v)

	#open up encoded file, the goal is to take in each character and put it into a list
	#we then need to convert each character into a binary string, and then make sure that
	#each string's length is equal to 8 bits. We then join all of the bits into one string
	#called binary_input
	in_file = open('huffmanOutput.dat', 'r')
	binary_input = ''
	for i in in_file:
		d = list(i)
		new_ary = [char_to_bit(x) for x in d]
		eight_bit_ary = [make_eight_bit(i) for i in new_ary]
		temp = ''.join(eight_bit_ary)
		binary_input += temp
	in_file.close()

	current_node = huffmanTree.head
	final_str = ''
	for digit in binary_input:
		if current_node.hasCharacter():
			final_str += current_node.getData()
			current_node = huffmanTree.head
		if digit == '0':
			current_node = current_node.left
		if digit == '1':
			current_node = current_node.right

	#print final_str
	out_file = open('huffmanFinal.dat', 'w')
	for i in final_str:
		out_file.write(i)
	out_file.close()


'''
	DateTime class
		create a class that can accurately represent a date and time for the user
		the class should be able to add and subtract days, weeks, months, minutes, seconds, hours from a DateTime
		the class should be able to return a unix timestamp for a DateTime
		the class should be able to format the output of a datetime in various different formats specified by the user: (day, month, year), (day, hour, minute)
		the class should accurately account for leap years, and leap seconds
		hint: store one value that records the time since a specific moment in history. everything else references that value
'''
