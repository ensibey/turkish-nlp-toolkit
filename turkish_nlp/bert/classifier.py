"""Wrapper around dbmdz/bert-base-turkish-cased for sequence classification."""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional, Sequence

logger = logging.getLogger(__name__)

try:
    import torch
    from torch.optim import AdamW
    from torch.utils.data import DataLoader, Dataset
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        get_linear_schedule_with_warmup,
    )

    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False

DEFAULT_MODEL = "dbmdz/bert-base-turkish-cased"


class _EncodedDataset(Dataset):
    def __init__(self, encodings: Dict[str, Any], labels: Optional[Sequence[int]] = None) -> None:
        self.encodings = encodings
        self.labels = labels

    def __len__(self) -> int:
        return len(self.encodings["input_ids"])

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        item = {key: val[idx] for key, val in self.encodings.items()}
        if self.labels is not None:
            item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item


class TurkishClassifier:
    """Fine-tune and run inference with a HuggingFace Turkish BERT checkpoint."""

    def __init__(
        self,
        num_labels: int,
        label_names: Optional[List[str]] = None,
        model_name: str = DEFAULT_MODEL,
        max_length: int = 128,
        device: Optional[str] = None,
    ) -> None:
        if not _TORCH_AVAILABLE:
            raise ImportError(
                "PyTorch and Transformers are required for turkish_nlp.bert. "
                "Install with: pip install torch transformers scikit-learn"
            )
        self.num_labels = num_labels
        self.label_names = label_names
        self.model_name = model_name
        self.max_length = max_length
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model: Optional[Any] = None

    def _encode(self, texts: Sequence[str]) -> Dict[str, Any]:
        return self.tokenizer(
            list(texts),
            truncation=True,
            padding=True,
            max_length=self.max_length,
            return_tensors="pt",
        )

    def train(
        self,
        texts: Sequence[str],
        labels: Sequence[int],
        epochs: int = 3,
        batch_size: int = 16,
        lr: float = 2e-5,
        val_texts: Optional[Sequence[str]] = None,
        val_labels: Optional[Sequence[int]] = None,
    ) -> Dict[str, List[float]]:
        """Fine-tune the sequence classification head and return training metrics."""
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=self.num_labels,
        ).to(self.device)

        enc = {k: v.to(self.device) for k, v in self._encode(texts).items()}
        loader = DataLoader(_EncodedDataset(enc, labels), batch_size=batch_size, shuffle=True)
        optimizer = AdamW(self.model.parameters(), lr=lr)
        total_steps = len(loader) * epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=int(total_steps * 0.1),
            num_training_steps=total_steps,
        )

        history: Dict[str, List[float]] = {"train_loss": []}
        for epoch in range(1, epochs + 1):
            self.model.train()
            epoch_loss = 0.0
            for batch in loader:
                optimizer.zero_grad()
                inputs = {k: v.to(self.device) for k, v in batch.items()}
                outputs = self.model(**inputs)
                outputs.loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()
                epoch_loss += float(outputs.loss.item())

            avg_loss = epoch_loss / max(len(loader), 1)
            history["train_loss"].append(avg_loss)

            if val_texts is not None and val_labels is not None:
                metrics = self.evaluate(val_texts, val_labels)
                history.setdefault("val_accuracy", []).append(metrics["accuracy"])
                logger.info(
                    "epoch=%d/%d train_loss=%.4f val_acc=%.4f",
                    epoch,
                    epochs,
                    avg_loss,
                    metrics["accuracy"],
                )
            else:
                logger.info("epoch=%d/%d train_loss=%.4f", epoch, epochs, avg_loss)

        return history

    def predict(self, texts: Sequence[str]) -> List[str]:
        indices = self.predict_indices(texts)
        if self.label_names:
            return [self.label_names[i] for i in indices]
        return [str(i) for i in indices]

    def predict_indices(self, texts: Sequence[str]) -> List[int]:
        if self.model is None:
            raise RuntimeError("Model has not been trained or loaded.")
        self.model.eval()
        enc = {k: v.to(self.device) for k, v in self._encode(texts).items()}
        with torch.no_grad():
            outputs = self.model(**enc)
        return outputs.logits.argmax(dim=-1).cpu().tolist()

    def predict_proba(self, texts: Sequence[str]) -> List[List[float]]:
        if self.model is None:
            raise RuntimeError("Model has not been trained or loaded.")
        self.model.eval()
        enc = {k: v.to(self.device) for k, v in self._encode(texts).items()}
        with torch.no_grad():
            outputs = self.model(**enc)
        return torch.softmax(outputs.logits, dim=-1).cpu().tolist()

    def evaluate(self, texts: Sequence[str], labels: Sequence[int]) -> Dict[str, float]:
        preds = self.predict_indices(texts)
        acc = sum(p == l for p, l in zip(preds, labels)) / max(len(labels), 1)
        result: Dict[str, float] = {"accuracy": acc}
        try:
            from sklearn.metrics import f1_score

            result["f1_macro"] = float(f1_score(labels, preds, average="macro"))
        except ImportError:
            pass
        return result

    def save(self, path: str) -> None:
        if self.model is None:
            raise RuntimeError("Cannot save an uninitialized model.")
        os.makedirs(path, exist_ok=True)
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)

    @classmethod
    def load(
        cls,
        path: str,
        num_labels: int,
        label_names: Optional[List[str]] = None,
        device: Optional[str] = None,
    ) -> "TurkishClassifier":
        instance = cls.__new__(cls)
        instance.num_labels = num_labels
        instance.label_names = label_names
        instance.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        instance.tokenizer = AutoTokenizer.from_pretrained(path)
        instance.model = AutoModelForSequenceClassification.from_pretrained(
            path,
            num_labels=num_labels,
        ).to(instance.device)
        return instance
