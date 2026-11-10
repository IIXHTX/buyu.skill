# -*- coding: utf-8 -*-
"""表达DNA量化：高频词、口癖、句式统计"""
import re, collections, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = r"C:\Users\ASUS\.workbuddy\skills\buyu-perspective\references\sources\buyu_all.txt"
texts = []
with open(SRC, encoding='utf-8') as f:
    lines = [l.rstrip("\n") for l in f]
i = 0
while i < len(lines):
    if lines[i].startswith("[") and "]" in lines[i]:
        i += 1
        buf = []
        while i < len(lines) and not lines[i].startswith("["):
            if lines[i].strip():
                buf.append(lines[i].strip())
            i += 1
        if buf:
            texts.append("\n".join(buf))
    else:
        i += 1

total = "\n".join(texts)
print("消息数:", len(texts), "总字符:", len(total))

# 高频口癖统计
patterns = ["宝宝","别这么说","喵","哦哦哦","我去","好难受","神了","绝了","嘻嘻嘻","嗯嗯嗯","没有哦","此乃","命苦","？","好的","OK","ok","okok","怎么了","对啊","没有没有","呃","呜呜呜","赏","难受","哭了","好可爱","可爱","甜甜","神人","老六","烂仔","哈夫币","暴率","撤了","上号","在上班","下班","晚安","早八","写小说","AI","ai","小律","甜甜的","怎么","什么"]
counts = {p: total.count(p) for p in patterns}
for p, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"{p}: {c}")

# 标点风格
print("---")
print("省略号(...):", total.count("...") + total.count("。。。"))
print("问号总数:", total.count("？") + total.count("?"))
print("感叹号:", total.count("!") + total.count("！"))
print("波浪号~:", total.count("~"))
print("哈哈哈:", total.count("哈哈"))
print("啊啊啊:", total.count("啊啊"))

# 单句消息（纯短消息）占比
solo = sum(1 for t in texts if len(t) <= 4)
print("≤4字的弹幕式消息占比:", round(solo/len(texts)*100, 1), "%")

# 疑问句消息占比
q = sum(1 for t in texts if "？" in t or "?" in t)
print("含问号的消息占比:", round(q/len(texts)*100, 1), "%")
