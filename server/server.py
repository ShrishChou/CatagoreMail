from flask import Flask, jsonify
from flask_cors import CORS
import pickle

e)

app = Flask(__name__)
CORS(app)


@app.route("/api/train", methods=["GET", "POST"])
def train():
    if request.method == "POST":
        emails = request.json.get('emails', [])
        # Process the emails here
        # For now, we'll just return the count of emails received
        print(emails)
        return jsonify({
            "message": f"Received {len(emails)} emails for training",
            "emailCount": len(emails)
        })
    else:
        return jsonify({
            "message": str(request.method)
        })

@app.route("/train_importance", methods=["POST"])
def train_importance():
    if cuda.is_available():
        device = 'cuda'
    else:
        print('WARNING: you are running this assignment on a cpu!')
        device = 'cpu'
    unread_emails = pd.read_csv(unread_emails_path)
    read_emails = pd.read_csv(read_emails_path)
    emails = pd.concat([read_emails, unread_emails], ignore_index = True)

    df = pd.DataFrame()
    df['text'] = (
        'subject: ' + emails['subject'] + '\n' +
        'sender: ' + emails['sender'] + '\n' +
        'body: ' + emails['body']
    )
    df['read'] = emails['read']
    df['text'] = df['text'].astype(str)

    # First split: separate out the test set (20% of the data)
    df_train_val, df_test = train_test_split(df, test_size=0.1, stratify=df.read, random_state=42)

    # Second split: divide the remaining data into train and validation sets
    df_train, df_eval = train_test_split(df_train_val, test_size=0.11, stratify=df_train_val.read, random_state=42)

    # The resulting split will be approximately 60% train, 20% validation, 20% test

    checkpoint = "distilbert-base-uncased-finetuned-sst-2-english" # Define which pre-trained model we will be using
    classifier = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2).to(device) # Get the classifier
    tokenizer = AutoTokenizer.from_pretrained(checkpoint) # Get the tokenizer

    # Load the training data
    raw_datasets = DatasetDict({
        "train": Dataset.from_pandas(df_train),
        "eval": Dataset.from_pandas(df_eval),
        "test": Dataset.from_pandas(df_test)
    })

    # Tokenize the text, and truncate the text if it exceed the tokenizer maximum length. Batched=True to tokenize multiple texts at the same time.
    tokenized_datasets = raw_datasets.map(lambda dataset: tokenizer(dataset['text'], truncation=True), batched=True)
    # print(tokenized_datasets)

    # Check the first row
    tokenized_datasets = tokenized_datasets.remove_columns(["text", "__index_level_0__"])
    tokenized_datasets = tokenized_datasets.rename_column("read", "labels")


    # Padding for batch of data that will be fed into model for training
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # Training args
    training_args = TrainingArguments("test-trainer", num_train_epochs=3, evaluation_strategy="epoch",
                                    weight_decay=5e-4, save_strategy="no", report_to="none")


    def compute_metrics(eval_preds):
        logits, labels = eval_preds
        predictions = np.argmax(logits, axis=-1)
        # Calculate F-beta score (e.g., beta=2 to penalize false negatives more)
        f_beta = fbeta_score(labels, predictions, beta=2, average='binary')
        # Calculate accuracy
        accuracy = accuracy_score(labels, predictions)

        return {"f_beta": f_beta, "accuracy": accuracy}


    # Define trainer
    trainer = Trainer(
        classifier,
        training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["eval"],
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    # Start the fine-tuning
    trainer.train()

    test_dataset = tokenized_datasets["test"]
    test_predictions = trainer.predict(test_dataset)
    preds = np.argmax(test_predictions.predictions, axis=-1)
    with open('model.pkl') as file:
        pickle.dump(trainer, file)
    


@app.route("/predict_importance", methods=["POST"])
def predict_importance():
    with open('model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
    
    loaded_model(unread_emails_tests)


        



if __name__ == "__main__":
    app.run(debug=True, port=8080)