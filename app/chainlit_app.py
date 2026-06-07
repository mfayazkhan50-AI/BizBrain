import chainlit as cl
import requests

@cl.on_chat_start
async def start():
    await cl.Message(
        content=" Welcome to **BizBrain**! Upload a PDF and ask anything."
    ).send()

@cl.on_message
async def main(message: cl.Message):
    question = message.content

    if message.elements:
        for element in message.elements:
            if element.mime == "application/pdf":
                with open(element.path, "rb") as f:
                    response = requests.post(
                        "http://localhost:8000/upload",
                        files={"file": (element.name, f, "application/pdf")}
                    )
                if response.status_code == 200:
                    await cl.Message(
                        content=f" **{element.name}** uploaded and ready!"
                    ).send()
                return

    response = requests.post(
        "http://localhost:8000/ask",
        json={"question": question}
    )

    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", "No answer found")
        sources = data.get("sources", [])

        if sources:
            sources_text = "\n".join([f" {s}" for s in sources])
        else:
            sources_text = "No sources found"

        await cl.Message(
            content=f"{answer}\n\n---\n** Sources:**\n{sources_text}"
        ).send()
    else:
        await cl.Message(content=" Something went wrong.").send()