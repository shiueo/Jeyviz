import natsort

files = list(map(int, natsort.natsorted(
        []
    )))
print(files, max(files))