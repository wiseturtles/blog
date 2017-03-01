Title: create restricted linux user for ssh tunnel
Date: 2017-03-01 11:30
Tags: Linux, SSH, tunnel
Slug: create-restricted-linux-user-for-ssh-tunnel
Author: ox0spy
Summary: Linux中创建一个受限的用户，专门做ssh tunnel

由于国内访问一些网站特别慢，所以，使用一台新加坡节点的机器做代理，提高浏览器、mobile访问网站速度。

最近发现访问AWS的EC2也特别慢，所以，希望通过该代理加速SSH连接速度，`ProxyCommand ssh -q -W %h:%p proxy`这行加入希望访问的主机`~/.ssh/config`中即可。

但，如果团队成员也有此需求，但又不想让团队成员有`ssh`登陆代理主机的权限，那么就继续往下看。

## 在代理主机上配置受限用户、sshd及团队成员的ssh公钥

### 创建用户

    $ sudo addgroup proxy
    $ sudo useradd -m -s /usr/sbin/nologin -g proxy proxy

注: 只创建用户而不为用户生成密码；ssh应该配置成只能通过`ssh key`认证

### 修改sshd config

修改 `/etc/ssh/sshd_config` 配置

    PermitRootLogin no
    PasswordAuthentication no
    PermitEmptyPasswords no
    Match User proxy
      AllowTcpForwarding yes
      X11Forwarding yes
      PermitTunnel yes
      AllowAgentForwarding yes

### 修改 ~proxy/.ssh/authorized_keys，配置团队成员ssh公钥

将需要使用该代理主机做ssh加速的用户 `ssh public key` 加入 `~proxy/.ssh/authorized_keys`

## 本机ssh config配置

添加代理主机信息并使用代理主机加速AWS主机ssh访问。

修改 `~/.ssh/config`，添加代理主机信息：

    Host proxy
        Hostname 1.2.3.4  # 填写自己的代理主机IP
        User proxy        # 修改为在代理主机上创建的用户名
        Port 22           # 修改为自己代理主机的ssh监听端口
        IdentityFile ~/.ssh/id_rsa  # 修改为添加到代理主机上的ssh public key对应的ssh private key

修改 `~/.ssh/config`，让AWS主机通过代理主机中转，提高访问速度。

    Host aws-host
        Hostname 1.2.3.4  # 填写自己的aws ec2主机IP
        User ec2-user     # 修改为在代理主机上创建的用户名
        Port 22           # 修改为自己代理主机的ssh监听端口
        IdentityFile ~/.ssh/id_rsa  # 修改为添加到aws ec2主机上的ssh public key对应的ssh private key
        ProxyCommand ssh -q -W %h:%p proxy  # 这句话的意思就是通过代理主机做中转，然后访问aws ec2

注：配置和之前类似，只是多了一条 `ProxyCommand`

## 验证

登陆代理主机：

    $ ssh proxy
    This account is currently not available.

    注：
    1. 因为代理主机上的`proxy`用户使用`/usr/sbin/nologin`做shell，所以会有这样的提示。
    2. 这句话标明`ssh key`认证成功。

登陆`aws-host`：

    $ ssh aws-host

    注: 应该可以正常登陆并明显感觉访问速度更快。
