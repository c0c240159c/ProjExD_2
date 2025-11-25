import os
import random
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {pg.K_UP:(0,-5),pg.K_DOWN:(0,5),
          pg.K_LEFT:(-5,0),pg.K_RIGHT:(5,0),}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんrectまたは爆弾rect
    値：判定結果タプル
    画面内ならTrue、外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False # 横方向判定
    if rct.top <0 or HEIGHT < rct.bottom:
        tate = False # 縦方向判定
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    font = pg.font.Font(None, 80)
    txt = font.render("gameover",True, (255, 255, 255)) # テキスト

    k_cry_img = pg.image.load("fig/8.png") # こうかとん

    go_screen = pg.Surface((WIDTH, HEIGHT)) # 黒スクリーン
    go_screen.fill((0, 0, 0))
    go_screen.set_alpha(160)

    go_screen.blit(txt, [400, 275]) 
    go_screen.blit(k_cry_img, [325, 275])
    go_screen.blit(k_cry_img, [700, 275]) # 描写
    screen.blit(go_screen, [0, 0])
    pg.display.update()



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) # 爆弾ランダム生成
    vx, vy = +5, +5 # 爆弾の速度
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): # 衝突判定
            gameover(screen)
            time.sleep(5)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, mv in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += mv[0] # 横方向
                sum_mv[1] += mv[1] # 縦方向

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 移動取り消し
        
        screen.blit(kk_img, kk_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx,vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
