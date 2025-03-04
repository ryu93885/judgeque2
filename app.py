import streamlit as st
import pandas as pd
from datetime import datetime

class ProblemAnalyzer:
    def __init__(self):
        self.groups = {
            1: "得意な問題のグループ（発展問題に挑戦、解法を説明）",
            2: "確認が必要なグループ（解答を読み直し、類似問題を解く）",
            3: "計算ミスの傾向を修正（ミスパターン分析、丁寧な計算練習）",
            4: "一時的なミス（再確認）",
            5: "基礎知識の再暗記",
            6: "応用知識の補強",
            7: "応用力の強化",
            8: "基礎からのやり直し",
            9: "用語知識の補強",
            10: "読解力の向上",
            11: "根本的な理解の深化"
        }

    def analyze_problem(self):
        st.title("学習問題分析")

        # 正解状況
        correct = st.radio("問題に正解しましたか？", ["正解", "不正解"])
        
        if correct == "正解":
            # 解答プロセス
            hesitation = st.radio("解答中の状況", ["スムーズに解けた", "途中で手が止まった"])
            group = 1 if hesitation == "スムーズに解けた" else 2
        else:
            # 間違いの原因
            cause = st.radio("間違いの主な原因", [
                "A.計算ミスやケアレスミス", 
                "B.知識不足", 
                "C.解法が思いつかない", 
                "D.問題文の理解不足"
            ])
            
            if cause == "A.計算ミスやケアレスミス":
                repeated_mistake = st.radio("ミスの状況", ["初めてのミス", "同じミスを繰り返している"])
                group = 3 if repeated_mistake == "同じミスを繰り返している" else 4
            
            elif cause == "B.知識不足":
                knowledge_level = st.radio("知識不足のレベル", ["基本事項の暗記ミス", "応用知識の不足"])
                group = 5 if knowledge_level == "基本事項の暗記ミス" else 6
            
            elif cause == "C.解法が思いつかない":
                similar_experience = st.radio("類似問題の経験", ["経験あり", "経験なし"])
                group = 7 if similar_experience == "経験あり" else 8
            
            else:  # D.問題文の理解不足
                comprehension_issue = st.radio("具体的な問題", [
                    "A.用語の意味が分からない",
                    "B.問題文の日本語が難しい", 
                    "C.解答を読んでも理解できない"
                ])
                
                if comprehension_issue == "A.用語の意味が分からない":
                    group = 9
                elif comprehension_issue == "B.問題文の日本語が難しい":
                    group = 10
                else:
                    group = 11

        # 分析結果の表示
        st.success(f"あなたは【グループ{group}】です。")
        st.info(f"推奨される学習方法:\n{self.groups[group]}")

        # 結果の保存
        if st.button("結果を保存"):
            self.save_result(group)

    def save_result(self, group):
        # セッション状態を使用してデータを保存
        if 'results' not in st.session_state:
            st.session_state.results = []
        
        result = {
            '日付': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'グループ番号': group,
            '学習方法': self.groups[group]
        }
        
        st.session_state.results.append(result)
        
        # 結果の表示
        df = pd.DataFrame(st.session_state.results)
        st.dataframe(df)

def main():
    # ログイン機能（簡易版）
    st.sidebar.title("ログイン")
    username = st.sidebar.text_input("ユーザー名")
    password = st.sidebar.text_input("パスワード", type="password")
    
    if st.sidebar.button("ログイン"):
        if username and password:
            analyzer = ProblemAnalyzer()
            analyzer.analyze_problem()
        else:
            st.sidebar.error("ユーザー名とパスワードを入力してください")

if __name__ == "__main__":
    main()
