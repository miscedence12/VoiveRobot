import asyncio  
import edge_tts  
import os
# TEXT = "这里是语音流测试"  
# VOICE = "zh-CN-XiaoyiNeural"  
# OUTPUT_FILE = "test.mp3"  
# WEBVTT_FILE = "test.vtt"  
  
  
async def edge_tt(TEXT,VOICE = "zh-CN-XiaoyiNeural",OUTPUT_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),"response.mp3" )) -> None:  
    communicate = edge_tts.Communicate(TEXT, VOICE)  
    submaker = edge_tts.SubMaker()  
    with open(OUTPUT_FILE, "wb") as file:  
        async for chunk in communicate.stream():  
            if chunk["type"] == "audio":  
                file.write(chunk["data"])  
            elif chunk["type"] == "WordBoundary":  
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])  
  
    # with open(WEBVTT_FILE, "w", encoding="utf-8") as file:  
    #     file.write(submaker.generate_subs())  
  
  
if __name__ == "__main__":  
    asyncio.run(edge_tt(TEXT="您好,我是您的机器人语音助手小文，您可以直接和我对话哦。",VOICE = "zh-CN-XiaoyiNeural",OUTPUT_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),"voice","introduce.mp3" )))
