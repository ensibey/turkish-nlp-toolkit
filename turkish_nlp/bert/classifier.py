"""
Turkish BERT text classifier.
Fine-tunes dbmdz/bert-base-turkish-cased for any classification task.

Example:
    from turkish_nlp.bert import TurkishClassifier
    clf = TurkishClassifier(num_labels=2, label_names=["negative","positive"])
    clf.train(train_texts, train_labels, epochs=3)
    clf.predict(["Bu urun harika!", "Berbat bir deneyim."])
    # -> ['positive', 'negative']

Requires: pip install torch transformers scikit-learn
"""
try:
    import torch
    from torch.utils.data import DataLoader, Dataset
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup
    from torch.optim import AdamW
    _OK = True
except ImportError:
    _OK = False

DEFAULT_MODEL = "dbmdz/bert-base-turkish-cased"

class _DS(Dataset):
    def __init__(self, enc, labels=None):
        self.enc = enc; self.labels = labels
    def __len__(self): return len(self.enc["input_ids"])
    def __getitem__(self, i):
        item = {k: v[i] for k, v in self.enc.items()}
        if self.labels is not None:
            item["labels"] = torch.tensor(self.labels[i], dtype=torch.long)
        return item

class TurkishClassifier:
    """Fine-tune dbmdz/bert-base-turkish-cased for text classification."""

    def __init__(self, num_labels, label_names=None,
                 model_name=DEFAULT_MODEL, max_length=128, device=None):
        if not _OK: raise ImportError("pip install torch transformers scikit-learn")
        self.num_labels = num_labels
        self.label_names = label_names
        self.model_name = model_name
        self.max_length = max_length
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = None
        print(f"[TurkishClassifier] device={self.device} model={model_name}")

    def _encode(self, texts):
        return self.tokenizer(texts, truncation=True, padding=True,
                              max_length=self.max_length, return_tensors="pt")

    def train(self, texts, labels, epochs=3, batch_size=16, lr=2e-5,
              val_texts=None, val_labels=None):
        """Fine-tune the model. Returns loss history."""
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name, num_labels=self.num_labels).to(self.device)
        enc = {k: v.to(self.device) for k, v in self._encode(texts).items()}
        loader = DataLoader(_DS(enc, labels), batch_size=batch_size, shuffle=True)
        opt = AdamW(self.model.parameters(), lr=lr)
        sched = get_linear_schedule_with_warmup(opt, int(len(loader)*epochs*0.1), len(loader)*epochs)
        history = {"train_loss": []}
        for ep in range(1, epochs+1):
            self.model.train(); total = 0
            for batch in loader:
                opt.zero_grad()
                out = self.model(**{k: v.to(self.device) for k, v in batch.items()})
                out.loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                opt.step(); sched.step(); total += out.loss.item()
            avg = total / len(loader)
            history["train_loss"].append(avg)
            print(f"  Epoch {ep}/{epochs} loss={avg:.4f}", end="")
            if val_texts:
                acc = self.evaluate(val_texts, val_labels)["accuracy"]
                history.setdefault("val_accuracy", []).append(acc)
                print(f" val_acc={acc:.4f}", end="")
            print()
        return history

    def predict(self, texts):
        idxs = self.predict_indices(texts)
        return [self.label_names[i] for i in idxs] if self.label_names else [str(i) for i in idxs]

    def predict_indices(self, texts):
        self.model.eval()
        enc = {k: v.to(self.device) for k, v in self._encode(texts).items()}
        with torch.no_grad(): out = self.model(**enc)
        return out.logits.argmax(-1).cpu().tolist()

    def predict_proba(self, texts):
        self.model.eval()
        enc = {k: v.to(self.device) for k, v in self._encode(texts).items()}
        with torch.no_grad(): out = self.model(**enc)
        return torch.softmax(out.logits, -1).cpu().tolist()

    def evaluate(self, texts, labels):
        preds = self.predict_indices(texts)
        acc = sum(p==l for p,l in zip(preds,labels)) / len(labels)
        result = {"accuracy": acc}
        try:
            from sklearn.metrics import f1_score
            result["f1_macro"] = f1_score(labels, preds, average="macro")
        except ImportError: pass
        return result

    def save(self, path):
        import os; os.makedirs(path, exist_ok=True)
        self.model.save_pretrained(path); self.tokenizer.save_pretrained(path)

    @classmethod
    def load(cls, path, num_labels, label_names=None, device=None):
        obj = cls.__new__(cls)
        obj.num_labels = num_labels; obj.label_names = label_names
        obj.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        obj.tokenizer = AutoTokenizer.from_pretrained(path)
        obj.model = AutoModelForSequenceClassification.from_pretrained(
            path, num_labels=num_labels).to(obj.device)
        return obj
