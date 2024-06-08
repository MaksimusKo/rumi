from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
import yaml
# Загрузка конфигурации из YAML файла
with open ("config.yaml", "r") as f:
    config = yaml.safe_load (f)

# Инициализация FastAPI
app = FastAPI ()

# Инициализация модели и токенизатора с использованием конфигурации из YAML файла
base_model = AutoModelForCausalLM.from_pretrained (
    config['model']['name'],
    trust_remote_code=True,
    use_auth_token=config['model']['token'],
    device_map="auto",
    torch_dtype=eval (config['model']['dtype']),
    load_in_4bit=config['model']['load_in_4bit']
)
tokenizer = AutoTokenizer.from_pretrained (config['model']['name'], trust_remote_code=True)
model = PeftModel.from_pretrained (base_model, config['model']['checkpoint']).to (config['model']['device'])


# Модель данных для входного сообщения
class Message (BaseModel):
    message: str


@app.get ("/")
def read_root():
    return {"message": "Welcome to RUMI GPT Server! The server is running successfully."}


@app.post ("/talk")
async def talk(request: Request):
    try:
        data = await request.json ()
        user_message = data.get ("message")

        if not user_message:
            raise HTTPException (status_code=400, detail="Message content is missing.")

        messages = [{"role": "user", "content": user_message}]

        # Применение шаблона для сообщений и генерация input_ids
        input_ids = tokenizer.apply_chat_template (
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to (model.device)

        # Генерация ответа
        outputs = model.generate (input_ids)
        response = outputs[0]
        response_text = tokenizer.decode (response, skip_special_tokens=True)

        return JSONResponse (content={"response": response_text})

    except Exception as e:
        raise HTTPException (status_code=500, detail=str (e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run (app, host=config['server']['host'], port=config['server']['port'])
