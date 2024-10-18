#!/usr/bin/env python3

from roop import core

if __name__ == "__main__":
    # src_path = '/home/thinkdiff/Downloads/roop/testfunc/tar.jpg'
    # vid_path = '/home/thinkdiff/Downloads/roop/testfunc/neymar-game-football.mp4'
    # output = '/home/thinkdiff/Downloads/roop/testfunc/test1.mp4'
    for i in range(0, 5):
        src_path = "media_test/boy.jpg"
        vid_path = "media_test/girl_wedding.mp4"
        output = f"media_test/testt{i}.mp4"
        core.runvid(src_path, vid_path, output)
