# ynu-dns-consul

### What is it

This is the repository for storing configuration files and construction commands to build a auto-generated `bind9/named` configuration files system based on consul/consul-template/supervisor.

### How to use

1. Clone this repository

    ```
    git clone https://github.com/liudonghua123/ynu-dns-consul.git
    ```
    
2. Change your consul `datacenter`/`acl_token`/`ip` configurations in **`data/consul/config/agent.json`** and **`data/consul/config/dns.json`**

    Find your replacement using
    
    ```
    grep replace -r data
    ```
    
3. Copy data and configurations to /

    ```
    cp -r data /
    ```

4. Install consul and consul-template
    
    * Download the latest proper packages on [DOWNLOAD CONSUL][DOWNLOAD CONSUL] and  [DOWNLOAD CONSUL TOOLS][DOWNLOAD CONSUL TOOLS]
    * Unpack to `/usr/local/bin` or some other location in $PATH
    
5. Install supervisor according to your system
    
    * Debian/Ubuntu
        
        ```bash
        sudo apt-get install supervisor
        cp supervisord/* /etc/supervisor/conf.d/
        ```
        
    * Fedora/CentOS
        
        ```bash
        yum install python-setuptools
        sudo easy_install supervisor
        sudo mkdir /etc/supervisord.d/
        sudo cp supervisord/* /etc/supervisord.d/
        # cp supervisord.conf /etc/
        sudo echo_supervisord_conf > /etc/
        sudo vi /etc/supervisord.conf
        :
        [include]
        files = /etc/supervisord.d/*.conf
        :
        sudo cp supervisord /etc/init.d/
        sudo chmod +x /etc/init.d/supervisord
        sudo chkconfig --add supervisord
        sudo chkconfig supervisord on
        ```
        
6. Run consul and consul-template using supervisor

    ```
    # under debian/ubuntu
    service supervisor restart
    # under fedora/centos
    service supervisord restart
    ```   

### How to maintenance

Visit `consul web ui` and manage your dns record under `key/value` tab

### Project file structure

```
# tree
.
├── data
│   ├── consul
│   │   └── config
│   │       ├── agent.json
│   │       └── dns.json
│   └── consul-template
│       ├── config.hcl
│       └── dns.ct
├── README.md
├── supervisord
├── supervisord.conf
└── supervisord.d
    ├── consul.conf
    └── consul-template.conf
```

### License

Apache License 2.0

### Reference

1. [consul][consul]
2. [consul-template][consul-template]
3. [Setting Up Python and Supervisor on CentOS][Setting Up Python and Supervisor on CentOS]
4. [consulate][consulate]
5. [KEY/VALUE DATA][KEY/VALUE DATA]


[DOWNLOAD CONSUL]: https://www.consul.io/downloads.html
[DOWNLOAD CONSUL TOOLS]: https://www.consul.io/downloads_tools.html
[Setting Up Python and Supervisor on CentOS]: https://rayed.com/wordpress/?p=1496
[consul]: https://www.consul.io/
[consul-template]: https://github.com/hashicorp/consul-template
[consulate]: http://consulate.readthedocs.io/en/stable/index.html
[KEY/VALUE DATA]: https://www.consul.io/intro/getting-started/kv.html

