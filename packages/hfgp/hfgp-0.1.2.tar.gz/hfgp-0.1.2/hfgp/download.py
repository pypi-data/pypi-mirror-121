from transformers import BertTokenizer, AutoModel, Text2TextGenerationPipeline
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")
tokenizer.save_pretrained(save_directory="D:\code\codalab\starting_kit\sample_code_submission\\bert-base-uncased")
model.save_pretrained(save_directory="D:\code\codalab\starting_kit\sample_code_submission\\bert-base-uncased")


