from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# מודל
llm = ChatOpenAI(model="gpt-4.1-nano")

# תבנית פרומפט
prompt = ChatPromptTemplate.from_messages(
    [("system", "Translate the following into Hebrew"),
     ("user", "{text}")]
)

# פונקציה שמחזירה גם תרגום וגם ספירת מילים
def combine(inputs: dict) -> dict:
    translation = inputs["translation"]
    original_text = inputs["original_text"]
    count = len(original_text.split())
    return {
        "translation": translation,
        "word_count": count
    }

# שרשרת
chain = (
        {
            "translation": prompt | llm | StrOutputParser(),
            "original_text": RunnablePassthrough()
        }
        | RunnableLambda(combine)
)

# בדיקה
response = chain.invoke("this is a table")
print(response)
