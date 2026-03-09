async def stream_llm_response(llm, prompt, websocket):
    
    async for chunk in llm.astream(prompt):

        token = chunk.content

        await websocket.send_json({
            "type": "token",
            "content": token
        })