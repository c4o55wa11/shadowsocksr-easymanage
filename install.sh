ssr_path='./shadowsocksr'
if [ ! -d "$ssr_path"]; then
    echo '[+] clone SSR project.'
    git clone https://github.com/shadowsocksr/shadowsocksr.git
    echo '[+] init configure files.'
    cd shadowsocksr && ./initcfg.sh 
    echo '[+] backup old configure file.'
    mv user-config.json{,.bak}
    echo '[+] replace configure file.'
    cp ../user-config.json ./
    echo '[+] start ssr service and ssr monitor service.'
    cd .. && python monitor.py 8080 ./shadowsocksr/shadowsocks server.py
    echo '[+] install finished.Have a good day!'
else
    echo '[-]ShadowsocksR project already exists.'
    echo "[-]If you still want to install or reinstall SSR, pleaser run 'rm -rf ./shadowsocksr' first."
fi
