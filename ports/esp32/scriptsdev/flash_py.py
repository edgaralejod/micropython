import os
arr = os.listdir('.')
print(arr)

for f in arr:
    if '.py' in f:
        print(f)
        os.system('ampy put ' + f)