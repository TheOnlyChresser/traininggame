import typing
from collections import OrderedDict

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

from data.torchDATA import TorcHdata


LayerSpec = dict[str, typing.Any]


class UserAI:
    SUPPORTED_LAYERS = {"Linear", "Flatten", "Dropout"}
    SUPPORTED_LOSSES = {"L1Loss", "MSELoss", "HuberLoss", "BCEWithLogitsLoss", "KLDivLoss"}

    def __init__(
        self,
        layers: list[LayerSpec],
        activation_name: str,
        loss_name: str,
        epochs: int,
        learning_rate: float = 1e-3,
        device: str | None = None,
    ) -> None:
        self.layers = layers
        self.activation_name = activation_name
        self.loss_name = loss_name
        self.epochs = max(1, int(epochs))
        self.learning_rate = float(learning_rate)
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))

    def _activation(self) -> nn.Module:
        activation_cls = TorcHdata["aktFunktioner"].get(self.activation_name)
        if activation_cls is None:
            raise ValueError(f"Unsupported activation: {self.activation_name}")
        if self.activation_name == "Softmax":
            return activation_cls(dim=1)
        return activation_cls()

    def _loss(self) -> nn.Module:
        if self.loss_name not in self.SUPPORTED_LOSSES:
            supported = ", ".join(sorted(self.SUPPORTED_LOSSES))
            raise ValueError(f"Unsupported loss for this game: {self.loss_name}. Supported: {supported}")
        loss_cls = TorcHdata["lossFunktioner"].get(self.loss_name)
        if loss_cls is None:
            raise ValueError(f"Unknown loss function: {self.loss_name}")
        if self.loss_name == "KLDivLoss":
            return loss_cls(reduction="batchmean")
        return loss_cls()

    def _build_layer(self, layer_type: str, params: dict[str, typing.Any]) -> nn.Module:
        if layer_type not in self.SUPPORTED_LAYERS:
            supported = ", ".join(sorted(self.SUPPORTED_LAYERS))
            raise ValueError(f"Unsupported layer type in game mode: {layer_type}. Supported: {supported}")

        if layer_type == "Linear":
            in_features = int(params["in_features"])
            out_features = int(params["out_features"])
            return nn.Linear(in_features, out_features)
        if layer_type == "Flatten":
            start_dim = int(params.get("start_dim", 1))
            end_dim = int(params.get("end_dim", -1))
            return nn.Flatten(start_dim=start_dim, end_dim=end_dim)
        if layer_type == "Dropout":
            p = float(params.get("p", 0.5))
            return nn.Dropout(p=p)
        raise ValueError(f"Unsupported layer: {layer_type}")

    def _build_model(self) -> nn.Sequential:
        modules: list[tuple[str, nn.Module]] = []
        linear_indices = [i for i, layer in enumerate(self.layers) if str(layer.get("type")) == "Linear"]
        if not linear_indices:
            self.layers.append({"type": "Linear", "params": {"in_features": 784, "out_features": 10}})
            linear_indices = [len(self.layers) - 1]

        previous_out = 784

        for index, layer in enumerate(self.layers):
            layer_type = str(layer["type"])
            params = typing.cast(dict[str, typing.Any], layer["params"])
            if layer_type == "Linear":
                in_features = params.get("in_features", previous_out)
                out_features = params.get("out_features")
                if out_features is None:
                    out_features = 10 if index == linear_indices[-1] else 128
                params["in_features"] = int(in_features)
                params["out_features"] = int(out_features)
                previous_out = int(out_features)
            modules.append((f"{layer_type.lower()}_{index}", self._build_layer(layer_type, params)))
            if layer_type == "Linear" and index < len(self.layers) - 1:
                modules.append((f"activation_{index}", self._activation()))

        last_linear_index = linear_indices[-1]
        last_linear = typing.cast(dict[str, typing.Any], self.layers[last_linear_index]["params"])
        if int(last_linear["out_features"]) != 10:
            modules.append(("final_head", nn.Linear(int(last_linear["out_features"]), 10)))

        if not modules:
            raise ValueError("No layers configured.")

        model = nn.Sequential(OrderedDict(modules))
        return model.to(self.device)

    @staticmethod
    def _one_hot(target: torch.Tensor, num_classes: int) -> torch.Tensor:
        return torch.nn.functional.one_hot(target, num_classes=num_classes).float()

    def _compute_loss(self, criterion: nn.Module, output: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        num_classes = output.shape[1]
        if self.loss_name == "KLDivLoss":
            target_probs = self._one_hot(target, num_classes=num_classes)
            return criterion(torch.log_softmax(output, dim=1), target_probs)
        if self.loss_name in {"MSELoss", "L1Loss", "HuberLoss", "BCEWithLogitsLoss"}:
            target_vec = self._one_hot(target, num_classes=num_classes)
            return criterion(output, target_vec)
        return criterion(output, target)

    def run_training(self, progress_callback: typing.Callable[[dict[str, typing.Any]], None] | None = None) -> dict[str, typing.Any]:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

        train_set = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
        test_set = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

        train_subset = Subset(train_set, range(0, min(10000, len(train_set))))
        test_subset = Subset(test_set, range(0, min(2000, len(test_set))))

        train_loader = DataLoader(train_subset, batch_size=64, shuffle=True)
        test_loader = DataLoader(test_subset, batch_size=256, shuffle=False)

        model = self._build_model()
        criterion = self._loss()
        optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)

        latest_loss = 0.0
        for epoch_index in range(self.epochs):
            model.train()
            epoch_loss = 0.0
            batch_count = 0

            for data, target in train_loader:
                data = data.to(self.device)
                target = target.to(self.device)
                data = data.view(data.size(0), -1)

                optimizer.zero_grad()
                output = model(data)
                loss = self._compute_loss(criterion, output, target)
                loss.backward()
                optimizer.step()

                epoch_loss += float(loss.item())
                batch_count += 1

            latest_loss = epoch_loss / max(1, batch_count)
            if progress_callback:
                progress_callback(
                    {
                        "phase": "training",
                        "epoch": epoch_index + 1,
                        "epochs_total": self.epochs,
                        "progress": (epoch_index + 1) / self.epochs,
                        "loss": latest_loss,
                    }
                )

        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for data, target in test_loader:
                data = data.to(self.device)
                target = target.to(self.device)
                data = data.view(data.size(0), -1)
                output = model(data)
                predicted = output.argmax(dim=1)
                correct += int((predicted == target).sum().item())
                total += int(target.size(0))

        accuracy = 100.0 * correct / max(1, total)
        result = {"phase": "done", "progress": 1.0, "loss": latest_loss, "accuracy": accuracy}
        if progress_callback:
            progress_callback(result)
        return result
