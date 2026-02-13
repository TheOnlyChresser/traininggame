import ast
import collections
import threading
from typing import Any, Callable, Dict, List, Optional

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from data.torchDATA import TorcHdata

ProgressCallback = Callable[[Dict[str, Any]], None]
NO_ACTIVATION = "Ingen"


def _split_top_level_commas(raw: str) -> List[str]:
    parts: List[str] = []
    current: List[str] = []
    depth = 0

    for char in raw:
        if char in "([{" :
            depth += 1
        elif char in ")]}":
            depth = max(0, depth - 1)

        if char == "," and depth == 0:
            segment = "".join(current).strip()
            if segment:
                parts.append(segment)
            current = []
            continue

        current.append(char)

    tail = "".join(current).strip()
    if tail:
        parts.append(tail)

    return parts


def parse_param_value(value: str) -> Any:
    stripped = value.strip()
    lowered = stripped.lower()

    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in ("none", "null"):
        return None

    if stripped:
        try:
            return int(stripped)
        except ValueError:
            pass

        try:
            return float(stripped)
        except ValueError:
            pass

        try:
            return ast.literal_eval(stripped)
        except (ValueError, SyntaxError):
            pass

    return stripped


def parse_param_string(raw_params: str) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    raw = (raw_params or "").strip()
    if not raw:
        return params

    for token in _split_top_level_commas(raw):
        if "=" not in token:
            raise ValueError(f"Ugyldigt parameter-format: '{token}'. Brug key=value.")
        key, value = token.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Ugyldigt parameter-format: '{token}'. Noeglen mangler.")
        params[key] = parse_param_value(value)

    return params


def _friendly_model_error(error: Exception) -> str:
    text = str(error)

    if "mat1 and mat2 shapes cannot be multiplied" in text:
        return (
            "Model validering fejlede: shape-fejl mellem lag. "
            "Tip: Tilfoej Flatten foer Linear og kontroller in_features."
        )

    if "Expected 4D" in text or "expected 4-dimensional input" in text.lower():
        return "Model validering fejlede: et lag forventer 4D input (batch, kanal, hoejde, bredde)."

    if "Expected 2D" in text or "expected 2-dimensional input" in text.lower():
        return "Model validering fejlede: et lag forventer 2D input. Tip: brug Flatten foer et Dense/Linear lag."

    return f"Model validering fejlede: {text}"


def build_sequential_model(layer_defs: List[Dict[str, Any]]) -> nn.Sequential:
    if not layer_defs:
        raise ValueError("Du skal tilfoeje mindst et lag.")

    ordered_layers: "collections.OrderedDict[str, nn.Module]" = collections.OrderedDict()

    for index, layer_def in enumerate(layer_defs, start=1):
        layer_type = (layer_def.get("type") or "").strip()
        if not layer_type:
            raise ValueError(f"Lag {index}: lagtype mangler.")
        if layer_type not in TorcHdata["lagTyper"]:
            raise ValueError(f"Lag {index}: ukendt lagtype '{layer_type}'.")

        params_raw = layer_def.get("params", "")
        try:
            params = parse_param_string(params_raw)
        except ValueError as error:
            raise ValueError(f"Lag {index}: {error}") from error

        layer_constructor = TorcHdata["lagTyper"][layer_type]
        try:
            layer_instance = layer_constructor(**params)
        except TypeError as error:
            raise ValueError(
                f"Lag {index} ({layer_type}): parametre passer ikke. Fejl: {error}"
            ) from error

        ordered_layers[f"lag_{index}_{layer_type}"] = layer_instance

        activation_name = (layer_def.get("activation") or NO_ACTIVATION).strip()
        if activation_name and activation_name != NO_ACTIVATION:
            if activation_name not in TorcHdata["aktFunktioner"]:
                raise ValueError(f"Lag {index}: ukendt aktiveringsfunktion '{activation_name}'.")

            activation_constructor = TorcHdata["aktFunktioner"][activation_name]
            try:
                activation_instance = activation_constructor()
            except TypeError:
                if activation_name == "Softmax":
                    activation_instance = activation_constructor(dim=1)
                else:
                    raise

            ordered_layers[f"akt_{index}_{activation_name}"] = activation_instance

    return nn.Sequential(ordered_layers)


def validate_model_shape(model: nn.Module) -> None:
    dummy_batch = torch.randn(1, 1, 28, 28)
    try:
        with torch.no_grad():
            output = model(dummy_batch)
    except Exception as error:
        raise ValueError(_friendly_model_error(error)) from error

    if output.ndim < 2:
        raise ValueError(
            "Model validering fejlede: output skal mindst vaere 2D (batch, klasser/features)."
        )


def format_model_summary(model: nn.Module) -> str:
    lines: List[str] = []
    for name, layer in model.named_children():
        lines.append(f"{name}: {layer}")
    return "\n".join(lines)


def _mnist_loaders(batch_size: int = 32) -> tuple[DataLoader, DataLoader]:
    mnist_transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )

    train_set = datasets.MNIST(root="./data", train=True, download=True, transform=mnist_transform)
    test_set = datasets.MNIST(root="./data", train=False, download=True, transform=mnist_transform)

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=512, shuffle=False)
    return train_loader, test_loader


def _compute_loss(
    criterion: nn.Module,
    output: torch.Tensor,
    target: torch.Tensor,
) -> torch.Tensor:
    try:
        return criterion(output, target)
    except Exception as error:
        if output.ndim == 2 and target.ndim == 1:
            one_hot_target = F.one_hot(target, num_classes=output.shape[1]).float()
            return criterion(output, one_hot_target)
        raise error


class UserAI:
    """Brugerdefineret AI-builder med stabil traenings-API."""

    def __init__(self, *_: Any, **__: Any):
        # Behold fleksibel signatur for bagudkompatibilitet med gammel kode.
        pass

    def train(
        self,
        config: Dict[str, Any],
        progress_callback: Optional[ProgressCallback] = None,
        cancel_event: Optional[threading.Event] = None,
    ) -> Dict[str, Any]:
        history: List[Dict[str, Any]] = []

        def make_result(
            status: str,
            final_loss: Optional[float] = None,
            accuracy: Optional[float] = None,
            model_summary: str = "",
            error: Optional[str] = None,
        ) -> Dict[str, Any]:
            return {
                "status": status,
                "final_loss": final_loss,
                "accuracy": accuracy,
                "model_summary": model_summary,
                "history": history,
                "error": error,
            }

        try:
            epochs = int(config.get("epochs", 0))
            learning_rate = float(config.get("learning_rate", 0.0))
            loss_name = (config.get("loss") or "").strip()
            layer_defs = config.get("layers") or []

            if epochs <= 0:
                return make_result("failed", error="Epoker skal vaere et heltal over 0.")
            if learning_rate <= 0:
                return make_result("failed", error="Laeringsrate skal vaere over 0.")
            if loss_name not in TorcHdata["lossFunktioner"]:
                return make_result("failed", error="Vaelg en gyldig lossfunktion.")

            model = build_sequential_model(layer_defs)
            validate_model_shape(model)
            model_summary = format_model_summary(model)

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)

            loss_constructor = TorcHdata["lossFunktioner"][loss_name]
            criterion = loss_constructor()
            optimizer = optim.Adam(model.parameters(), lr=learning_rate)

            train_loader = config.get("train_loader")
            test_loader = config.get("test_loader")
            if train_loader is None or test_loader is None:
                train_loader, test_loader = _mnist_loaders(batch_size=32)

            total_batches = max(1, len(train_loader) * epochs)
            completed_batches = 0
            final_loss: Optional[float] = None

            model.train()
            for epoch in range(1, epochs + 1):
                for batch_index, (data, target) in enumerate(train_loader, start=1):
                    if cancel_event is not None and cancel_event.is_set():
                        return make_result(
                            status="cancelled",
                            final_loss=final_loss,
                            model_summary=model_summary,
                        )

                    data = data.to(device)
                    target = target.to(device)

                    optimizer.zero_grad()
                    output = model(data)
                    loss_tensor = _compute_loss(criterion, output, target)
                    loss_tensor.backward()
                    optimizer.step()

                    final_loss = float(loss_tensor.item())
                    completed_batches += 1
                    progress = min(1.0, completed_batches / total_batches)

                    step_record = {
                        "status": "running",
                        "epoch": epoch,
                        "epochs": epochs,
                        "batch": batch_index,
                        "batches": len(train_loader),
                        "loss": final_loss,
                        "progress": progress,
                    }
                    history.append(step_record)

                    if progress_callback:
                        progress_callback(step_record)

            model.eval()
            correct = 0
            total = 0

            with torch.no_grad():
                for data, target in test_loader:
                    if cancel_event is not None and cancel_event.is_set():
                        return make_result(
                            status="cancelled",
                            final_loss=final_loss,
                            model_summary=model_summary,
                        )

                    data = data.to(device)
                    target = target.to(device)
                    output = model(data)

                    if output.ndim < 2:
                        continue

                    prediction = output.argmax(dim=1)
                    correct += int((prediction == target).sum().item())
                    total += int(target.numel())

            accuracy = (100.0 * correct / total) if total > 0 else 0.0
            return make_result(
                status="completed",
                final_loss=final_loss,
                accuracy=accuracy,
                model_summary=model_summary,
            )

        except Exception as error:
            return make_result(status="failed", error=str(error))


