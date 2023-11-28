import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1200, 600
delta = {  #3 方向キーの移動量の辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5, 0)
}
def check_bound(rct: pg.Rect)->tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し　真理値タプルを返す関数
    引数rct　こうかとんor爆弾Surfaceのrct
    戻り値　横方向　縦方向はみ出し判定結果（画面内　True/画面外　False）
    """
    yoko, tate = True, False
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or WIDTH < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()  #練習3　こうかとんSurfaceのrectを抽出
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20,20))  #練習1　透明なSurfaceの作成
    bb_img.set_colorkey((0, 0, 0))  #黒を透過させる
    pg.draw.circle(bb_img,(255, 0, 0), (10,10),10)  #練習1　中心に半径10の赤い円を描画
    bb_rct = bb_img.get_rect()  #練習2　爆弾Surfaceのrectを抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  #練習2：爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if kk_rct.colliderect(bb_rct):
                print("Game over")
                return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst [k]:  #練習3　キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)  #練習3：こうかとんを移動させる
        bb_rct.move_ip(vx, vy)
        yoko = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()