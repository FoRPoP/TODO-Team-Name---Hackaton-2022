import pygame
import os
from pygame.locals import *

# Global Variables

global transparency_colorkey
transparency_colorkey = (255, 255, 255)

global animation_database           # image_id ----> copy of image
animation_database = {}

global animation_higher_database    # [entity_type][animation_id] ----> animation_order
animation_higher_database = {}

global particle_images              # particle_type (folder) ----> number of img
particle_images = {}

# Transperency

def set_global_colorkey (colorkey):

    global transparency_colorkey
    transparency_colorkey = colorkey
    
# Physics

def collision_test (test_obj, obj_list):        # returns a list of objects with which test_obj collided
    
    collision_list = []
    for obj in obj_list:
        if obj.colliderect(test_obj):
            collision_list.append(obj)
    
    return collision_list


class physics_obj (object):

    def __init__ (self, x, y, x_size, y_size):

        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = x
        self.y = y

    def move (self, movement_tuple, platforms):     # moves the object, returns types of collisions that occured

        collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False, 'data': []}

        self.x += movement_tuple[0]
        self.rect.x = int(self.x)

        collision_list = collision_test(self.rect, platforms)
        for collision in collision_list:
            markers = [False, False, False, False]  # right, left, bottom, top

            if movement_tuple[0] > 0:
                self.rect.right = collision.left
                collision_types['right'] = True
                markers[0] = True
            elif movement_tuple[0] < 0:
                self.rect.left = collision.right
                collision_types['left'] = True
                markers[1] = True
            
            collision_types['data'].append([collision, markers])
            self.x = self.rect.x

        self.y += movement_tuple[1]
        self.rect.y = int(self.y)

        collision_list = collision_test(self.rect, platforms)
        for collision in collision_list:
            markers = [False, False, False, False]  # right, left, bottom, top

            if movement_tuple[1] > 0:
                self.rect.bottom = collision.top
                collision_types['bottom'] = True
                markers[2] = True
            elif movement_tuple[1] < 0:
                self.rect.top = collision.bottom
                collision_types['top'] = True
                markers[3] = True
            
            collision_types['data'].append([collision, markers])
            self.change_y = 0
            self.y = self.rect.y

        return collision_types
        
# Entities

def make_entity (x, y, type):
    return entity(x, y, 1, 1, type)

def flip (img, flip_boolean = True):
    return pygame.transform.flip(img, flip_boolean, False)

def blit_center (surf1, surf2, pos):        # blits the center of surface2 to the position on the surface1

    x = int(surf2.get_width()/2)
    y = int(surf2.get_height()/2)
    surf1.blit(surf2, (pos[0] - x, pos[1] - y))

class entity (object):
    global animation_database, animation_higher_database

    def __init__ (self, x, y, x_size, y_size, entity_type):

        self.x = x
        self.y = y
        self.width = x_size
        self.height = y_size
        self.obj = physics_obj(x, y, x_size, y_size)
        self.image = None
        self.animation = None
        self.animation_frame = 0
        self.animation_tags = []
        self.flip = False
        self.offset = [0, 0]
        self.rotation = 0
        self.entity_type = entity_type
        self.action_timer = 0
        self.action = ''
        self.set_action('idle')

    def set_pos (self, x, y):

        self.x = x
        self.y = y
        self.obj.x = x
        self.obj.y = y
        self.obj.rect.x = x
        self.obj.rect.y = y

    def move (self, movement_tuple, platforms):

        collisions = self.obj.move(movement_tuple, platforms)
        self.x = self.obj.x
        self.y = self.obj.y

        return collisions

    def rect (self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def set_image (self, img):
        self.image = img

    def get_image (self):
        if self.animation == None:
            if self.image != None:
                return flip(self.image, self.flip)
            else:
                return None
        else:
            return flip(animation_database[self.animation[self.animation_frame]], self.flip)

    def set_animation (self, sequence):     # sequence is animation_order
        self.animation = sequence
        self.animation_frame = 0

    def set_frame (self, amount):
        self.animation_frame = amount

    def change_frame (self, amount):

        self.animation_frame += amount
        if self.animation != None:
            while self.animation_frame < 0:
                if 'loop' in self.animation_tags:
                    self.animation_frame += len(self.animation)
                else:
                    self.animation = 0
            while self.animation_frame >= len(self.animation):
                if 'loop' in self.animation_tags:
                    self.animation_frame -= len(self.animation)
                else:
                    self.animation_frame = len(self.animation) - 1

    def handle(self):
        self.action_timer += 1
        self.change_frame(1)

    def set_animation_tags (self, tags):
        self.animation_tags = tags

    def clear_animation (self):
        self.animation = None

    def set_flip(self, flip_boolean):
        self.flip = flip_boolean

    def set_offset (self, offset):
        self.offset = offset

    def set_action (self, action_id, force = False):
        
        if (self.action == action_id) and (force == False):
            pass
        else:
            self.action = action_id
            animation = animation_higher_database[self.entity_type][action_id]
            self.animation = animation[0]
            self.set_animation_tags(animation[1])
            self.animation_frame = 0

    def get_center (self):
        x = self.x + int(self.width / 2)
        y = self.y + int(self.height / 2)

        return [x, y]

    def display (self, surface, scroll):

        render_image = None
        if self.animation == None:
            if self.image != None:
                render_image = flip(self.image, self.flip).copy()
        else:
            render_image = flip(animation_database[self.animation[self.animation_frame]], self.flip).copy()
        if render_image != None:
            center_x = render_image.get_width() / 2
            center_y = render_image.get_height() / 2
            render_image = pygame.transform.rotate(render_image, self.rotation)
            
            blit_center(surface, render_image, (int(self.x) - scroll[0] + self.offset[0] + center_x, int(self.y) - scroll[1] + self.offset[1] + center_y))


# Animations

# sequence ----> [[image_name (as int), duration of image in animation (as int)] .... []]
def animation_sequence (seq, path, colorkey = (255, 255, 255), transparency = 255):     # returns animation's images order and repetitions

    global animation_database
    result = []

    for frame in seq:
        image_id = path + path.split('/')[-2] + '_' + str(frame[0])
        image = pygame.image.load(image_id + '.png').convert()
        image.set_colorkey(colorkey)
        image.set_alpha(transparency)
        animation_database[image_id] = image.copy()
        for i in range (frame[1]):
            result.append(image_id)

    return result
    
def get_frame (animation_id):
    global animation_database
    return animation_database[animation_id]

def load_animations (path):

    global animation_higher_database, transparency_colorkey

    f = open(path + 'entity_animations.txt', 'r')
    data = f.read()
    f.close()

    for animation in data.split('\n'):
        sections = animation.split(' ')
        animation_path = sections[0]
        entity_info = animation_path.split('/')
        entity_type = entity_info[0]
        animation_id = entity_info[1]
        timings = sections[1].split(';')
        tags = sections[2].split(';')

        seq = []
        n = 0
        for timing in timings:
            seq.append([n, int(timing)])
            n += 1

        animation_order = animation_sequence(seq, path + animation_path, transparency_colorkey)
        if entity_type not in animation_higher_database:
            animation_higher_database[entity_type] = {}
        animation_higher_database[entity_type][animation_id] = [animation_order.copy(), tags]


# Particles

def particle_file_sort (list):
    list1 = []
    for object in list:
        list1.append((object[:-4]))
    list1.sort()

    list_final = []
    for object in list1:
        list_final.append(str(object) + '.png')
    
    return list_final

def load_particle_images (path):

    global particle_images, transparency_colorkey
    
    file_list = os.listdir(path)
    for folder in file_list:
        try:
            img_list = os.listdir(path + '/' + folder)
            img_list = particle_file_sort(img_list)
            images = []
            for img in img_list:
                images.append(pygame.image.load(path + '/' + folder + '/' + img).convert())
            for img in images:
                img.set_colorkey(transparency_colorkey)
            particle_images[folder] = images.copy()
        except:
            pass
        
class particle (object):

    def __init__ (self, x, y, particle_type, movement_tuple, decay_rate, start_frame, custom_color = None):

        self.x = x
        self.y = y
        self.particle_type = particle_type
        self.movement_tuple = movement_tuple
        self.decay_rate = decay_rate
        self.frame = start_frame
        self.color = custom_color

    def draw (self, surface, scroll):

        global particle_images

        if self.frame > len(particle_images[self.particle_type]) - 1:
            self.frame = len(particle_images[self.particle_type]) - 1
        if self.color == None:
            blit_center(surface, particle_images[self.particle_type][int(self.frame)], (self.x - scroll[0], self.y - scroll[1]))
        else:
            blit_center(surface,swap_color(particle_images[self.particle_type][int(self.frame)],(255,255,255),self.color),(self.x-scroll[0],self.y-scroll[1]))

    def update (self):

        self.frame += self.decay_rate
        running = True
        if self.frame > len(particle_images[self.particle_type]) - 1:
            running = False
        self.x += self.movement_tuple[0]
        self.y += self.movement_tuple[1]

        return running

# Other function

def swap_color (img, old_color, new_color):

    global transparency_colorkey

    img.set_colorkey(old_color)
    surf = img.copy()
    surf.fill(new_color)
    surf.blit(img, (0, 0))
    surf.set_colorkey(transparency_colorkey)

    return surf

