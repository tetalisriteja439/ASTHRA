import nest_asyncio
from llama_parse import LlamaParse  


def parser(file_location):
    nest_asyncio.apply()
    parser = LlamaParse(
        api_key="",  # can also be set in your env as LLAMA_CLOUD_API_KEY
        result_type="markdown"  # "markdown" and "text" are available
    )

    # sync
    documents = parser.load_data(file_location)

    # Dumping parsed document in markdown file
    current_pfile = './parsed_pdf.md'

    with open(current_pfile, 'w', encoding="UTF-8") as f:
        f.write(documents[0].text)