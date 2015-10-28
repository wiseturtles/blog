Ubuntu上手动安装JDK
###################
:date: 2013-11-03 19:09
:tags: ubuntu, jdk
:slug: install-jdk
:author: crazygit
:summary: install jdk
:description: install jdk

Ubuntu上面自己手动安装JDK的方法如下:
首先下载jdk-7u45-linux-i586.tar.gz压缩包，并解压到 :code:`/usr/local/lib/jdk1.7.0_45` , 再执行下面的脚本

.. code-block:: bash

    #!/bin/bash
    JDK_BIN_PATH=/usr/local/lib/jdk1.7.0_45/bin
    for x in $(find $JDK_BIN_PATH)
    do
        name=$(basename $x)
        sudo update-alternatives --install /usr/bin/$name $name $x 300
    done
