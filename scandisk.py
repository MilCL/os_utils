def du(path):
            """disk usage in human readable format (e.g. '2,1GB')"""
            return subprocess.check_output(['du','-ahx', '--max-depth=2', path ]).decode('utf-8')
        


def scan_disk() :
            #Scanning memory usage
            print('Scanning disk...')
            print('du scanning')
            print(du('/'))

            print('os listdir')
            dirs = os.listdir('.')
            memory_usage = [ f'({dir_}, {os.path.getsize(dir_)/1000000} Mo )' for dir_ in dirs]
            print('memroy usage =', memory_usage)

            dirs = [dir_ for dir_ in dirs if os.path.isdir(dir_)]
            for dir_ in dirs :
                memory_folder = [ f'({file}, {os.path.getsize(f"{dir_}/{file}")/1000000} Mo )' for file in os.listdir(f'./{dir_}')]
                print('\n', dir_, ' -->',  memory_folder)

            print('total memory scanning')
            total, used, free = shutil.disk_usage("/")

            print("Total: %d GiB" % (total // (2**30)))
            print("Used: %d GiB" % (used // (2**30)))
            print("Free: %d GiB" % (free // (2**30)))

            print('Scanning ends')   
            return

        scan_disk()