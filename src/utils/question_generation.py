from pydantic import BaseModel

from src.utils.llm_clients.schema import ChatMessage, LLMCLient

BASE_PROMT_EN = f"""You are helpful assistant who generates questions for a given text.
                    Based on the provided text you generate five questions. 
                    It should be possible to answer the questions based on the text.
                    You don't generate direct questions. 
                    Question are self-contained and general, without explicitly mentioning a context, system, course, or extract.
                    You provide your response in JSON format with the following structure:
                    {{
                        "questions": [
                            "Question 1",
                            "Question 2",
                            "Question 3",
                        ]
                    }}"""

BASE_PROMT_PL = """Jesteś pomocnym asystentem, który generuje pytania do danego tekstu.
                    Na podstawie podanego tekstu generujesz pięć pytań. 
                    Powinno być możliwe odpowiedzenie na pytania na podstawie tekstu.
                    Nie generujesz bezpośrednich pytań. 
                    Pytania są samodzielne i ogólne, bez wyraźnego wskazywania kontekstu, systemu, kursu czy fragmentu.
                    Odpowiedź podajesz w formacie JSON o następującej strukturze:
                    {{
                        "questions": [
                            "Pytanie 1",
                            "Pytanie 2",
                            "Pytanie 3",
                        ]
                    }}"""



class GeneratedQuestions(BaseModel):
    questions: list[str]


def generate_question_for_text(llm_client: LLMCLient, extracted, base_promt=BASE_PROMT_EN) -> GeneratedQuestions:
    answer = llm_client.chat([ChatMessage(role='system', content=base_promt),
                              ChatMessage(role='user', content=f"Source text: {extracted}")],
                              _format=GeneratedQuestions)

    return answer.response

