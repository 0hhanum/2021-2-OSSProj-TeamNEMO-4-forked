import pygame.time

from Games.game_settings import *

def message_to_screen_center(surface, msg, color, text_font, y):
    textSurf, textRect = text_objects(msg, color, text_font)
    textRect.center = SCREEN_WIDTH / 2, y
    surface.blit(textSurf, textRect)


def message_to_screen_left(surface, msg, color, font, x, y):
    textSurf, textRect = text_objects(msg, color, font)
    surface.blit(textSurf, (x, y))

class TugOfWar:
    # 클래스 변수
    WIN_LEVEL = 5 # LEVEL 5 통과하면 게임 끝
    A_TIME = random.randint(3, 5) # A 누를 수 있는 시간
    D_TIME = random.randint(3, 5)
    numClick = 30 # level마다 눌러야하는 키 수

    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        # 화면 설정
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(WHITE)
        pygame.display.set_caption(title)
        # 이미지 불러오기
        self.char_1 = pygame.image.load("Images/char1.png")
        self.char_2 = pygame.image.load("Images/char2.png")
        self.imgBG = pygame.image.load("Images/TugOfWarBack.png")
        # 타이머 설정
        self.game_over_timer = None
        self.a_TIMER = False

    def start_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_e:
                        self.run_game_loop(1)
            # 배경 설정
            self.screen.fill(WHITE)
            self.screen.blit(self.imgBG, (0, 0))
            # 문구 놓기
            message_to_screen_center(self.screen, '줄다리기 게임', WHITE, korean_font, SCREEN_HEIGHT / 4)
            message_to_screen_left(self.screen, '[조작법]', WHITE, korean_font_small_size, 150, 320)
            message_to_screen_left(self.screen, 'A 클릭하여 줄 당기기', WHITE, korean_font_small_size, 150, 370)
            message_to_screen_left(self.screen, 'D 클릭하여 버티기', WHITE, korean_font_small_size, 150, 420)
            message_to_screen_left(self.screen, 'E 로 시작, Q 또는 Esc로 종료', WHITE, korean_font_small_size, 150, 480)
            pygame.display.update()

    # 통과 화면
    def win_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return False
            # 배경 설정
            self.screen.fill(BLACK)
            # 문구 넣기
            message_to_screen_center(self.screen, '줄 다리기 게임을 통과했습니다', BLUE, korean_font, 200)
            message_to_screen_center(self.screen, '시작화면으로 이동 : R', BLUE, korean_font, 300)
            message_to_screen_center(self.screen, '게임 종료 : Q', BLUE, korean_font, 400)
            pygame.display.update()

        # 실패 화면
    def lose_game(self):
        message_to_screen_center(self.screen, '탈 락 하 셨 습 니 다', RED, korean_font, self.width / 2)
        pygame.display.update()
        clock.tick(2)

    def game_restart(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return False
            # 배경 넣기
            self.screen.fill(WHITE)
            # 문구 넣기
            message_to_screen_center(self.screen, '재시도 : R', RED, korean_font, 300)
            message_to_screen_center(self.screen, '시작화면으로 이동 : Q', RED, korean_font, 400)
            pygame.display.update()

    def run_game_loop(self, level):
        game_over = False
        did_win = True
        click_wrong = False
        click = 0
        nClick = level * self.numClick

        # 게임 오버(전체 시간) 타이머 설정
        if level == 1:
            self.game_over_timer = GameOverTimer(100)

        print('---------------------')
        print('LEVEL {}'.format(level))

        start_ticks = pygame.time.get_ticks()
        a_ticks = pygame.time.get_ticks()

        while not game_over:
            # 게임 오버 타이머 남은 시간
            all_left_time = self.game_over_timer.time_checker()

            # 배경 다시 설정
            self.screen.fill(WHITE)
            self.screen.blit(self.imgBG, (0, 0))

            # 캐릭터 배치
            for i in range(0, 211, 70):
                self.screen.blit(self.char_1, (i, 240))
            for i in range(760, 549, -70):
                self.screen.blit(self.char_2, (i, 240))

            # d 누르는 타이머 설정
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            d_timer = round(float(self.D_TIME - elapsed_time), 1)
            # LEVEL 표시
            message_to_screen_left(
                self.screen, 'LEVEL {}'.format(level), WHITE, level_font, 0, 0)
            # 남은 전체 시간 화면에 표시
            message_to_screen_left(
                self.screen, 'Left Time : {}'.format(all_left_time), WHITE, level_font, 0, 35)
            # 남은 클릭 수 화면에 표시
            message_to_screen_center(
                self.screen, 'Left Click : {}'.format((nClick - click)), WHITE, level_font, 10)
            # 메세지 표시 when d 누르는 시간일 때
            if d_timer > 0:
                message_to_screen_center(
                    self.screen, "Click D", WHITE, large_font, self.height / 2)
                message_to_screen_center(
                    self.screen, f'{d_timer}', WHITE, large_font, self.height / 3)

            # a 누르는 시간 (d 누르는 시간 끝남)
            if d_timer <= 0:
                self.a_TIMER = True
                a_time_checker = round(self.A_TIME - (d_timer) * (-1), 1)
                message_to_screen_center(
                    self.screen, "Click A", WHITE, large_font, self.height / 2)
                message_to_screen_center(
                    self.screen, f'{a_time_checker}', WHITE, large_font, self.height / 3)
                if a_time_checker <= 0:  # a 누르는 시간 끝나면 d 누르는 타이머 초기화
                    self.a_TIMER = False
                    start_ticks = pygame.time.get_ticks()
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                    d_timer = round(float(self.D_TIME - elapsed_time), 1)
                else:
                    a_elapsed_time = (pygame.time.get_ticks() - a_ticks) / 1000
                    a_timer = round(float(self.A_TIME - a_elapsed_time), 1)
                    if a_timer <= 0:
                        a_ticks = pygame.time.get_ticks()
                        a_elapsed_time = (pygame.time.get_ticks() - a_ticks) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if d_timer > 0: # d 누르는 타이머 돌아갈 때
                        if event.key == pygame.K_d:
                            click += 1
                        elif event.key == pygame.K_a:
                            click_wrong = True
                            break
                    elif d_timer < 0: # a 누르는 타이머 돌아갈 때
                        if event.key == pygame.K_a:
                            click += 1
                        elif event.key == pygame.K_d:
                            click_wrong = True
                            break

            # 키 잘못 입력 or 전체 시간 끝나면 게임 종료
            if click_wrong or all_left_time < 0:
                did_win = False
                break
            # 클릭 수 채운 경우 ~> did_win이 True인 상태로 반복문 탈출
            if click == nClick:
                message_to_screen_center(
                    self.screen, ' Level {} Clear'.format(level), BLUE, level_font, self.height / 3)
                break
            pygame.display.update()

        if did_win:
            if level >= self.WIN_LEVEL:
                self.win_game()
            else:
                message_to_screen_left(self.screen, 'LEVEL {}'.format(level), WHITE, level_font, 0, 0)
                self.run_game_loop(level + 1)
        elif self.game_restart():
            self.run_game_loop(1)
        else:
            return




pygame.init()
new_game = TugOfWar(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.start_game()

pygame.quit()
quit()


