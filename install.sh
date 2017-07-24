git clone https://github.com/shadowsocksr/shadowsocksr.git
cd shadowsocksr && ./initcfg.sh && mv user-config.json{,.bak} && cp ../user-config.json ./
cd .. && python monitor.py 8080 ./shadowsocksr/shadowsocks server.py
