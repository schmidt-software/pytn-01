import random
from src.using_apis_in_python.schemas.schemas import TriviaRequest
from src.using_apis_in_python import utils
from src.using_apis_in_python.schemas.enums import QuestionType


MULTIPLE_CHOICE = QuestionType.MultipleChoice.value.lower()


def main() -> None:
    token, token_creation_time = utils.get_api_token()

    category = utils.get_user_category()
    difficulty = utils.get_difficulty()
    question_type = utils.get_question_type()
   

    trivia_request = TriviaRequest(
        amount=1,
        category=category,
        difficulty=difficulty,
        question_type=question_type,
        token=token
    )

    correct_questions = []
    incorrect_questions = []

    while True:
        token, token_creation_time = utils.get_api_token(
            token=token, token_creation_time=token_creation_time
        )
        trivia_request.token = token

        question = utils.get_trivia_questions(trivia_request=trivia_request)[0]
       
        print("\n\n")
        print(question.question)
        print("Type 'exit' to stop the programme.")
       
        if question.question_type == MULTIPLE_CHOICE:
            answers = question.incorrect_answers + [question.correct_answer]
            random.shuffle(answers)
            correct_answer = answers.index(question.correct_answer)
            print("Possible answers: ")
            for i, answer in enumerate(answers):
                print(f"{i}. {answer}")
        else:
            print("True or False")
            correct_answer = question.correct_answer

        answer = input("answer: ")
        if answer.lower() == "exit":
            break
        elif question.question_type == MULTIPLE_CHOICE and correct_answer and correct_answer == int(answer):
            print("Correct answer!")
            correct_questions.append(question.question)
        elif answer.lower() == question.correct_answer.lower():
            print("Correct Answer!")
            correct_questions.append(question.question)
        else:
            print(f"Wrong! The correct answer is {correct_answer}")
            incorrect_questions.append(question.question)
   
    utils.save_results(
        correct_questions=correct_questions,
        incorrect_questions=incorrect_questions
    )


if __name__ == "__main__":
    main()
