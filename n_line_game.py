# マスの状態のクラス
class Piece:
    # 空きマス
    SPACE = " "
    # 先攻を○とする
    FISRT = "x"
    # 後攻を×とする
    SECOND = "o"

# マスのクラスを定義
class Cell:
    # マスの状態を初期化
    def __init__(self):
        self.__state = Piece.SPACE
    
    # Cellクラスのstate変数のgetter
    @property
    def state(self):
        return self.__state

    # cellクラスのstate変数のsetter
    @state.setter
    def state(self, set_state):
        self.__state = set_state

# 盤面のクラスを定義
class Board:

    # 盤面を初期化(盤面のリストの要素にはCellクラスのインスタンスをセット)
    def __init__(self, board_size):
        self.cells = [[0]*board_size for n in range(board_size)]
        for x in [i for i in range(board_size)]:
            for y in [j for j in range(board_size)]:
                self.cells[y][x] = Cell()
    
    # 盤面の一辺の長さを返す
    def __len__(self):
        return len(self.cells[0])

    # 盤面を出力する時に呼び出し
    def __str__(self):
        print( "\ni\\j  ",end="")
        for row_num in range(len(self.cells)):
            print("({})  ".format(row_num+1), end="   ")
        print( "\n-----", end="")
        for row_num in range(len(self.cells)):
            print("-"*8, end="")
        print("")
        for i in range(0,len(self.cells)):
            print( "(%d)   "%(i+1), end="" )
            print( f"{self.cells[i][0].state}", end="" ) 
            for j in range(1,len(self.cells)):
                print( "   |   ", end="" )
                print( f"{self.cells[i][j].state}", end="" ) 

            print( "   ", end="" )
            print( "\n-----", end="")
            for row_num in range(len(self.cells)):
                print("-"*8, end="")
            print("")
        
        return ""

# プレイヤーの基本クラスの定義
class Player:
    # 名前と戦略をセットする
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        
# 人間の戦略クラス
class HumanStrategy:
    # 打つ手の決定
    def decide_choice(self, game, cells, turn):
        while  True:
            print( "Input row and column (i j): ", end="" )
            try:
                x, y = map(int, input().split())
            except ValueError:
                print("*** Input a pair of numbers 1-{}\n".format(len(cells)))
                continue
            x -= 1
            y -= 1
            if ((x<0) or (x>(len(cells)-1)) or (y<0) or (y>(len(cells)-1))):
            # ユーザーに入力した場所が存在しないことの説明をする
                print("Your input cell is out range of board")
                continue
            # ユーザーに入力したマスが既に埋まっていることの説明をする
            if (cells[x][y].state != Piece.SPACE):
                print("Your iuput cell is already used")
                continue
            else:
                return x, y

# CPUの戦略クラス
class CPUStrategy:

    # 考える選択肢を初期化
    def __init__(self):
        self.x = 0
        self.y = 0
        
    # 細かい部分以外はサンプルプログラムと同様
    def find_max(self, game, cells, turn, turn0):
        maximum=-999
        score = 0
        
        #   評価関数
        # (コンピュータが先攻・後攻かを判断して, それに合わせて評価関数の符号を変える)
        if ((turn>len(cells) ** 2)) and (game.judge()==Piece.SPACE): return(0) # draw
        if ((game.judge()==Piece.SECOND) and turn0 % 2 == 0) or ((game.judge()==Piece.FISRT) and turn0 % 2 == 1):return(((len(cells) ** 2)+2)-turn)
        if ((game.judge()==Piece.SECOND) and turn0 % 2 == 1) or ((game.judge()==Piece.FISRT) and turn0 % 2 == 0): return(-1*((len(cells) ** 2)+2)+turn)
        
        # find a position with the maximum value
        for i in range(0,len(cells)):
            for j in range(0,len(cells)):
                if( cells[i][j].state==Piece.SPACE ):
                    cells[i][j].state = Piece.FISRT if turn % 2 == 1 else Piece.SECOND
                    score  = self.find_min(game, cells, turn+1, turn0)
                    if( score > maximum ):
                        maximum = score
                        max_x = i
                        max_y = j
                    cells[i][j].state = Piece.SPACE

        self.x = max_x # return x position
        self.y = max_y # return y position
        return maximum 

    def find_min(self, game, cells, turn, turn0):
        minimum=999
        
        #   評価関数
        # (コンピュータが先攻・後攻かを判断して, それに合わせて評価関数の符号を変える)
        if ((turn>len(cells) ** 2)) and (game.judge()==Piece.SPACE): return(0) # draw
        if ((game.judge()==Piece.SECOND) and turn0 % 2 == 0) or ((game.judge()==Piece.FISRT) and turn0 % 2 == 1):return(((len(cells) ** 2)+2)-turn)
        if ((game.judge()==Piece.SECOND) and turn0 % 2 == 1) or ((game.judge()==Piece.FISRT) and turn0 % 2 == 0): return(-1*((len(cells) ** 2)+2)+turn)

        # find a position with the minimum value 
        for i in range(0,len(cells)):
            for j in range(0,len(cells)):
                if( cells[i][j].state==Piece.SPACE ):
                    cells[i][j].state = Piece.FISRT if turn % 2 == 1 else Piece.SECOND  
                    score = self.find_max(game, cells, turn+1, turn0)
                    if( score < minimum ):
                        minimum=score
                        min_x = i
                        min_y = j
                    cells[i][j].state = Piece.SPACE
        
        self.x = min_x # return x position
        self.y = min_y # return y position
        return minimum 

    # 打つ手の決定
    def decide_choice(self, game, cells, turn):
        score = self.find_max(game, cells, turn, turn)
        return self.x, self.y

# プレイヤーの行動のクラスを定義
class Action:
    # 盤面とターン数をセット
    def __init__(self, cells, turn):
        self.cells = cells
        self.turn = turn

    # 手を打つメソッド(ターン数から○か×を打つかを決定)
    def hit(self, x, y):
        self.cells[x][y].state = Piece.FISRT if self.turn % 2 != 0 else Piece.SECOND

# ゲームのクラスを定義
class Game:
    # ゲーム情報の初期化
    def __init__(self, first_player, second_player, board_size):
        
        # 盤面のインスタンスを生成
        self.board = Board(board_size)

        # 先攻・後攻のプレイヤーのセット
        self.first_player = first_player
        self.second_player = second_player


    # ゲームの終了判定
    def judge(self):
        # horizontal check
        for i in range(0,len(self.board.cells)):
            state_list = []
            for j in range(0, len(self.board.cells)):
                state_list.append(self.board.cells[i][j].state)
            if ( state_list.count(Piece.FISRT)==len(self.board.cells) ): return Piece.FISRT
            if ( state_list.count(Piece.SECOND)==len(self.board.cells) ): return Piece.SECOND

        # vertical check 
        for j in range(0,len(self.board.cells)):
            state_list = []
            for i in range(0,len(self.board.cells)):
                state_list.append(self.board.cells[i][j].state)
            if ( state_list.count(Piece.FISRT)==len(self.board.cells) ): return Piece.FISRT
            if ( state_list.count(Piece.SECOND)==len(self.board.cells) ): return Piece.SECOND

        # diagonal check 
        state_list = []
        for i in range(0,len(self.board.cells)):
            state_list.append(self.board.cells[i][i].state)

        if ( state_list.count(Piece.FISRT)==len(self.board.cells) ): return Piece.FISRT
        if ( state_list.count(Piece.SECOND)==len(self.board.cells) ): return Piece.SECOND

        state_list = []
        for i in range(0,len(self.board.cells)):
            state_list.append(self.board.cells[i][2-i].state)
        if ( state_list.count(Piece.FISRT)==len(self.board.cells) ): return Piece.FISRT
        if ( state_list.count(Piece.SECOND)==len(self.board.cells) ): return Piece.SECOND

        return Piece.SPACE


    # ゲームを開始
    def play(self):
        # 開始ターン数の定義
        turn = 1

        # 最初の盤面出力
        print(self.board)

        while True:
            print(f"\nTurn:{turn}", end=",")
            
            # 先攻か後攻かをターン数から判断
            # 戦略から打つ手を決定
            if turn % 2 == 1:
                print("Player:{}".format(self.first_player.name))
                x, y = self.first_player.strategy().decide_choice(self, self.board.cells, turn)
            else:
                print("Player:{}".format(self.second_player.name))
                x, y = self.second_player.strategy().decide_choice(self, self.board.cells, turn)

            # 戦略より決定した手を打つ
            Action(self.board.cells, turn).hit(x, y)

            # 盤面を出力
            print(self.board)

            # どちらかが勝利していたら
            if self.judge() in [Piece.FISRT, Piece.FISRT]:
                print( "{} won!\n".format(self.judge()))
                return

            # ターン数がマスの数を超えたら
            if turn >= len(self.board.cells) ** 2:
                print( "Draw!\n" )
                return
            
            print(f"\nFinish turn:{turn}", end=",")

            # 次のターンに進む
            turn += 1

# メインのメソッド
def main():

    # 先攻プレイヤーの選択
    first_player = input("先攻のプレイヤーは人間ですか? 人間なら「yes」を入力してください。CPUを選ぶ場合は, そのままEnterを押してください\n")
    # もしプレイヤーが人間なら
    if first_player == "yes":
        first_name = input("名前を入れてください。\n")
        # 名前と戦略をセット
        first_player = Player(first_name, HumanStrategy)
    # もしプレイヤーがCPUなら
    else:
        # 名前と戦略をセット
        first_player = Player("CPU", CPUStrategy)

    # 後攻プレイヤーの選択
    second_player = input("後攻のプレイヤーは人間ですか? 人間なら「yes」を入力してください。CPUを選ぶ場合は, そのままEnterを押してください\n")
    # もしプレイヤーが人間なら
    if second_player == "yes":
        # 名前と戦略をセット
        second_name = input("名前を入れてください。\n")
        second_player = Player(second_name, HumanStrategy)
    # もしプレイヤーがCPUなら
    else:
        # 名前と戦略をセット
        second_player = Player("CPU", CPUStrategy)
        
    # ゲームのインスタンスを生成
    board_size = int(input("自然数を入力してください(n目並べ):"))
    game = Game(first_player, second_player, board_size)

    # ゲーム開始
    game.play()
    
if __name__ == "__main__":
    main()