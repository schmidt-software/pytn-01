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
        amount=5,
        category=category,
        difficulty=difficulty,
        question_type=question_type,
        token=token
    )

    correct_questions = []
    incorrect_questions = []

    should_exit = False
    while not should_exit:
        token, token_creation_time = utils.get_api_token(
            token=token, token_creation_time=token_creation_time
        )
        trivia_request.token = token

        questions = utils.get_trivia_questions(trivia_request=trivia_request)

        for question in questions:
            print("\n\n")
            print(question.question)
            print("Type 'exit' to stop the programme.")

            if question.question_type == MULTIPLE_CHOICE:
                answers = question.incorrect_answers + [question.correct_answer]
                random.shuffle(answers)
                correct_answer_index = answers.index(question.correct_answer)
                print("Possible answers: ")
                for i, answer_option in enumerate(answers):
                    print(f"{i}. {answer_option}")
            else:
                print("True or False")

            answer = input("answer: ")
            if answer.lower() == "exit":
                should_exit = True
                break

            if question.question_type == MULTIPLE_CHOICE:
                if answer.isdigit() and int(answer) == correct_answer_index:
                    print("Correct answer!")
                    correct_questions.append(question.question)
                else:
                    print(f"Wrong! The correct answer is {correct_answer_index}")
                    incorrect_questions.append(question.question)
            elif answer.lower() == question.correct_answer.lower():
                print("Correct Answer!")
                correct_questions.append(question.question)
            else:
                print(f"Wrong! The correct answer is {question.correct_answer}")
                incorrect_questions.append(question.question)
   
    utils.save_results(
        correct_questions=correct_questions,
        incorrect_questions=incorrect_questions
    )


if __name__ == "__main__":
    main()
