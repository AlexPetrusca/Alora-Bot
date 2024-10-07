import cv2 as cv


class Images:
    MONKFISH = cv.imread('../resources/item/monkfish.png', cv.IMREAD_UNCHANGED)
    SHARK = cv.imread('../resources/item/shark.png', cv.IMREAD_UNCHANGED)
    MANTA_RAY = cv.imread('../resources/item/manta_ray.png', cv.IMREAD_UNCHANGED)

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
