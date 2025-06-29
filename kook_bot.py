import os
import json
import time
import zlib
import requests
import threading
import websocket
import difflib

TOKEN = '1/MzQyODc=/w3wyFI7IrGImypTYs6cEUw=='
GATEWAY_API = 'https://www.kookapp.cn/api/v3/gateway'
API_BASE = 'https://www.kookapp.cn/api/v3'

CHANNEL_QUERY_MAP = '2789866606081599'
CHANNEL_QUERY_SERVER = '3052143113725118'
CHANNEL_QUERY_RATES = '7307201985294513'
CHANNEL_QUERY_HATCH = '8616469274729516'

LOCAL_IMAGE_ROOT = '/home/bobo/kook/123'
TRANSLATION_FILE = os.path.join(LOCAL_IMAGE_ROOT, 'resource_translations.json')

with open(TRANSLATION_FILE, encoding='utf-8') as f:
    raw_json = json.load(f)

full_dict = raw_json.get("_maps", {})
map_keys = [
    "孤岛", "焦土", "中心岛", "仙境", "灭绝", "畸变", "繁星",
    "创世纪", "创世纪2", "失落之岛", "水晶群岛", "方舟港湾", "泰坦地图",
    "The Island", "ScorchedEarth", "TheCenter", "Ragnarok", "Extinction",
    "Aberration", "Astraeosr", "Genesis", "Genesis2", "Lost Island",
    "Crystal Isles", "The Gateway", "Titan"
]

map_dict = {k: full_dict[k] for k in map_keys if k in full_dict}
resource_dict = {k: v for k, v in full_dict.items() if k not in map_keys}

print("🔍 加载地图翻译数：", len(map_dict))
print("🔍 加载资源翻译数：", len(resource_dict))
print("🪪 示例 '南巨' 映射：", resource_dict.get("南巨"))
print("🪪 示例 '霸王龙' 映射：", resource_dict.get("霸王龙"))

def fuzzy_match(query, options, cutoff=0.6):
    result = difflib.get_close_matches(query, options, n=1, cutoff=cutoff)
    return result[0] if result else None

def send_message(channel_id, content):
    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}
    payload = {"type": 1, "target_id": channel_id, "content": content}
    requests.post(f"{API_BASE}/message/create", headers=headers, json=payload)

def upload_image_to_kook(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()

    headers = {"Authorization": f"Bot {TOKEN}"}
    files = {'file': (os.path.basename(file_path), file_data, 'image/png')}

    print("📄 正在上传图片...", file_path)
    resp = requests.post(f"{API_BASE}/asset/create", headers=headers, files=files)
    try:
        res = resp.json()
    except:
        raise Exception(f"响应异常：{resp.status_code}, {resp.text}")
    print("📟 上传返回：", res)

    if res.get("code") != 0:
        raise Exception(f"上传失败：{res}")
    
    # 使用返回的 URL
    image_url = res["data"].get("url")
    if not image_url:
        raise Exception(f"返回 URL 异常：{res}")
    return image_url

def send_image_to_channel(channel_id, image_url):
    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

    # 直接将图片的 URL 发送到 content 字段
    payload = {
        "type": 2,  # 图片消息类型
        "target_id": channel_id,
        "content": image_url  # 直接发送图片的 URL
    }

    print("📨 正在发送图片消息：", payload)
    resp = requests.post(f"{API_BASE}/message/create", headers=headers, json=payload)
    print("📨 KOOK 响应：", resp.status_code, resp.text)

def handle_map_image_message(content, channel_id):
    parts = content.strip().split()
    if len(parts) != 2:
        send_message(channel_id, "❗ 格式错误，应为：`地图名 资源名`（如：仙境 水晶）")
        return

    map_key, res_key = parts

    real_map = map_dict.get(map_key) or fuzzy_match(map_key, map_dict.keys())
    real_res = resource_dict.get(res_key) or fuzzy_match(res_key, resource_dict.keys())

    print(f"📥 地图匹配 [{map_key}] ➔ {real_map}")
    print(f"📥 资源匹配 [{res_key}] ➔ {real_res}")

    if not real_map:
        send_message(channel_id, f"❌ 未识别地图名：{map_key}")
        return
    if not real_res:
        send_message(channel_id, f"❌ 未识别资源名：{res_key}")
        return

    file_path = os.path.join(LOCAL_IMAGE_ROOT, real_map, f"{real_res}.png")

    if not os.path.isfile(file_path):
        send_message(channel_id, f"❌ 找不到图片文件：{file_path}")
        return

    try:
        image_url = upload_image_to_kook(file_path)
        print(f"🖼️ 图片上传成功：{image_url}")
        send_image_to_channel(channel_id, image_url)
    except Exception as e:
        send_message(channel_id, f"❌ 图片上传失败：{e}")

# 查询服务器信息
def handle_server_query(content, channel_id):
    if not content.isdigit():
        send_message(channel_id, "❗ 格式错误，应为：服务器编号（纯数字）")
        return
    try:
        resp = requests.get(f'http://80.251.208.216:5000/{content}', timeout=8)
        data = resp.json()
        if 'error' in data:
            send_message(channel_id, f'❌ {data["error"]}')
        else:
            rates = "\n".join([f"- {k}：{v}" for k, v in data['倍率信息'].items()])
            send_message(channel_id,
                f"🌐 **{data['服务器名称']}**\n"
                f"🗺️ 地图：{data['地图']}\n"
                f"🔗 地址：{data['地址']}\n"
                f"📶 状态：{data['在线状态']}\n"
                f"👥 人数：{data['服务器人数']} / {data['最大人数']}\n"
                f"📌 类型：{data['服务器类型']}\n"
                f"📈 倍率信息：\n{rates}")
    except Exception as e:
        send_message(channel_id, f'❌ 查询失败：{e}')

# 查询倍率信息
def handle_rates_query(channel_id):
    try:
        resp = requests.get('http://80.251.208.216:5000/rates', timeout=8)
        data = resp.json()
        text = ""
        for k, v in data.items():
            text += f"📘 **{k}**\n" + "\n".join([f"- {key}：{val}" for key, val in v.items()]) + "\n\n"
        send_message(channel_id, text.strip())
    except Exception as e:
        send_message(channel_id, f"❌ 获取倍率失败：{e}")

# 孵化计算
def handle_hatch_query(content, channel_id):
    parts = content.strip().split()
    if len(parts) != 4:
        send_message(channel_id, "❗ 格式错误，应为：`恐龙 食物 倍率 当前进度`（如：Ankylosaurus 700 1 0.2）")
        return
    dino, food, rate, progress = parts
    try:
        url = f"http://45.159.51.27:8000/{dino}/{food}/{rate}/{progress}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if 'error' in data:
            send_message(channel_id, f"❌ {data['error']}")
        else:
            result = "\n".join([f"- {k}：{v}" for k, v in data.items()])
            send_message(channel_id, f"🦖 孵化结果：\n{result}")
    except Exception as e:
        send_message(channel_id, f"❌ 孵化计算失败：{e}")

def handle_message(content, channel_id, msg_id):
    global last_messages
    if last_messages.get(channel_id) == msg_id:
        return
    last_messages[channel_id] = msg_id

    content = content.strip()
    if channel_id == CHANNEL_QUERY_MAP:
        handle_map_image_message(content, channel_id)
    elif channel_id == CHANNEL_QUERY_SERVER:
        handle_server_query(content, channel_id)
    elif channel_id == CHANNEL_QUERY_RATES and '倍率' in content:
        handle_rates_query(channel_id)
    elif channel_id == CHANNEL_QUERY_HATCH:
        handle_hatch_query(content, channel_id)

last_messages = {}

def on_message(ws, message):
    try:
        msg = json.loads(zlib.decompress(message).decode()) if isinstance(message, bytes) else json.loads(message)
        if msg.get("s") == 0 and msg["d"].get("type") == 9:
            if msg["d"].get("extra", {}).get("author", {}).get("bot"):
                return
            handle_message(
                msg["d"].get("content", ""),
                msg["d"].get("target_id", ""),
                msg["d"].get("msg_id", "")
            )
        elif msg.get("s") == 1:
            ws.send(json.dumps({"s": 3}))
        elif msg.get("s") == 0 and "hello" in str(message):
            ws.send(json.dumps({
                "s": 2,
                "d": {
                    "token": TOKEN,
                    "intents": 1024,
                    "properties": {"$os": "linux", "$browser": "python", "$device": "python"}
                }
            }))
    except Exception as e:
        print("💥 消息处理错误：", e)

def on_open(ws): print("✅ WebSocket 已连接")
def on_close(ws, code, msg): print("❌ WebSocket 断开", code, msg)
def on_error(ws, err): print("❗ WebSocket 错误：", err)

def run():
    def connect():
        while True:
            try:
                url = requests.get(GATEWAY_API, headers={"Authorization": f"Bot {TOKEN}"}).json()['data']['url']
                ws = websocket.WebSocketApp(url,
                                            on_message=on_message,
                                            on_open=on_open,
                                            on_close=on_close,
                                            on_error=on_error)
                ws.run_forever()
            except Exception as e:
                print("⚠️ 尝试重连", e)
                time.sleep(5)
    threading.Thread(target=connect, daemon=True).start()
    while True:
        time.sleep(30)

if __name__ == '__main__':
    print("🚀 KOOK Bot 启动中...")
    run()
