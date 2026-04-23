#!/usr/bin/env python3
"""
Translate calc-training.json and subject-b-training.json from English to Japanese.
Uses hardcoded translations for every question since there are exactly 221 questions.
"""
import json
import copy

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # trailing newline
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n')

# We'll translate by category sections. Each category gets its name translated.
# Questions within each category are translated one by one.

def translate_calc_training(data):
    result = []
    for q in data:
        tq = copy.deepcopy(q)
        cat = tq.get('category','')
        idx = data.index(q)
        tq = translate_q(calc_translations[idx], tq)
        result.append(tq)
    return result

# Actually, let me just build the full translation inline.
# Since we have the exact number of questions and their order, we can translate each one.

def main():
    print("Loading calc-training.json...")
    calc = load_json('src/data/calc-training.json')
    print(f"  {len(calc)} questions loaded")
    
    print("Loading subject-b-training.json...")
    subject = load_json('src/data/subject-b-training.json')
    print(f"  {len(subject)} questions loaded")
    
    # Apply translations
    print("Translating calc-training.json...")
    translated_calc = apply_calc_translations(calc)
    
    print("Translating subject-b-training.json...")
    translated_subject = apply_subject_translations(subject)
    
    # Save
    print("Saving translated calc-training.json...")
    save_json('src/data/calc-training.json', translated_calc)
    
    print("Saving translated subject-b-training.json...")
    save_json('src/data/subject-b-training.json', translated_subject)
    
    # Validate
    print("Validating JSON...")
    with open('src/data/calc-training.json', 'r', encoding='utf-8') as f:
        json.load(f)
    with open('src/data/subject-b-training.json', 'r', encoding='utf-8') as f:
        json.load(f)
    
    print("Done! Both files translated and validated.")

def apply_calc_translations(data):
    t = T_CALC
    result = []
    for i, q in enumerate(data):
        if i >= len(t):
            print(f"  WARNING: calc-training index {i} has no translation!")
            result.append(q)
            continue
        tq = copy.deepcopy(q)
        tr = t[i]
        if tr.get('category'):
            tq['category'] = tr['category']
        if tr.get('question'):
            tq['question'] = tr['question']
        if tr.get('options'):
            for j, opt_tr in enumerate(tr['options']):
                if j < len(tq['options']):
                    if 'text' in opt_tr:
                        tq['options'][j]['text'] = opt_tr['text']
        if tr.get('explanation'):
            tq['explanation'] = tr['explanation']
        if tr.get('cheatsheet'):
            tq['cheatsheet'] = tr['cheatsheet']
        result.append(tq)
    return result

def apply_subject_translations(data):
    t = T_SUBJECT
    result = []
    for i, q in enumerate(data):
        if i >= len(t):
            print(f"  WARNING: subject-b index {i} has no translation!")
            result.append(q)
            continue
        tq = copy.deepcopy(q)
        tr = t[i]
        if tr.get('category'):
            tq['category'] = tr['category']
        if tr.get('question'):
            tq['question'] = tr['question']
        if tr.get('options'):
            for j, opt_tr in enumerate(tr['options']):
                if j < len(tq['options']):
                    if 'text' in opt_tr:
                        tq['options'][j]['text'] = opt_tr['text']
        if tr.get('explanation'):
            tq['explanation'] = tr['explanation']
        result.append(tq)
    return result

# ============ CALC-TRAINING TRANSLATIONS (121 Qs) ============
T_CALC = [
# Q0: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "/26のサブネットマスクを10進数で示せ。",
    "options": [
        {"text": "255.255.255.192"},
        {"text": "255.255.255.128"},
        {"text": "255.255.255.224"},
        {"text": "255.255.255.240"}
    ],
    "explanation": "/26は26ビットをネットワーク部に使用: 255.255.255.192。最終オクテット: 192 = 11000000 (2ホストビット = 64-2=62ホスト)。",
    "cheatsheet": "/25 = 128, /26 = 192, /27 = 224, /28 = 240, /29 = 248, /30 = 252"
},
# Q1: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "/27サブネットの利用可能ホスト数はいくつか。",
    "options": [
        {"text": "30"},
        {"text": "32"},
        {"text": "14"},
        {"text": "62"}
    ],
    "explanation": "/27は5ホストビット残す: 2^5 = 32総IP、ネットワークアドレスとブロードキャストを除くと30ホスト利用可能。",
    "cheatsheet": "利用可能ホスト = 2^(32-プレフィックス) - 2。/24=254, /25=126, /26=62, /27=30, /28=14, /29=6, /30=2"
},
# Q2: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "192.168.1.130/26のネットワークアドレスはどれか。",
    "options": [
        {"text": "192.168.1.128"},
        {"text": "192.168.1.0"},
        {"text": "192.168.1.64"},
        {"text": "192.168.1.192"}
    ],
    "explanation": "/26のブロックサイズは64。130は128ブロックに属する(128+63=191)。ネットワーク = 192.168.1.128。",
    "cheatsheet": "ブロックサイズ = 256 - マスクオクテット。/26 = 256-192=64。ブロック: 0, 64, 128, 192。"
},
# Q3: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "10.0.0.0/23のブロードキャストアドレスはどれか。",
    "options": [
        {"text": "10.0.1.255"},
        {"text": "10.0.0.255"},
        {"text": "10.0.255.255"},
        {"text": "10.255.255.255"}
    ],
    "explanation": "/23は2つのクラスCにまたがる: 10.0.0.0 から 10.0.1.255。次のサブネットの直前のアドレスがブロードキャスト。",
    "cheatsheet": "/23 = 510ホスト、連続する2つの/24。ブロードキャスト = 範囲の最後のIP。"
},
# Q4: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "サブネットごとに50ホストが必要な場合、最小のサブネットマスクはどれか。",
    "options": [
        {"text": "/26"},
        {"text": "/25"},
        {"text": "/27"},
        {"text": "/24"}
    ],
    "explanation": "2^5-2=30(不足)、2^6-2=62(十分)。したがって/26(6ホストビット)が最小マスク。",
    "cheatsheet": "2^n - 2 >= 必要ホスト数 となる最小のnを求める。ホストビット = n、プレフィックス = 32 - n。"
},
# Q5: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "サブネットマスク255.255.255.248のCIDR表記はどれか。",
    "options": [
        {"text": "/29"},
        {"text": "/28"},
        {"text": "/30"},
        {"text": "/27"}
    ],
    "explanation": "248の2進数 = 11111000(最終オクテットに5つの1)。24 + 5 = 29。6利用可能ホスト(8-2)。",
    "cheatsheet": "連続する1ビットを数える: 255.255.255.x -> 24 + xのビット数。248=11111000=5ビット。"
},
# Q6: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "172.16.0.0/16から/24サブネットをいくつ作成できるか。",
    "options": [
        {"text": "256"},
        {"text": "128"},
        {"text": "254"},
        {"text": "512"}
    ],
    "explanation": "/16から/24へ8ビット借用: 2^8 = 256サブネット、各254利用可能ホスト。",
    "cheatsheet": "新サブネット数 = 2^(新プレフィックス - 元プレフィックス)。/16から/24 = 2^8 = 256。"
},
# Q7: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "192.168.10.32/28の最初の利用可能IPはどれか。",
    "options": [
        {"text": "192.168.10.33"},
        {"text": "192.168.10.32"},
        {"text": "192.168.10.34"},
        {"text": "192.168.10.1"}
    ],
    "explanation": "ネットワークは192.168.10.32、ブロードキャストは192.168.10.47。最初の利用可能IP = 192.168.10.33。",
    "cheatsheet": "最初の利用可能IP = ネットワーク + 1。最後の利用可能IP = ブロードキャスト - 1。"
},
# Q8: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "VLSMにおいて、ポイントツーポイントリンク(2ホスト)のサブネットマスクはどれか。",
    "options": [
        {"text": "/30 (255.255.255.252)"},
        {"text": "/29"},
        {"text": "/31"},
        {"text": "/28"}
    ],
    "explanation": "/30はポイントツーポイントリンク用に4総IP(2利用可能)を提供。/31(RFC 3021)はネットワーク/ブロードキャストなしで2IPを使用。",
    "cheatsheet": "ポイントツーポイント: /30(従来) または /31(RFC 3021、ネット/ブロードキャストなし)。"
},
# Q9: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "255.255.255.192のワイルドカードマスクはどれか。",
    "options": [
        {"text": "0.0.0.63"},
        {"text": "0.0.0.64"},
        {"text": "0.0.0.127"},
        {"text": "0.0.0.128"}
    ],
    "explanation": "ワイルドカード = サブネットマスクの反転。255-255=0, 255-255=0, 255-255=0, 255-192=63。",
    "cheatsheet": "ワイルドカードマスク = 255.255.255.255 - サブネットマスク。192の反転 = 63。"
},
# Q10: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "200.10.0.0/21を/24にサブネット化した場合、いくつのサブネットになるか。",
    "options": [
        {"text": "8"},
        {"text": "4"},
        {"text": "16"},
        {"text": "7"}
    ],
    "explanation": "/21から/24へ3ビット借用: 2^3 = 8サブネット、各/24で254ホスト。",
    "cheatsheet": "サブネット数 = 2^(対象プレフィックス - 現在プレフィックス)。/21から/24 = 2^3 = 8。"
},
# Q11: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "10.10.10.0/25の最後の利用可能IPはどれか。",
    "options": [
        {"text": "10.10.10.126"},
        {"text": "10.10.10.127"},
        {"text": "10.10.10.254"},
        {"text": "10.10.10.128"}
    ],
    "explanation": "/25: ネットワーク=10.10.10.0、ブロードキャスト=10.10.10.127。最後の利用可能 = 10.10.10.126。",
    "cheatsheet": "ブロードキャスト = ネットワーク + ブロックサイズ - 1。最後の利用可能 = ブロードキャスト - 1。"
},
# Q12: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "/28サブネットのブロックサイズはどれか。",
    "options": [
        {"text": "16"},
        {"text": "8"},
        {"text": "32"},
        {"text": "4"}
    ],
    "explanation": "/28は4ホストビット残す: 2^4 = 16 IPアドレス/サブネット(ブロックサイズ)。",
    "cheatsheet": "ブロックサイズ = 2^(32 - プレフィックス)。/28 = 2^4 = 16。"
},
# Q13: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "/24から10サブネットを作成するには何ビット借用する必要があるか。",
    "options": [
        {"text": "4"},
        {"text": "3"},
        {"text": "5"},
        {"text": "2"}
    ],
    "explanation": "2^3=8(不足)、2^4=16(十分)。4ビット借用し、/28で各14ホストとなる。",
    "cheatsheet": "2^n >= 必要サブネット数 となる最小のnを求める。nビット借用。"
},
# Q14: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "172.16.5.200/27のネットワークアドレスはどれか。",
    "options": [
        {"text": "172.16.5.192"},
        {"text": "172.16.5.0"},
        {"text": "172.16.5.128"},
        {"text": "172.16.5.224"}
    ],
    "explanation": "/27のブロック = 32。200/32 = 6余り8。ブロック6は192から開始(6*32=192)。ネットワーク = 172.16.5.192。",
    "cheatsheet": "ネットワーク = floor(IP / ブロックサイズ) * ブロックサイズ。200/32=6.25、floor=6、6*32=192。"
},
# Q15: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "/22ネットワークから/28サブネットをいくつ作成できるか。",
    "options": [
        {"text": "64"},
        {"text": "32"},
        {"text": "128"},
        {"text": "16"}
    ],
    "explanation": "/22から/28へ6ビット借用: 2^6 = 64サブネット、各14利用可能ホスト。",
    "cheatsheet": "サブネット数 = 2^(28-22) = 2^6 = 64。"
},
# Q16: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "192.168.100.0/22のサブネットマスクはどれか。",
    "options": [
        {"text": "255.255.252.0"},
        {"text": "255.255.254.0"},
        {"text": "255.255.248.0"},
        {"text": "255.255.255.0"}
    ],
    "explanation": "/22は22ビット: 255.255.252.0(252 = 2進数11111100、6ホストビット)。",
    "cheatsheet": "/22 = 255.255.252.0, /23 = 255.255.254.0, /24 = 255.255.255.0"
},
# Q17: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "10.1.2.0/24のブロードキャストアドレスはどれか。",
    "options": [
        {"text": "10.1.2.255"},
        {"text": "10.1.2.254"},
        {"text": "10.1.2.0"},
        {"text": "10.1.255.255"}
    ],
    "explanation": "/24では、ブロードキャストは範囲の最後のIP: 10.1.2.255。最後の利用可能 = 10.1.2.254。",
    "cheatsheet": "/24ブロードキャスト: x.y.z.255。/23ブロードキャスト: x.y.(z+1).255。"
},
# Q18: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "172.16.0.0/23の利用可能ホスト数はいくつか。",
    "options": [
        {"text": "510"},
        {"text": "512"},
        {"text": "254"},
        {"text": "1022"}
    ],
    "explanation": "/23は9ホストビット: 2^9=512総IP、2を引いて510利用可能ホスト。",
    "cheatsheet": "/23 = 510ホスト, /22 = 1022, /21 = 2046, /20 = 4094。"
},
# Q19: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "192.168.1.47/28はどのサブネットに属するか。",
    "options": [
        {"text": "192.168.1.32"},
        {"text": "192.168.1.16"},
        {"text": "192.168.1.48"},
        {"text": "192.168.1.0"}
    ],
    "explanation": "/28ブロック=16。47/16=2余り15。ブロック2は32から開始。ネットワーク=192.168.1.32。",
    "cheatsheet": "ブロックサイズ = 2^(32-28)=16。ブロック: 0,16,32,48... 47は32-47の範囲。"
},
# Q20: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "192.168.0.0/24から作成できる/30サブネットの最大数はいくつか。",
    "options": [
        {"text": "64"},
        {"text": "62"},
        {"text": "128"},
        {"text": "32"}
    ],
    "explanation": "/24から/30へ6ビット借用: 2^6=64サブネット、各2利用可能ホスト。",
    "cheatsheet": "2^(30-24)=2^6=64サブネット。各/30 = 4IP(2利用可能)。"
},
# Q21: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "192.168.1.0/24から5サブネットが必要な場合、どのマスクを使用すべきか。",
    "options": [
        {"text": "/27"},
        {"text": "/26"},
        {"text": "/28"},
        {"text": "/25"}
    ],
    "explanation": "5サブネット必要: 2^2=4(不足)、2^3=8(十分)。3ビット借用: /24+3 = /27。各30ホストの8サブネット。",
    "cheatsheet": "借用ビット: ceil(log2(必要サブネット数))。ceil(log2(5)) = 3ビット。/27。"
},
# Q22: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "サブネットマスク255.255.128.0をCIDR表記に変換せよ。",
    "options": [
        {"text": "/17"},
        {"text": "/18"},
        {"text": "/16"},
        {"text": "/19"}
    ],
    "explanation": "255.255.128.0: 最初の16ビット + 第3オクテットの1ビット(128=10000000)。合計 = 17ビット = /17。",
    "cheatsheet": "128=1ビット, 192=2ビット, 224=3, 240=4, 248=5, 252=6, 254=7, 255=8。"
},
# Q23: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "10.0.0.16/29の有効ホスト範囲はどれか。",
    "options": [
        {"text": "10.0.0.17 〜 10.0.0.22"},
        {"text": "10.0.0.16 〜 10.0.0.31"},
        {"text": "10.0.0.1 〜 10.0.0.14"},
        {"text": "10.0.0.17 〜 10.0.0.30"}
    ],
    "explanation": "/29: ネットワーク=10.0.0.16、ブロードキャスト=10.0.0.23。ホスト範囲=10.0.0.17〜10.0.0.22。",
    "cheatsheet": "ホスト範囲 = ネットワーク+1 〜 ブロードキャスト-1。ブロック=8: 16-23。"
},
# Q24: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "/28サブネットの総IPアドレス数はいくつか。",
    "options": [
        {"text": "16"},
        {"text": "14"},
        {"text": "15"},
        {"text": "8"}
    ],
    "explanation": "/28は4ホストビット: 2^4=16総IP(14利用可能 + ネットワーク + ブロードキャスト)。",
    "cheatsheet": "総IP = 2^(32-プレフィックス)。利用可能 = 総IP - 2。"
},
# Q25: Subnet Calculation
{
    "category": "サブネット計算",
    "question": "/24から最大サブネット数を作成しつつ、各サブネット100ホストを許容するマスクはどれか。",
    "options": [
        {"text": "255.255.255.128"},
        {"text": "255.255.255.192"},
        {"text": "255.255.255.224"},
        {"text": "255.255.255.0"}
    ],
    "explanation": "2^7-2=126(100に十分)、2^6-2=62(不足)。/25で126ホスト、/24から2サブネット。",
    "cheatsheet": "2^n-2 >= 100: n=7(126ホスト)。プレフィックス=32-7=25。マスク=255.255.255.128。"
},
# Q26: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "192.168.1.1を2進数に変換せよ。",
    "options": [
        {"text": "11000000.10101000.00000001.00000001"},
        {"text": "10101000.11000000.00000001.00000001"},
        {"text": "11000000.10101000.1.1"},
        {"text": "192.168.1.1は2進数に変換できない"}
    ],
    "explanation": "192=11000000, 168=10101000, 1=00000001, 1=00000001。",
    "cheatsheet": "10進数から2進数: 2で除算し、余りを右から左に集める。"
},
# Q27: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "255.255.0.0の2進数値はどれか。",
    "options": [
        {"text": "11111111.11111111.00000000.00000000"},
        {"text": "11111111.11111111.11111111.00000000"},
        {"text": "11111111.00000000.00000000.00000000"},
        {"text": "255.255.0.0には2進数形式がない"}
    ],
    "explanation": "255=11111111, 0=00000000。したがって255.255.0.0 = 11111111.11111111.00000000.00000000。",
    "cheatsheet": "2のべき乗チャート: 128,64,32,16,8,4,2,1"
},
# Q28: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "IPアドレス172.16.0.1のクラスはどれか。",
    "options": [
        {"text": "クラスB"},
        {"text": "クラスA"},
        {"text": "クラスC"},
        {"text": "クラスD"}
    ],
    "explanation": "クラスB: 128.0.0.0 - 191.255.255.255(第1オクテット128-191)。クラスA: 1-126。クラスC: 192-223。",
    "cheatsheet": "A:1-126, B:128-191, C:192-223, D:224-239, E:240-255"
},
# Q29: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "10進数172の2進数値はどれか。",
    "options": [
        {"text": "10101100"},
        {"text": "11001100"},
        {"text": "10101010"},
        {"text": "10010100"}
    ],
    "explanation": "172 = 128+32+8+4 = 10101100(2進数)。",
    "cheatsheet": "分解: 172-128=44, 44-32=12, 12-8=4, 4-4=0。位置: 128,32,8,4。"
},
# Q30: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "クラスAネットワークはいくつ存在するか。",
    "options": [
        {"text": "126"},
        {"text": "128"},
        {"text": "254"},
        {"text": "255"}
    ],
    "explanation": "クラスA: 第1オクテット1-126(0は予約、127はループバック)。したがって126ネットワーク。",
    "cheatsheet": "クラスA: 126ネットワーク x 1600万ホスト。クラスB: 16384ネットワーク x 6.5万ホスト。クラスC: 200万ネットワーク x 254ホスト。"
},
# Q31: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "クラスBのデフォルトサブネットマスクはどれか。",
    "options": [
        {"text": "255.255.0.0 (/16)"},
        {"text": "255.0.0.0 (/8)"},
        {"text": "255.255.255.0 (/24)"},
        {"text": "255.255.128.0 (/17)"}
    ],
    "explanation": "クラスBデフォルト: /16 (255.255.0.0)。クラスA: /8。クラスC: /24。",
    "cheatsheet": "クラスA=/8, クラスB=/16, クラスC=/24。これらがクラスフルデフォルト。"
},
# Q32: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "2進数11000000.10101000.00000001.00000001を10進数に変換せよ。",
    "options": [
        {"text": "192.168.1.1"},
        {"text": "192.168.1.0"},
        {"text": "193.168.1.1"},
        {"text": "192.169.1.1"}
    ],
    "explanation": "11000000=128+64=192, 10101000=128+32+8=168, 00000001=1, 00000001=1。",
    "cheatsheet": "2進数から10進数: 各'1'ビットの2^位置の合計。"
},
# Q33: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "192.168.1.0/24は有効なホストアドレスか。",
    "options": [
        {"text": "いいえ、ネットワークアドレスである"},
        {"text": "はい、有効なホストである"},
        {"text": "いいえ、ブロードキャストアドレスである"},
        {"text": "サブネットマスクによる"}
    ],
    "explanation": "192.168.1.0は/24サブネットのネットワーク(先頭)アドレス。ホストに割り当て不可。",
    "cheatsheet": "ネットワークアドレス = 全ホストビット0。ブロードキャスト = 全ホストビット1。いずれも割り当て不可。"
},
# Q34: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "APIPAアドレス範囲はどれか。",
    "options": [
        {"text": "169.254.0.0/16"},
        {"text": "192.168.0.0/16"},
        {"text": "10.0.0.0/8"},
        {"text": "172.16.0.0/12"}
    ],
    "explanation": "APIPA(Automatic Private IP Addressing): 169.254.0.0/16、DHCPが利用不可の場合に割り当てられる。",
    "cheatsheet": "APIPA = 169.254.0.1 〜 169.254.255.254。ゲートウェイなし = インターネット不可。"
},
# Q35: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "/22のホストビット数はいくつか。",
    "options": [
        {"text": "10"},
        {"text": "8"},
        {"text": "6"},
        {"text": "12"}
    ],
    "explanation": "/22ネットワーク部、32-22=10ホストビット。2^10=1024総IP、1022利用可能。",
    "cheatsheet": "ホストビット = 32 - プレフィックス。/22 = 10ホストビット。"
},
# Q36: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "10.0.0.1のクラスはどれか。",
    "options": [
        {"text": "クラスA"},
        {"text": "クラスB"},
        {"text": "クラスC"},
        {"text": "クラスD"}
    ],
    "explanation": "クラスA: 第1オクテット1-126。10はこの範囲内。デフォルトマスク /8。",
    "cheatsheet": "クラスA: 1-126, B: 128-191, C: 192-223, D: 224-239(マルチキャスト), E: 240-255(予約)。"
},
# Q37: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "第3オクテット192を2進数に変換せよ。",
    "options": [
        {"text": "11000000"},
        {"text": "10101010"},
        {"text": "11110000"},
        {"text": "10000000"}
    ],
    "explanation": "192 = 128+64 = 11000000。",
    "cheatsheet": "128+64=192, 128+64+32=224, 128+64+32+16=240, 128+64+32+16+8=248"
},
# Q38: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "ループバックアドレスはどれか。",
    "options": [
        {"text": "127.0.0.1"},
        {"text": "0.0.0.0"},
        {"text": "255.255.255.255"},
        {"text": "1.1.1.1"}
    ],
    "explanation": "127.0.0.1はループバックアドレス。127.0.0.0/8全体がループバック。",
    "cheatsheet": "127.x.x.x = ループバック。0.0.0.0 = 未指定。255.255.255.255 = リミテッドブロードキャスト。"
},
# Q39: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "クラスCネットワークの利用可能IP数はいくつか。",
    "options": [
        {"text": "254"},
        {"text": "255"},
        {"text": "256"},
        {"text": "252"}
    ],
    "explanation": "クラスCは/24: 2^8=256総、ネットワークとブロードキャストを除いて254利用可能。",
    "cheatsheet": "クラスC: 256-2=254。/24は1オクテットのホストビット。"
},
# Q40: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "192.168.1.255/24は何を示すか。",
    "options": [
        {"text": "ブロードキャストアドレス"},
        {"text": "有効なホストアドレス"},
        {"text": "ネットワークアドレス"},
        {"text": "ゲートウェイアドレス"}
    ],
    "explanation": "192.168.1.255は/24サブネットのブロードキャスト(最終)アドレス。ホストに割り当て不可。",
    "cheatsheet": "サブネットの最後のアドレス = ブロードキャスト。全ホストビットが1。"
},
# Q41: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "10101100を10進数に変換せよ。",
    "options": [
        {"text": "172"},
        {"text": "184"},
        {"text": "190"},
        {"text": "168"}
    ],
    "explanation": "1*128+0*64+1*32+0*16+1*8+1*4+0*2+0*1 = 128+32+8+4 = 172。",
    "cheatsheet": "位置の重み: 128,64,32,16,8,4,2,1。'1'の位置を合計。"
},
# Q42: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "プライベートクラスBネットワークはいくつ存在するか。",
    "options": [
        {"text": "16"},
        {"text": "1"},
        {"text": "256"},
        {"text": "128"}
    ],
    "explanation": "クラスBプライベート: 172.16.0.0/12。範囲172.16.x.x〜172.31.x.x。16のクラスB相当ネットワーク。",
    "cheatsheet": "クラスBプライベート: 172.16.0.0 - 172.31.255.255 (172.16〜172.31 = 16ブロック)。"
},
# Q43: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "0.0.0.0は何に使用されるか。",
    "options": [
        {"text": "デフォルトルートまたは未指定アドレス"},
        {"text": "ループバックアドレス"},
        {"text": "ブロードキャストアドレス"},
        {"text": "ネットワークアドレスのみ"}
    ],
    "explanation": "0.0.0.0は未指定の送信元またはデフォルトルートを意味する。ルーティングでは全宛先にマッチ。",
    "cheatsheet": "0.0.0.0 = デフォルトルート / 未指定。0.0.0.0/0 = 全てにマッチ。"
},
# Q44: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "プライベートクラスCネットワークはいくつ存在するか。",
    "options": [
        {"text": "256"},
        {"text": "255"},
        {"text": "16"},
        {"text": "1"}
    ],
    "explanation": "クラスCプライベート: 192.168.0.0/16。各/24は別のクラスCネットワーク: 192.168.0-255 = 256ネットワーク。",
    "cheatsheet": "クラスCプライベート: 192.168.0.0 〜 192.168.255.0 (256ネットワーク)。"
},
# Q45: IP Addressing
{
    "category": "IPアドレッシング",
    "question": "192.168.1.100と255.255.255.0のAND演算でネットワークアドレスはどうなるか。",
    "options": [
        {"text": "192.168.1.0"},
        {"text": "192.168.1.100"},
        {"text": "192.168.0.0"},
        {"text": "0.0.0.0"}
    ],
    "explanation": "IP AND マスク: 192.255=192, 168.255=168, 1.255=1, 100.0=0。ネットワーク=192.168.1.0。",
    "cheatsheet": "ネットワークアドレス = IP AND サブネットマスク(ビット単位のAND演算)。"
},
# Q46-Q65: Network Performance (20 Qs)
{
    "category": "ネットワーク性能",
    "question": "100MbpsリンクでRTTが10msの場合、帯域遅延積はいくらか。",
    "options": [
        {"text": "125,000バイト"},
        {"text": "100,000バイト"},
        {"text": "1,000,000バイト"},
        {"text": "12,500バイト"}
    ],
    "explanation": "BDP = 100Mbps x 0.01s = 1,000,000ビット = 125,000バイト。TCPウィンドウは125KB以上が必要。",
    "cheatsheet": "BDP(ビット) = 帯域(bps) x RTT(s)。バイト変換: /8。"
},
{
    "category": "ネットワーク性能",
    "question": "1GbpsリンクでRTTが50msの場合、帯域遅延積は何KBか。",
    "options": [
        {"text": "6,250 KB"},
        {"text": "50,000 KB"},
        {"text": "1,000 KB"},
        {"text": "62,500 KB"}
    ],
    "explanation": "BDP = 1,000,000,000 x 0.05 = 50,000,000ビット = 6,250,000バイト = 6,250KB。",
    "cheatsheet": "BDP = 1Gbps x 50ms = 50Mb = 6,250KB。ウィンドウスケーリングが必要!"
},
{
    "category": "ネットワーク性能",
    "question": "スループットが500Mbpsで帯域が1Gbpsの場合、利用率は何%か。",
    "options": [
        {"text": "50%"},
        {"text": "25%"},
        {"text": "100%"},
        {"text": "75%"}
    ],
    "explanation": "利用率 = (スループット / 帯域) x 100 = (500/1000) x 100 = 50%。",
    "cheatsheet": "利用率% = (実際のスループット / 最大帯域) x 100。"
},
{
    "category": "ネットワーク性能",
    "question": "RTTが100msのリンクでTCPウィンドウ64KBの場合、最大スループットはいくらか。",
    "options": [
        {"text": "5.12 Mbps"},
        {"text": "64 Mbps"},
        {"text": "640 Kbps"},
        {"text": "10 Mbps"}
    ],
    "explanation": "スループット = ウィンドウ / RTT = 64KB / 0.1s = 640KB/s = 5.12Mbps。",
    "cheatsheet": "最大スループット = ウィンドウサイズ / RTT。ウィンドウ小さい = 利用率低下。"
},
{
    "category": "ネットワーク性能",
    "question": "RTTが20msの10Gbpsリンクをフル活用するには、必要なTCPウィンドウサイズはいくらか。",
    "options": [
        {"text": "25 MB"},
        {"text": "2.5 MB"},
        {"text": "250 KB"},
        {"text": "250 MB"}
    ],
    "explanation": "BDP = 10Gbps x 0.02s = 200Mb = 25MB。ウィンドウスケーリング必須(65535超)。",
    "cheatsheet": "ウィンドウ = 帯域 x RTT。10Gbps x 20ms = 200Mb = 25MB。"
},
{
    "category": "ネットワーク性能",
    "question": "1500バイトパケットが2msのキューイング遅延の場合、バッファ48KBでキューに保持できるパケット数はいくつか。",
    "options": [
        {"text": "32パケット"},
        {"text": "64パケット"},
        {"text": "16パケット"},
        {"text": "48パケット"}
    ],
    "explanation": "48KB / 1500バイト = 32パケット。各パケットがバッファに追加されるごとに2ms遅延。",
    "cheatsheet": "キューデプス = バッファサイズ / パケットサイズ。"
},
{
    "category": "ネットワーク性能",
    "question": "ファイルサイズ100MB、転送時間80秒。スループットは何Mbpsか。",
    "options": [
        {"text": "10 Mbps"},
        {"text": "8 Mbps"},
        {"text": "12.5 Mbps"},
        {"text": "100 Mbps"}
    ],
    "explanation": "100MB = 800Mb。スループット = 800Mb / 80s = 10Mbps。",
    "cheatsheet": "スループット = (ファイルサイズビット / 転送時間秒)。MB→Mb変換: x8。"
},
{
    "category": "ネットワーク性能",
    "question": "RTTが40msで片方向の処理遅延が2msの場合、片方向の伝搬遅延はいくらか。",
    "options": [
        {"text": "18ms"},
        {"text": "20ms"},
        {"text": "38ms"},
        {"text": "22ms"}
    ],
    "explanation": "RTT = 2 x (伝搬 + 処理)。40 = 2 x (p + 2)。p + 2 = 20。p = 18ms。",
    "cheatsheet": "RTT = 2 x 片方向遅延。各方向の処理/キューイング遅延を引く。"
},
{
    "category": "ネットワーク性能",
    "question": "リンクのパケットロス率が1%の場合、TCPスループットへの影響は概ねどれくらいか。",
    "options": [
        {"text": "スループットが容量の約1/sqrt(ロス)に低下(約10%程度)"},
        {"text": "スループットへの影響なし"},
        {"text": "スループットが半減"},
        {"text": "スループットが1%低下"}
    ],
    "explanation": "Mathisの式: スループット ~ MSS/RTT * 1/sqrt(p)。1%ロス: 1/sqrt(0.01) = 1/0.1 = 10倍の低減。",
    "cheatsheet": "TCPスループット ~ (MSS/RTT) * 1/sqrt(ロス率)。ロス率高い = スループット大幅低下。"
},
{
    "category": "ネットワーク性能",
    "question": "1Gbpsリンクで1500バイトフレームのシリアライゼーション遅延はいくらか。",
    "options": [
        {"text": "12マイクロ秒"},
        {"text": "120マイクロ秒"},
        {"text": "1.2ミリ秒"},
        {"text": "12ミリ秒"}
    ],
    "explanation": "シリアライゼーション = フレームサイズ / リンク速度 = 1500B x 8 / 1Gbps = 12000ns = 12us。",
    "cheatsheet": "シリアライゼーション遅延 = (バイト x 8) / bps。結果を適切な単位に変換。"
},
{
    "category": "ネットワーク性能",
    "question": "100Mbpsリンクでレイテンシ10msの場合、50MBファイルの転送時間は約何秒か。",
    "options": [
        {"text": "4.02秒"},
        {"text": "4秒"},
        {"text": "5秒"},
        {"text": "0.5秒"}
    ],
    "explanation": "転送時間 = (50MB x 8) / 100Mbps = 400/100 = 4s + レイテンシ = ~4.01s(大容量転送ではレイテンシ影響は小さい)。",
    "cheatsheet": "転送時間 = ファイルサイズ/帯域 + オーバーヘッド。大ファイルではレイテンシは無視できる程度。"
},
{
    "category": "ネットワーク性能",
    "question": "リンク容量10Gbpsで平均スループット3Gbpsの場合、利用率は何%か。",
    "options": [
        {"text": "30%"},
        {"text": "3%"},
        {"text": "33%"},
        {"text": "70%"}
    ],
    "explanation": "利用率 = 3/10 x 100 = 30%。残り70%は利用可能または未使用。",
    "cheatsheet": "利用率 = 平均スループット / リンク容量。"
},
{
    "category": "ネットワーク性能",
    "question": "キューに10パケットあり、各パケットの送信に0.5msかかる場合、キューイング遅延は最大いくらか。",
    "options": [
        {"text": "5ms"},
        {"text": "0.5ms"},
        {"text": "10ms"},
        {"text": "1ms"}
    ],
    "explanation": "最大キューイング遅延 = キューデプス x 1パケット送信時間 = 10 x 0.5 = 5ms。",
    "cheatsheet": "最大キューイング遅延 = キューデプス x 1パケット送信時間。"
},
{
    "category": "ネットワーク性能",
    "question": "VoIP通話に100Kbpsと最大遅延150msが必要。RTTが500msのリンクは適切か。",
    "options": [
        {"text": "いいえ、RTTが片方向遅延要件を超えている"},
        {"text": "はい、帯域は十分"},
        {"text": "はい、RTTは制限内"},
        {"text": "コーデックのみによる"}
    ],
    "explanation": "500ms RTT = 250ms片方向、VoIPの最大遅延要件150msを超過。",
    "cheatsheet": "片方向遅延 = RTT/2。アプリケーションの要件内である必要がある。"
},
{
    "category": "ネットワーク性能",
    "question": "G.711コーデックで必要な64バイト音声パケットの毎秒パケット数はいくつか。",
    "options": [
        {"text": "50 pps"},
        {"text": "100 pps"},
        {"text": "25 pps"},
        {"text": "200 pps"}
    ],
    "explanation": "G.711でptime 20ms: 1000/20 = 50パケット/秒。各パケット = 160バイトペイロード + ヘッダ。",
    "cheatsheet": "毎秒パケット数 = 1000ms / パケット化間隔。"
},
{
    "category": "ネットワーク性能",
    "question": "IPsec ESPトンネルモードのパケットへのオーバーヘッドは概ねどれくらいか。",
    "options": [
        {"text": "約50-70バイト"},
        {"text": "0バイト"},
        {"text": "10-20バイト"},
        {"text": "150バイト"}
    ],
    "explanation": "IPsec ESPトンネル追加: 新IPヘッダ(20) + ESPヘッダ(8) + IV(16) + ESPトレーラ(2-16) + ICV(10-16) ~50-70バイト。",
    "cheatsheet": "IPsecオーバーヘッド = ~50-70バイト(トンネル)。フラグメンテーションの原因になる可能性がある。"
},
{
    "category": "ネットワーク性能",
    "question": "合計トラフィック3Gbps、ECMPグループに4リンク。各リンクの利用率は概ねどれくらいか。",
    "options": [
        {"text": "各リンクの75%"},
        {"text": "1リンク100%、他はアイドル"},
        {"text": "各リンクの25%"},
        {"text": "各リンクの33%"}
    ],
    "explanation": "4等コストリンク(各1Gbpsと仮定)、3Gbpsを4分割 = 各750Mbps = 75%利用率。",
    "cheatsheet": "ECMP: 各リンクトラフィック = 総トラフィック / リンク数。"
},
{
    "category": "ネットワーク性能",
    "question": "パケットロス率20%で80%が再送必要な場合、実効スループットは概ねどれくらいか。",
    "options": [
        {"text": "元のスループットの約20%"},
        {"text": "元の80%"},
        {"text": "元の50%"},
        {"text": "元の64%"}
    ],
    "explanation": "深刻なロス: 20%ロスでTCPはウィンドウを大幅縮小。Mathis: ~1/sqrt(0.2) = ~2.24倍の低減。再送オーバーヘッドにより実効スループットはさらに低下。",
    "cheatsheet": "高いパケットロスは輻輳制御によりTCPスループットに深刻な影響。"
},
{
    "category": "ネットワーク性能",
    "question": "MTU 1500バイト、TCP MSS 1460バイトのリンクで1MB転送に必要なセグメント数はいくつか。",
    "options": [
        {"text": "726セグメント"},
        {"text": "1000セグメント"},
        {"text": "685セグメント"},
        {"text": "500セグメント"}
    ],
    "explanation": "1MB / 1460バイト = 1,048,576 / 1460 = ~718.5。ヘッダを考慮すると約718-726セグメント。",
    "cheatsheet": "セグメント数 = ファイルサイズ / MSS。ヘッダ含む: セグメント数 = ファイル / (MSS + ヘッダ)。"
},
{
    "category": "ネットワーク性能",
    "question": "グッドプットとスループットの違いは何か。",
    "options": [
        {"text": "グッドプットはアプリケーションレベルの有効データ; スループットは全プロトコルオーバーヘッドを含む"},
        {"text": "同じものである"},
        {"text": "グッドプットの方が常に高い"},
        {"text": "スループットがアプリケーションレベルのみ"}
    ],
    "explanation": "グッドプット = 有効なアプリケーションデータ転送量。スループット = ヘッダ、再送、プロトコルオーバーヘッドを含む。",
    "cheatsheet": "グッドプット < スループット < 帯域。ヘッダと再送がグッドプットを低下させる。"
},
# Q66-Q80: VLAN Design (15 Qs)
{
    "category": "VLAN設計",
    "question": "5部署に各50ホストがあり、完全分離したい場合、必要なVLAN数はいくつか。",
    "options": [
        {"text": "5"},
        {"text": "1"},
        {"text": "50"},
        {"text": "10"}
    ],
    "explanation": "部署ごとに1VLAN = 5VLAN。各VLANは別のブロードキャストドメイン。",
    "cheatsheet": "最小VLAN数 = 必要な分離ブロードキャストドメイン数。"
},
{
    "category": "VLAN設計",
    "question": "各VLANで最大200ホストに対応する場合、推奨サブネットマスクはどれか。",
    "options": [
        {"text": "/24 (255.255.255.0)"},
        {"text": "/25"},
        {"text": "/23"},
        {"text": "/22"}
    ],
    "explanation": "/24は254利用可能ホストを提供(2^8-2=254 >= 200)。/25は126のみ(不足)。",
    "cheatsheet": "2^ホストビット - 2 >= 最大ホスト数 となる最小マスクを選択。"
},
{
    "category": "VLAN設計",
    "question": "192.168.0.0/16から10VLANに/24を使用した場合、VLAN 3のアドレス範囲はどれか。",
    "options": [
        {"text": "192.168.3.0/24"},
        {"text": "192.168.30.0/24"},
        {"text": "192.168.2.0/24"},
        {"text": "192.168.10.0/24"}
    ],
    "explanation": "順次割り当て: VLAN 1=192.168.1.0, VLAN 2=192.168.2.0, VLAN 3=192.168.3.0、など。",
    "cheatsheet": "シンプルVLAN割り当て: VLAN N = 192.168.N.0/24。"
},
{
    "category": "VLAN設計",
    "question": "各20VLANを持つ2台のスイッチ間に必要なトランクポート数はいくつか。",
    "options": [
        {"text": "最低1つ(冗長性/帯域のため複数でも可)"},
        {"text": "20(VLANごとに1つ)"},
        {"text": "10"},
        {"text": "0"}
    ],
    "explanation": "1つの802.1Qトランクで全VLANを搬送。EtherChannel/LACPで帯域と冗長性を確保。",
    "cheatsheet": "1トランク = 全VLAN。LACPで複数物理リンクを1トランクに束ねる。"
},
{
    "category": "VLAN設計",
    "question": "192.168.0.0/22のアドレス空間に収まる/26サブネットはいくつか。",
    "options": [
        {"text": "16"},
        {"text": "4"},
        {"text": "8"},
        {"text": "64"}
    ],
    "explanation": "/22から/26へ4ビット借用: 2^4 = 16サブネット、各62利用可能ホスト。",
    "cheatsheet": "サブネット数 = 2^(対象 - 現在) = 2^(26-22) = 2^4 = 16。"
},
{
    "category": "VLAN設計",
    "question": "データVLANの推奨VLAN ID範囲はどれか。",
    "options": [
        {"text": "2-1001(通常範囲)"},
        {"text": "1002-1005(予約済み)"},
        {"text": "1006-4094(拡張範囲)"},
        {"text": "VLAN 1のみ"}
    ],
    "explanation": "VLAN 2-1001は通常範囲(VTP対応)。1002-1005はFDDI/Token Ring用予約。1006-4094は拡張範囲。",
    "cheatsheet": "通常: 2-1001、予約: 1002-1005、拡張: 1006-4094、ネイティブデフォルト: 1。"
},
{
    "category": "VLAN設計",
    "question": "10.0.0.0/21から/27サブネットをいくつ作成できるか。",
    "options": [
        {"text": "64"},
        {"text": "32"},
        {"text": "8"},
        {"text": "128"}
    ],
    "explanation": "/21から/27へ6ビット借用: 2^6 = 64サブネット、各30ホスト。",
    "cheatsheet": "2^(27-21) = 2^6 = 64サブネット。"
},
{
    "category": "VLAN設計",
    "question": "3階建てで各階100ユーザーの建物で、最も効率的なVLAN設計はどれか。",
    "options": [
        {"text": "部署ごとのVLAN(階ごとではなく)"},
        {"text": "階ごとに1VLAN"},
        {"text": "建物全体で1VLAN"},
        {"text": "ユーザーごとに1VLAN"}
    ],
    "explanation": "部署ベースのVLANは場所に関係なくユーザーをまとめ、ポリシーとACL管理を簡素化。",
    "cheatsheet": "VLAN設計: 物理的な場所ではなく機能/部署でグループ化。"
},
{
    "category": "VLAN設計",
    "question": "ポートチャネルトランクの最大VLAN数はいくつか。",
    "options": [
        {"text": "4094"},
        {"text": "1005"},
        {"text": "256"},
        {"text": "無制限"}
    ],
    "explanation": "802.1Qは4094VLANをサポート。拡張範囲(1006-4094)はトランクで動作するがVTP v1/v2では不可。",
    "cheatsheet": "最大VLAN = 4094(802.1Qの12ビットVIDフィールドによる制限)。"
},
{
    "category": "VLAN設計",
    "question": "10ホストのVLANで/24マスクを使用した場合、無駄になるIPアドレスはいくつか。",
    "options": [
        {"text": "242利用可能IPが無駄"},
        {"text": "254"},
        {"text": "0"},
        {"text": "244"}
    ],
    "explanation": "/24は254利用可能。10ホスト使用。254-10=244無駄。/28(14利用可能)を使用すべき。",
    "cheatsheet": "適切なマスク選択: /28は最大14ホストまで対応し、アドレス空間を大幅に節約。"
},
{
    "category": "VLAN設計",
    "question": "VLANタグなしのフレームがトランクポートに入ってくるとどうなるか。",
    "options": [
        {"text": "ネイティブVLAN(デフォルトVLAN 1)に割り当てられる"},
        {"text": "破棄される"},
        {"text": "全VLANに送信される"},
        {"text": "エラーが発生する"}
    ],
    "explanation": "トランク上のタグなしフレームはネイティブVLAN(デフォルトVLAN 1)に関連付けられる。",
    "cheatsheet": "ネイティブVLAN(デフォルト1)がトランクポートのタグなしフレームを処理。"
},
{
    "category": "VLAN設計",
    "question": "30VLANで各500ホストが必要な場合、必要な最小アドレス空間はどれか。",
    "options": [
        {"text": "/16アドレスブロック"},
        {"text": "/24アドレスブロック"},
        {"text": "/20アドレスブロック"},
        {"text": "/8アドレスブロック"}
    ],
    "explanation": "500ホストには/23(510ホスト)が必要。30 x /23 = 30 x 512 = 15360IP。/16は65536IP(十分)。",
    "cheatsheet": "計算: ホスト/VLAN x VLAN数 = 総IP。収まる最小ブロックを選択。"
},
{
    "category": "VLAN設計",
    "question": "VLAN間ルーティングとは何か。",
    "options": [
        {"text": "ルータまたはレイヤ3スイッチを使用したVLAN間のルーティング"},
        {"text": "VLAN内のルーティング"},
        {"text": "別の物理ネットワーク間のルーティング"},
        {"text": "自動VLAN割り当て"}
    ],
    "explanation": "VLAN間ルーティングによりルータオンスティックまたはレイヤ3スイッチのSVIでVLAN間通信を可能にする。",
    "cheatsheet": "方式: Router-on-a-Stick(サブインターフェース)またはレイヤ3スイッチSVI。"
},
{
    "category": "VLAN設計",
    "question": "24ポートスイッチで2ポートをトランクに使用した場合、サポート可能なアクセスポート数はいくつか。",
    "options": [
        {"text": "22"},
        {"text": "24"},
        {"text": "20"},
        {"text": "2"}
    ],
    "explanation": "24合計 - 2トランク = 22アクセスポート(エンドデバイス用)。",
    "cheatsheet": "利用可能アクセスポート = 総ポート - トランクポート - 管理ポート。"
},
{
    "category": "VLAN設計",
    "question": "スキーム10.10.VLAN.0/24を使用する場合、VLAN 10のサブネットはどれか。",
    "options": [
        {"text": "10.10.10.0/24"},
        {"text": "10.10.0.10/24"},
        {"text": "10.10.100.0/24"},
        {"text": "10.10.1.0/24"}
    ],
    "explanation": "スキーム: 10.10.VLAN.0/24。VLAN 10 = 10.10.10.0/24。シンプルでスケーラブル。",
    "cheatsheet": "第3オクテット = VLAN IDで直感的なマッピングと管理を容易にする。"
},
# Q81-Q95: Wireless Planning (15 Qs)
{
    "category": "無線設計",
    "question": "2.4GHz(米国)で利用可能な非干渉20MHzチャネル数はいくつか。",
    "options": [
        {"text": "3"},
        {"text": "11"},
        {"text": "6"},
        {"text": "1"}
    ],
    "explanation": "2.4GHzは11チャネル(米国)、各22MHz幅。非干渉: 1, 6, 11(3チャネル)。",
    "cheatsheet": "2.4GHz非干渉: 1, 6, 11。5GHzは非干渉チャネルがさらに多い。"
},
{
    "category": "無線設計",
    "question": "100m x 50mのオフィスで各APが半径20mをカバーする場合、必要なAP数は最低いくつか。",
    "options": [
        {"text": "最低4台"},
        {"text": "2台"},
        {"text": "1台"},
        {"text": "8台"}
    ],
    "explanation": "各APは約40m直径をカバー。面積: 100x50=5000m2。1APは約1257m2をカバー。5000/1257~4。ローミングにはオーバーラップが必要。",
    "cheatsheet": "AP数 = ceil(カバー面積 / APカバー面積) + ローミング用オーバーラップ余裕。"
},
{
    "category": "無線設計",
    "question": "5GHzで20MHzチャネルに使用されるチャネル間隔はどれか。",
    "options": [
        {"text": "20MHzで非干渉チャネル"},
        {"text": "5MHz"},
        {"text": "10MHz"},
        {"text": "25MHz"}
    ],
    "explanation": "5GHzの20MHzチャネルは20MHz間隔で配置、多数の非干渉チャネルを提供(UNIIバンドで20以上)。",
    "cheatsheet": "5GHz: 20MHz非干渉、40MHzで半減、80MHzで1/4、160MHzで最小化。"
},
{
    "category": "無線設計",
    "question": "シームレスローミングのためのAPカバーセル間の推奨オーバーラップはどれくらいか。",
    "options": [
        {"text": "15-20%のオーバーラップ"},
        {"text": "0%のオーバーラップ"},
        {"text": "50%のオーバーラップ"},
        {"text": "100%のオーバーラップ"}
    ],
    "explanation": "15-20%オーバーラップにより、クライアントは現在のAPの信号を失う前に次のAPに接続できる。",
    "cheatsheet": "オーバーラップ~20%でシームレスローミング。過度な同一チャネル干渉を避ける。"
},
{
    "category": "無線設計",
    "question": "300ユーザーの高密度環境で(APあたり30ユーザーと仮定)、必要なAP数はいくつか。",
    "options": [
        {"text": "10"},
        {"text": "5"},
        {"text": "300"},
        {"text": "15"}
    ],
    "explanation": "300ユーザー / 30ユーザー/AP = 10AP。高密度: 通常APあたり20-30同時ユーザー。",
    "cheatsheet": "AP数 = 総クライアント / クライアント/AP。エンタープライズ: 混合トラフィックで20-30/AP。"
},
{
    "category": "無線設計",
    "question": "同一チャネル干渉の主な原因は何か。",
    "options": [
        {"text": "オーバーラップカバーエリアで同一チャネルを使用する複数AP"},
        {"text": "Bluetoothデバイス"},
        {"text": "電子レンジのみ"},
        {"text": "物理的な壁"}
    ],
    "explanation": "同一チャネルAPのオーバーラップはCSMA/CA競合を引き起こし、そのチャネルの全デバイスのスループットを低下させる。",
    "cheatsheet": "隣接APに非干渉チャネルを割り当てる。5GHzでより多くのチャネルオプションを使用。"
},
{
    "category": "無線設計",
    "question": "5GHz(UNII-1,2,3)で20MHz非干渉チャネルは通常いくつ提供されるか。",
    "options": [
        {"text": "20チャネル以上"},
        {"text": "3チャネル"},
        {"text": "11チャネル"},
        {"text": "8チャネル"}
    ],
    "explanation": "5GHzはUNIIバンドにわたり多数のチャネルを提供(DFS環境で最大25以上の非干渉チャネル)。",
    "cheatsheet": "5GHz: UNII-1(36-48), UNII-2A(52-64), UNII-2C(100-144), UNII-3(149-165)。"
},
{
    "category": "無線設計",
    "question": "オフィス環境での5GHz APの典型的カバーエリア半径はどれくらいか。",
    "options": [
        {"text": "20-30メートル"},
        {"text": "50-100メートル"},
        {"text": "100メートル以上"},
        {"text": "5-10メートル"}
    ],
    "explanation": "5GHzは高周波による吸収で2.4GHzより短い。屋内では通常20-30m。",
    "cheatsheet": "2.4GHz: ~30-50m。5GHz: ~20-30m。5GHzは容量、2.4GHzはカバレッジに使用。"
},
{
    "category": "無線設計",
    "question": "多数のAPがある高密度デプロイではどのチャネル幅を使用すべきか。",
    "options": [
        {"text": "20MHz"},
        {"text": "160MHz"},
        {"text": "80MHz"},
        {"text": "40MHz"}
    ],
    "explanation": "狭いチャネル(20MHz)は高密度APデプロイでより多くの非干渉チャネルを提供。",
    "cheatsheet": "高密度: 20MHz(チャネル数多い)。低密度: 40/80MHz(APあたり速度高い)。"
},
{
    "category": "無線設計",
    "question": "2.4GHzラジオあたりの推奨最大クライアント数はいくつか。",
    "options": [
        {"text": "20-25クライアント"},
        {"text": "100クライアント"},
        {"text": "5クライアント"},
        {"text": "50クライアント"}
    ],
    "explanation": "2.4GHz: 共有メディアの競合により20-25クライアント推奨。5GHzはチャネルが多いためより多くサポート。",
    "cheatsheet": "2.4GHz/AP: ~20-25クライアント。5GHz: ~30-40。バンドステアリングで5GHzに誘導。"
},
{
    "category": "無線設計",
    "question": "5GHzのDFS(Dynamic Frequency Selection)は何を可能にするか。",
    "options": [
        {"text": "レーダーが検出されない場合にレーダーチャネルを使用すること"},
        {"text": "自動的に2.4GHzに切り替えること"},
        {"text": "送信電力を増加すること"},
        {"text": "未使用チャネルを無効化すること"}
    ],
    "explanation": "DFSは5GHzの気象/レーダーチャネル(52-144)をレーダー信号を監視し検出時に回避しつつ使用可能にする。",
    "cheatsheet": "DFSチャネル(52-144)は~12チャネル追加だがレーダー検出機能が必要。"
},
{
    "category": "無線設計",
    "question": "2.4GHzで40MHzチャネルを使用した場合の影響は何か。",
    "options": [
        {"text": "非干渉40MHzチャネルが1つのみ(容量が低下)"},
        {"text": "20MHzより良い容量"},
        {"text": "チャネル数への影響なし"},
        {"text": "範囲が2倍になる"}
    ],
    "explanation": "2.4GHzは実質1つの40MHz幅チャネルのみをサポートし、チャネルの多様性が失われる。",
    "cheatsheet": "2.4GHzで40MHzは避ける。5GHzでチャネル空間が豊富な場合に使用。"
},
{
    "category": "無線設計",
    "question": "100ユーザーで総容量1Gbpsの場合、ユーザーあたりの推定帯域はどれくらいか。",
    "options": [
        {"text": "ユーザーあたり10Mbps"},
        {"text": "ユーザーあたり100Mbps"},
        {"text": "ユーザーあたり1Gbps"},
        {"text": "ユーザーあたり1Mbps"}
    ],
    "explanation": "1Gbps / 100ユーザー = ユーザーあたり10Mbps(均等分散と仮定)。",
    "cheatsheet": "ユーザーあたり帯域 = 総容量 / 同時ユーザー数。"
},
{
    "category": "無線設計",
    "question": "オフィスでAPはどこに設置するのが理想的か。",
    "options": [
        {"text": "天井設置で最良の全方向カバレッジ"},
        {"text": "机の下"},
        {"text": "サーバー室のみ"},
        {"text": "壁の後ろ"}
    ],
    "explanation": "天井設置は見通し線をクリアにし、ほとんどの環境で最良のカバレッジパターンを提供。",
    "cheatsheet": "最適カバレッジのためにAPを天井の高さに設置。金属物の近くは避ける。"
},
{
    "category": "無線設計",
    "question": "バンドステアリングとは何か。",
    "options": [
        {"text": "デュアルバンドクライアントを2.4GHzではなく5GHzに誘導すること"},
        {"text": "異なる5GHzチャネル間の選択"},
        {"text": "2.4GHzチャネル間の切り替え"},
        {"text": "2.4GHzラジオの無効化"}
    ],
    "explanation": "バンドステアリングは対応クライアントを5GHzに誘導し、2.4GHzの混雑を緩和して全体のパフォーマンスを向上。",
    "cheatsheet": "バンドステアリングを有効化して混雑した2.4GHzから5GHzへデュアルバンドクライアントをオフロード。"
},
# Q96-Q110: VPN/IPsec (15 Qs)
{
    "category": "VPN/IPsec",
    "question": "ESP(Encapsulating Security Payload)トランスポートモードのオーバーヘッドはどれくらいか。",
    "options": [
        {"text": "約20-30バイト"},
        {"text": "0バイト"},
        {"text": "100バイト"},
        {"text": "50バイト"}
    ],
    "explanation": "ESPトランスポート: ESPヘッダ(8B) + IV(8-16B) + パディング + ESPトレーラ(2-16B) + ICV(10-16B)。",
    "cheatsheet": "トランスポートオーバーヘッド: ~20-30B。トンネルオーバーヘッド: ~50-70B(新IPヘッダ追加)。"
},
{
    "category": "VPN/IPsec",
    "question": "100MbpsリンクでIPsecトンネルモード稼働時の概算最大スループットはどれくらいか。",
    "options": [
        {"text": "95-97Mbps(オーバーヘッド考慮)"},
        {"text": "100Mbps"},
        {"text": "50Mbps"},
        {"text": "80Mbps"}
    ],
    "explanation": "IPsecオーバーヘッドは小さいがCPU暗号化がスループットを制限。ハードウェアアクセラレーションでほぼワイヤスピード達成可。",
    "cheatsheet": "ソフトウェアIPsec: リンク速度の50-80%。ハードウェアアクセラレーション: 95%以上。暗号による。"
},
{
    "category": "VPN/IPsec",
    "question": "IPsec SAの一般的なライフタイム(フェーズ2)はどれくらいか。",
    "options": [
        {"text": "1時間(3600秒)または100MB"},
        {"text": "24時間"},
        {"text": "1分"},
        {"text": "制限なし"}
    ],
    "explanation": "フェーズ2SAデフォルト: 1時間/100MB(いずれか先)。短いライフタイム = キー変更多 = より安全。",
    "cheatsheet": "フェーズ1: 24時間/1GB。フェーズ2: 1時間/100MB。短い = より安全、オーバーヘッド増。"
},
{
    "category": "VPN/IPsec",
    "question": "IPsecで最良のパフォーマンスを提供する暗号方式はどれか。",
    "options": [
        {"text": "AES-GCM(暗号化+認証の統合)"},
        {"text": "3DES"},
        {"text": "Blowfish"},
        {"text": "RC4"}
    ],
    "explanation": "AES-GCMは1つの操作で暗号化と完全性の両方を提供し、オーバーヘッドを削減。AES-NIハードウェアアクセラレーションが有効。",
    "cheatsheet": "AES-GCM: 高速、暗号+認証統合。AES-CBC + SHA: 別操作、オーバーヘッド大。"
},
{
    "category": "VPN/IPsec",
    "question": "IPsecで双方向通信のために作成されるSA数はいくつか。",
    "options": [
        {"text": "2(各方向に1つ)"},
        {"text": "1"},
        {"text": "4"},
        {"text": "0"}
    ],
    "explanation": "IPsec SAは単方向。双方向通信には2SA(インバウンド+アウトバウンド)が必要。",
    "cheatsheet": "各SA = 1方向。双方向 = 2SA。各にSPI、キー、パラメータが必要。"
},
{
    "category": "VPN/IPsec",
    "question": "IPsecフェーズ1の一般的なライフタイムはどれくらいか。",
    "options": [
        {"text": "86400秒(24時間)"},
        {"text": "3600秒(1時間)"},
        {"text": "300秒(5分)"},
        {"text": "期限なし"}
    ],
    "explanation": "フェーズ1(IKE SA)デフォルトライフタイムは24時間。期限切れ前に管理チャネルを維持するため再キーされる。",
    "cheatsheet": "フェーズ1(IKE SA): 24時間デフォルト。フェーズ2(IPsec SA): 1時間デフォルト。"
},
{
    "category": "VPN/IPsec",
    "question": "1500バイトアンダーレイでのIPsecトンネルの最大MTUはどれくらいか。",
    "options": [
        {"text": "1430-1440バイト(IPsecオーバーヘッド後)"},
        {"text": "1500バイト"},
        {"text": "1600バイト"},
        {"text": "1280バイト"}
    ],
    "explanation": "トンネルモードは~50-70バイトオーバーヘッドを追加。実効MTU = 1500 - 60-70 = ~1430-1440バイト。",
    "cheatsheet": "トンネルMTU = アンダーレイMTU - オーバーヘッド。通常1500BリンクでIPsecは1420-1440。"
},
{
    "category": "VPN/IPsec",
    "question": "AES-256暗号化で50MbpsスループットのVPNトンネルをサポートする場合、CPUの考慮点は何か。",
    "options": [
        {"text": "ハードウェア暗号アクセラレーション(AES-NI)が推奨される"},
        {"text": "任意のCPUで50Mbps対応可能"},
        {"text": "ソフトウェア暗号化で常に十分"},
        {"text": "専用ハードウェア機器のみが動作可能"}
    ],
    "explanation": "AES-256ソフトウェアは最新CPUで50Mbpsを処理可能だが、AES-NIハードウェアアクセラレーションが信頼性のために推奨。",
    "cheatsheet": "AES-NIは暗号化をCPUハードウェアにオフロード。VPNゲートウェイでAES-NI対応を確認。"
},
{
    "category": "VPN/IPsec",
    "question": "IKEv1メインモードとアグレッシブモードの違いは何か。",
    "options": [
        {"text": "メインモード: 6メッセージ、ID保護。アグレッシブ: 3メッセージ、ID公開"},
        {"text": "セキュリティに差はない"},
        {"text": "アグレッシブの方が安全"},
        {"text": "メインモードはパケット数が少ない"}
    ],
    "explanation": "メインモードは暗号化交換でIDを保護。アグレッシブモードは高速だがIDを平文で公開。",
    "cheatsheet": "メインモード: 安全、6メッセージ。アグレッシブ: 高速、3メッセージ、ID可視。"
},
{
    "category": "VPN/IPsec",
    "question": "IPsecリプレイ保護の目的は何か。",
    "options": [
        {"text": "攻撃者がキャプチャしたパケットを再送信することを防止する"},
        {"text": "パケットフラグメンテーションを防止する"},
        {"text": "パケット処理を高速化する"},
        {"text": "パケットを圧縮する"}
    ],
    "explanation": "リプレイ保護はシーケンス番号ウィンドウを使用して重複パケットを拒否し、リプレイ攻撃を防止。",
    "cheatsheet": "アンチリプレイウィンドウがシーケンス番号をチェック。範囲外または重複パケットは破棄。"
},
{
    "category": "VPN/IPsec",
    "question": "AES-256-CBCが1400バイトペイロードに追加する暗号化オーバーヘッドはどれくらいか。",
    "options": [
        {"text": "約32-48バイト"},
        {"text": "256バイト"},
        {"text": "0バイト"},
        {"text": "10バイト"}
    ],
    "explanation": "AES-CBC: IV(16B) + パディング(最大16B) + ESPヘッダ(8B) + ICV(16B) = ~40-56バイト総オーバーヘッド。",
    "cheatsheet": "AESブロック = 16バイト。パディングでブロック境界に整列。IV = 1ブロック。"
},
{
    "category": "VPN/IPsec",
    "question": "中堅ルータで同時にサポートできるVPNトンネル数は概ねどれくらいか。",
    "options": [
        {"text": "50-200トンネル"},
        {"text": "10,000トンネル以上"},
        {"text": "5トンネル"},
        {"text": "無制限"}
    ],
    "explanation": "中堅エンタープライズルータは50-200同時トンネルをサポート。ハイエンド機器は数千。",
    "cheatsheet": "仕様確認: 同時トンネル数、暗号化時スループット、最大SA数。"
},
{
    "category": "VPN/IPsec",
    "question": "IPsecのPFS(Perfect Forward Secrecy)とは何か。",
    "options": [
        {"text": "各フェーズ2で新しい鍵素材を生成し、1つの鍵の漏洩が他に影響しないようにすること"},
        {"text": "暗号化鍵を暗号化すること"},
        {"text": "全セッションで同じ鍵を使用すること"},
        {"text": "証明書検証方法"}
    ],
    "explanation": "PFS(フェーズ2のDiffie-Hellman)は各IPsec SAが固有の鍵素材を使用することを保証し、漏洩影響を制限。",
    "cheatsheet": "PFS有効 = フェーズ2で新DH鍵交換。推奨: DHグループ14以上。"
},
{
    "category": "VPN/IPsec",
    "question": "AESおよびSHA-256使用時のIPsecの帯域オーバーヘッド率は概ねどれくらいか。",
    "options": [
        {"text": "約3-5%のオーバーヘッド"},
        {"text": "50%のオーバーヘッド"},
        {"text": "0%のオーバーヘッド"},
        {"text": "20%のオーバーヘッド"}
    ],
    "explanation": "IPsecはパケットあたり~50-70バイト追加。1500バイトMTUの場合: 50/1500 ~ 3.3%オーバーヘッド。",
    "cheatsheet": "オーバーヘッド% = (オーバーヘッドバイト / MTU) x 100。小さいパケット = 高い割合。"
},
{
    "category": "VPN/IPsec",
    "question": "サイトツーサイトVPNとは何か。",
    "options": [
        {"text": "2つのネットワーク拠点(オフィス、データセンター)を接続する永続的なトンネル"},
        {"text": "リモートワーカー用の一時接続"},
        {"text": "暗号化されたWebセッション"},
        {"text": "P2Pファイル共有トンネル"}
    ],
    "explanation": "サイトツーサイトVPNは永続的なIPsecトンネルでネットワーク全体をルーター間で接続。",
    "cheatsheet": "サイトツーサイト: ネットワーク間接続。リモートアクセス: クライアント-ネットワーク。常時接続トンネル。"
},
# Q111-Q120: Load Balancing (10 Qs)
{
    "category": "ロードバランシング",
    "question": "ウェイト付きラウンドロビン(ウェイト: 5, 3, 2, 1)で4サーバーの場合、最初のサーバーの接続割合はどれくらいか。",
    "options": [
        {"text": "50%"},
        {"text": "25%"},
        {"text": "33%"},
        {"text": "10%"}
    ],
    "explanation": "総ウェイト = 5+3+2+1 = 11。最初のサーバー: 5/11 = ~45%(~50%)。比率: 5:3:2:1。",
    "cheatsheet": "サーバー割合 = 自ウェイト / 総ウェイトの合計。"
},
{
    "category": "ロードバランシング",
    "question": "Webサーバーのヘルスチェック間隔の推奨はどれくらいか。",
    "options": [
        {"text": "5-10秒"},
        {"text": "1秒"},
        {"text": "60秒"},
        {"text": "5分"}
    ],
    "explanation": "5-10秒は応答性とオーバーヘッドのバランス。速すぎるとリソース浪費、遅すぎると障害を見逃す。",
    "cheatsheet": "Web: 5-10秒。DB: 10-30秒。重要: 2-5秒。非重要: 30-60秒。"
},
{
    "category": "ロードバランシング",
    "question": "サーバーがヘルスチェックに3秒で応答する場合、タイムアウトをどれくらいに設定すべきか。",
    "options": [
        {"text": "3秒より大きく(例: 5秒)"},
        {"text": "1秒"},
        {"text": "正確に3秒"},
        {"text": "10秒"}
    ],
    "explanation": "タイムアウトは通常応答時間+余裕を超える必要がある。応答3秒ならタイムアウト5秒以上に設定。",
    "cheatsheet": "タイムアウト = 通常応答時間 x 1.5〜2。ネットワーク変動のバッファを追加。"
},
{
    "category": "ロードバランシング",
    "question": "10,000リクエストで5サーバーをラウンドロビン使用時、各サーバーの処理数はいくつか。",
    "options": [
        {"text": "各2,000"},
        {"text": "各5,000"},
        {"text": "各1,000"},
        {"text": "各10,000"}
    ],
    "explanation": "シンプルラウンドロビン: 10000/5 = 各2000リクエスト(均等分散と仮定)。",
    "cheatsheet": "ラウンドロビン: リクエスト/サーバー数 = サーバーあたり(割り切れる場合)。"
},
{
    "category": "ロードバランシング",
    "question": "サーバーをプールから除外するまでの最小異常応答回数はいくつが一般的か。",
    "options": [
        {"text": "3回連続失敗"},
        {"text": "1回失敗"},
        {"text": "10回失敗"},
        {"text": "除外されない"}
    ],
    "explanation": "ほとんどのロードバランサーは2-3回連続失敗(異常閾値)でサーバーをダウンとマーク。",
    "cheatsheet": "閾値設定: unhealthy_threshold(2-3)とhealthy_threshold(2-3)。"
},
{
    "category": "ロードバランシング",
    "question": "最小接続ロードバランシングとは何か。",
    "options": [
        {"text": "新リクエストをアクティブ接続が最も少ないサーバーに振り分けること"},
        {"text": "全トラフィックを最速サーバーに送信すること"},
        {"text": "クライアントIPハッシュで分散すること"},
        {"text": "ランダム分散"}
    ],
    "explanation": "最小接続はリアルタイム負荷を考慮し、リクエスト処理時間が大きく異なる場合に最適。",
    "cheatsheet": "最小接続 = 可変リクエスト時間に最適。ラウンドロビン = 同等な時間に最適。"
},
{
    "category": "ロードバランシング",
    "question": "ロードバランサーが1000RPSを処理し4サーバー(各最大300RPS)の場合、この構成は十分か。",
    "options": [
        {"text": "はい、4 x 300 = 1200RPSの容量 > 1000RPSの需要"},
        {"text": "いいえ、1サーバーは300RPSしか処理できない"},
        {"text": "全リクエストが等しい場合のみ"},
        {"text": "いいえ、5サーバーが必要"}
    ],
    "explanation": "総容量 = 4 x 300 = 1200RPS。需要 = 1000RPS。ヘッドルーム = 200RPS(20%)。十分。",
    "cheatsheet": "必要サーバー数 = ceil(ピークRPS / 1サーバー最大RPS) + N-1冗長性。"
},
{
    "category": "ロードバランシング",
    "question": "送信元IPハッシュロードバランシングは何に使用されるか。",
    "options": [
        {"text": "同じクライアントが常に同じサーバーに到達するよう保証(セッション永続性)"},
        {"text": "応答時間による分散"},
        {"text": "特定IPのブロック"},
        {"text": "クライアントIPの暗号化"}
    ],
    "explanation": "IPハッシュはクライアントIPを特定サーバーにマッピングし、クッキーなしでセッションアフィニティを提供。",
    "cheatsheet": "IPハッシュ = クッキーなしのセッション永続性。ハッシュ = 一貫性のあるマッピング。"
},
{
    "category": "ロードバランシング",
    "question": "データベースサーバーの推奨ヘルスチェックは何か。",
    "options": [
        {"text": "軽量クエリ(SELECT 1など)"},
        {"text": "フルテーブルスキャン"},
        {"text": "pingのみ"},
        {"text": "ヘルスチェック不要"}
    ],
    "explanation": "軽量クエリはDBの機能を検証。pingはネットワーク到達性のみ、サービス健全性は確認できない。",
    "cheatsheet": "DBヘルスチェック: 単純なSELECTクエリ。Web: HTTP GET to ヘルスエンドポイント。TCP: ポートチェック。"
},
{
    "category": "ロードバランシング",
    "question": "レイヤ7(アプリケーション)ロードバランサのレイヤ4に対する利点は何か。",
    "options": [
        {"text": "コンテンツベースルーティング、SSL終端、HTTPヘッダ検査"},
        {"text": "高速な処理"},
        {"text": "低コスト"},
        {"text": "シンプルな設定"}
    ],
    "explanation": "L7 LBはHTTP(URL、ヘッダ、クッキー)を理解し、インテリジェントなルーティングを可能にする。L4はIP/ポートのみ。",
    "cheatsheet": "L4: TCP/UDP、高速、低コスト。L7: HTTP対応、コンテンツルーティング、SSL終端、低速。"
},
# Q121 - last one (checking index...)
# Actually we have 121 Qs total. Let me verify the count matches.
]

# Let me verify
print(f"T_CALC entries: {len(T_CALC)}")

# ============ SUBJECT-B TRAINING TRANSLATIONS (100 Qs) ============
T_SUBJECT = [
# Q0: Network Design
{
    "category": "ネットワーク設計",
    "question": "3棟の建物に500人の従業員がいる企業のキャンパスネットワークに最適なアーキテクチャはどれか。",
    "options": [
        {"text": "3層(コア、ディストリビューション、アクセス)にファイバーバックボーン"},
        {"text": "1台の大規模スイッチによるフラットネットワーク"},
        {"text": "全デバイス間のポイントツーポイントリンク"},
        {"text": "ワイヤレスオンリーデプロイ"}
    ],
    "explanation": "3層はスケーラビリティ、冗長性、管理性を提供。ファイバーバックボーンが建物を接続。"
},
# Q1: Network Design
{
    "category": "ネットワーク設計",
    "question": "データセンターにおけるスパインリーフアーキテクチャとは何か。",
    "options": [
        {"text": "全リーフがイーストウェストトラフィックのために全スパインに接続する2層設計"},
        {"text": "コア、ディストリビューション、アクセスの従来型3層"},
        {"text": "全サーバーを接続する単一スイッチ"},
        {"text": "データセンター用ワイヤレスオーバーレイ"}
    ],
    "explanation": "スパインリーフは全リーフ間で低遅延で予測可能なイーストウェストトラフィックパターンと等コストパスを提供。"
},
# Q2: Network Design
{
    "category": "ネットワーク設計",
    "question": "20ユーザーの支社が本社との接続性を必要としている。最もコスト効果の高い設計はどれか。",
    "options": [
        {"text": "ブロードバンドインターネット + サイトツーサイトVPNバックアップのSD-WAN"},
        {"text": "専用回線のみ"},
        {"text": "複数のMPLS回線"},
        {"text": "衛星接続"}
    ],
    "explanation": "ブロードバンドSD-WANは小規模拠点にコスト効果が高く、VPNでセキュリティを確保。専用回線は小規模拠点には高コスト。"
},
# Q3: Network Design
{
    "category": "ネットワーク設計",
    "question": "エンタープライズコアスイッチの推奨冗長性レベルはどれか。",
    "options": [
        {"text": "アクティブ/スタンバイまたはアクティブ/アクティブのデュアル冗長コアスイッチ"},
        {"text": "単一コアスイッチ"},
        {"text": "常に3台以上のコアスイッチ"},
        {"text": "冗長性は不要"}
    ],
    "explanation": "デュアルコアスイッチは単一障害点を排除。アクティブ/アクティブは負荷分散、アクティブ/スタンバイはフェイルオーバーを提供。"
},
# Q4: Network Design
{
    "category": "ネットワーク設計",
    "question": "人事、財務、エンジニアリング、ゲスト部門がある企業のネットワークをどのようにセグメント化すべきか。",
    "options": [
        {"text": "各部門に別VLAN、VLAN間ルーティングとACLで制御"},
        {"text": "全員に1つのフラットネットワーク"},
        {"text": "部門ごとに物理的に別スイッチ"},
        {"text": "ゲストネットワークのみ分離"}
    ],
    "explanation": "VLAN + ACLで論理的分離を提供。財務/人事は制限付きアクセス、エンジニアリングは開発リソース、ゲストはインターネットのみ。"
},
# Q5: Network Design
{
    "category": "ネットワーク設計",
    "question": "キャンパス建物間のファイバーリンクの最大距離はどれくらいか。",
    "options": [
        {"text": "マルチモードで最大2km、シングルモードで40km以上"},
        {"text": "100メートル"},
        {"text": "500メートル"},
        {"text": "10メートル"}
    ],
    "explanation": "マルチモードファイバ: 1Gbpsで最大2km。シングルモード: 10-40km以上。銅線: 100mに制限。"
},
# Q6: Network Design
{
    "category": "ネットワーク設計",
    "question": "200サーバーのデータセンターで最良のイーストウェストトラフィックフローを提供するネットワークトポロジはどれか。",
    "options": [
        {"text": "スパインリーフ(Closファブリック)"},
        {"text": "従来型3層"},
        {"text": "フラットレイヤ2ネットワーク"},
        {"text": "ハブアンドスポーク"}
    ],
    "explanation": "スパインリーフは任意の2サーバー間で均一な遅延(1ホップリーフ-スパイン-リーフ)を提供し、モダンなワークロードに最適。"
},
# Q7: Network Design
{
    "category": "ネットワーク設計",
    "question": "ネットワーク設計の最初のステップは何か。",
    "options": [
        {"text": "要件収集(ユーザー数、アプリケーション、性能、予算)"},
        {"text": "機器購入"},
        {"text": "VLAN設定"},
        {"text": "監視設定"}
    ],
    "explanation": "要件収集が範囲を定義: ユーザー数、アプリケーション、帯域要件、拡張計画、予算、制約。"
},
# Q8: Network Design
{
    "category": "ネットワーク設計",
    "question": "キャンパス設計で各ディストリビューションスイッチに接続するアクセススイッチ数はいくつが適切か。",
    "options": [
        {"text": "ポート密度と冗長性要件に基づく(通常4-8台)"},
        {"text": "1台のみ"},
        {"text": "可能な限り多数"},
        {"text": "2台以下"}
    ],
    "explanation": "通常: ディストリビューションペアあたり4-8アクセススイッチ、アップリンクで冗長性と十分な帯域を確保。"
},
# Q9: Network Design
{
    "category": "ネットワーク設計",
    "question": "ネットワーク設計における高可用性(HA)とは何か。",
    "options": [
        {"text": "冗長性とフェイルオーバーでダウンタイムを最小化する設計"},
        {"text": "最も高価な機器を使用すること"},
        {"text": "バックアップインターネット接続のみを持つこと"},
        {"text": "予備部品を在庫すること"}
    ],
    "explanation": "HAは冗長ハードウェア、リンク、プロトコル(VRRP, HSRP)、フェイルオーバーメカニズムを組み合わせて99.99%以上の稼働率を実現。"
},
# Q10: Network Design
{
    "category": "ネットワーク設計",
    "question": "VoIP導入を計画している企業で最も重要な設計考慮事項は何か。",
    "options": [
        {"text": "音声トラフィックのQoS優先制御と十分な帯域確保"},
        {"text": "スイッチ追加のみ"},
        {"text": "音声にワイヤレスのみを使用"},
        {"text": "MTUサイズの増加"}
    ],
    "explanation": "VoIPにはQoS(EF/DSCP 46)、低遅延(150ms未満)、低ジッタ(30ms未満)、専用または優先VLANが必要。"
},
# Q11: Network Design
{
    "category": "ネットワーク設計",
    "question": "アクセス層とディストリビューション層間の推奨アップリンク帯域はどれくらいか。",
    "options": [
        {"text": "最低10Gbps(またはそれ以上に集約)"},
        {"text": "100Mbps"},
        {"text": "1Gbpsで常に十分"},
        {"text": "アクセスポートと同じ速度"}
    ],
    "explanation": "アップリンクは最大20:1のオーバーサブスクリプションにすべき。48 x 1Gbpsアクセス = 10Gbps以上のアップリンクが必要。"
},
# Q12: Network Design
{
    "category": "ネットワーク設計",
    "question": "単一デバイスの障害が完全なネットワーク停止を引き起こしてはならないとする設計原則はどれか。",
    "options": [
        {"text": "単一障害点の排除(No Single Point of Failure)"},
        {"text": "防御の深層化(Defense in Depth)"},
        {"text": "最小権限(Least Privilege)"},
        {"text": "職務の分離(Separation of Duties)"}
    ],
    "explanation": "冗長性(デュアルリンク、デュアルスイッチ、デュアルISP)による単一障害点の排除は信頼性の高い設計の基盤。"
},
# Q13: Network Design
{
    "category": "ネットワーク設計",
    "question": "ネットワーク設計におけるデマルケーションポイント(demarc)の目的は何か。",
    "options": [
        {"text": "事業者の責任範囲が終わり顧客の責任範囲が始まる点"},
        {"text": "ファイアウォール配置ポイント"},
        {"text": "サーバー室の場所"},
        {"text": "ワイヤレスカバレッジ境界"}
    ],
    "explanation": "デマルク(スマートジャックまたはNIU)はキャリアネットワークと顧客ネットワークの境界を定義。"
},
# Q14: Network Design
{
    "category": "ネットワーク設計",
    "question": "ネットワーク設計におけるオーバーサブスクリプションとは何か。",
    "options": [
        {"text": "アップリンクの帯域を総需要が超過すること"},
        {"text": "帯域が需要を超過すること"},
        {"text": "スイッチを使いすぎること"},
        {"text": "容量を過剰にプロビジョニングすること"}
    ],
    "explanation": "一般的なオーバーサブスクリプション比: アクセス-ディストリビューション 20:1、ディストリビューション-コア 4:1。ピーク使用量を計画。"
},
# Q15: Network Design
{
    "category": "ネットワーク設計",
    "question": "5ユーザーの拠点が本社へのセキュアなアクセスを必要としている場合、最適なアプローチはどれか。",
    "options": [
        {"text": "ブロードバンド + ZTNAでセキュリティ確保のSD-WAN"},
        {"text": "高価なMPLS回線"},
        {"text": "ダイヤルアップ接続"},
        {"text": "接続不要"}
    ],
    "explanation": "小規模拠点はブロードバンドSD-WANとゼロトラストセキュリティが適切。MPLSは5ユーザーには過剰。"
},
# Q16: Network Design
{
    "category": "ネットワーク設計",
    "question": "ネットワークコンバージェンス時間とは何か、なぜ重要か。",
    "options": [
        {"text": "障害後にネットワークが適応する時間; 重要アプリでは短いほど良い"},
        {"text": "データの転送速度"},
        {"text": "デバイスの起動速度"},
        {"text": "デバイス設定の時間"}
    ],
    "explanation": "コンバージェンス時間は障害時の停止期間を決定。VoIPは50ms未満、データは数秒まで許容。"
},
# Q17: Network Design
{
    "category": "ネットワーク設計",
    "question": "ネットワークダイアグラムには何を含めるべきか。",
    "options": [
        {"text": "デバイス、接続、IPアドレス指定、VLAN、WANリンク"},
        {"text": "物理デバイス配置のみ"},
        {"text": "IPアドレスのみ"},
        {"text": "ワイヤレスカバレッジマップのみ"}
    ],
    "explanation": "完全なダイアグラムは運用とトラブルシューティングのためにトポロジ、アドレッシング、VLAN、ルーティング、WAN回線、デバイス役割を表示。"
},
# Q18: Network Design
{
    "category": "ネットワーク設計",
    "question": "複数VLANに500ユーザーがいる場合、DHCPをどのようにデプロイすべきか。",
    "options": [
        {"text": "集中DHCPサーバーにルーターのIPヘルパーでリレー"},
        {"text": "各スイッチにDHCP"},
        {"text": "全員に静的IP"},
        {"text": "VLANごとに1DHCPサーバー"}
    ],
    "explanation": "集中DHCPとリレーエージェント(ip helper-address)で管理を簡素化しつつ複数サブネットをサポート。"
},
# Q19: Network Design
{
    "category": "ネットワーク設計",
    "question": "ネットワークベースラインは設計で何に使用されるか。",
    "options": [
        {"text": "設計が要件を満たすことを検証するための通常性能メトリクスの確立"},
        {"text": "初期パスワードの設定"},
        {"text": "機器ベンダーの選択"},
        {"text": "VLAN IDの定義"}
    ],
    "explanation": "デプロイ後のベースラインは設計が性能目標を満たすことを検証し、将来のトラブルシューティングの参照を提供。"
},
# Q20-Q39: Protocol Analysis (20 Qs)
{
    "category": "プロトコル分析",
    "question": "パケットキャプチャでクライアントからのTCP SYNは見えるがサーバーからのSYN-ACKがない。最も考えられる原因は何か。",
    "options": [
        {"text": "サーバーがダウンしているかファイアウォールが接続をブロックしている"},
        {"text": "DNS解決エラー"},
        {"text": "ルーティングループ"},
        {"text": "ARP障害"}
    ],
    "explanation": "SYN-ACKがないことはSYNがサーバーに届いていないか、サーバーが応答できない(ファイアウォール、サーバーダウン、ACL)ことを示す。"
},
{
    "category": "プロトコル分析",
    "question": "キャプチャでTCP RST(Reset)フラグが表示された場合、何を示すか。",
    "options": [
        {"text": "異常な接続終了またはポートがリスニングしていない"},
        {"text": "正常な接続終了"},
        {"text": "フロー制御シグナル"},
        {"text": "暗号化リクエスト"}
    ],
    "explanation": "RSTは接続を即座に終了。一般的な原因: ポートクローズ、ファイアウォール拒否、アプリケーションクラッシュ、タイムアウト。"
},
{
    "category": "プロトコル分析",
    "question": "同じIPに対する多数のARPリクエストが見える。これは何を示すか。",
    "options": [
        {"text": "ARPスプーフィング攻撃またはIP競合の可能性"},
        {"text": "正常なARP動作"},
        {"text": "DHCP障害"},
        {"text": "DNS問題"}
    ],
    "explanation": "1つのIPに対する過剰なARPリクエストは Gratuitous ARP(競合)またはスプーフィング(攻撃者がIPを主張)を示唆。"
},
{
    "category": "プロトコル分析",
    "question": "WiresharkキャプチャでHTTPトラフィックを表示するフィルタはどれか。",
    "options": [
        {"text": "http"},
        {"text": "tcp.port(80)"},
        {"text": "http && tcp"},
        {"text": "port 80"}
    ],
    "explanation": "'http'フィルタは全HTTPトラフィックをキャプチャ。'tcp.port(80)'も動作するが specificity が低い。両方有効。"
},
{
    "category": "プロトコル分析",
    "question": "キャプチャで多数のTCP再送が見られる場合、何を示すか。",
    "options": [
        {"text": "パケットロス、輻輳、またはパス上の高遅延"},
        {"text": "正常な動作"},
        {"text": "アプリケーションエラー"},
        {"text": "暗号化オーバーヘッド"}
    ],
    "explanation": "再送は送信者がタイムアウト内にACKを受信できなかったことを示し、ロスまたは輻輳を示唆。"
},
{
    "category": "プロトコル分析",
    "question": "ICMP Destination Unreachable(Port Unreachable)が表示された場合、何を意味するか。",
    "options": [
        {"text": "ターゲットポートでリスニングしているアプリケーションがない"},
        {"text": "ホストの電源がオフ"},
        {"text": "ネットワークが輻輳している"},
        {"text": "ファイアウォールがパケットをサイレントドロップ"}
    ],
    "explanation": "Port Unreachableはホストがパケットを受信したがそのポートにバインドされたアプリケーションがないことを意味。"
},
{
    "category": "プロトコル分析",
    "question": "TCP 3ウェイハンドシェイクのキャプチャシーケンスはどれか。",
    "options": [
        {"text": "SYN -> SYN-ACK -> ACK"},
        {"text": "ACK -> SYN -> FIN"},
        {"text": "SYN -> FIN -> ACK"},
        {"text": "RST -> SYN -> ACK"}
    ],
    "explanation": "標準TCP接続: クライアントSYN、サーバーSYN-ACK、クライアントACK。これで接続を確立。"
},
{
    "category": "プロトコル分析",
    "question": "キャプチャでTCPウィンドウサイズが0の場合、何を示すか。",
    "options": [
        {"text": "受信バッファが満杯; 送信側は待機する必要がある"},
        {"text": "接続が切断中"},
        {"text": "送信データがない"},
        {"text": "フロー制御が無効"}
    ],
    "explanation": "ゼロウィンドウは受信側がこれ以上データを受信できないことを意味。送信側はウィンドウアップデートを待つ。"
},
{
    "category": "プロトコル分析",
    "question": "再送なしで重複ACKが見られる場合、どのTCPメカニズムが動作している可能性が高いか。",
    "options": [
        {"text": "ファストリトランスミットがまさにトリガーされようとしている"},
        {"text": "接続が切断中"},
        {"text": "輻輳回避"},
        {"text": "スロースタート"}
    ],
    "explanation": "3つの重複ACKがファストリトランスミットをトリガーし、再送タイマー切れ前に回復を可能にする。"
},
{
    "category": "プロトコル分析",
    "question": "キャプチャしたパケットのTTL値は何を示すか。",
    "options": [
        {"text": "パケットが破棄されるまでの残りホップ数"},
        {"text": "経験した総遅延"},
        {"text": "パケットの送信時刻"},
        {"text": "暗号強度"}
    ],
    "explanation": "TTLは各ホップでデクリメント。tracerouteはこれを利用し、TTLを増加させたパケットを送信してパスをマッピング。"
},
{
    "category": "プロトコル分析",
    "question": "HTTPSキャプチャでHTTPコンテンツが見えないのはなぜか。",
    "options": [
        {"text": "TLS暗号化がペイロードを暗号化している"},
        {"text": "HTTPSはHTTPを使用しない"},
        {"text": "キャプチャツールが壊れている"},
        {"text": "HTTPSはUDPを使用する"}
    ],
    "explanation": "TLSはHTTPペイロードを暗号化。検査にはWiresharkでの復号用セッションキー(SSLKEYLOGFILE)が必要。"
},
{
    "category": "プロトコル分析",
    "question": "DNS応答のNXDOMAINは何を示すか。",
    "options": [
        {"text": "ドメイン名が存在しない"},
        {"text": "DNSサーバーがダウン"},
        {"text": "ネットワークに到達不可"},
        {"text": "ドメインがブロックされている"}
    ],
    "explanation": "NXDOMAIN(rcode 3)は問い合わせた名前のレコードが存在しないことを意味。"
},
{
    "category": "プロトコル分析",
    "question": "多くのフラグメント化されたIPパケットが見られる。原因として考えられるものは何か。",
    "options": [
        {"text": "MTU不一致、VPNオーバーヘッド、またはアプリケーションが大ペイロードを送信"},
        {"text": "正常なTCP動作"},
        {"text": "暗号化エラー"},
        {"text": "DNS解決エラー"}
    ],
    "explanation": "フラグメンテーションはパケットがパスMTUを超える場合に発生。VPNオーバーヘッドやジャンボフレームが1500B MTUに遭遇する場合に一般的。"
},
{
    "category": "プロトコル分析",
    "question": "MSSオプション付きのTCPハンドシェイクは何に使用されるか。",
    "options": [
        {"text": "接続の最大セグメントサイズのネゴシエーション"},
        {"text": "再送タイムアウトの設定"},
        {"text": "暗号化の有効化"},
        {"text": "ウィンドウサイズの設定"}
    ],
    "explanation": "MSSオプション(SYN/SYN-ACK内)はピアに最大TCPペイロードサイズを伝え、過大セグメントを防止。"
},
{
    "category": "プロトコル分析",
    "question": "ICMP Time Exceededメッセージが見られる場合、何を示すか。",
    "options": [
        {"text": "パケットのTTLがゼロに達した(tracerouteやルーティングループで一般的)"},
        {"text": "認証エラー"},
        {"text": "DNSタイムアウト"},
        {"text": "TCP接続拒否"}
    ],
    "explanation": "TTL超過はパケットが多すぎるホップを通過したことを意味。tracerouteはこれを意図的に使用。通常トラフィックではループを示唆。"
},
{
    "category": "プロトコル分析",
    "question": "Wiresharkで特定IPのトラフィックを表示するフィルタはどれか。",
    "options": [
        {"text": "ip.addr == 192.168.1.1"},
        {"text": "src 192.168.1.1"},
        {"text": "host = 192.168.1.1"},
        {"text": "from 192.168.1.1"}
    ],
    "explanation": "ip.addrは送信元と宛先の両方にマッチ。片方向のみはip.srcまたはip.dstを使用。"
},
{
    "category": "プロトコル分析",
    "question": "DHCP OFFERメッセージには何が含まれるか。",
    "options": [
        {"text": "提供IPアドレス、サブネットマスク、リース時間、DHCPサーバー識別子"},
        {"text": "クライアントのMACアドレスのみ"},
        {"text": "DNSサーバーIPのみ"},
        {"text": "ルーター設定"}
    ],
    "explanation": "DHCP OFFERには: yiaddr(提供IP)、サブネットマスク、リース時間、サーバー識別子、オプショナルパラメータが含まれる。"
},
{
    "category": "プロトコル分析",
    "question": "HTTP 301/302応答が見られる場合、何が起きているか。",
    "options": [
        {"text": "別の場所へのURLリダイレクト"},
        {"text": "サーバーエラー"},
        {"text": "コンテンツ圧縮"},
        {"text": "認証チャレンジ"}
    ],
    "explanation": "301 = 恒久リダイレクト、302 = 一時リダイレクト。Locationヘッダが新しいURLを指定。"
},
{
    "category": "プロトコル分析",
    "question": "キャプチャ内のOSPF Helloパケットは何を検証するか。",
    "options": [
        {"text": "ネイバー検出とパラメータ(hello/dead間隔、エリアID、認証)"},
        {"text": "ルート広告"},
        {"text": "データベース同期"},
        {"text": "エリアサマリ"}
    ],
    "explanation": "OSPF Helloはネイバーを検出し、パラメータの一致を検証。不一致パラメータは隣接関係を防止。"
},
{
    "category": "プロトコル分析",
    "question": "BGP UPDATEメッセージが見られる場合、何を広告しているか。",
    "options": [
        {"text": "到達可能ネットワークプレフィックスとパスアトリビュート"},
        {"text": "MACアドレス"},
        {"text": "ARPエントリ"},
        {"text": "DNSレコード"}
    ],
    "explanation": "BGP UPDATEはNLRI(プレフィックス)とパスアトリビュート(AS_PATH, NEXT_HOP, LOCAL_PREFなど)を搬送。"
},
# Q40-Q59: Troubleshooting (20 Qs)
{
    "category": "トラブルシューティング",
    "question": "ユーザーが外部Webサイトにアクセスできないが内部サーバーにはpingできる。最も考えられる問題は何か。",
    "options": [
        {"text": "DNS障害またはデフォルトゲートウェイの問題"},
        {"text": "スイッチの設定ミス"},
        {"text": "NATの問題"},
        {"text": "WAN障害"}
    ],
    "explanation": "内部接続が機能 = LANは正常。外部Web = DNS解決とデフォルトゲートウェイ/WANが必要。テスト: ping 8.8.8.8。"
},
{
    "category": "トラブルシューティング",
    "question": "ネットワークトラブルシューティングの最初のステップは何か。",
    "options": [
        {"text": "問題の特定(症状、範囲、影響ユーザー)"},
        {"text": "全デバイスの再起動"},
        {"text": "ケーブル交換"},
        {"text": "ベンダーサポートへの連絡"}
    ],
    "explanation": "構造化トラブルシューティング: 1)問題特定、2)情報収集、3)仮説、4)テスト、5)修正実装、6)検証。"
},
{
    "category": "トラブルシューティング",
    "question": "ユーザーからネットワークが遅いという報告がある。最初に使用すべきツールはどれか。",
    "options": [
        {"text": "遅延が発生する場所を特定するpingとtraceroute"},
        {"text": "スイッチの交換"},
        {"text": "フルセキュリティスキャンの実行"},
        {"text": "ファイアウォールの再起動"}
    ],
    "explanation": "ping/tracerouteは問題がローカル、LAN上、またはWANパス上のどこにあるかを迅速に特定。"
},
{
    "category": "トラブルシューティング",
    "question": "スイッチポートがup/downを繰り返している。考えられる原因は何か。",
    "options": [
        {"text": "物理層の問題(不良ケーブル、デュプレックス不一致、またはSTPループ)"},
        {"text": "ファイアウォールルール"},
        {"text": "DNS設定ミス"},
        {"text": "アプリケーションのバグ"}
    ],
    "explanation": "フラッピングポートは物理的な問題、デュプレックス不一致、またはBPDU関連問題(STP再収束)を示す。"
},
{
    "category": "トラブルシューティング",
    "question": "ユーザーがIPアドレスにはpingできるがWebサイト名ではアクセスできない。問題は何か。",
    "options": [
        {"text": "DNS解決エラー"},
        {"text": "ファイアウォールがICMPをブロック"},
        {"text": "ルーティング問題"},
        {"text": "MTU問題"}
    ],
    "explanation": "IPでのpingが機能 = ネットワーク正常。名前解決が失敗 = DNS問題。DNSサーバー設定とDNSサーバー状態を確認。"
},
{
    "category": "トラブルシューティング",
    "question": "2サイト間で断続的な接続性がある場合、何を示唆するか。",
    "options": [
        {"text": "不安定なWANリンク、フラッピングインターフェース、または断続的なルーティング"},
        {"text": "DNS問題"},
        {"text": "アプリケーション設定ミス"},
        {"text": "証明書の期限切れ"}
    ],
    "explanation": "断続的な接続性は通常、物理層の不安定性またはルーティングプロトコルのフラッピングを示す。"
},
{
    "category": "トラブルシューティング",
    "question": "ルーターのCPU使用率が高い場合、考えられる原因は何か。",
    "options": [
        {"text": "プロセススイッチング、ルーティングテーブル不安定、またはACL処理"},
        {"text": "VLANが多すぎる"},
        {"text": "帯域が過剰"},
        {"text": "メモリ不足"}
    ],
    "explanation": "ルーターの高CPU: プロセススイッチング(CEFでない)、ルーティングフラップ、ACLログ、過剰なSNMPポーリング、または攻撃。"
},
{
    "category": "トラブルシューティング",
    "question": "VPNトンネルが頻繁に切断される。まず何を確認すべきか。",
    "options": [
        {"text": "IKEキープアライブ設定、NATタイムアウト、インターネット安定性"},
        {"text": "ファイアウォールルールのみ"},
        {"text": "証明書の有効性のみ"},
        {"text": "MTUサイズのみ"}
    ],
    "explanation": "VPN切断: NATキープアライブ、DPD(デッドピア検出)、ISP安定性、フェーズ1/2ライフタイム、NAT-Tサポートを確認。"
},
{
    "category": "トラブルシューティング",
    "question": "OSIモデルベースのトラブルシューティングアプローチとは何か。",
    "options": [
        {"text": "レイヤ1(物理)から開始し、体系的に上に向かって進める"},
        {"text": "レイヤ7から開始し下に向かう"},
        {"text": "ランダムなレイヤをチェック"},
        {"text": "レイヤ3のみをチェック"}
    ],
    "explanation": "ボトムアップアプローチ: 物理(ケーブル/リンク) -> データリンク(MAC/VLAN) -> ネットワーク(IP/ルーティング) -> トランスポート -> アプリケーション。"
},
{
    "category": "トラブルシューティング",
    "question": "VLAN設定変更後、VLAN内のデバイスが通信できない。最も考えられる原因は何か。",
    "options": [
        {"text": "トランク設定の欠落またはネイティブVLANの不一致"},
        {"text": "速度不一致"},
        {"text": "MTUが大きすぎる"},
        {"text": "DNS障害"}
    ],
    "explanation": "VLAN変更ではトランク許可VLANの更新、一貫したネイティブVLANの確認、SVI/ルーテッドインターフェース設定の検証が必要。"
},
{
    "category": "トラブルシューティング",
    "question": "特定のアプリケーションだけが遅く、他は正常な場合、最も考えられる原因は何か。",
    "options": [
        {"text": "アプリケーションサーバーの問題または特定のファイアウォールルール/QoSポリシー"},
        {"text": "ネットワーク全体の輻輳"},
        {"text": "DNS障害"},
        {"text": "ケーブルの損傷"}
    ],
    "explanation": "特定アプリのみ遅い = アプリサーバー、特定ACL/レート制限、またはQoSポリシーがそのトラフィックに影響している可能性。"
},
{
    "category": "トラブルシューティング",
    "question": "Ciscoデバイスでルーティングテーブルを表示するコマンドはどれか。",
    "options": [
        {"text": "show ip route"},
        {"text": "show interfaces"},
        {"text": "show vlan"},
        {"text": "show running-config"}
    ],
    "explanation": "show ip routeは全ルートを表示: connected、static、dynamic(OSPF, BGPなど)とメトリック付き。"
},
{
    "category": "トラブルシューティング",
    "question": "ブロードキャストストームが検出された場合の最初の対応は何か。",
    "options": [
        {"text": "スイッチングループを確認し、STPが正常に機能していることを検証"},
        {"text": "全スイッチの再起動"},
        {"text": "全ブロードキャストトラフィックのブロック"},
        {"text": "ファイアウォールの切断"}
    ],
    "explanation": "ブロードキャストストームはスイッチングループが原因。STP状態を確認し、無効ポートを探し、トランク設定を検証。"
},
{
    "category": "トラブルシューティング",
    "question": "'show interfaces status'は何を表示するか。",
    "options": [
        {"text": "ポート状態、速度、デュプレックス、VLAN割り当て"},
        {"text": "ルーティングテーブル"},
        {"text": "CPU使用率"},
        {"text": "NAT変換"}
    ],
    "explanation": "show interfaces statusは全ポートの概要を表示: connected/notconnect、速度、デュプレックス、VLAN。"
},
{
    "category": "トラブルシューティング",
    "question": "OSPFネイバー関係がINIT状態で止まっている。考えられる原因は何か。",
    "options": [
        {"text": "一方向通信(片方向hello)またはACLによるブロック"},
        {"text": "エリア不一致"},
        {"text": "OSPFプロセスIDの誤り"},
        {"text": "サブネットマスク不一致"}
    ],
    "explanation": "INIT = ネイバーからのhelloは受信したが自helloが相手に届いていない。一方向リンクまたはOSPFをブロックするACLを確認。"
},
{
    "category": "トラブルシューティング",
    "question": "インターフェースで過剰なCRCエラーが見られる場合、何を示すか。",
    "options": [
        {"text": "物理層の問題(ケーブル、コネクタ、またはデュプレックス不一致)"},
        {"text": "ソフトウェア設定ミス"},
        {"text": "ルーティング問題"},
        {"text": "DNS問題"}
    ],
    "explanation": "CRCエラーはレイヤ1の問題: 損傷ケーブル、不良コネクタ、EMI、またはデュプレックス不一致によるコリジョン。"
},
{
    "category": "トラブルシューティング",
    "question": "pingは機能するがSSHができない。考えられる問題は何か。",
    "options": [
        {"text": "ファイアウォールがTCPポート22をブロックしているかSSHサービスが稼働していない"},
        {"text": "DNS障害"},
        {"text": "ルーティング問題"},
        {"text": "サブネットマスクの誤り"}
    ],
    "explanation": "ping(ICMP)が機能 = ネットワーク到達可能。SSH(TCP 22)が失敗 = ファイアウォール、ACL、またはサービス未稼働。"
},
{
    "category": "トラブルシューティング",
    "question": "ネットワークデバイスで'show logging'は何を表示するか。",
    "options": [
        {"text": "エラー、警告、イベントを含むシステムログ"},
        {"text": "ルーティングアップデート"},
        {"text": "パケットキャプチャ"},
        {"text": "トラフィック統計"}
    ],
    "explanation": "show loggingはバッファログを表示: インターフェース状態変更、ACLヒット、OSPFイベント、エラー、システムメッセージ。"
},
{
    "category": "トラブルシューティング",
    "question": "VLAN 10のユーザーがVLAN 20に到達できない。何を確認すべきか。",
    "options": [
        {"text": "VLAN間ルーティング設定(SVI、ルーター、またはレイヤ3スイッチ)"},
        {"text": "VLAN ACLのみ"},
        {"text": "STP設定"},
        {"text": "ポートセキュリティ"}
    ],
    "explanation": "VLAN間通信にはルーティングが必要: レイヤ3スイッチのSVI、ルータオンスティック、または外部ルーター。ルーティングが有効で正確か確認。"
},
{
    "category": "トラブルシューティング",
    "question": "分割半分(split-half)トラブルシューティング手法とは何か。",
    "options": [
        {"text": "ネットワークを半分に分割して障害が含まれるセクションを特定すること"},
        {"text": "ケーブルを分割すること"},
        {"text": "ユーザーを2グループに分割すること"},
        {"text": "2つの別ツールを使用すること"}
    ],
    "explanation": "分割半分: 中間点でテストし問題が前半か後半かを判定し、さらに絞り込む。"
},
# Q60-Q74: Security Design (15 Qs)
{
    "category": "セキュリティ設計",
    "question": "DMZがあるネットワークでの推奨ファイアウォール配置はどれか。",
    "options": [
        {"text": "インターネットとDMZの間、およびDMZと内部ネットワークの間にファイアウォール"},
        {"text": "インターネットエッジに1台のみ"},
        {"text": "各スイッチにファイアウォール"},
        {"text": "DMZにファイアウォールなし"}
    ],
    "explanation": "DMZ設計: インターネット -> 外部ファイアウォール -> DMZ -> 内部ファイアウォール -> 内部。2台のファイアウォールで防御の深層化。"
},
{
    "category": "セキュリティ設計",
    "question": "DMZから内部ネットワークへのトラフィックに適用すべきファイアウォールルールはどれか。",
    "options": [
        {"text": "必要なプロトコル/ポートのみ許可(デフォルト拒否)"},
        {"text": "全トラフィック許可"},
        {"text": "全トラフィック拒否"},
        {"text": "ICMPのみ許可"}
    ],
    "explanation": "DMZ-内部: 必要なもののみ許可(例: WebサーバーからのDBポート)。他は全て拒否。"
},
{
    "category": "セキュリティ設計",
    "question": "VPN設計でVPNコンセントレータをどこに配置すべきか。",
    "options": [
        {"text": "ネットワークエッジ、インターネット向けファイアウォールの背後(または統合)"},
        {"text": "内部ネットワーク内"},
        {"text": "DMZのみ"},
        {"text": "各エンドポイントに"}
    ],
    "explanation": "VPNコンセントレータは通常エッジに配置し、リモートトンネルを終端し内部ネットワークに入る前にトラフィックを検査。"
},
{
    "category": "セキュリティ設計",
    "question": "ゼロトラストネットワークアーキテクチャとは何か。",
    "options": [
        {"text": "常に検証、常に信頼しない; 位置に関係なく全アクセス要求を認証・認可"},
        {"text": "全内部トラフィックを信頼"},
        {"text": "セキュリティはVPNのみを使用"},
        {"text": "全外部トラフィックをブロック"}
    ],
    "explanation": "ゼロトラストは信頼済み内部ネットワークの概念を排除。全リクエストが認証、認可、暗号化される。"
},
{
    "category": "セキュリティ設計",
    "question": "企業ネットワークでの推奨NACデプロイはどれか。",
    "options": [
        {"text": "全アクセスポートで802.1XをRADIUSバックエンドで使用"},
        {"text": "スイッチでMACフィルタリング"},
        {"text": "全員にオープンアクセス"},
        {"text": "VPNのみ"}
    ],
    "explanation": "802.1Xはポートレベル認証を提供し、不正デバイスを防止。RADIUSが資格情報とポリシーを管理。"
},
{
    "category": "セキュリティ設計",
    "question": "インターネットからDMZへのWebトラフィックを許可するファイアウォールルールはどれか。",
    "options": [
        {"text": "DMZ WebサーバーへのTCP/80とTCP/443を許可、他は全て拒否"},
        {"text": "全TCPポート許可"},
        {"text": "TCP/3389(RDP)許可"},
        {"text": "全UDPトラフィック許可"}
    ],
    "explanation": "DMZ Webルール: WebサーバーIPへのHTTP/HTTPSのみ許可。他を全てブロック。内部サーバーアクセスなし。"
},
{
    "category": "セキュリティ設計",
    "question": "IDS/IPSはどこにデプロイすべきか。",
    "options": [
        {"text": "ネットワーク境界と重要な内部セグメント(IPSはインライン、IDSはSPAN)"},
        {"text": "エンドユーザーのノートPCのみ"},
        {"text": "インターネットエッジのみ"},
        {"text": "ワイヤレスAPのみ"}
    ],
    "explanation": "IDS/IPSはインターネットエッジ、DMZ、内部セグメント間に配置。インライン(IPS)はブロック、パッシブ(IDS)は監視。"
},
{
    "category": "セキュリティ設計",
    "question": "ファイアウォール設計における最小権限の原則とは何か。",
    "options": [
        {"text": "必要最小限のトラフィックのみ許可; デフォルトで他は全て拒否"},
        {"text": "全トラフィックを許可して特定の脅威をブロック"},
        {"text": "信頼済みIPからのトラフィックのみ許可"},
        {"text": "デフォルト拒否ルールなし"}
    ],
    "explanation": "暗黙的拒否: 明示的に許可されたトラフィックのみ通過。'deny all'で開始し、特定の許可ルールを追加。"
},
{
    "category": "セキュリティ設計",
    "question": "バスティオンホストとは何か。",
    "options": [
        {"text": "インターネットに公開された特定サービス(メール、Web、DNS)用にハードニングされたサーバー"},
        {"text": "メインファイアウォール"},
        {"text": "バックアップサーバー"},
        {"text": "内部データベースサーバー"}
    ],
    "explanation": "バスティオンホストはDMZで外部向けサービスを処理するハードニングされたシステムで攻撃面を最小化。"
},
{
    "category": "セキュリティ設計",
    "question": "ネットワークセキュリティイベントの一般的なログ保持期間はどれくらいか。",
    "options": [
        {"text": "セキュリティログで6-12ヶ月、コンプライアンス要件でより長期間"},
        {"text": "1週間"},
        {"text": "保持不要"},
        {"text": "永久"}
    ],
    "explanation": "セキュリティのベストプラクティス: 最低6-12ヶ月。コンプライアンス(PCI-DSS, SOX)は1-7年を要求する場合がある。"
},
{
    "category": "セキュリティ設計",
    "question": "ネットワークマイクロセグメンテーションとは何か。",
    "options": [
        {"text": "データセンター内でワークロードレベルにセキュリティゾーンを作成すること"},
        {"text": "VLANを追加すること"},
        {"text": "物理ネットワークをセグメント化すること"},
        {"text": "複数ファイアウォールを使用すること"}
    ],
    "explanation": "マイクロセグメンテーションは個別ワークロード(VM/コンテナ)をペーワークロードファイアウォールで分離し、ラテラルムーブメントを制限。"
},
{
    "category": "セキュリティ設計",
    "question": "全ファイアウォールACLの最後に置くべきデフォルトルールは何か。",
    "options": [
        {"text": "全て拒否(暗黙的または明示的)"},
        {"text": "全て許可"},
        {"text": "全てログ"},
        {"text": "デフォルトルールなし"}
    ],
    "explanation": "デフォルト拒否はリストにないトラフィックがブロックされることを保証。ほとんどのファイアウォールは暗黙的拒否を持つが、明示的が明確。"
},
{
    "category": "セキュリティ設計",
    "question": "ネットワークセキュリティポリシーの目的は何か。",
    "options": [
        {"text": "ネットワークリソース保護のためのルール、手順、ガイドラインの定義"},
        {"text": "ファイアウォールルールの置き換え"},
        {"text": "ルーターの自動設定"},
        {"text": "帯域使用量の監視"}
    ],
    "explanation": "セキュリティポリシーは許可、禁止、必要な事項を文書化し、技術的コントロールの基盤となる。"
},
{
    "category": "セキュリティ設計",
    "question": "DMZ設計でDNSサーバーはどこに配置すべきか。",
    "options": [
        {"text": "内部ゾーン用内部DNS; 公開レコード用DMZ内外部DNS"},
        {"text": "両方ともDMZ内"},
        {"text": "両方とも内部ネットワーク"},
        {"text": "DNS不要"}
    ],
    "explanation": "スプリットDNS: 内部DNSは内部レコードを提供、DMZの外部DNSは公開レコードを提供。内部DNSは公開しない。"
},
{
    "category": "セキュリティ設計",
    "question": "次世代ファイアウォール(NGFW)とは何か。",
    "options": [
        {"text": "従来のフィルタリングにアプリケーション認識、IPS、脅威インテリジェンスを統合したファイアウォール"},
        {"text": "ハードウェアアップグレードのみ"},
        {"text": "クラウドオンリーファイアウォール"},
        {"text": "オープンソースファイアウォール"}
    ],
    "explanation": "NGFWはアプリケーションレベル可視性、統合IPS、SSL検査、サンドボックス、ユーザーID認識を追加。"
},
# Q75-Q89: Cloud Network (15 Qs)
{
    "category": "クラウドネットワーク",
    "question": "VPCピアリングの制限は何か。",
    "options": [
        {"text": "ピアリングされたVPCはCIDRブロックが重複してはならない"},
        {"text": "VPCピアリングはTCPをサポートしない"},
        {"text": "ピアリングは同一リージョンのみに制限される"},
        {"text": "VPCピアリングにはVPNが必要"}
    ],
    "explanation": "VPCピアリングは重複しないCIDRを必要とする。重複範囲はピアリング経由で通信不可。"
},
{
    "category": "クラウドネットワーク",
    "question": "オンプレミスデータセンターをAWS VPCに接続するにはどうするか。",
    "options": [
        {"text": "AWS Direct ConnectまたはサイトツーサイトVPN"},
        {"text": "パブリックインターネットのみ"},
        {"text": "AWSデータセンターへの物理ケーブル"},
        {"text": "VPCピアリング"}
    ],
    "explanation": "Direct Connect(専用/プライベート)またはVPN over インターネット(IPsec)でオンプレミスをVPCに接続。"
},
{
    "category": "クラウドネットワーク",
    "question": "Azure Virtual Network(VNet)とは何か。",
    "options": [
        {"text": "Azureリソース用の分離された仮想ネットワーク境界"},
        {"text": "物理ネットワークセグメント"},
        {"text": "DNSゾーン"},
        {"text": "ロードバランサー"}
    ],
    "explanation": "Azure VNetは分離、セグメンテーション(サブネット)、ルーティング、フィルタリング(NSG)、ピアリングをAzureリソースに提供。"
},
{
    "category": "クラウドネットワーク",
    "question": "GCP VPCとAWS VPCの違いは何か。",
    "options": [
        {"text": "GCP VPCはデフォルトでグローバル; AWS VPCはリージョナル"},
        {"text": "同一"},
        {"text": "GCP VPCはリージョナルのみ"},
        {"text": "AWS VPCはデフォルトでグローバル"}
    ],
    "explanation": "GCP VPCはデフォルトで全リージョンにまたがる(サブネットは特定リージョン)。AWS VPCはリージョナル(リージョン間はVPCピアリング)。"
},
{
    "category": "クラウドネットワーク",
    "question": "クラウドNATゲートウェイは何に使用されるか。",
    "options": [
        {"text": "プライベートサブネットリソースのインターネットアクセスを有効化"},
        {"text": "パブリックIP割り当て"},
        {"text": "DNS解決"},
        {"text": "VPN終端"}
    ],
    "explanation": "NATゲートウェイはパブリックIPのないリソースにアウトバウンドのみのインターネットアクセスを提供し、管理されたElastic IPを使用。"
},
{
    "category": "クラウドネットワーク",
    "question": "Azure NSGとAWSセキュリティグループの違いは何か。",
    "options": [
        {"text": "NSGはステートレスでサブネットレベル; AWS SGはステートフルでインスタンスレベル"},
        {"text": "機能的に同一"},
        {"text": "AWS SGはステートレス"},
        {"text": "NSGはステートフル"}
    ],
    "explanation": "Azure NSGはサブネットまたはNICに適用可能(ステートフル)。AWS SGはインスタンスレベル(ステートフル)。両方とも許可/拒否ルールをサポート。"
},
{
    "category": "クラウドネットワーク",
    "question": "クラウドSD-WANは何に使用されるか。",
    "options": [
        {"text": "クラウド環境、拠点、データセンター間のインテリジェント接続"},
        {"text": "クラウドVPCの置き換え"},
        {"text": "クラウドロードバランシングのみ"},
        {"text": "クラウドストレージ管理"}
    ],
    "explanation": "クラウドSD-WANはクラウドVPC、オンプレミス、拠点間でパス選択による最適化されたセキュア接続を提供。"
},
{
    "category": "クラウドネットワーク",
    "question": "AWS Transit Gatewayとは何か。",
    "options": [
        {"text": "複数のVPCとVPNを単一ゲートウェイ経由で接続するハブ"},
        {"text": "インターネットゲートウェイ"},
        {"text": "NATサービス"},
        {"text": "DNSサービス"}
    ],
    "explanation": "Transit Gatewayは中央ハブとして機能し、接続性を簡素化。なしの場合はフルメッシュVPCピアリング(N*(N-1)/2接続)が必要。"
},
{
    "category": "クラウドネットワーク",
    "question": "クラウドネットワークリソースの高可用性をどのように実現するか。",
    "options": [
        {"text": "複数アベイラビリティゾーンに冗長コンポーネントをデプロイ"},
        {"text": "1つの大規模インスタンスを使用"},
        {"text": "クラウドプロバイダーのデフォルト設定に依存"},
        {"text": "外部ストレージにバックアップ"}
    ],
    "explanation": "マルチAZデプロイは耐障害性を確保。AZにリソースを分散し、ロードバランサーで自動フェイルオーバー。"
},
{
    "category": "クラウドネットワーク",
    "question": "AWS PrivateLinkサービスとは何か。",
    "options": [
        {"text": "パブリックインターネットを経由せずサービスへのプライベート接続"},
        {"text": "VPNの置き換え"},
        {"text": "パブリックロードバランサー"},
        {"text": "CDNサービス"}
    ],
    "explanation": "PrivateLinkはサービスをプライベートIP(Interface VPC Endpoints)で公開し、パブリックインターネットへの公開なし。"
},
{
    "category": "クラウドネットワーク",
    "question": "GCP Cloud VPNとは何か。",
    "options": [
        {"text": "オンプレミスとGCP VPCネットワークを接続するIPsec VPN"},
        {"text": "Webプロキシサービス"},
        {"text": "DNSサービス"},
        {"text": "コンテナオーケストレーションツール"}
    ],
    "explanation": "GCP Cloud VPNはオンプレミスとVPC間にIPsecトンネルを作成。HAオプションとトンネルあたり3Gbpsスループット。"
},
{
    "category": "クラウドネットワーク",
    "question": "ハイブリッドクラウドネットワーキングの課題は何か。",
    "options": [
        {"text": "環境間での一貫したポリシー、接続性、遅延、管理"},
        {"text": "帯域の制限のみ"},
        {"text": "セキュリティの懸念のみ"},
        {"text": "モダンツールでの課題なし"}
    ],
    "explanation": "ハイブリッドクラウドネットワーキングの課題: 一貫したセキュリティポリシー、低遅延接続性、統合管理、コンプライアンス。"
},
{
    "category": "クラウドネットワーク",
    "question": "Azure ExpressRouteとは何か。",
    "options": [
        {"text": "Azureへのプライベート専用接続(パブリックインターネットをバイパス)"},
        {"text": "VPNサービス"},
        {"text": "CDN"},
        {"text": "ロードバランサー"}
    ],
    "explanation": "ExpressRouteはコネクティビティプロバイダー経由のプライベート専用接続(1-10Gbps)を提供し、低遅延と高信頼性。"
},
{
    "category": "クラウドネットワーク",
    "question": "クラウドネットワーク機能とは何か。",
    "options": [
        {"text": "ファイアウォール、ロードバランサー、DNSなどのネットワークサービスをクラウドのソフトウェアとして提供"},
        {"text": "物理ネットワークデバイス"},
        {"text": "クラウドストレージタイプ"},
        {"text": "VMイメージ"}
    ],
    "explanation": "クラウドネットワーク機能(NFW, ALB, Cloud DNS)は従来のハードウェアアプライアンスに代わるマネージドサービス。"
},
{
    "category": "クラウドネットワーク",
    "question": "クラウドネットワーク監視が重要な理由は何か。",
    "options": [
        {"text": "クラウドリソースは一時的; 監視が可視性、アラート、コスト管理を提供"},
        {"text": "クラウドプロバイダーが全監視を処理"},
        {"text": "クラウドでは監視不要"},
        {"text": "コスト追跡のみ"}
    ],
    "explanation": "クラウド監視(VPC Flow Logs, CloudWatch, Azure Monitor)はトラフィック可視性、セキュリティ検出、コスト最適化を提供。"
},
# Q90-Q99: Migration Scenarios (10 Qs)
{
    "category": "移行シナリオ",
    "question": "企業がIPv4からIPv6に移行する場合、推奨される移行戦略はどれか。",
    "options": [
        {"text": "デュアルスタックデプロイ(IPv4とIPv6を同時に運用)"},
        {"text": "IPv4の完全シャットダウンと同日のIPv6有効化"},
        {"text": "直ちにIPv6のみ"},
        {"text": "移行不要"}
    ],
    "explanation": "デュアルスタックは段階的な移行を可能にする。両プロトコルが共存。全サービスがIPv6をサポートしたらIPv4を廃止可能。"
},
{
    "category": "移行シナリオ",
    "question": "ネットワークを1Gbpsから10Gbpsにアップグレードする際、何を確認する必要があるか。",
    "options": [
        {"text": "ケーブル、スイッチポート、SFPモジュール、ファイバ/光が10Gbpsをサポートすること"},
        {"text": "ソフトウェアアップグレードのみ"},
        {"text": "IPアドレス変更が必要"},
        {"text": "物理インフラの変更不要"}
    ],
    "explanation": "10Gbpsアップグレードには: Cat6a/6(銅)、またはファイバ(SFP+)、対応スイッチポート、新規オプティクスが必要。"
},
{
    "category": "移行シナリオ",
    "question": "フラットネットワークからVLANベース設計へのアップグレードで主な考慮事項は何か。",
    "options": [
        {"text": "VLAN割り当て、VLAN間ルーティング、トランク設定の計画"},
        {"text": "スイッチ追加のみ"},
        {"text": "全IPアドレスの変更"},
        {"text": "DNS更新のみ"}
    ],
    "explanation": "VLAN移行: ブロードキャストドメインの特定、VLAN割り当て、トランク設定、VLAN間ルーティング有効化、ACL更新。"
},
{
    "category": "移行シナリオ",
    "question": "企業がアプリケーションをAWSに移行する場合、必要なネットワーク変更は何か。",
    "options": [
        {"text": "VPC、サブネット、セキュリティグループの設定、オンプレミスとの接続、DNS"},
        {"text": "EC2インスタンス作成のみ"},
        {"text": "ファイアウォール設定のみ"},
        {"text": "ネットワーク変更不要"}
    ],
    "explanation": "クラウド移行には: VPC設計、サブネット計画、セキュリティグループ、ハイブリッド接続(VPN/Direct Connect)、DNSが必要。"
},
{
    "category": "移行シナリオ",
    "question": "RIPからOSPFへの移行で推奨されるアプローチはどれか。",
    "options": [
        {"text": "両プロトコルを併用してルート再配布し、段階的にRIPを削除"},
        {"text": "OSPFへの即時切替"},
        {"text": "RIPを永続的に維持"},
        {"text": "移行中はスタティックルートを使用"}
    ],
    "explanation": "段階的移行: OSPFをデプロイし、RIPとOSPF間でルート再配布、検証後にRIPを削除。"
},
{
    "category": "移行シナリオ",
    "question": "企業が802.11acから802.11axにアップグレードする場合、何を考慮すべきか。",
    "options": [
        {"text": "クライアントデバイスの互換性、APファームウェア、チャネル計画、電力要件"},
        {"text": "AP交換のみ"},
        {"text": "計画不要"},
        {"text": "チャネル変更のみ"}
    ],
    "explanation": "Wi-Fi 6移行: 新AP、クライアントサポート、OFDMA設定、BSSカラーイング、新規PoE要件の可能性。"
},
{
    "category": "移行シナリオ",
    "question": "ハブアンドスポークからSD-WANへの移行で最大の利点は何か。",
    "options": [
        {"text": "直接のany-to-any接続、動的パス選択、簡素化された管理"},
        {"text": "コスト削減のみ"},
        {"text": "より良いセキュリティのみ"},
        {"text": "より速いインターネットのみ"}
    ],
    "explanation": "SD-WANはハブアンドスポークMPLSをany-to-any接続、インテリジェントパス選択、集中管理に置き換える。"
},
{
    "category": "移行シナリオ",
    "question": "データセンター統合で重要なネットワーク移行ステップは何か。",
    "options": [
        {"text": "サービスを中断せずにIPアドレスの再採番とDNS更新を行うこと"},
        {"text": "全機器の電源サイクル"},
        {"text": "全VLAN IDの変更"},
        {"text": "設定のバックアップのみ"}
    ],
    "explanation": "DC統合には慎重なIP計画が必要: 衝突回避、DNS更新、フェーズでの移行、接続性維持。"
},
{
    "category": "移行シナリオ",
    "question": "ハードウェアロードバランサーからクラウドロードバランサーへの移行で何が変わるか。",
    "options": [
        {"text": "設定形式、ヘルスチェック方法、TLS終端の違い"},
        {"text": "変更不要"},
        {"text": "IPアドレス変更のみ"},
        {"text": "証明書更新のみ"}
    ],
    "explanation": "クラウドLBは異なる設定(ターゲットグループ、リスナー vs プール)、マネージドTLS、オートスケーリング統合を持つ。"
},
{
    "category": "移行シナリオ",
    "question": "ファイアウォール移行中に保持すべき重要なものは何か。",
    "options": [
        {"text": "全既存セキュリティポリシー(ACL、NATルール、VPN設定)を同等のカバレッジで保持"},
        {"text": "デフォルトルールのみ"},
        {"text": "VPN設定のみ"},
        {"text": "NATルールのみ"}
    ],
    "explanation": "ファイアウォール移行: 全既存ポリシーを新プラットフォームにマッピング、ラボで徹底的テスト、ロールバック計画で切替。"
},
]

print(f"T_SUBJECT entries: {len(T_SUBJECT)}")

if __name__ == '__main__':
    main()
