from tkFileDialog import askopenfile

encodings = {}

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

class huffmanEncode:
	def __init__(self, binary_tree):
		self.binary_tree = binary_tree

	def open(self, new_file):
		f = open(new_file, 'r')
		return f

	def run(self):
			#open file and read in text
		f = askopenfile(title='Please select a file to compress')
		string_input = f.read()

		#create list of list, with each inner list containing a character and it's frequency
		ary = [[i, string_input.count(i)] for i in string_input]

		#remove duplicate values from the list	
		final_list = removeDuplicates(ary)

		#create list of trees, each containing a node with a [character, frequency] as data
		tree_ary = TreeAry(final_list)

		#perform huffmanStep on tree_ary
		for i in range(len(tree_ary) - 1):
			huffmanStep(tree_ary)

		#create encodings for each character using tree and post_traverse recursive function
		for i in tree_ary:
			i.post_traverse()

		#take the entire string (characters from file) and encode them using the encode function
		encoded_ary = encode(string_input)

		#take the encoded array and create a new array where each item's length is equal to 8 bits
		eight_bit_ary = create_eight_bit_strings(encoded_ary)

		#open files and write encodings to separate file
		f = open("huffmanOutput.dat", "wb")
		g = open("huffmanTree.dat", "w")
		g.write(str(encodings))
		g.close()

		#for every 8 bit item in the array, write the corresponding character to the output file
		for i in eight_bit_ary:
			d = byte_printer(i)
			f.write(d)
		f.close()

class huffmanDecode:
	def __init__(self, binary_tree):
		self.binary_tree = binary_tree

	def run(self):
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


def removeDuplicates(ary):
	'''(list) -> list

	This function returns a list with duplicate values removed.'''

	final_list = []
	for i in ary:
		if not i in final_list:
			final_list.append(i)

	return final_list


def TreeAry(ary):
	'''(list) -> list of binary trees

	This function takes a list, and returns a list of binary trees, each of which containing a
	head node with the data from the original list. 
	'''

	final_list = []
	for i in ary:
		temp_node = TreeNode()
		temp_node.insertData(i)
		tree = Tree(temp_node)
		final_list.append(tree)

	return final_list


def getMin(tree_ary):
	'''(list of binary trees) -> binary tree, list of binary trees

	This function sorts the tree_ary from smallest to largest by the number/frequency 
	of characters. This value is found in the 1st index of the head node. The function returns
	the tree with the lowest numerical value along with an adjusted list that no longer has the
	minimum tree inside'''

	sorted_tree = sorted(tree_ary, key=lambda tree: tree.head.getData()[1])
	min_tree = sorted_tree[0]
	sorted_tree.pop(0)
	adjusted_list = sorted_tree

	return min_tree, adjusted_list


def huffmanStep(tree_ary):
	'''(list of binary trees) -> list of binary trees

	This function performs the main huffman process. It takes the two binary trees in the list with
	the lowest numerical value (or frequency of characters, in this case) and removes them from the 
	list of binary trees. It then creates a temporary node, whose data is equal to the sum of the two 
	frequencies. The head nodes of the trees that were previously removed are then appended to the 
	temporary node as left/right children. The temporary node is then turned into the head node of a
	new tree, and that tree is added back to the original list. 

	This is important, because it sets up the binary tree datastructure that we will need to 
	traverse in order to create our encodings and compress the file.'''

	min_tree1, first_array = getMin(tree_ary)
	min_tree2, second_arry = getMin(first_array)
	temp_node = TreeNode([None, min_tree1.head.getData()[1] + min_tree2.head.getData()[1]])
	temp_node.left = min_tree1.head
	temp_node.right = min_tree2.head
	tree_ary.remove(min_tree1)
	tree_ary.remove(min_tree2)
	new_tree = Tree(temp_node)
	final_ary = tree_ary.append(new_tree)
	return final_ary


def encode(string):
	'''(str) -> list

	This function takes a string of characters and adds the encoded value of each character
	to an array. The encodings should have already been created using our binary tree datastructure,
	and are found in the encodings dictionary.
	'''

	x = []
	for char in string:
		x.append(encodings[char])
	return x


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

def char_to_bit(char):
	num = ord(char)
	ans = bin(num)
	return ans[2:]

def make_eight_bit(num):
	bin_str = num
	while len(bin_str) < 8:
		bin_str = '0' + bin_str
	return bin_str



if __name__ == '__main__':
	temp_node = TreeNode()
	temp_tree = Tree(temp_node)
	var = huffmanEncode(temp_tree)
	var.open('data.dat')
	var.run()
	print 'encoding complete'
	dec = huffmanDecode(temp_tree)
	dec.run()
	print 'decoding complete'

	
