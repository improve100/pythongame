'''
公众号：一行玩python，关注领取5T编程资料
'''
import pygame, os
import time
import random
from pygame.sprite import Sprite
from pygame.sprite import Group


def fire_music():
    pass
    # 设置开火音乐
    # effect = pygame.mixer.Sound('sounds/fire.wav')
    # pygame.mixer.Sound.play(effect)

class Boss(Sprite):
    def __init__(self,boss_img_name):
        super().__init__()
        # 加载BOSS图片
        self.image = pygame.image.load('图片/'+boss_img_name+'.png').convert_alpha()
        # 转换BOSS大小
        # self.image = pygame.transform.scale(self.image, (1, 12))
        # 生成BOSS矩形框架
        self.rect = self.image.get_rect()
        self.blood = 1000
        # boss左右移动的速度
        self.speed = 3.5

    def move(self):
        if self.rect.centerx>=512:
            self.speed =-self.speed
        if self.rect.centerx<=0:
            self.speed = -self.speed
        self.rect.centerx +=self.speed



class Enemy(Sprite):
    def __init__(self,screen):
        # 必须设置继承精灵 不然在使用精灵函数时会报错
        super().__init__()
        # 获取屏幕对象
        self.screen = screen
        # 随机 生成5个编号
        alien_num = random.randint(1,5)
        # 随机 加载五个飞机中的某个
        self.image = pygame.image.load('图片/alien_' + str(alien_num) + '.png')
        # picture = pygame.transform.scale(picture, (1280, 720))
        self.image = pygame.transform.scale(self.image,(62,62))
        # 获取飞机的 rect
        self.rect = self.image.get_rect()
        # 击落本机获得的分数
        self.score = 10
        # 加载子弹的图片
        self.bullet_img = pygame.image.load("图片/alien_bullet.png").convert_alpha()
        self.bullet_img = pygame.transform.scale(self.bullet_img, (12, 12))
        # 以下为可以调节子弹尺寸的代码
        # picture = pygame.transform.scale(picture, (1280, 720))
        #飞机的移动速度
        self.speed = random.randint(3,5)

        #生成子弹精灵组合
        self.bullets = Group()
        # 敌机射击频率
        self.shoot_frequency = 0

    # 飞机出现
    def move(self):
        self.rect.top += 5
        #暂时不用射击
        # self.shoot()
        # self.moveBullet()
    # 发射子弹
    def shoot(self):
        if self.shoot_frequency % 200 == 0:
            bullet = Enemy_Bullet(self.bullet_img, self.rect.midbottom)
            self.bullets.add(bullet)
        self.shoot_frequency += 1
        if self.shoot_frequency > 200:
            self.shoot_frequency = 1
    # 删除子弹
    def moveBullet(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
    # 绘制子弹
    def drawBullets(self, scr):
        self.bullets.draw(scr)


class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, init_pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("图片/alien_bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (12, 12))
        self.rect = self.image.get_rect()
        # 敌机子弹初始位置设置
        self.rect.midbottom = init_pos
        self.rect.centery +=36
        self.speed = 8

    def move(self):
        self.rect.top += self.speed
class MyHero(Sprite):
    _rate = 100 # 每帧停留的毫秒数
    def __init__(self,screen,size = 1):
        super().__init__()
        # 获取屏幕对象
        self.screen = screen
        # 获取整张图片
        self.image_big = pygame.image.load('图片/hero.png').convert_alpha()
        # subsurface 形成大图的子表面框架
        # 获取飞机正面图片
        self.image = self.image_big.subsurface(pygame.Rect(120, 0, 318 - 240, 87))
        # 获取飞机正面矩形框架尺寸
        self.rect = self.image.get_rect()
        # 获取屏幕对象矩形
        self.screen_rect = screen.get_rect()
        # 获取屏幕正中x坐标
        self.rect.centerx = self.screen_rect.centerx
        # 获取屏幕底部y坐标
        self.rect.centery = self.screen_rect.bottom - self.rect.height
        # 设置飞机初始位置
        self.centerX = float(self.rect.centerx)
        self.centerY = float(self.rect.centery)
        # 飞机尾焰
        self.air = None
        # 设置飞机尾焰位置
        self.air_rect = pygame.Rect(self.centerX - 20,self.centerY+int((self.rect.height+72)/2)-10-36,40,72)

        #玩家所有发射子弹的集合
        self.bullets = Group()
        self.bullet_image = pygame.image.load('图片/bullet_1.png').convert_alpha()

    # 子弹射击
    def shoot(self):
        # 产生一颗子弹实例
        bullet = Bullet(self.bullet_image,self.rect.midtop)
        # 在group子弹精灵集合中加入子弹
        self.bullets.add(bullet)
    # 子弹删除
    def moveBullet(self):
        # 逐个检查子弹精灵集合 到达屏幕顶端的子弹删除
        for bullet in self.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
    # 子弹显示
    def drawBullets(self, scr):
        # 将精灵集合中的子弹绘制到屏幕上
        self.bullets.draw(scr)



    # 向上飞时，增加喷射火焰
    def set_air(self, case):
        if case == 'up':
            air = pygame.image.load('图片/air.png').convert_alpha()
            img = air.subsurface(pygame.Rect(80, 0, 50, 87))
            self.air = img
        elif case == 'remove':
            self.air = None

    # 根据移动方向获取飞机移动状态的图片
    def set_image(self, case):
        if case=='left':
            rect = pygame.Rect(195,0,318-248,87)
            image = self.image_big.subsurface(rect)
        elif case =='right':
            rect = pygame.Rect(195,0,318-248,87)
            image = pygame.transform.flip(self.image_big.subsurface(rect), True, False)
        elif case == 'up' or case == 'down':
            rect = pygame.Rect(120, 0, 318 - 240, 87)
            image = self.image_big.subsurface(rect)
        self.image = image

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = bullet_img.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 25

    def move(self):
        self.rect.top -= self.speed


# 初始化pygame
pygame.init()
# pygame.mixer.init()
# pygame.mixer_music.load('sounds/enviro.mp3') # 加载播放音乐
# pygame.mixer.music.play(-1) #-1 为循环播放
# 设置游戏主题
pygame.display.set_caption('AirCraft')
# 初始化屏幕大小
screen = pygame.display.set_mode((512,768))

# 设置游戏背景图片
# 游戏刚开始时的背景图
bg_img0 = pygame.image.load('图片/start_bg.jpg').convert()
# 加载游戏开始图标
start_img = pygame.image.load('图片/start.png').convert_alpha()
start_rect = start_img.get_rect()
start_rect.centerx = 262
start_rect.centery = 455
#  游戏进行中的背景图
bg_img1 = pygame.image.load('图片/map1.jpg').convert()
bg_img2 = bg_img1.copy()
# 游戏结束时的背景图
bg_img3 = pygame.image.load('图片/map3.jpg').convert()
# 加载游戏结束图标
gameover_img = pygame.image.load('图片/gameover.png').convert_alpha()
# 加载游戏成功图标
gamesuccess = pygame.image.load('图片/success.png').convert_alpha()

# 加载重玩图标
restart_img = pygame.image.load('图片/restart.png').convert_alpha()
restart_rect = restart_img.get_rect()
restart_rect.centerx = 249
restart_rect.centery = 420
# 背景图片初始位置
pos_y1 = -768
pos_y2 = 0

# 实例化BOSS
boss = Boss('boss_1')
bosses = Group()
bosses.add(boss)
# 测试主角图片
# air = pygame.image.load('图片/air.png').convert_alpha()
# img = air.subsurface(pygame.Rect(80, 0, 50, 87))
# image_big = pygame.image.load('图片/hero.png').convert_alpha()
# image = image_big.subsurface(pygame.Rect(195,0,318-248,87))

# 生成我方飞机
student_plane = MyHero(screen)

# 生成敌方飞机
# 生成敌机group
enemies = Group()
# 生成敌机子弹
enemy_bullets = Group()
max_enemies = 9  # 设置敌机数量总数为9
# 敌机随机出现的节奏 下方randint参数 为43,55
ran1,ran2 = 30,40


# 生成计时频率变量
sec = 0
# 生成分数
score = 0
# 设置系统字体
my_font = pygame.font.Font('fonts/msyh.ttf', 18)

# 游戏主循环
# 设置游戏状态  开始 结束
game = 'wait'

while True:
    # 游戏在等待状态
    if game =='wait':
        # 最小游戏框架一个都不能省略
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # 检测鼠标是否按下 重新开始按钮
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 检测鼠标点击位置是否与重启rect重叠
                if start_rect.collidepoint(event.pos):
                    student_plane.__init__(screen)
                    game = 'ing'
        # 游戏结束游戏画面暂停
        screen.blit(bg_img0, (0, 0))
        screen.blit(start_img, start_rect)
        # 测试尾焰位置
        pygame.display.flip()
        time.sleep(0.05)

    # 游戏进行状态
    elif game == 'ing':
        # 设置这3行 监听事件 并且内部设定了延迟防止游戏卡死
        # 屏幕滚动-----------------------------------------------------
        screen.blit(bg_img1, (0, pos_y1))
        screen.blit(bg_img2, (0, pos_y2))
        # 测试尾焰位置
        # screen.blit(img, (100, 100))
        pos_y1 += 1
        pos_y2 += 1
        # 屏幕背景滚动完毕后重置位置
        if pos_y1 >= 0:
            pos_y1 = -768
        if pos_y2 >= 768:
            pos_y2 = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # 监听键盘事件
            # 按键弹起取消飞机向上尾焰 矫正飞机姿势
            if event.type == pygame.KEYUP:
                student_plane.set_image('down')
                student_plane.air = None
            # 发射子弹
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(student_plane.bullets) <6: # 检查子弹集合的数量限制子弹最大数量
                    fire_music()
                    # 产生一颗子弹实例
                    # 在group子弹精灵集合中加入子弹
                    student_plane.shoot()
        # 将精灵集合中的子弹绘制到屏幕上
        student_plane.drawBullets(screen)
        # 逐个检查子弹精灵集合 到达屏幕顶端的子弹删除
        student_plane.moveBullet()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            # 设置飞机状态图片
            student_plane.set_image('left')
            if student_plane.rect.centerx>=40:
                student_plane.rect.centerx -=8.5

        elif keys[pygame.K_d]:
            # 设置飞机状态图片
            student_plane.set_image('right')
            if student_plane.rect.centerx <= 478:
                student_plane.rect.centerx +=8.5

        elif keys[pygame.K_w]:
            #设置飞机状态图片
            student_plane.set_image('up')
            student_plane.set_air('up')

            if student_plane.rect.centery >= 45:
                student_plane.rect.centery -=8.5

        elif keys[pygame.K_s]:
            # 设置飞机状态图片
            student_plane.set_image('down')
            if student_plane.rect.centery <= 727:
                student_plane.rect.centery +=8.5

        # 显示飞机
        screen.blit(student_plane.image,student_plane.rect)
        if student_plane.air != None:
            screen.blit(student_plane.air, (student_plane.rect.centerx-30, student_plane.rect.centery+33))

        # 敌机 ---------------------------------------------------------------------------------------

        # 敌机移动
        # 控制时间节奏 sec变量
        sec +=1
        #随机控制生成敌机的节奏
        rhy = random.randint(ran1,ran2)
        # 敌机最多数量

        if sec%rhy ==0 and len(enemies) < max_enemies or sec ==1: # 设置敌机数量总数为9
            # 生成一只敌机
            enemy = Enemy(screen)
            enemy.rect.centerx=random.randint(0,512)
            # 生成上述敌机的子弹
            enemy_bullet = Enemy_Bullet((enemy.rect.centerx,enemy.rect.centery))
            # 敌机group 和 敌机子弹group加载敌机和子弹
            enemies.add(enemy)
            enemy_bullets.add(enemy_bullet)
        # 敌机出现 和 敌机子弹出现
        enemies.draw(screen)
        enemy_bullets.draw(screen)
        # 迭代敌机集合
        for enemy in enemies:
            # 让每个对象移动起来
            enemy.move()
            # 敌机超出屏幕边界后 自动删除敌机
            collision_over1 = pygame.sprite.collide_rect(student_plane, enemy)

            if collision_over1:
                # 为了重启游戏时 防止有旧子弹和飞机存在
                enemies.remove(enemy)
                game = 'over'
            if enemy.rect.bottom >768:
                enemies.remove(enemy)
        for enemy_bullet in enemy_bullets:
            # 让每个对象移动起来
            enemy_bullet.move()

            collision_over2 = pygame.sprite.collide_rect(student_plane, enemy_bullet)
            if collision_over2:
                # 为了重启游戏时 防止有旧子弹和飞机存在
                enemy_bullets.remove(enemy_bullet)
                game = 'over'
            # 敌机子弹超出屏幕边界后 自动删除敌机
            if enemy_bullet.rect.bottom >768:
                enemy_bullets.remove(enemy_bullet)


        #  -----------------------Boss --------------------------
        if score >=140:
            # 小敌机出现的节奏
            ran1,ran2 = 15,25
            max_enemies = 17
            screen.blit(boss.image,boss.rect)
            boss.move()
            for my_bullet in student_plane.bullets:
                hit_boss = pygame.sprite.collide_rect(boss,my_bullet)
                if hit_boss:
                    boss.blood -=1.2
                    score+=1
                if boss.blood <=0:
                    game = 'success'


        # 处理碰撞    ---------------------------碰撞检测--------------------------------------------------
        # 　　参数：
        # 　　group1：精灵组1。
        # 　　group2：精灵组2。
        # 　　dokill1：发生碰撞时，是否销毁精灵组1中的发生碰撞的精灵。
        # 　　dokill2：发生碰撞时，是否销毁精灵组2中的发生碰撞的精灵。
        collisions = pygame.sprite.groupcollide(student_plane.bullets, enemies, True, True)
        if collisions:
            score+=10

        # -----------游戏结束------------

        # 分数和奖励的显示-------------------------------------------------------------------------
        surface1 = my_font.render(u"当前得分：%s"%(score),True,[255,0,0])
        screen.blit(surface1,[20,20])

        # 更新画面
        pygame.display.flip()
        # 设置帧数和延迟
        time.sleep(0.05)

    #游戏结束状态
    elif game == 'over':
        score = 0
        # 最小游戏框架一个都不能省略
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # 检测鼠标是否按下 重新开始按钮
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 检测鼠标点击位置是否与重启rect重叠
                if restart_rect.collidepoint(event.pos):
                    student_plane.__init__(screen)
                    game = 'ing'

        # 游戏结束游戏画面暂停
        screen.blit(bg_img1, (0, pos_y1))
        screen.blit(bg_img2, (0, pos_y2))

        screen.blit(gameover_img, (163, 310))
        screen.blit(restart_img, restart_rect)
        # 测试尾焰位置
        # screen.blit(img, (100, 100))
        pos_y1 += 0
        pos_y2 += 0
        pygame.display.flip()
        time.sleep(0.05)
        # surface2 = my_font.render("Game Over" , True, [255, 0, 0])
        # screen.blit(surface1, [250, 350])
    elif game == 'success':
        score = 0
        boss.blood = 1000
        # 最小游戏框架一个都不能省略
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # 检测鼠标是否按下 重新开始按钮
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 检测鼠标点击位置是否与重启rect重叠
                if restart_rect.collidepoint(event.pos):
                    student_plane.__init__(screen)
                    game = 'ing'

        # 游戏结束游戏画面暂停
        screen.blit(bg_img1, (0, pos_y1))
        screen.blit(bg_img2, (0, pos_y2))

        screen.blit(gamesuccess, (170, 220))
        screen.blit(restart_img, restart_rect)
        # 测试尾焰位置
        # screen.blit(img, (100, 100))
        pos_y1 += 0
        pos_y2 += 0
        pygame.display.flip()
        time.sleep(0.05)
