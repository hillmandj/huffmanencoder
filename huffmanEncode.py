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

class Tree:
	def __init__(self, node=None):
		self.head = node

	def post_traverse(self):
		encodings = {}
		self.head.post_traverse('')

	def prn(self):
		print self.head.getData()


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


if __name__ == '__main__':
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


