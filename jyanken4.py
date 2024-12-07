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

# ループでコンソール入力を受け付ける
while True:
    user_input = input("入力してください（終了するには 'exit' と入力）：")
    if user_input.lower() == 'exit':
        print("終了します。")
        break

    # ユーザー入力をメッセージに設定
    messages = [{'role': 'user', 'content': user_input}]

    response: ChatResponse = chat(
        #'llama3.1',
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
        messages.append(response.message)
        messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

        final_response = chat('llama3.1', messages=messages)
        print('Final response:', final_response.message.content)

    else:
        # 関数呼び出しがない場合はそのまま応答を表示
        print('Response:', response.message.content)
