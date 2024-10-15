import os
import cv2 as cv


# todo: turn this into a ResourceLoader + move this somewhere else
class ImageLoader:
    VISION_DIR = os.path.dirname(os.path.abspath(__file__))
    RESOURCES_DIR = VISION_DIR[0:VISION_DIR.find('/src/')] + '/resources'
    
    @staticmethod
    def read(path):
        return cv.imread(f'{ImageLoader.RESOURCES_DIR}/{path}', cv.IMREAD_UNCHANGED)


class Images:
    HEAL_OPTION = ImageLoader.read('menu/heal_option.png')
    YELLOW_MARKERS = [
        ImageLoader.read('label/marker/yellow/0.png'),
        ImageLoader.read('label/marker/yellow/1.png'),
        ImageLoader.read('label/marker/yellow/2.png'),
        ImageLoader.read('label/marker/yellow/3.png'),
        ImageLoader.read('label/marker/yellow/4.png'),
        ImageLoader.read('label/marker/yellow/5.png'),
        ImageLoader.read('label/marker/yellow/6.png'),
        ImageLoader.read('label/marker/yellow/7.png'),
        ImageLoader.read('label/marker/yellow/8.png'),
        ImageLoader.read('label/marker/yellow/9.png'),
    ]

    class Barrows:
        AVAILABLE_LABELS = dict(
            A=ImageLoader.read('label/barrows/available/A.png'),
            D=ImageLoader.read('label/barrows/available/D.png'),
            G=ImageLoader.read('label/barrows/available/G.png'),
            K=ImageLoader.read('label/barrows/available/K.png'),
            T=ImageLoader.read('label/barrows/available/T.png'),
            V=ImageLoader.read('label/barrows/available/V.png'),
        )
        UNAVAILABLE_LABELS = dict(
            A=ImageLoader.read('label/barrows/unavailable/A.png'),
            D=ImageLoader.read('label/barrows/unavailable/D.png'),
            G=ImageLoader.read('label/barrows/unavailable/G.png'),
            K=ImageLoader.read('label/barrows/unavailable/K.png'),
            T=ImageLoader.read('label/barrows/unavailable/T.png'),
            V=ImageLoader.read('label/barrows/unavailable/V.png'),
        )


class Food:
    MONKFISH = ImageLoader.read('item/food/monkfish.png')
    SHARK = ImageLoader.read('item/food/shark.png')
    MANTA_RAY = ImageLoader.read('item/food/manta_ray.png')


class Potion:
    class PotionDescriptor:
        def __init__(self, potion):
            self.doses = [
                None,
                ImageLoader.read(f'item/potion/{potion}/1.png'),
                ImageLoader.read(f'item/potion/{potion}/2.png'),
                ImageLoader.read(f'item/potion/{potion}/3.png'),
                ImageLoader.read(f'item/potion/{potion}/4.png'),
            ]
            self.status = ImageLoader.read(f'status/{potion}.png')

    ANTIFIRE = PotionDescriptor('antifire')


class Status:
    ATTACK = ImageLoader.read('status/attack.png')
    STRENGTH = ImageLoader.read('status/strength.png')
    DEFENSE = ImageLoader.read('status/defense.png')
    RANGED = ImageLoader.read('status/ranged.png')

    ANTI_VENOM = ImageLoader.read('status/anti_venom.png')
    ANTIFIRE = ImageLoader.read('status/antifire.png')

    GREATER_SKELETON = ImageLoader.read('status/greater_skeleton.png')


class PrayerProtect:
    MELEE = ImageLoader.read('prayer/melee.png')
    MAGIC = ImageLoader.read('prayer/magic.png')
    RANGED = ImageLoader.read('prayer/ranged.png')
