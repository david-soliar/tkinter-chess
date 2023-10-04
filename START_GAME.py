import chess.chess as chess
import tkinter
import random
import math


root = tkinter.Tk()
root.title("Chess")
root.configure(bg="gray25")
root.resizable(False, False)
root.iconbitmap("gallery/chess.ico")

canvas = tkinter.Canvas(width=640,
                        height=640,
                        bg="light green")
canvas.config(highlightthickness=0)
canvas.grid(rowspan=40,
            columnspan=1)


canvas_promotion = tkinter.Canvas(width=120,
                                  height=120,
                                  bg="gray30")
canvas_promotion.config(highlightthickness=0)
canvas_promotion.grid(row=39,
                      column=1)


canvas_time = tkinter.Canvas(width=120,
                             height=120,
                             bg="gray30")
canvas_time.config(highlightthickness=0)
canvas_time.grid(row=25,
                 column=1)


class play_chess():
    def __init__(self,
                 against_pc,
                 game_time,
                 start):

        if not start:
            return None

        canvas.delete("all")

        self.against_pc = against_pc
        self.black = False

        self.is_time_set = bool(game_time)
        self.time_black = game_time*60
        self.time_white = game_time*60
        self.number_of_moves = 0

        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.board = chess.Board(fen)
        self.board_tkinter = dict()
        self.middle = list()

        self.images = {
            "r": "rookb",
            "n": "knightb",
            "b": "bishopb",
            "q": "queenb",
            "k": "kingb",
            "p": "pawnb",
            "R": "rookw",
            "N": "knightw",
            "B": "bishopw",
            "Q": "queenw",
            "K": "kingw",
            "P": "pawnw",
        }

        self.create_tkinter_board()

    def create_tkinter_board(self):
        for y in range(8):
            for x in range(8):
                color = "green" if ((x+y) % 2) else "light green"
                canvas.create_rectangle(x*80, y*80,
                                        x*80 + 80, y*80 + 80,
                                        width=0,
                                        fill=color,
                                        tags="board_square")

                self.middle.append(tuple((x*80 + 40, y*80 + 40)))
                canvas.after(1)
                canvas.update()

        for i in range(8):
            canvas.create_text(i*80+70, 630,
                               text=chr(ord("A")+i),
                               font=("Arial Rounded MT Bold", "12", "bold"),
                               tags="square_text_corner",
                               fill="gray")

            canvas.create_text(10, i*80+10,
                               text=8-i,
                               font=("Arial Rounded MT Bold", "12", "bold"),
                               tags="square_text_corner",
                               fill="gray")

        for key in self.images:
            path_image = "gallery/" + self.images[key] + ".png"
            self.images[key] = (self.images[key],
                                tkinter.PhotoImage(file=path_image))

        self.update_board()

        canvas.create_text(320, 320,
                           text="START",
                           font=("Arial Rounded MT Bold", "80", "bold"),
                           tags="start_text",
                           fill="red")
        canvas.update()
        canvas.after(700)
        canvas.delete("start_text")
        canvas.update()

        canvas.tag_bind("board_square",
                        "<Button-1>",
                        self.unfocus_possible_moves)

        canvas.tag_bind("possible_move",
                        "<Button-1>",
                        self.move_piece)

        canvas.tag_bind("piece",
                        "<Button-1>",
                        self.visualize_possible_moves)

        canvas.bind_all("<Button-1>",
                        self.time_update)

    def update_board(self):
        canvas.delete("possible_move")
        canvas.delete("selected_piece")
        canvas.delete("piece")
        canvas_promotion.delete("all")

        root.focus_set()

        init_board = str(self.board).replace(" ", "").replace("\n", "")

        n = 0
        for y in range(8):
            for x in "abcdefgh":
                square_obj = init_board[n]

                self.board_tkinter[x+str(8-y)] = (square_obj,
                                                  self.middle[n],
                                                  "no")

                if square_obj != ".":
                    piece = self.images[square_obj]

                    canvas.create_image(self.middle[n],
                                        tags=(square_obj,
                                              piece[0],
                                              x+str(8-y),
                                              "piece"),
                                        image=piece[1])

                    self.board_tkinter[x+str(8-y)] = (init_board[n],
                                                      self.middle[n],
                                                      self.images[square_obj])
                n += 1

        if self.against_pc and self.black:

            black_positions = list()
            positions = list(self.board_tkinter.keys())

            for index in range(len(init_board)):
                if init_board[index].islower():
                    for position in positions:
                        if position != positions[index]:
                            black_positions.append(positions[index]+position)

            promotions = list()

            for black_position in black_positions:
                for new_piece in "rnbq":
                    promotions.append(black_position + new_piece)

            black_possible_positions = black_positions + promotions
            random.shuffle(black_possible_positions)

            for move in black_possible_positions:
                if (chess.Move.from_uci(uci=move) in self.board.legal_moves):
                    self.board.push(chess.Move.from_uci(move))
                    self.black = not self.black
                    canvas.update()
                    self.update_board()

        else:
            self.black = not self.black
            self.number_of_moves += 1
            canvas.update()

        if self.check_status():
            canvas.tag_unbind("piece",
                              "<Button-1>")
            canvas.update()
            return None

    def time_update(self, *event):
        canvas.unbind_all("<Button-1>")

        if not self.is_time_set:
            return None

        if (self.number_of_moves >= 2) and self.is_time_set:
            if not self.black:
                self.time_black -= 1

                minutes = math.floor(self.time_black/60)
                seconds = self.time_black % 60

                time_left = "{:02}:{:02}".format(minutes,
                                                 seconds)

                canvas_time.itemconfig("black_time", text=time_left)

            else:
                self.time_white -= 1

                minutes = math.floor(self.time_white/60)
                seconds = self.time_white % 60

                time_left = "{:02}:{:02}".format(minutes,
                                                 seconds)

                canvas_time.itemconfig("white_time", text=time_left)

            canvas_time.update()

        if self.time_white == 0:
            self.is_time_set = False

            canvas.create_text(320, 320,
                               text="Winner is black - time",
                               font=("Arial Rounded MT Bold",
                                     "50",
                                     "bold"),
                               tags="end",
                               fill="red")
            canvas.tag_unbind("piece",
                              "<Button-1>")

        elif self.time_black == 0:
            self.is_time_set = False

            canvas.create_text(320, 320,
                               text="Winner is white - time",
                               font=("Arial Rounded MT Bold",
                                     "50",
                                     "bold"),
                               tags="end",
                               fill="red")
            canvas.tag_unbind("piece",
                              "<Button-1>")

        canvas_time.after(1000, self.time_update)

    def unfocus_possible_moves(self, event):
        canvas.delete("possible_move")
        canvas.delete("selected_piece")

    def visualize_possible_moves(self, event):
        canvas.delete("possible_move")
        canvas.delete("selected_piece")

        position = canvas.gettags("current")[2]

        px, py = self.board_tkinter[position][1]

        canvas.create_oval(px + 35, py + 35,
                           px - 35, py - 35,
                           width=3,
                           outline="HotPink2",
                           tags="selected_piece")

        for move in self.board_tkinter:
            for promote in "rnbq ":
                move_to = "0000" if position == move else position+move+promote
                move_to = move_to.replace(" ", "")

                if chess.Move.from_uci(uci=move_to) in self.board.legal_moves:
                    x, y = self.board_tkinter[move][1]

                    canvas.create_oval(x - 30, y - 30,
                                       x + 30, y + 30,
                                       fill="pale green",
                                       outline="dark olive green",
                                       tags=(move_to, "possible_move"))
        canvas.update()

    def move_piece(self, event):
        move = canvas.gettags("current")[0]

        if len(move) == 5:
            self.promotion_move = move[:4]
            self.create_choose_promotion()
            return None

        self.board.push(chess.Move.from_uci(move))
        self.update_board()

    def create_choose_promotion(self):
        pieces = list(self.images.keys())

        n = 6 if self.black else 0

        for y in range(2):
            for x in range(2):
                piece = pieces[n]
                canvas_promotion.create_image(x*60+30, y*60+30,
                                              image=self.images[piece][1],
                                              tags=(piece, "promotion"))
                n += 1

        canvas_promotion.update()
        canvas_promotion.tag_bind("promotion",
                                  "<Button-1>",
                                  self.choose_promotion)

    def choose_promotion(self, event):
        piece = canvas_promotion.gettags("current")[0]

        canvas_promotion.delete("all")

        self.board.push(chess.Move.from_uci(self.promotion_move+piece.lower()))
        self.update_board()

    def check_status(self):
        status_checkmate = self.board.is_checkmate()
        status_stalemate = self.board.is_stalemate()
        status_not_enough_pieces = self.board.is_insufficient_material()

        if status_checkmate:
            canvas.create_text(320, 320,
                               text="Checkmate",
                               font=("Arial Rounded MT Bold",
                                     "50",
                                     "bold"),
                               tags="end",
                               fill="red")
            self.is_time_set = False
            return True

        elif status_stalemate or status_not_enough_pieces:
            canvas.create_text(320, 320,
                               text="Stalemate",
                               font=("Arial Rounded MT Bold",
                                     "50",
                                     "bold"),
                               tags="end",
                               fill="red")
            self.is_time_set = False
            return True

    def destroy_time(self):
        self.is_time_set = False


class settings_chess():
    def __init__(self):
        self.chess = play_chess(False, False, False)

        self.start = tkinter.Button(root,
                                    text="START",
                                    command=self.start_game,
                                    anchor=tkinter.CENTER,
                                    highlightbackground="gray25")
        self.start.grid(row=0,
                        column=1)

        opponents = {
                "PC": "1",
                "1vs1": "0",
            }
        self.opponent = tkinter.StringVar(root, 1)
        for (opponent_, index) in opponents.items():
            row = 3+int(index)
            tkinter.Radiobutton(root,
                                text=opponent_,
                                variable=self.opponent,
                                bg="gray25",
                                fg="white",
                                selectcolor="gray25",
                                anchor=tkinter.W,
                                value=index).grid(row=row, column=1)

        self.label_time = tkinter.Label(root,
                                        text="Set time",
                                        bg="gray25",
                                        fg="white")
        self.label_time.grid(row=8,
                             column=1)

        is_number_entry = root.register(self.is_number)
        self.set_time = tkinter.Entry(root,
                                      highlightbackground="gray25",
                                      width=10,
                                      validate="key",
                                      validatecommand=(is_number_entry, "%P"))
        self.set_time.grid(row=9,
                           column=1)

    def start_game(self):
        canvas.delete("all")
        canvas_promotion.delete("all")
        canvas_time.delete("white_time")
        canvas_time.delete("black_time")

        self.start.config(text="NEW GAME")

        self.create_time()
        self.chess.destroy_time()

        self.chess = play_chess(bool(int(self.opponent.get())),
                                int(self.game_time),
                                True)

    def is_number(self, P):
        return P.isdigit() or P == ""

    def create_time(self):
        self.game_time = self.set_time.get()

        if not len(self.game_time):
            self.game_time = "0"

        canvas_time.create_rectangle(0, 0, 120, 60,
                                     fill="white",
                                     width=0)

        canvas_time.create_rectangle(0, 60, 120, 120,
                                     fill="black",
                                     width=0)

        canvas_time.create_text(60, 30,
                                text=self.game_time,
                                tags="white_time",
                                font=("Arial Rounded MT Bold",
                                      "15",
                                      "bold"),
                                fill="black")

        canvas_time.create_text(60, 90,
                                text=self.game_time,
                                tags="black_time",
                                font=("Arial Rounded MT Bold",
                                      "15",
                                      "bold"),
                                fill="white")


settings_chess()
