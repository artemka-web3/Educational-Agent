
from gigachat import GigaChat
from prompt import make_prompt
from collect_text_from_video import read_from_file
import os
from dotenv import load_dotenv

# Используйте токен, полученный в личном кабинете из поля Авторизационные данные
def gen_qs_as():
    with GigaChat(credentials=os.getenv('GIGACHAT_TOKEN'), verify_ssl_certs=False) as giga:
        prompt = make_prompt(read_from_file())
        response = giga.chat(prompt)
        return response.choices[0].message.content





def scrap_questions(string: str):
    questions = []
    start = "Вопросы:"
    end = "Ответы:"
    start_index = string.find(start) + len(start)
    end_index = string.find(end)

    question_block = string[start_index:end_index]

    questions = question_block.split('\n')

    questions = [question for question in questions if question]

    return '\n'.join(questions)



def scrap_answers(string: str):
    answers = []
    start = "Ответы:"
    end = ""

    start_index = string.find(start) + len(start)
    end_index = len(string)

    answer_block = string[start_index:end_index]

    answers = answer_block.split('\n')

    answers = [answer for answer in answers if answer]

    return '\n'.join(answers)