import os
import glob

videoFileall_path = os.path.join(os.getcwd(), f'/tmp/Videos')
names = [x for x in glob.glob(os.path.join(os.getcwd(), f"/tmp/Videos/*.mp4"))]

print(videoFileall_path)

# ###  Remove - pytest_cache cammand  ###
# Remove-Item .pytest_cache -Recurse -Force