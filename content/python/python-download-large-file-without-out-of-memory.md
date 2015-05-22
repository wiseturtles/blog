Title: Python下载大文件
Date: 2015-05-22
Category: Python
Tags: Python, OOM
Slug: python-download-large-file-without-out-of-memory
Authors: Zhang Wanming
Summary: Python下载大文件

requests
----------

    :::python

    def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename



urllib2
---------

    :::python
    file = urllib2.urlopen('url')
    with open('filename','w') as f:
        while True:
            tmp = file.read(1024)
            if not tmp:
                break 
            f.write(tmp)

详见:

1. http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
2. http://stackoverflow.com/questions/27053028/how-to-download-large-file-without-memoryerror-in-python
