import os
#|-----------------------------------------------------|
#| HallinbircH ESRGAN_Helper LOW RAM BATCH MODE LOOPER |
#|-----------------------------------------------------|
# restarts Li_ESRGAN_Helper every time it crashes until it completes
# intended for fixing the Memory Errors in large numbers of images (around 1500 for me)
while (1 + 1) != 3:
    if os.path.exists('./Done.xao') != True:
        os.system('python3 Li_ESRGAN_Helper.py')
    else:
        print('THE SCRIPT HAS COMPLETED CORRECTLY')
        input()
        os.remove("./Done.xao")
        os.remove("./JoinAlready.xao")
        os.remove("./SlicedAlready.xao")
        break
