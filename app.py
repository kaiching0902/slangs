import io
import qrcode
import streamlit as st

# 設定網頁標題與版面
st.set_page_config(page_title="日常英文俚語字卡學習機", page_icon="📘", layout="centered")

# 語庫資料庫（包含五大場合，每種場合 20 句俚語）[cite: 1]
SLANG_DB = {
    "讚美": {
        1: {"en": "You're a natural.", "zh": "你天生就很有天分。", "ex": "You're a natural at dancing. You learned that choreography so quickly!", "ex_zh": "你跳舞真的很有天分！你這麼快就學會那支舞了！"},
        2: {"en": "You're a quick learner.", "zh": "你學得很快。", "ex": "You've only been taking Korean classes for two months? You're a quick learner!", "ex_zh": "你才上韓文課兩個月嗎？你學得真快！"},
        3: {"en": "You nailed it!", "zh": "你做得太好了！／你完美完成了！", "ex": "Your presentation was amazing. You nailed it!", "ex_zh": "你的報告太精彩了！你真的表現得非常好！"},
        4: {"en": "You went above and beyond.", "zh": "你做得超出預期。／你真的付出了很多。", "ex": "Thank you for helping me with the project. You really went above and beyond.", "ex_zh": "謝謝你幫我完成這個專案。你真的付出了超乎預期的努力。"},
        5: {"en": "You're a pro!", "zh": "你根本是專家！／你很專業！", "ex": "Wow, you edited this video so quickly. You're a pro!", "ex_zh": "哇，你這麼快就把影片剪好了！你根本是專家！"},
        6: {"en": "You're on fire!", "zh": "你今天狀態超好！／你表現太出色了！", "ex": "You got the highest score on three tests in a row. You're on fire!", "ex_zh": "你連續三次考試都拿最高分！你最近也太猛了吧！"},
        7: {"en": "You look stunning!", "zh": "你美得令人驚艷！", "ex": "You look absolutely stunning in that dress.", "ex_zh": "你穿那件洋裝真的美得令人驚艷！"},
        8: {"en": "You look like a million bucks!", "zh": "你看起來超有魅力！／你看起來棒極了！", "ex": "You look like a million bucks in that suit!", "ex_zh": "你穿那套西裝看起來超帥、超有魅力！"},
        9: {"en": "You clean up nicely!", "zh": "你打扮起來真好看！／你正式打扮後真帥！", "ex": "Wow! You clean up nicely. I almost didn't recognize you!", "ex_zh": "哇！你打扮起來真好看，我差點認不出你了！"},
        10: {"en": "You've got great taste.", "zh": "你的品味真好！", "ex": "I love your outfit. You've got great taste in fashion.", "ex_zh": "我好喜歡你的穿搭！你的時尚品味真好。"},
        11: {"en": "You have a great sense of style.", "zh": "你的風格品味很好。／你很有自己的風格。", "ex": "I always love your outfits. You have a great sense of style.", "ex_zh": "我一直都很喜歡你的穿搭，你真的很有自己的風格。"},
        12: {"en": "You light up the room.", "zh": "你一出現，整個氣氛都亮起來了。／你讓整個空間都充滿活力。", "ex": "Whenever you walk into the room, you light up the room.", "ex_zh": "每當你走進房間，整個氣氛都變得明亮、充滿活力。"},
        13: {"en": "You wear it well.", "zh": "你穿起來真好看。／你很能駕馭這個造型。", "ex": "I love that new haircut. You really wear it well.", "ex_zh": "我好喜歡你新的髮型！你真的很適合這個造型。"},
        14: {"en": "You're someone people can count on.", "zh": "你是個值得信賴、可以依靠的人。", "ex": "Whenever we have a problem, you're always there to help. You're someone we can count on.", "ex_zh": "每當我們遇到問題，你總是會出來幫忙。你真的是一個值得依靠的人。"},
        15: {"en": "You have a way with words.", "zh": "你很會說話。／你很懂得運用言語。", "ex": "I was struggling to explain my feelings, but you always have a way with words.", "ex_zh": "我一直不知道該怎麼表達自己的感受，但你總是很懂得用言語表達。"},
        16: {"en": "You're a gem.", "zh": "你真是個寶藏！／你真是個難得的好人！", "ex": "Thank you for always being there for me. You're a real gem.", "ex_zh": "謝謝你一直陪伴在我身邊。你真的是個很難得的人。"},
        17: {"en": "You have a great sense of humor.", "zh": "你的幽默感真好。／你真的很有趣。", "ex": "I always enjoy spending time with you. You have a great sense of humor.", "ex_zh": "我一直都很喜歡和你相處，你真的很有幽默感。"},
        18: {"en": "You bring out the best in people.", "zh": "你能激發別人最好的一面。／你讓別人變得更好。", "ex": "You're such a great teacher. You always bring out the best in your students.", "ex_zh": "你真的是一位很棒的老師，你總是能讓學生發揮出最好的一面。"},
        19: {"en": "You're one of a kind.", "zh": "你是獨一無二的。／你真的很特別。", "ex": "There will never be another person like you. You're one of a kind.", "ex_zh": "不會再有另一個像你這樣的人了。你真的是獨一無二的。"},
        20: {"en": "You have a heart of gold.", "zh": "你有一顆善良的心。／你真的是個心地很好的人。", "ex": "She's always willing to help others. She has a heart of gold.", "ex_zh": "她總是願意幫助別人，她真的是一個非常善良的人。"}
    },
    "情緒": {
        1: {"en": "Over the moon", "zh": "欣喜若狂、開心不得了", "ex": "I'm over the moon about my exam results!", "ex_zh": "我對自己的考試成績開心不得了！"},
        2: {"en": "On cloud nine", "zh": "樂不可支、開心到飄飄然", "ex": "She's been on cloud nine since she got accepted into college.", "ex_zh": "自從她被大學錄取後，就一直開心不得了。"},
        3: {"en": "I'm hyped!", "zh": "我超興奮的！我超期待！", "ex": "I'm so hyped for the concert this weekend!", "ex_zh": "我超期待這週末的演唱會！"},
        4: {"en": "Living my best life", "zh": "享受人生、過著最棒的生活", "ex": "I'm on vacation, eating good food and living my best life.", "ex_zh": "我正在度假，吃著美食，享受人生。"},
        5: {"en": "I'm stoked!", "zh": "我超期待！我超開心！", "ex": "I'm stoked about my upcoming trip to Japan.", "ex_zh": "我超期待即將到來的日本之旅！"},
        6: {"en": "Feeling blue", "zh": "感到憂鬱、心情低落", "ex": "I've been feeling blue lately because of school.", "ex_zh": "最近因為學校的事情，我心情有點低落。"},
        7: {"en": "Bummed out", "zh": "感到失望、沮喪", "ex": "I was really bummed out when the event got canceled.", "ex_zh": "活動取消時，我真的很失望。"},
        8: {"en": "Down in the dumps", "zh": "情緒低落、悶悶不樂", "ex": "He's been down in the dumps since his best friend moved away.", "ex_zh": "自從他最好的朋友搬走後，他就一直悶悶不樂。"},
        9: {"en": "That sucks!", "zh": "那真糟糕！太衰了吧！", "ex": "You failed the driving test? That sucks!", "ex_zh": "你駕照考試沒過？那也太衰了吧！"},
        10: {"en": "It breaks my heart", "zh": "讓我心碎、讓我非常難過", "ex": "It breaks my heart to see animals being abandoned.", "ex_zh": "看到動物被遺棄，真的讓我很難過。"},
        11: {"en": "Pissed off", "zh": "非常生氣、火大", "ex": "I'm so pissed off because he lied to me.", "ex_zh": "他竟然騙我，我真的氣炸了！"},
        12: {"en": "Get on someone's nerves", "zh": "惹某人心煩、讓某人很煩躁", "ex": "My brother keeps making noises. He's getting on my nerves.", "ex_zh": "我弟一直在製造噪音。他讓我感到很煩躁。"},
        13: {"en": "Lose it", "zh": "情緒失控、忍不住爆發", "ex": "I almost lost it when I found out what happened.", "ex_zh": "當我知道發生什麼事時，我差點就情緒失控。"},
        14: {"en": "Drive someone crazy", "zh": "把某人逼瘋、讓某人受不了", "ex": "This constant noise is driving me crazy!", "ex_zh": "這些持續不斷的噪音真的快把我逼瘋了！"},
        15: {"en": "Have a short fuse", "zh": "脾氣很差、容易發怒", "ex": "He has a short fuse, so be careful what you say.", "ex_zh": "他脾氣比較暴躁，所以說話要小心。"},
        16: {"en": "Freak out", "zh": "嚇壞、慌張、情緒激動", "ex": "I freaked out when I realized I had lost my phone.", "ex_zh": "當我發現手機不見時，我整個慌了。"},
        17: {"en": "Mind-blowing", "zh": "令人震驚的、令人難以置信的", "ex": "The plot twist in that movie was mind-blowing!", "ex_zh": "那部電影的劇情反轉真的太令人震驚了！"},
        18: {"en": "Make a fool of yourself", "zh": "出糗、讓自己看起來很丟臉", "ex": "I made a fool of myself when I accidentally called my teacher \"Mom.\"", "ex_zh": "我不小心叫老師「媽媽」，真的糗大了。"},
        19: {"en": "I'm shook!", "zh": "我震驚了！我傻眼了！", "ex": "Did you hear the news? I'm literally shook!", "ex_zh": "你聽到那個消息了嗎？我真的整個傻眼！"},
        20: {"en": "Have butterflies in my stomach", "zh": "緊張到心裡七上八下、忐忑不安", "ex": "I always get butterflies in my stomach before a presentation.", "ex_zh": "我每次上台報告前都會緊張得心裡七上八下。"}
    },
    "職場": {
        1: {"en": "On the same page", "zh": "達成共識、想法一致、對事情有相同理解。", "ex": "Let's make sure we're on the same page before the meeting.", "ex_zh": "在會議開始前，讓我們確認彼此的想法一致。"},
        2: {"en": "Touch base", "zh": "簡短聯繫、碰面討論、確認近況。", "ex": "I'll touch base with you tomorrow about the project.", "ex_zh": "我明天會再跟你聯繫，討論專案的事情。"},
        3: {"en": "Keep me in the loop", "zh": "隨時讓我知道最新進度、讓我掌握資訊。", "ex": "Please keep me in the loop if there are any changes.", "ex_zh": "如果有任何變動，請隨時讓我知道。"},
        4: {"en": "Get the ball rolling", "zh": "開始進行、啟動某件事情。", "ex": "Let's get the ball rolling on the new project.", "ex_zh": "我們開始進行這個新專案吧！"},
        5: {"en": "On track", "zh": "按照進度、進展順利。", "ex": "We're on track to finish the project by Friday.", "ex_zh": "我們預計可以按照進度在星期五前完成專案。"},
        6: {"en": "Under the gun", "zh": "時間緊迫、承受很大的時間壓力。", "ex": "We're under the gun to finish this report by tomorrow.", "ex_zh": "我們必須承受時間壓力，在明天前完成這份報告。"},
        7: {"en": "Swamped", "zh": "忙翻了、工作多到應付不來。", "ex": "I'm swamped with work this week.", "ex_zh": "我這週工作真的忙翻了。"},
        8: {"en": "Back-to-back meetings", "zh": "連續不間斷的會議。", "ex": "I have back-to-back meetings all morning.", "ex_zh": "我整個早上都有連續的會議。"},
        9: {"en": "Crunch time", "zh": "最後衝刺階段、關鍵趕工期。", "ex": "It's crunch time, so we need to focus on the deadline.", "ex_zh": "現在是最後衝刺階段，所以我們必須專注於截止日期。"},
        10: {"en": "Call it a day", "zh": "今天就到這裡、收工。", "ex": "We've finished everything on the list. Let's call it a day.", "ex_zh": "我們已經完成清單上的所有事情，今天就到這裡吧。"},
        11: {"en": "Think outside the box", "zh": "跳脫框架思考、打破既有思維。", "ex": "We need to think outside the box to solve this problem.", "ex_zh": "我們需要跳脫框架思考，才能解決這個問題。"},
        12: {"en": "Brainstorm", "zh": "腦力激盪、集思廣益。", "ex": "Let's brainstorm some ideas for the new marketing campaign.", "ex_zh": "我們一起為新的行銷活動集思廣益吧。"},
        13: {"en": "Throw someone under the bus", "zh": "出賣某人、把責任推給別人。", "ex": "He threw his teammate under the bus to avoid taking responsibility.", "ex_zh": "他為了逃避責任，把錯推給自己的隊友。"},
        14: {"en": "Step up", "zh": "挺身而出、主動承擔責任。", "ex": "We need someone to step up and lead this project.", "ex_zh": "我們需要有人挺身而出，帶領這個專案。"},
        15: {"en": "Go the extra mile", "zh": "額外付出、比原本要求做得更多。", "ex": "She always goes the extra mile to satisfy her customers.", "ex_zh": "她總是額外付出更多努力，讓客戶滿意。"},
        16: {"en": "Get down to business", "zh": "開始談正事、進入正題。", "ex": "Now that everyone is here, let's get down to business.", "ex_zh": "既然大家都到齊了，我們就開始談正事吧。"},
        17: {"en": "In the loop / Out of the loop", "zh": "In the loop：掌握最新消息；Out of the loop：不清楚最新狀況。", "ex": "I was out of the loop because I missed the last meeting.", "ex_zh": "因為我錯過了上次的會議，所以不太清楚最新進度。"},
        18: {"en": "Low-hanging fruit", "zh": "容易達成的目標、可以優先處理的簡單任務。", "ex": "Let's focus on the low-hanging fruit before tackling bigger problems.", "ex_zh": "在處理更大的問題之前，我們先專注於容易完成的任務。"},
        19: {"en": "A win-win situation", "zh": "雙贏局面、雙方都能受益的情況。", "ex": "This agreement is a win-win situation for both companies.", "ex_zh": "這項協議對兩家公司來說都是雙贏的局面。"},
        20: {"en": "Ballpark figure", "zh": "大概的數字、粗略估計。", "ex": "Can you give me a ballpark figure for the project cost?", "ex_zh": "你可以給我這個專案成本的大概估算嗎？"}
    },
    "簡訊": {
        1: {"en": "TTYL — Talk To You Later", "zh": "晚點再聊。", "ex": "I have a meeting now. TTYL!", "ex_zh": "我現在要開會，晚點再聊！"},
        2: {"en": "BRB — Be Right Back", "zh": "馬上回來。", "ex": "BRB, I need to get some water.", "ex_zh": "等我一下，我去拿個水。"},
        3: {"en": "LOL — Laughing Out Loud", "zh": "哈哈哈、笑死了。", "ex": "That video is so funny LOL!", "ex_zh": "那個影片真的太好笑了哈哈！"},
        4: {"en": "OMG — Oh My God", "zh": "我的天啊！", "ex": "OMG! You got the job!", "ex_zh": "我的天啊！你得到那份工作了！"},
        5: {"en": "BTW — By The Way", "zh": "順帶一提。", "ex": "BTW, are you free this weekend?", "ex_zh": "順帶一提，你這個週末有空嗎？"},
        6: {"en": "FYI — For Your Information", "zh": "提供給你參考。", "ex": "FYI, the meeting has been moved to 3 PM.", "ex_zh": "提醒你一下，會議已經改到下午三點。"},
        7: {"en": "IDK — I Don't Know", "zh": "我不知道。", "ex": "IDK what time the movie starts.", "ex_zh": "我不知道電影幾點開始。"},
        8: {"en": "IMO — In My Opinion", "zh": "依我看、我認為。", "ex": "IMO, this restaurant is better than the other one.", "ex_zh": "我認為這間餐廳比另一間好。"},
        9: {"en": "TBH — To Be Honest", "zh": "老實說。", "ex": "TBH, I'm a little tired today.", "ex_zh": "老實說，我今天有點累。"},
        10: {"en": "ASAP — As Soon As Possible", "zh": "盡快、越快越好。", "ex": "Please send me the file ASAP.", "ex_zh": "請盡快把檔案傳給我。"},
        11: {"en": "NVM — Never Mind", "zh": "算了、沒關係。", "ex": "NVM, I found the answer.", "ex_zh": "沒關係，我找到答案了。"},
        12: {"en": "JK — Just Kidding", "zh": "開玩笑的啦。", "ex": "You're so annoying! JK!", "ex_zh": "你真的很煩耶！開玩笑的啦！"},
        13: {"en": "NP — No Problem", "zh": "沒問題、不客氣。", "ex": "Thanks for helping me! — NP!", "ex_zh": "謝謝你幫我！——不客氣！"},
        14: {"en": "TY / THX — Thank You / Thanks", "zh": "謝謝。", "ex": "THX for the information!", "ex_zh": "謝謝你提供這些資訊！"},
        15: {"en": "LMK — Let Me Know", "zh": "再告訴我、讓我知道。", "ex": "LMK if you need any help.", "ex_zh": "如果你需要幫忙，再告訴我。"},
        16: {"en": "GTG / G2G — Got To Go", "zh": "我得先走了。", "ex": "GTG! I have class in five minutes.", "ex_zh": "我得先走了！五分鐘後我要上課。"},
        17: {"en": "OMW — On My Way", "zh": "我正在路上。", "ex": "OMW! I'll be there in ten minutes.", "ex_zh": "我正在路上！十分鐘後到。"},
        18: {"en": "RN — Right Now", "zh": "現在、此刻。", "ex": "I'm really busy RN.", "ex_zh": "我現在真的很忙。"},
        19: {"en": "BFF — Best Friends Forever", "zh": "永遠的好朋友。", "ex": "She's my BFF. We've known each other for ten years.", "ex_zh": "她是我最好的朋友，我們已經認識十年了。"},
        20: {"en": "DM — Direct Message", "zh": "私訊。", "ex": "DM me if you have any questions.", "ex_zh": "如果你有任何問題，可以私訊我。"}
    },
    "打招呼": {
        1: {"en": "What's up?", "zh": "最近怎麼樣？／在幹嘛？", "ex": "Hey! What's up?", "ex_zh": "嘿！最近怎麼樣？"},
        2: {"en": "Sup?", "zh": "嗨！最近如何？", "ex": "Sup, dude?", "ex_zh": "嘿，老兄！最近如何？"},
        3: {"en": "Yo!", "zh": "嘿！嗨！", "ex": "Yo! What's going on?", "ex_zh": "嘿！最近在忙什麼？"},
        4: {"en": "Howdy!", "zh": "哈囉！你好！", "ex": "Howdy, partner! How are you doing?", "ex_zh": "哈囉，夥伴！你最近好嗎？"},
        5: {"en": "Hey there!", "zh": "嗨！你好呀！", "ex": "Hey there! Nice to see you again.", "ex_zh": "嗨！很高興再次見到你。"},
        6: {"en": "What's good?", "zh": "最近如何？／有什麼好事？", "ex": "Hey, what's good?", "ex_zh": "嘿，最近過得如何？"},
        7: {"en": "What's crackin'?", "zh": "最近有什麼新鮮事？", "ex": "Hey, what's crackin'?", "ex_zh": "嘿，最近有什麼新鮮事？"},
        8: {"en": "What's poppin'?", "zh": "最近有什麼好玩的？", "ex": "Yo! What's poppin' tonight?", "ex_zh": "嘿！今晚有什麼好玩的活動嗎？"},
        9: {"en": "How's it going?", "zh": "最近過得如何？", "ex": "Hey! How's it going?", "ex_zh": "嘿！最近過得如何？"},
        10: {"en": "How ya doing?", "zh": "你好嗎？／最近如何？", "ex": "Hey, how ya doing?", "ex_zh": "嘿，你最近好嗎？"},
        11: {"en": "Long time no see!", "zh": "好久不見！", "ex": "Wow! Long time no see!", "ex_zh": "哇！真的好久不見！"},
        12: {"en": "Hey, stranger!", "zh": "嘿，好久不見的陌生人！", "ex": "Hey, stranger! Where have you been?", "ex_zh": "嘿，好久不見！你最近去哪了？"},
        13: {"en": "Look who's here!", "zh": "看看是誰來了！", "ex": "Well, look who's here!", "ex_zh": "哎呀！看看是誰來了！"},
        14: {"en": "There you are!", "zh": "你終於來了！／原來你在這裡！", "ex": "There you are! I've been looking for you.", "ex_zh": "你終於出現了！我一直在找你。"},
        15: {"en": "Hey, buddy!", "zh": "嘿，老兄！／嘿，朋友！", "ex": "Hey, buddy! How have you been?", "ex_zh": "嘿，老兄！你最近過得如何？"},
        16: {"en": "What's going on?", "zh": "最近怎麼樣？／發生什麼事了？", "ex": "Hey! What's going on?", "ex_zh": "嘿！最近怎麼樣？"},
        17: {"en": "How's life?", "zh": "最近生活如何？", "ex": "Hey! How's life treating you?", "ex_zh": "嘿！最近生活過得如何？"},
        18: {"en": "What's the word?", "zh": "最近有什麼消息？／有什麼新動態？", "ex": "Hey, what's the word?", "ex_zh": "嘿，最近有什麼新消息？"},
        19: {"en": "Well, well, well!", "zh": "哎呀呀！這不是……嗎！", "ex": "Well, well, well! Look who we have here!", "ex_zh": "哎呀呀！看看這位是誰！"},
        20: {"en": "What's happening?", "zh": "最近怎麼樣？／有什麼新鮮事？", "ex": "Hey, what's happening?", "ex_zh": "嘿，最近有什麼新鮮事？"}
    }
}

# 初始化狀態（僅存於當次瀏覽器分頁記憶體，不儲存個資與歷史紀錄）
if "selected_cat" not in st.session_state:
    st.session_state.selected_cat = None
if "result_card" not in st.session_state:
    st.session_state.result_card = None

# 錯誤提示彈窗（按下 Enter 鍵自動觸發確認按鈕關閉）
@st.dialog("輸入提示")
def show_error_dialog(msg):
    st.write(msg)
    if st.button("確定 (Enter)", type="primary", use_container_width=True):
        st.rerun()

st.markdown("### 請選擇想學習的厘語場合:")

# 五個場合按鈕
categories = ["讚美", "情緒", "職場", "簡訊", "打招呼"]
cols = st.columns(5)
for idx, cat in enumerate(categories):
    btn_type = "primary" if st.session_state.selected_cat == cat else "secondary"
    if cols[idx].button(cat, key=f"btn_{cat}", type=btn_type, use_container_width=True):
        st.session_state.selected_cat = cat
        st.rerun()

# 目前選擇狀態
if st.session_state.selected_cat:
    st.success(f"目前選擇場合：【{st.session_state.selected_cat}】")
else:
    st.error("目前選擇場合：尚未選擇")

# 輸入標號表單（支援直接按 Enter 送出）
with st.form(key="slang_form", clear_on_submit=True):
    raw_num = st.text_input("請輸入俚語標號 (1-20)：", placeholder="請輸入 1 到 20 的正整數")
    submitted = st.form_submit_button("查詢字卡", type="primary", use_container_width=True)

if submitted:
    clean_num = raw_num.strip()
    if not st.session_state.selected_cat:
        show_error_dialog("請先點擊上方的五個按鈕選擇一個俚語場合！")
    elif not clean_num.isdigit():
        show_error_dialog("格式不符！請勿輸入負數、中英文字、空白或標點符號，僅限輸入 1 到 20 的正整數。")
    else:
        num = int(clean_num)
        if num < 1 or num > 20:
            show_error_dialog("數字超出範圍！不可輸入 0 或大於 20 的數字，請輸入 1 到 20 之間的正整數。")
        else:
            st.session_state.result_card = (st.session_state.selected_cat, num, SLANG_DB[st.session_state.selected_cat][num])

# 顯示字卡內容
st.divider()
if st.session_state.result_card:
    cat_name, num_val, data = st.session_state.result_card
    with st.container(border=True):
        st.caption(f"【 {cat_name} - 第 {num_val} 句 】")
        st.markdown(f"**英文俚語：** :blue[{data['en']}]")
        st.markdown(f"**中文意思：** {data['zh']}")
        st.markdown(f"**例句：** {data['ex']}")
        st.markdown(f"**例句翻譯：** {data['ex_zh']}")
else:
    with st.container(border=True):
        st.caption("【 字卡內容顯示區 】")
        st.write("英文俚語：—")
        st.write("中文意思：—")
        st.write("例句：—")
        st.write("例句翻譯：—")

# 分享 QR Code 區塊（展開即可讓其他人掃碼）
with st.expander("📱 顯示分享用 QR Code"):
    app_url = st.text_input("貼上您的公開網址以產生 QR Code：", value="https://share.streamlit.io")
    if app_url.strip():
        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(app_url.strip())
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=200, caption="掃描即可開啟字卡學習機（免登入、不留紀錄）")