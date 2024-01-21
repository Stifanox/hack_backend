import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from transformers import Trainer, TrainingArguments
from transformers import DataCollatorForLanguageModeling
import os


class GPT2Trainer:
    def __init__(self, model_name='gpt2', max_length=50):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = TFGPT2LMHeadModel.from_pretrained(model_name)
        self.max_length = max_length
        self.interactions = []

    def add_interaction(self, question, answer):
        interaction = f"Pytanie: {question} Odpowiedź: {answer}"
        self.interactions.append(interaction)

    def train(self, epochs=1, batch_size=32, learning_rate=5e-5):
        encoded_interactions = [self.tokenizer.encode(interaction, add_special_tokens=True) for interaction in
                                self.interactions]
        max_length = min(max([len(i) for i in encoded_interactions]), self.max_length)
        padded_interactions = tf.keras.preprocessing.sequence.pad_sequences(encoded_interactions, maxlen=max_length,
                                                                            padding="post")

        dataset = tf.data.Dataset.from_tensor_slices((padded_interactions, padded_interactions))
        dataset = dataset.shuffle(len(self.interactions)).batch(batch_size, drop_remainder=True)

        training_args = TrainingArguments(
            output_dir='./results',
            overwrite_output_dir=True,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            learning_rate=learning_rate,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            data_collator=DataCollatorForLanguageModeling(tokenizer=self.tokenizer, mlm=False),
        )

        trainer.train()

    def generate_response(self, question, max_length=50):
        encoded_input = self.tokenizer.encode(question, return_tensors='tf')
        output = self.model.generate(
            input_ids=encoded_input,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            early_stopping=True
        )
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response

    def save_model(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
