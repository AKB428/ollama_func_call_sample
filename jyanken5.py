from ollama import chat
from ollama import ChatResponse
import random

def rock_paper_scissors(player1: str, player2: str) -> str:
    """
    じゃんけんの勝敗を判定する

    Args:
        player1 (str): プレイヤー1の手（グー、チョキ、パー）
        player2 (str): プレイヤー2の手（グー、チョキ、パー）

    Returns:
        str: 勝敗の結果 ("Player 1 Wins", "Player 2 Wins", "Draw")
    """
    rules = {
        'グー': 'チョキ',
        'チョキ': 'パー',
        'パー': 'グー'
    }
    if player1 == player2:
        return "Draw"
    elif rules[player1] == player2:
        return "Player 1 Wins"
    else:
        return "Player 2 Wins"

def play_against_ai(player1: str) -> str:
    """
    プレイヤー1の手を受け取り、AIの手をランダムに生成して勝敗を判定する

    Args:
        player1 (str): プレイヤー1の手（グー、チョキ、パー）

    Returns:
        str: 勝敗の結果とAIの手
    """
    choices = ['グー', 'チョキ', 'パー']
    player2 = random.choice(choices)
    result = rock_paper_scissors(player1, player2)
    return f"Player 1: {player1}, AI: {player2}, Result: {result}"

def add_two_numbers(a: int, b: int) -> int:
  """
  Add two numbers

  Args:
    a (int): The first number
    b (int): The second number

  Returns:
    int: The sum of the two numbers
  """
  return a + b

available_functions = {
    'rock_paper_scissors': rock_paper_scissors,
    'add_two_numbers': add_two_numbers,
    'play_against_ai': play_against_ai
}

# ループの外でmessagesを初期化
messages = []

# ループでコンソール入力を受け付ける
while True:
    print('入力してください。複数行の場合は """ で囲んでください（終了するには "exit" と入力）：')
    user_input = ""
    is_multiline = False
    while True:
        line = input()
        if line.strip() == '"""':
            if is_multiline:
                break
            else:
                is_multiline = True
                continue
        if not is_multiline and line.lower() == 'exit':
            print("終了します。")
            exit()
        if not is_multiline:
            user_input = line.strip()
            break
        user_input += line + "\n"

    if not is_multiline and user_input.strip() == "":
        print("無効な入力です。もう一度入力してください。")
        continue

    # ユーザー入力を会話履歴に追加
    messages.append({'role': 'user', 'content': user_input.strip()})

    response: ChatResponse = chat(
        'llama3.1',
        messages=messages,
        tools=[rock_paper_scissors, add_two_numbers, play_against_ai]
    )

    if response.message.tool_calls:
        # 関数呼び出しがある場合
        for tool in response.message.tool_calls:
            # 関数が利用可能か確認し、呼び出す
            if function_to_call := available_functions.get(tool.function.name):
                print('Calling function:', tool.function.name)
                print('Arguments:', tool.function.arguments)
                output = function_to_call(**tool.function.arguments)
                print('Function output:', output)
            else:
                print('Function', tool.function.name, 'not found')

        # モデルに結果を渡して最終応答を得る
        messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

        final_response = chat('llama3.3:70b-instruct-q2_K', messages=messages)
        print('Final response:', final_response.message.content)

        # モデルの応答を履歴に追加
        messages.append({'role': 'assistant', 'content': final_response.message.content})
    else:
        # モデルの応答を履歴に追加
        messages.append({'role': 'assistant', 'content': response.message.content})
        print('Response:', response.message.content)
