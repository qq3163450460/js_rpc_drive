# js_rpc_drive
js逆向通杀免补环境工具

def run():
    data = {
        '1_str': 'params',
        '2_str': 'data',
        '3_str': 'ua'
    }
    # 传输类型 str dict int float
    url = 'http://127.0.0.1:8082/eval_js/get_a_b'
    res = requests.get(url=url, params=data).json()
    print(res.url)
    print(res.text)
示例
