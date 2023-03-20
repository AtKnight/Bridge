from MCTS_Node import MCTS_Node

class MCTS:
    # See https://www.youtube.com/watch?v=UXW2yZndl7U
   
    def __init__(self, state):
        # State = namedtuple("State", "parent handenDict huidigeSpeler actions troef kaartenHuidigeSlag aantalPuntenNZ")    

        self.rootNode = MCTS_Node(state)
        self.rootNode.expand()
        
        self.rootNode.toonAlles()
        print("---------------------------------")
        
    # -----------------------------------------------------------------------
    
    def search(self, numberOfIterations):
        for i in range(1, numberOfIterations + 1):
            node = self.rootNode.selectNode()
            
            print("Na selectNode return_node = ", node)
            
            if node.numberOfVisits != 0:
                 node.expand()
                 node = node.getFirstChildNode() 
                 node = node.node
     
            node.backPropagate(node.rollOut())
            print("Einde iteratie ", i)
            #print("-------------------")
            #self.rootNode.toonAlles()
            print("===================")
            
            print(end='\n\n')
            
            if i == 400:
                return
          
    # -----------------------------------------------------------------------
  
    def showResult(self):
        bestCouple = self.rootNode.getBestchildAndValue()
        print("Best Node: ", bestCouple.node)
        print("Best variant: ")
        
        print("showResult: ", self.rootNode)
        
        if self.rootNode != None:
            self.rootNode.showResult()
            
    def toonAlles(self):
        print("root")
        self.rootNode.toonAlles(1)