import contextlib

with contextlib.suppress(Exception):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

from goldenverba.components.chunk import Chunk
from goldenverba.components.interfaces import Chunker
from goldenverba.components.document import Document
from goldenverba.components.types import InputConfig
from goldenverba.components.interfaces import Embedding


class RecursiveChunker(Chunker):
    """
    RecursiveChunker for Verba using LangChain.
    """

    def __init__(self):
        super().__init__()
        self.name = "Recursive"
        self.requires_library = ["langchain_text_splitters "]
        self.description = (
            "Recursively split documents based on predefined characters using LangChain"
        )
        self.config = {
            "Chunk Size": InputConfig(
                type="number",
                value=500,
                description="Choose how many characters per chunks",
                values=[],
            ),
            "Seperators": InputConfig(
                type="multi",
                value="",
                description="Select seperators to split the text",
                values=[
                    "\n\n",
                    "\n",
                    " ",
                    ".",
                    ",",
                    "\u200b",
                    "\uff0c",
                    "\u3001",
                    "\uff0e",
                    "\u3002",
                    "",
                ],
            ),
        }

    async def chunk(
        self,
        config: dict,
        documents: list[Document],
        embedder: Embedding | None = None,
        embedder_config: dict | None = None,
    ) -> list[Document]:

        units = int(config["Chunk Size"].value)
        seperators = config["Seperators"].values

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=units,
            length_function=len,
            is_separator_regex=False,
            separators=seperators,
        )

        for document in documents:

            # Skip if document already contains chunks
            if len(document.chunks) > 0:
                continue

            for i, chunk in enumerate(text_splitter.split_text(document.content)):

                document.chunks.append(
                    Chunk(
                        content=chunk,
                        chunk_id=i,
                        start_i=0,
                        end_i=0,
                        content_without_overlap=chunk,
                    )
                )

        return documents
