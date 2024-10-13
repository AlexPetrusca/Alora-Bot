import cv2 as cv


class Images:
    HEAL_OPTION = cv.imread('../resources/menu/heal_option.png', cv.IMREAD_UNCHANGED)
    YELLOW_MARKERS = [
        cv.imread('../resources/label/marker/yellow/0.png', cv.IMREAD_UNCHANGED),
        cv.imread('../resources/label/marker/yellow/1.png', cv.IMREAD_UNCHANGED),
        cv.imread('../resources/label/marker/yellow/2.png', cv.IMREAD_UNCHANGED),
        cv.imread('../resources/label/marker/yellow/3.png', cv.IMREAD_UNCHANGED),
        cv.imread('../resources/label/marker/yellow/4.png', cv.IMREAD_UNCHANGED),
        cv.imread('../resources/label/marker/yellow/5.png', cv.IMREAD_UNCHANGED),
        cv.imread('../resources/label/marker/yellow/6.png', cv.IMREAD_UNCHANGED),
        cv.imread('../resources/label/marker/yellow/7.png', cv.IMREAD_UNCHANGED),
        cv.imread('../resources/label/marker/yellow/8.png', cv.IMREAD_UNCHANGED),
        cv.imread('../resources/label/marker/yellow/9.png', cv.IMREAD_UNCHANGED),
    ]

    class Barrows:
        AVAILABLE_LABELS = dict(
            A=cv.imread(f"../resources/label/barrows/available/A.png", cv.IMREAD_UNCHANGED),
            D=cv.imread(f"../resources/label/barrows/available/D.png", cv.IMREAD_UNCHANGED),
            G=cv.imread(f"../resources/label/barrows/available/G.png", cv.IMREAD_UNCHANGED),
            K=cv.imread(f"../resources/label/barrows/available/K.png", cv.IMREAD_UNCHANGED),
            T=cv.imread(f"../resources/label/barrows/available/T.png", cv.IMREAD_UNCHANGED),
            V=cv.imread(f"../resources/label/barrows/available/V.png", cv.IMREAD_UNCHANGED)
        )
        UNAVAILABLE_LABELS = dict(
            A=cv.imread(f"../resources/label/barrows/unavailable/A.png", cv.IMREAD_UNCHANGED),
            D=cv.imread(f"../resources/label/barrows/unavailable/D.png", cv.IMREAD_UNCHANGED),
            G=cv.imread(f"../resources/label/barrows/unavailable/G.png", cv.IMREAD_UNCHANGED),
            K=cv.imread(f"../resources/label/barrows/unavailable/K.png", cv.IMREAD_UNCHANGED),
            T=cv.imread(f"../resources/label/barrows/unavailable/T.png", cv.IMREAD_UNCHANGED),
            V=cv.imread(f"../resources/label/barrows/unavailable/V.png", cv.IMREAD_UNCHANGED)
        )


class Food:
    MONKFISH = cv.imread('../resources/item/food/monkfish.png', cv.IMREAD_UNCHANGED)
    SHARK = cv.imread('../resources/item/food/shark.png', cv.IMREAD_UNCHANGED)
    MANTA_RAY = cv.imread('../resources/item/food/manta_ray.png', cv.IMREAD_UNCHANGED)


class Potions:
    class Potion:
        def __init__(self, potion):
            self.doses = [
                None,
                cv.imread(f"../resources/item/potion/{potion}/1.png", cv.IMREAD_UNCHANGED),
                cv.imread(f"../resources/item/potion/{potion}/2.png", cv.IMREAD_UNCHANGED),
                cv.imread(f"../resources/item/potion/{potion}/3.png", cv.IMREAD_UNCHANGED),
                cv.imread(f"../resources/item/potion/{potion}/4.png", cv.IMREAD_UNCHANGED),
            ]
            self.status = cv.imread(f"../resources/status/{potion}.png", cv.IMREAD_UNCHANGED)

    ANTIFIRE = Potion("antifire", )


class Status:
    cv.imread(f"../resources/status/attack.png", cv.IMREAD_UNCHANGED),
    cv.imread(f"../resources/status/strength.png", cv.IMREAD_UNCHANGED),
    cv.imread(f"../resources/status/defense.png", cv.IMREAD_UNCHANGED),
    cv.imread(f"../resources/status/ranged.png", cv.IMREAD_UNCHANGED),

    cv.imread(f"../resources/status/anti_venom.png", cv.IMREAD_UNCHANGED),
    cv.imread(f"../resources/status/antifire.png", cv.IMREAD_UNCHANGED),

    cv.imread(f"../resources/status/antifire.png", cv.IMREAD_UNCHANGED),
