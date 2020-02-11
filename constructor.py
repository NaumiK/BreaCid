from core import map_view
from core.download_something import download_map_format_brcd, download_list_of_images_format_brcd
from core.user_interface.widgets.minimap_widget import Mini_map
from core.user_interface import Cursor
import pygame

pygame.init()
scr = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
clock = pygame.time.Clock()
fps = 60
cursor = Cursor(".data/cursors/cur1.png", ".data/cursors/cur2.png")
un = True


class Constructor(map_view.Board):
    def on_click(self, cell_indexes):
        x, y = cell_indexes
        self.board[x][y] = [i for i in range(len(self.cell_color))][(self.board[x][y] + 1) % len(self.cell_color)]


map_data = download_map_format_brcd("./.data/maps/Test_map/h.brcd")
tex_data = download_list_of_images_format_brcd("./.data/maps/Test_map/t.brcd")
min_map = Mini_map(0, 750-200, 200, 200, map_data[0], tex_data[2])
board = Constructor(len(map_data[0]), len(map_data[0][0]), scr, tex_data[0], tex_data[1])
board.set_view(0, 0, 30)
board.set_terrain(map_data[0], map_data[1], map_data[2])
camera = map_view.Camera()
running = True
while running:
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            un = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                un = True
            elif event.button == 4 or event.button == 5:
                camera.set_scale(event)
            else:
                board.get_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            camera.check_event(event)
        elif event.type == pygame.KEYUP and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]:
            camera.set_steps(0, 0)
        elif event.type == pygame.KEYUP and event.key == pygame.K_q:
            cell = board.get_cell((x, y))
            if cell:
                k, v = cell
                board.level_of_terrain[k][v] += 1
        elif event.type == pygame.KEYUP and event.key == pygame.K_w:
            cell = board.get_cell((x, y))
            if cell:
                k, v = cell
                board.level_of_terrain[k][v] -= 1
    camera.apply(board)
    clock.tick(fps)
    scr.fill((0, 0, 0))
    board.render()
    min_map.update(scr)
    cursor.switch_image(un)
    cursor.render_image(scr, x - 10, y - 5)
    pygame.display.flip()
