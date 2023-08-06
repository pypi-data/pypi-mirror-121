from urllib.request import urlretrieve

import requests
import os
import sys
from functools import wraps


def get_file(fname,
             origin,
             cache_dir=None):
    base_dir, fname = os.path.split(fname)

    if cache_dir is None:
        if 'DEEP_UTILS_HOME' in os.environ:
            cache_dir = os.environ.get('DEEP_UTILS_HOME')
        else:
            cache_dir = os.path.join(os.path.expanduser('~'), '.deep_utils')

    datadir_base = os.path.expanduser(cache_dir)
    datadir = os.path.join(datadir_base, base_dir)
    os.makedirs(datadir, exist_ok=True)

    fpath = os.path.join(datadir, fname)
    if fpath.endswith(".zip"):
        check_path = fpath[:-4]
    else:
        check_path = fpath
    download = False if os.path.exists(check_path) else True

    if download:
        print('Downloading data from', origin)
        error_msg = 'URL fetch failure on {}'
        try:
            with open(fpath, 'wb') as f:
                response = requests.get(origin, stream=True)
                total = response.headers.get('content-length')

                if total is None:
                    f.write(response.content)
                else:
                    downloaded = 0
                    total = int(total)
                    for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                        downloaded += len(data)
                        f.write(data)
                        done = int(50 * downloaded / total)
                        sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                        sys.stdout.flush()
            sys.stdout.write('\n')
        except (Exception, KeyboardInterrupt):
            if os.path.exists(fpath):
                os.remove(fpath)
            raise Exception(error_msg.format(origin))
        if fpath.endswith(".zip"):
            from zipfile import ZipFile
            try:
                with ZipFile(fpath, 'r') as zip:
                    zip.printdir()
                    print(f'extracting {fpath}')
                    zip.extractall(fpath[:-4])
                    print(f'extracting is done!')
                os.remove(fpath)
            except (Exception, KeyboardInterrupt):
                raise Exception(f"Error in extracting {fpath}")
    if fpath.endswith('.zip'):
        fpath = fpath[:-4]
    return fpath


from tqdm import tqdm


def get_new_file(fname,
                 url,
                 cache_dir=None):
    base_dir, fname = os.path.split(fname)

    if cache_dir is None:
        if 'DEEP_UTILS_HOME' in os.environ:
            cache_dir = os.environ.get('DEEP_UTILS_HOME')
        else:
            cache_dir = os.path.join(os.path.expanduser('~'), '.deep_utils')

    datadir_base = os.path.expanduser(cache_dir)
    datadir = os.path.join(datadir_base, base_dir)
    os.makedirs(datadir, exist_ok=True)

    fpath = os.path.join(datadir, fname)
    if fpath.endswith(".zip"):
        check_path = fpath[:-4]
    else:
        check_path = fpath
    download = False if os.path.exists(check_path) else True

    if download:
        print('Downloading data from', url)
        error_msg = 'URL fetch failure on {}'

        class Download:
            bar = None

            @staticmethod
            def download(count, block_size, total_size):
                if Download.bar is None:
                    Download.bar = tqdm(total=total_size, desc=f"Downloading: ")
                else:
                    Download.bar.update(count * block_size)
        try:
            urlretrieve(url, fpath, Download.download)
        except (Exception, KeyboardInterrupt):
            if os.path.exists(fpath):
                os.remove(fpath)
            raise Exception(error_msg.format(url))

        if fpath.endswith(".zip"):
            from zipfile import ZipFile
            try:
                with ZipFile(fpath, 'r') as zip:
                    zip.printdir()
                    print(f'extracting {fpath}')
                    zip.extractall(fpath[:-4])
                    print(f'extracting is done!')
                os.remove(fpath)
            except (Exception, KeyboardInterrupt):
                raise Exception(f"Error in extracting {fpath}")
    if fpath.endswith('.zip'):
        fpath = fpath[:-4]
    return fpath


def download_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        config = self.config
        download_variables = self.download_variables
        for var in download_variables:
            if getattr(config, var) is None:
                url = getattr(config, var + '_url')
                f_name = getattr(config, var + '_cache')
                f_path = get_file(f_name, url)
                setattr(config, var, f_path)
        return func(self, *args, **kwargs)

    return wrapper


if __name__ == '__main__':
    url = 'https://github.com/Practical-AI/deep_utils/releases/download/0.2.0/RBF.zip'
    pa = get_new_file("RBF.zip", url, )
    print(pa)
    from tensorflow.keras.models import load_model

    model = load_model(pa)
    print(model.summary())
