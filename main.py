import asyncio
import os
import sys
import time

from datetime import datetime


"""

import cv2

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    print(ret)
    cv2.imshow("imagetest", frame)
    k = cv2.waitKey(1)
    if k != -1:
        break

cv2.imwrite("imagetest.jpg", frame)
cam.release()
cv2.destroyAllWindows()

"""


"""

sudo apt install fswebcam

fswebcam -r 1280x720 --no-banner --device /dev/video0 --skip 8 --frames 8 image.jpg

"""

debug = 1

async def takePicture(dev: str, output: str) -> bool:
    proc = await asyncio.create_subprocess_exec(
        "fswebcam",
        "-r", "1280x720",
        "--no-banner",
        "--device", dev,
        "--skip", "8",
        "--frames", "8",
        output,
        stderr=asyncio.subprocess.PIPE)
    await proc.wait()
    data = await proc.stderr.read()
    s = data.find(b"Writing JPEG image to") != -1
    if debug and not s:
        exit(data.decode())
    return s


async def test():
    s = await takePicture("v4l2:/dev/video0", "image.jpg")
    print(s)


def max(a, b) -> int:
    if a > b:
        return a
    return b


def dateUtc() -> str:
    return datetime.utcnow().strftime(r"%Y%m%d_%H%M%S")


async def main():

    if len(sys.argv) < 2:
        print(
            "usage: python3 main.py <interval_sec:int> <path:string>\n\n"
            "example: python3 main.py 5 /tmp\n"
        )
        return

    interval = max(int(sys.argv[1]), 5)
    path = sys.argv[2]

    print()
    print("interval(s) :", interval)
    print("path        :", path)
    print()

    while 1:
        t = time.time()
        output = os.path.join(path, dateUtc()) + ".jpg"
        print("save :", output)

        s = await takePicture("v4l2:/dev/video0", output)
        if not s:
            return

        duration = time.time() - t
        await asyncio.sleep(interval - duration)


if __name__ == "__main__":
    asyncio.run(main())
