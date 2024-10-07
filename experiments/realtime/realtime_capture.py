from time import time
import cv2 as cv
import numpy as np
import mss

with mss.mss() as sct:
    while True:
        last_time = time()

        img = np.array(sct.grab(sct.monitors[1]))
        cv.imshow("Computer Vision", img)

        print(f"FPS: {1 / (time() - last_time)}")

        # Press "q" to quit
        if cv.waitKey(1) & 0xFF == ord("q"):
            cv.destroyAllWindows()
            break
