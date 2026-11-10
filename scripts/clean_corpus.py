# -*- coding: utf-8 -*-
"""清洗 Moect 微信导出语料：解析消息、过滤占位符、产出不语的纯文本语料与基础统计"""
import re, json, collections, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = r"C:\Users\ASUS\.workbuddy\skills\buyu-perspective\references\sources\transcripts\不语_39e7122e.txt"
OUT_DIR = r"C:\Users\ASUS\.workbuddy\skills\buyu-perspective\references\sources"

msg_re = re.compile(r'^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (.+)$')
SKIP_BODY = "已按导出设置跳过"
placeholder_tags = re.compile(r'^\[(图片|动画表情|音视频通话|语音|视频号|链接|文件|转账|红包|位置|音乐|小程序|合并聊天记录|拍一拍|视频)\]$')

msgs = []  # (datetime, speaker, text)
cur_ts, cur_sp, cur_lines = None, None, []
header_done = False

def flush():
    global cur_ts, cur_sp, cur_lines
    if cur_sp is not None:
        body = "\n".join(cur_lines).strip()
        # drop pure placeholder / skipped media
        lines_kept = [l for l in cur_lines if SKIP_BODY not in l]
        body = "\n".join(lines_kept).strip()
        if body and not placeholder_tags.match(body):
            msgs.append((cur_ts, cur_sp, body))
    cur_ts, cur_sp, cur_lines = None, None, []

with open(SRC, encoding='utf-8') as f:
    for line in f:
        line = line.rstrip("\n")
        m = msg_re.match(line)
        if m:
            flush()
            cur_ts, cur_sp = m.group(1), m.group(2).strip()
            cur_lines = []
        elif cur_sp is not None:
            if SKIP_BODY in line:
                continue
            cur_lines.append(line)
    flush()

# ---- 基础统计 ----
by_sp = collections.Counter(s for _, s, _ in msgs)
print("总消息数:", len(msgs))
print("发言人分布:", dict(by_sp))
print("时间跨度:", msgs[0][0], "->", msgs[-1][0])

# 按天统计
by_day = collections.Counter(ts[:10] for ts, s, _ in msgs if s == "不语")
print("不语活跃天数:", len(by_day), "总天数跨度:", (len(set(ts[:10] for ts,_,_ in msgs))))

# 小时分布（不语）
by_hour = collections.Counter(int(ts[11:13]) for ts, s, _ in msgs if s == "不语")
print("不语小时分布:", dict(sorted(by_hour.items())))

# 消息长度（不语）
buyu = [t for ts, s, t in msgs if s == "不语"]
lens = [len(t) for t in buyu]
print("不语消息数:", len(buyu), "平均长度:", round(sum(lens)/len(lens),1), "中位:", sorted(lens)[len(lens)//2], "最长:", max(lens))
long_msgs = [t for t in buyu if len(t) >= 50]
print("不语≥50字消息数:", len(long_msgs))

# 连发模式：连续独白（不语连发未被打断）
streaks = []
cur = 0
for ts, s, t in msgs:
    if s == "不语":
        cur += 1
    else:
        if cur: streaks.append(cur)
        cur = 0
if cur: streaks.append(cur)
print("不语连发中位:", sorted(streaks)[len(streaks)//2], "最大连发:", max(streaks), "连发段数:", len(streaks))

# 保存清洗后的完整对话（含双方，供阅读）
with open(OUT_DIR + r"\cleaned_full.txt", "w", encoding='utf-8') as f:
    for ts, s, t in msgs:
        f.write(f"[{ts}] {s}\n{t}\n\n")
# 保存不语全部消息
with open(OUT_DIR + r"\buyu_all.txt", "w", encoding='utf-8') as f:
    for ts, s, t in msgs:
        if s == "不语":
            f.write(f"[{ts}]\n{t}\n\n")
print("已写出 cleaned_full.txt 和 buyu_all.txt")
