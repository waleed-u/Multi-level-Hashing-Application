from .Node import Node

from .HashFunc import HashFunc
import heapq
import string

class Encoder:
    
    """
    Encoder Class that creates a tree and hashes each node
    """
    
    def __init__(self, fileOrString:str, isFile:bool)->None:
        
        """
        Encoder.Constructor
        """
        
        if isFile:    
            self.file_path = fileOrString
            self.fileContent = self.readFile(fileOrString)
        else:
            self.sentence = fileOrString
            self.fileContent = self.readString(self.sentence)
        self.fileDict = self.parseFreq(self.fileContent)
        self.nodeList = self.makeNodes()
        self.makeTree()
        # self.printTree(self.nodeList[0])
        
    def getFinalHash(self)->str:
        
        """
        Encoder.getFinalHash
        """
        
        return self.nodeList[0].hashValue


    def hash(self, input_data:str, rounds=10)->str:
        
        """
        Encoder.hash
        """
        
        return HashFunc.custom_hash(input_data, rounds)

    def makeTree(self):
        
        """
        Encoder.makeTree
        """
                
        while len(self.nodeList) > 1:
            nodeL = heapq.heappop(self.nodeList)
            nodeR = heapq.heappop(self.nodeList)
            tempNode = Node(nodeL.freq+nodeR.freq, f"Temp Node")
            tempNode.leftChild = nodeL
            tempNode.rightChild = nodeR
            tempNode.setWordHash(self.hash, newWord=f"{nodeL.hashValue}{nodeR.hashValue}")
            heapq.heappush(self.nodeList, tempNode)
        

    def makeNodes(self)->list[Node]:
        
        """
        Encoder.makeNodes
        """        
        
        nodeList = []
        for word in self.fileDict.keys():
            tempNode = Node(self.fileDict[word], word)
            tempNode.setWordHash(self.hash)
            heapq.heappush(nodeList, tempNode)
        return nodeList
        

    def readString(self, sentence:str)->str:
        
        """
        Encoder.readString
        """
        
        translator = str.maketrans('', '', string.punctuation)
        return (sentence).translate(translator)
    

    def readFile(self, filePath:str)->str:
        
        """
        Encoder.readFile
        """
        
        translator = str.maketrans('', '', string.punctuation)
        with open(filePath, 'r') as file:
            return (file.read()).translate(translator)
            

    def parseFreq(self, fileContent:str)->dict:
        
        """
        Encoder.parseFreq
        """
        
        freqDict: dict = {}
        data:list[str] = fileContent.split(" ")
        for word in data:
            if word in freqDict:
                freqDict[word] += 1
            else:
                freqDict[word] = 1
            
        return freqDict
        

    def printNodes(self)->None:
        
        """
        Encoder.printNodes
        """
        
        for i in range(len(self.nodeList)):
            print(self.nodeList[i])


    def printTree(self, node:Node)->None:
        
        """
        Encoder.printTree
        """
        
        if node.leftChild == None and node.rightChild == None:
            print(node)
            return
        if node.leftChild != None:
            self.printTree(node.leftChild)
        print(node)
        if node.rightChild != None:
            self.printTree(node.rightChild)
            
            
    def getHashFunction(self):
        
        """
        Encoder.getHashFunction
        """
        
        return hash
    
    def getOriginalData(self)->str:
        
        """
        Encoder.getOriginalHash
        """
        
        return self.fileContent
    
    def get_proof_path(self, node: Node, target_word: str, path=None):
        """
        Generate a proof path for a specific word in the Merkle tree.
        """
        if path is None:
            path = []

        # Base case: Leaf node with the target word
        if not node.leftChild and not node.rightChild and node.word == target_word:
            return path

        # Traverse left child
        if node.leftChild:
            left_path = self.get_proof_path(node.leftChild, target_word, path + [("L", node.leftChild.hashValue)])
            if left_path:
                return left_path

        # Traverse right child
        if node.rightChild:
            right_path = self.get_proof_path(node.rightChild, target_word, path + [("R", node.rightChild.hashValue)])
            if right_path:
                return right_path

        return None

    def verify_chunk_with_path(self, data_chunk: str, proof_path, root_hash):
        """
        Verify a data chunk using its proof path and the root hash.
        """
        current_hash = self.hash(data_chunk)
        for direction, sibling_hash in proof_path:
            if direction == "L":
                current_hash = self.hash(sibling_hash + current_hash)
            elif direction == "R":
                current_hash = self.hash(current_hash + sibling_hash)

        return current_hash == root_hash
