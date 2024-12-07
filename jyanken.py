from ollama import chat
from ollama import ChatResponse

def determine_winner(player1: str, player2: str) -> str:
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

messages = [{'role': 'user', 'content': 'プレイヤー1がパーで、プレイヤー2がチョキならどちらが勝ちますか？'}]
print('Prompt:', messages[0]['content'])

available_functions = {
    'determine_winner': determine_winner
}

response: ChatResponse = chat(
    'llama3.1',
    messages=messages,
    tools=[determine_winner]
)

if response.message.tool_calls:
    # There may be multiple tool calls in the response
    for tool in response.message.tool_calls:
        # Ensure the function is available, and then call it
        if function_to_call := available_functions.get(tool.function.name):
            print('Calling function:', tool.function.name)
            print('Arguments:', tool.function.arguments)
            output = function_to_call(**tool.function.arguments)
            print('Function output:', output)
        else:
            print('Function', tool.function.name, 'not found')

# Only needed to chat with the model using the tool call results
if response.message.tool_calls:
    # Add the function response to messages for the model to use
    messages.append(response.message)
    messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

    # Get final response from model with function outputs
    final_response = chat('llama3.1', messages=messages)
    print('Final response:', final_response.message.content)

else:
    print('No tool calls returned from model')
