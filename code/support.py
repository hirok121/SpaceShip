import os

WIDTH ,HEIGHT = 800, 600
FPS = 60
assets = "assets/"

def check_assets():
        # check current directory if its has chid directory assets or it parent directory has assets
        if not os.path.isdir(assets):
            if os.path.isdir("../"+assets):
                return "../"+assets
                print("assets directory found in parent directory")
            else:
                print("assets directory not found")
        else:
            print("assets directory found in current directory")
        return None