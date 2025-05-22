from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredPDFLoader, PDFPlumberLoader
from my_enums import ENV_VALUES


def get_llm():
    llm = ChatGoogleGenerativeAI(
        google_api_key=ENV_VALUES.GEMINI_API_KEY.value,
        model=ENV_VALUES.GEMINI_MODEL.value,
        temperature=0.5,
    )

    return llm


def process_document(document: str):
    llm = get_llm()
    loader = PDFPlumberLoader(file_path=document)
    docs = loader.load()

    page2 = docs[1].page_content.splitlines()
    modified_content = []

    for line in page2:
        if line.startswith("PRE") or line.startswith("POST"):
            continue
        modified_content.append(line)

    template = PromptTemplate(
        template="{report_data}\n\nGenerate a detailed medical report on the given image along with a short summary for the doctor without including clinical language. An Interpretation section must be included with the report.",
        input_variables=["report_data"],
    )

    report_data = docs[0].page_content + "\n".join(modified_content)

    chain = template | llm

    result = chain.invoke({"report_data": report_data})
    print(docs)

    return result.content

# def process_document(document: str):
#     llm = get_llm()
#     loader = UnstructuredPDFLoader(file_path=document, mode="elements")
#     docs = loader.load()

#     for element in docs:
#         if element.page_content.startswith("PRE") or element.page_content.startswith(
#             "POST"
#         ):
#             docs.remove(element)

#     template = PromptTemplate(
#         template="{report_data}\n\nGenerate a detailed medical report on the given image along with a short summary for the doctor without including clinical language. An Interpretation section must be included with the report.",
#         input_variables=["report_data"],
#     )

#     chain = template | llm

#     result = chain.invoke({"report_data": docs})
#     # print(docs)

#     return result.content


# process_document(r"MS_KRITE_CHOUHAN_PFT_GRAPH.pdf")
