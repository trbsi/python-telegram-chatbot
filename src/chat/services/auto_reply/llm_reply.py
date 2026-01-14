import torch
from peft import PeftModel
from transformers import AutoTokenizer, AutoModel

from chatapp import settings


class LlmReplyService():
    def get_reply(self, chat_history: list) -> str:
        base_model = "mistralai/Mistral-7B-Instruct-v0.3"
        trained_model = f'{settings.BASE_DIR}/trained_model'

        tokenizer = AutoTokenizer.from_pretrained(base_model)
        model = AutoModel.from_pretrained(base_model, dtype=torch.float16, device_map={'': 'cuda'})

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        model = PeftModel.from_pretrained(model, trained_model)
        model.eval()

        input_text = tokenizer.apply_chat_template(
            chat_history,
            tokenize=False,
            system_message="Assistant should respond in short, casual sentences.",
            add_generation_prompt=True
        )

        input_tokens = tokenizer(input_text, return_tensors='pt').to(model.device)

        output = model.generate(
            **input_tokens,
            max_new_tokens=50,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

        input_token_length = input_tokens['input_ids'].shape[1]
        generated_tokens = output[0][input_token_length:]
        reply = tokenizer.decode(generated_tokens, skip_special_tokens=True)

        return reply
