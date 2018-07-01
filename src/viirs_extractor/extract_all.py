import os
import tarfile

archives_dir = '../../data/lightrasters_noaa/monthly/'

archnames = os.listdir(archives_dir)

print('fetched list of files to extract')

for archname in archnames:
    if archname.endswith('.tgz') and archname + '.part' not in archnames:
        success = False
        with tarfile.open(archives_dir + archname, "r") as tar:
            for member in tar.getmembers():
                filename = os.path.basename(member.name)
                if filename.endswith("avg_rade9h.tif") or filename.find('orm_') is not -1:
                    tar.extract(member, archives_dir)
                    print('extracted : ' + filename)
                    success = True
                    break
        if success:
            os.remove(archives_dir + archname)
        else:
            print('failed to locate [...]avg_rade9h.tif or [...]orm_[...] in archive ' + archname)

print('done !')
