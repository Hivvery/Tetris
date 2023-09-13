#Import modules
import math, pygame, random, sys
pygame.init()

#Window information
Config = {
    "framerate": 30,
    "screen_caption": "Pygame Template",
    "screen_x": 600,
    "screen_y": 720,
}
#Piece information
Pieces = {
    "I0": [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
    "I1": [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
    "I2": [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],
    "I3": [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
    "J0": [[0, 1, 0], [0, 1, 0], [0, 1, 1]],
    "J1": [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
    "J2": [[1, 1, 0], [0, 1, 0], [0, 1, 0]],
    "J3": [[0, 0, 0], [1, 1, 1], [1, 0, 0]],
    "L0": [[0, 1, 1], [0, 1, 0], [0, 1, 0]],
    "L1": [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    "L2": [[0, 1, 0], [0, 1, 0], [1, 1, 0]],
    "L3": [[0, 0, 0], [1, 1, 1], [0, 0, 1]],
    "O0": [[1, 1], [1, 1]],
    "O1": [[1, 1], [1, 1]],
    "O2": [[1, 1], [1, 1]],
    "O3": [[1, 1], [1, 1]],
    "S0": [[0, 0, 1], [0, 1, 1], [0, 1, 0]],
    "S1": [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
    "S2": [[0, 1, 0], [1, 1, 0], [1, 0, 0]],
    "S3": [[0, 0, 0], [1, 1, 0], [0, 1, 1]],
    "T0": [[0, 1, 0], [0, 1, 1], [0, 1, 0]],
    "T1": [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    "T2": [[0, 1, 0], [1, 1, 0], [0, 1, 0]],
    "T3": [[0, 0, 0], [1, 1, 1], [0, 1, 0]],
    "Z0": [[0, 1, 0], [0, 1, 1], [0, 0, 1]],
    "Z1": [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    "Z2": [[1, 0, 0], [1, 1, 0], [0, 1, 0]],
    "Z3": [[0, 0, 0], [0, 1, 1], [1, 1, 0]],
}
#Colors used when displaying pieces
Pieces_Colors = {
    "I": (  0, 255, 255),
    "J": (  0, 104, 255),
    "L": (255, 128,   0),
    "O": (255, 208,  52),
    "S": (  0, 255, 128),
    "T": (208,   0, 255),
    "Z": (255,  48,  64),
}
#Variables
Variables = {
    #Length of the falling cooldown in frames
    "cooldown_fall": 10,
    #Frame the falling was last done
    "cooldown_fall_time": 0,
    #Amount of frames passed
    "frames": 0,
    #Playing the game
    "game": True,
    #Grid tile size, width and height
    "grid_tile_size": 0,
    "grid_x": 10,
    "grid_y": 20,
    #Already swapped the piece with the held piece
    "held": False,
    "piece_number": 0,
    #Amount of next pieces shown
    "piece_previews": 5,
    #Piece is overlapping with a cell on the grid or going below the bottom of the grid
    "piece_overlapping": False,
    #Rotation of piece
    "piece_rotation": 0,
    #Type of piece and rotation
    "piece_type": "",
    #Current score
    "score": 0,
    #Amount to add to the score variable
    "score_get": 0,
    #Best score out of all games
    "score_high": 0,
    #Number of rows cleared
    "score_rows": 0,
    #Number of times four rows are cleared with one piece
    "score_tetrises": 0,
}
#Set tile size
Variables["grid_tile_size"] = Config["screen_y"] / Variables["grid_y"]

#Grid
Grid = [["" for j in range(Variables["grid_y"])] for i in range(Variables["grid_x"])]
#Positions of piece cells
Cell_Positions = []
#Bag of pieces to make random pieces gotten more balanced
Pieces_Bag = ["I", "J", "L", "O", "S", "T", "Z"]
Pieces_Order = []

#Position of the top left of the piece
Piece_Position = [math.floor(Variables["grid_x"] / 2), -1]

#Reset the game
def game_reset():
    global Grid
    Variables["game"] = True
    Variables["held"] = False
    Variables["piece_number"] = 0
    Variables["score"] = 0
    Variables["score_rows"] = 0
    Variables["score_tetrises"] = 0
    #Clear grid
    Grid.clear()
    Grid = [["" for j in range(Variables["grid_y"])] for i in range(Variables["grid_x"])]
    #Reset pieces bag
    Pieces_Bag.clear()
    Pieces_Bag.append("I")
    Pieces_Bag.append("J")
    Pieces_Bag.append("L")
    Pieces_Bag.append("O")
    Pieces_Bag.append("S")
    Pieces_Bag.append("T")
    Pieces_Bag.append("Z")
    #Reset piece order
    Pieces_Order.clear()
    Pieces_Order.append("")
    for i in range(Variables["piece_previews"] + 1):
        piece_add()
    piece_make()
#Add a piece to the pieces order list
def piece_add():
    Pieces_Order.append(Pieces_Bag[random.randint(0, len(Pieces_Bag) - 1)])
    Pieces_Bag.remove(Pieces_Order[len(Pieces_Order) - 1])
    if len(Pieces_Bag) == 0:
        Pieces_Bag.append("I")
        Pieces_Bag.append("J")
        Pieces_Bag.append("L")
        Pieces_Bag.append("O")
        Pieces_Bag.append("S")
        Pieces_Bag.append("T")
        Pieces_Bag.append("Z")
#Find where the piece's cells are
def piece_cells():
    Cell_Positions.clear()
    for i in range(len(Pieces[Variables["piece_type"]])):
        for j in range(len(Pieces[Variables["piece_type"]][0])):
            if Pieces[Variables["piece_type"]][i][j] == 1:
                Cell_Positions.append([Piece_Position[0] + i, Piece_Position[1] + j])
#Draw a piece icon on the screen
def piece_draw(piece, pos_x, pos_y, size_x, size_y):
    pygame.draw.rect(screen, (  0,  32,  64), [pos_x - size_x / 2, pos_y - size_y / 2, size_x, size_y])
    for i in range(len(Pieces[piece + str(0)])):
        for j in range(len(Pieces[piece + str(0)][0])):
            if Pieces[piece + str(0)][i][j] == 1:
                pygame.draw.rect(screen, Pieces_Colors[piece], [i * (size_x / len(Pieces[piece + str(0)])) + pos_x - size_x / 2, j * (size_y / len(Pieces[piece + str(0)][0])) + pos_y - size_y / 2, size_x / len(Pieces[piece + str(0)]), size_y / len(Pieces[piece + str(0)][0])])
#Put a piece on the grid
def piece_make():
    piece_add()
    Variables["piece_number"] += 1
    Variables["piece_rotation"] = random.randint(0, 3)
    Variables["piece_type"] = Pieces_Order[Variables["piece_number"]] + str(Variables["piece_rotation"])
    #Fix starting rotation
    if Variables["piece_type"] == "I1":
        Variables["piece_type"] = "I3"
    if Variables["piece_type"] == "I2":
        Variables["piece_type"] = "I0"
    if Variables["piece_type"] == "S0":
        Variables["piece_type"] = "S2"
    if Variables["piece_type"] == "S3":
        Variables["piece_type"] = "S1"
    if Variables["piece_type"] == "Z0":
        Variables["piece_type"] = "Z2"
    if Variables["piece_type"] == "Z3":
        Variables["piece_type"] = "Z1"
    #Put piece at the top middle of the grid
    Piece_Position[0] = math.ceil(Variables["grid_x"] / 2) - math.floor(len(Pieces[Variables["piece_type"]]) / 2)
    Piece_Position[1] = 0
    piece_cells()
    Variables["cooldown_fall"] = 10
    Variables["cooldown_fall_time"] = Variables["frames"]
    Variables["piece_overlapping"] = False
    Variables["score_get"] = 0
    #Clear empty rows
    for i in range(Variables["grid_y"]):
        if not "" in [Grid[j][i] for j in range(Variables["grid_x"])]:
            for j in range(Variables["grid_x"]):
                Grid[j].pop(i)
                Grid[j].insert(0, "")
            if Variables["score_get"] == 0:
                Variables["score_get"] = 10
            else:
                Variables["score_get"] *= 2
            Variables["score_rows"] += 1
    #Update score variables
    #0 rows: 1 point
    #1 rows: 10 points
    #2 rows: 20 points
    #3 rows: 40 points
    #4 rows: 80 points
    Variables["score"] += Variables["score_get"]
    if Variables["score_get"] > 0:
        Variables["score"] -= 1
        if Variables["score_get"] == 80:
            Variables["score_tetrises"] += 1
    #End the game if the top row has a cell in it
    if not [Grid[i][0] for i in range(Variables["grid_x"])] == ["" for i in range(Variables["grid_x"])]:
        Variables["game"] = False
#Move the falling piece down
def piece_move():
    piece_cells()
    #Keep cells in the grid
    if -1 in [Cell_Positions[i][0] for i in range(len(Cell_Positions))]:
        Piece_Position[0] += 1
        piece_cells()
    elif Variables["grid_x"] in [Cell_Positions[i][0] for i in range(len(Cell_Positions))]:
        Piece_Position[0] -= 1
        piece_cells()
    #Check for the piece overlapping
    if Variables["grid_y"] in [Cell_Positions[i][1] for i in range(len(Cell_Positions))]:
        Variables["piece_overlapping"] = True
    else:
        Piece_Cells_Empty = [Grid[Cell_Positions[i][0]][Cell_Positions[i][1]] for i in range(len(Cell_Positions))]
        if "I" in Piece_Cells_Empty or "J" in Piece_Cells_Empty or "L" in Piece_Cells_Empty or "O" in Piece_Cells_Empty or "S" in Piece_Cells_Empty or "T" in Piece_Cells_Empty or "Z" in Piece_Cells_Empty:
            Variables["piece_overlapping"] = True
    if Variables["piece_overlapping"]:
        #Move piece up
        Piece_Position[1] -= 1
        piece_cells()
        #Place piece
        for i in range(len(Cell_Positions)):
            Grid[Cell_Positions[i][0]][Cell_Positions[i][1]] = Variables["piece_type"][0]
        Variables["held"] = False
        Variables["score"] += 1
        piece_make()
#Draw the screen
def draw():
    screen.fill((  0,   0,   0))
    pygame.draw.rect(screen, (  0,  32,  64), [Config["screen_x"] / 5, 0, Config["screen_x"] * 0.6, Config["screen_y"]])
    for i in range(Variables["grid_x"]):
        for j in range(Variables["grid_y"]):
            if not Grid[i][j] == "":
                if Variables["game"]:
                    pygame.draw.rect(screen, Pieces_Colors[Grid[i][j]], [i * Variables["grid_tile_size"] + Config["screen_x"] / 5, j * Variables["grid_tile_size"], Variables["grid_tile_size"], Variables["grid_tile_size"]])
                else:
                    pygame.draw.rect(screen, (191, 191, 191), [i * Variables["grid_tile_size"] + Config["screen_x"] / 5, j * Variables["grid_tile_size"], Variables["grid_tile_size"], Variables["grid_tile_size"]])
    #Draw falling piece
    if Variables["game"]:
        for i in range(len(Cell_Positions)):
            pygame.draw.rect(screen, Pieces_Colors[Variables["piece_type"][0]], [Cell_Positions[i][0] * Variables["grid_tile_size"] + Config["screen_x"] / 5, Cell_Positions[i][1] * Variables["grid_tile_size"], Variables["grid_tile_size"], Variables["grid_tile_size"]])
    #Draw held piece and next pieces
    for i in range(Variables["piece_previews"]):
        piece_draw(Pieces_Order[Variables["piece_number"] + i + 1], Config["screen_x"] * 0.9, i * 70 + 80, 60, 60)
    if not Pieces_Order[0] == "":
        piece_draw(Pieces_Order[0], Config["screen_x"] * 0.1, 310, 60, 60)
    else:
        pygame.draw.rect(screen, (  0,  32,  64), [Config["screen_x"] * 0.1 - 30, 280, 60, 60])
    #Draw text
    font = pygame.font.SysFont("bahnschrift", 20)
    text = font.render("High Score", False, (255, 255, 255))
    text_rect = text.get_rect(center=(Config["screen_x"] / 10, 30))
    screen.blit(text, text_rect)
    text = font.render("Score", False, (255, 255, 255))
    text_rect = text.get_rect(center=(Config["screen_x"] / 10, 90))
    screen.blit(text, text_rect)
    text = font.render("Rows", False, (255, 255, 255))
    text_rect = text.get_rect(center=(Config["screen_x"] / 10, 150))
    screen.blit(text, text_rect)
    text = font.render("Tetrises", False, (255, 255, 255))
    text_rect = text.get_rect(center=(Config["screen_x"] / 10, 210))
    screen.blit(text, text_rect)
    text = font.render("Hold", False, (255, 255, 255))
    text_rect = text.get_rect(center=(Config["screen_x"] / 10, 270))
    screen.blit(text, text_rect)
    text = font.render("Next", False, (255, 255, 255))
    text_rect = text.get_rect(center=(Config["screen_x"] * 0.9, 30))
    screen.blit(text, text_rect)
    #Draw scores
    font = pygame.font.SysFont("bahnschrift", 30)
    text = font.render(str(Variables["score_high"]), False, (255, 255, 255))
    text_rect = text.get_rect(center=(Config["screen_x"] / 10, 60))
    screen.blit(text, text_rect)
    text = font.render(str(Variables["score"]), False, (255, 255, 255))
    text_rect = text.get_rect(center=(Config["screen_x"] / 10, 120))
    screen.blit(text, text_rect)
    text = font.render(str(Variables["score_rows"]), False, (255, 255, 255))
    text_rect = text.get_rect(center=(Config["screen_x"] / 10, 180))
    screen.blit(text, text_rect)
    text = font.render(str(Variables["score_tetrises"]), False, (255, 255, 255))
    text_rect = text.get_rect(center=(Config["screen_x"] / 10, 240))
    screen.blit(text, text_rect)
    pygame.display.update()
def main():
    global screen
    #Setup window
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((Config["screen_x"], Config["screen_y"]))
    pygame.display.set_caption(Config["screen_caption"])
    game_reset()
    while True:
        for event in pygame.event.get():
            #Check for window exiting
            if event.type == pygame.QUIT:
                sys.exit()
            #Check for key presses
            #A: Move piece left
            #D: Move piece right
            #S: Move piece down
            #X: Drop piece
            #E: Rotate piece
            #W: Hold piece
            if event.type == pygame.KEYDOWN:
                if Variables["game"]:
                    if Variables["cooldown_fall"] != 1:
                        if event.key == pygame.K_a:
                            if not 0 in [Cell_Positions[i][0] for i in range(len(Cell_Positions))]:
                                Piece_Position[0] -= 1
                        if event.key == pygame.K_d:
                            if not Variables["grid_x"] - 1 in [Cell_Positions[i][0] for i in range(len(Cell_Positions))]:
                                Piece_Position[0] += 1
                        if event.key == pygame.K_e:
                            Variables["piece_rotation"] += 1
                            if Variables["piece_rotation"] == 4:
                                Variables["piece_rotation"] = 0
                            Variables["piece_type"] = Variables["piece_type"][0] + str(Variables["piece_rotation"])
                        if event.key == pygame.K_s:
                            Piece_Position[1] += 1
                        if event.key == pygame.K_w and Pieces_Order[0] != Pieces_Order[Variables["piece_number"]] and not Variables["held"]:
                            #Swap piece with held piece
                            Variables["held"] = True
                            hold_new = Pieces_Order[0]
                            Pieces_Order[0] = Pieces_Order[Variables["piece_number"]]
                            Pieces_Order[Variables["piece_number"]] = hold_new
                            if Pieces_Order[Variables["piece_number"]] == "":
                                Pieces_Order.remove("")
                            Variables["piece_number"] -= 1
                            piece_make()
                    if event.key == pygame.K_x:
                        #Set falling cooldown to 1 to speed up piece movement
                        Variables["cooldown_fall"] = 1
                    piece_move()
                else:
                    if event.key == pygame.K_r:
                        game_reset()
        #Move falling piece down
        if Variables["game"] and (Variables["frames"] == 0 or Variables["frames"] >= Variables["cooldown_fall_time"] + Variables["cooldown_fall"]):
            Variables["cooldown_fall_time"] = Variables["frames"]
            Piece_Position[1] += 1
            piece_move()
        #Update high score
        if Variables["score"] > Variables["score_high"]:
            Variables["score_high"] = Variables["score"]
        draw()
        clock.tick(Config["framerate"])
        Variables["frames"] += 1
if __name__ == "__main__":
    main()