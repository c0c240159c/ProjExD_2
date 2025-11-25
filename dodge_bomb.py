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
    """
    引数：スクリーンサーフェス
    戻り値：黒背景にgameoverとこうかとんの画像
    """
    font = pg.font.Font(None, 80)
    txt = font.render("gameover",True, (255, 255, 255)) # テキスト

    k_cry_img = pg.image.load("fig/8.png") # こうかとん

    go_screen = pg.Surface((WIDTH, HEIGHT)) # 黒スクリーン
    go_screen.fill((0, 0, 0))
    go_screen.set_alpha(175)

    go_screen.blit(txt, [400, 275]) 
    go_screen.blit(k_cry_img, [325, 275])
    go_screen.blit(k_cry_img, [700, 275]) # 描写
    screen.blit(go_screen, [0, 0])
    pg.display.update()


def init_bb_imgs() -> tuple[list, list[int]]:
    """
    戻り値：10段階の大きさの爆弾と加速度
    """
    bb_imgs = []
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1,11)]

    return bb_imgs,bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    戻り値：角度に応じたこうかとんの向きの辞書
    """
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img,True,False)
    kk_dict = {
        ( 0, 0):pg.transform.rotozoom(kk_img,  0,0.9), # キー入力無し
        ( 5, 0):pg.transform.rotozoom(kk_img,  0,0.9), # 右
        ( 5,-5):pg.transform.rotozoom(kk_img, 45,0.9), # 右上
        ( 0,-5):pg.transform.rotozoom(kk_img, 90,0.9), # 上
        (-5,-5):pg.transform.rotozoom(kk_img, 45,0.9), # 左上
        (-5, 0):pg.transform.rotozoom(kk_img,  0,0.9), # 左
        (-5, 5):pg.transform.rotozoom(kk_img,-45,0.9), # 左下
        ( 0, 5):pg.transform.rotozoom(kk_img,-90,0.9), # 下
        ( 5, 5):pg.transform.rotozoom(kk_img,-45,0.9), # 右下
    }
    return kk_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) # 爆弾の初期位置ランダム生成
    vx, vy = +5, +5 # 爆弾の速度
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs() # 爆弾リスト取得
    kk_imgs = get_kk_imgs() # 角度に応じた向きの辞書取得
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

        kk_img = kk_imgs[tuple(sum_mv)]
        if sum_mv[0] < 0:
            kk_img = pg.transform.flip(kk_img,True,False) # 左を向いている時は左右反転
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 移動取り消し
        screen.blit(kk_img, kk_rct)

        bb_img = bb_imgs[min(tmr//500, 9)] # 大きさの変更
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)] # 速度変更
        bb_rct.width = bb_img.get_rect().width # 横判定の変更
        bb_rct.height = bb_img.get_rect().height #縦判定の変更
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
            avx *= -1 # 左右の壁に当たったら左右反転
        if not tate:
            vy *= -1
            avy *= -1 # 上下の壁に当たったら上下反転
        if abs(vx) > abs(avx): # 絶対値vxが絶対値avxより大きいならvxとvyで、でなければavxとavyで動かす
            bb_rct.move_ip(vx,vy)
        else:
            bb_rct.move_ip(avx,avy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
