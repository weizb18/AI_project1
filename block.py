class Block():
    
    def __init__(self, row, col, pattern = 0):
        self.row = row
        self.col = col
        self.pattern = pattern
        self.cost = 0
        self.turn = 0    # times of turn 
        self.direction = 0    # last move direction, for calculating turns
                              # 0 means no move before, 1 means upward, 2 means right, 3 means downward, 4 means left
        
    def __repr__(self):
        return "<Block (row={})(col={})(pattern={})(turn={})(direction={})>".format(self.row, self.col, self.pattern, self.turn, self.direction)

    def __lt__(self, other):
        pass

    def __eq__(self, other):
        pass

        