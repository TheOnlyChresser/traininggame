import threading
import unittest

import torch
from torch.utils.data import DataLoader, TensorDataset

from Include.ai import UserAI, build_sequential_model, parse_param_string, validate_model_shape
from data.ai_terms import NO_ACTIVATION


def tiny_loaders(batch_size=4):
    # Lille deterministisk datasamling, så tests er hurtige og stabile.
    torch.manual_seed(7)
    features = torch.randn(16, 1, 28, 28)
    labels = torch.randint(0, 10, (16,))

    train_dataset = TensorDataset(features, labels)
    test_dataset = TensorDataset(features.clone(), labels.clone())

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader


class BackendTests(unittest.TestCase):
    def test_parse_param_string_valid_values(self):
        # Verificerer typekonvertering for int, float, tuple og bool.
        parsed = parse_param_string("out_features=128,p=0.2,kernel_size=(3,3),batch_first=True")
        self.assertEqual(parsed["out_features"], 128)
        self.assertEqual(parsed["p"], 0.2)
        self.assertEqual(parsed["kernel_size"], (3, 3))
        self.assertIs(parsed["batch_first"], True)

    def test_parse_param_string_invalid_format(self):
        # Manglende '=' skal give en valideringsfejl.
        with self.assertRaises(ValueError):
            parse_param_string("out_features:128")

    def test_layer_instantiation_and_activation(self):
        # Bekræfter at lag og aktivering oprettes i korrekt rækkefølge.
        model = build_sequential_model(
            [
                {"type": "Flatten", "params": "", "activation": NO_ACTIVATION},
                {"type": "Linear", "params": "in_features=784,out_features=32", "activation": "ReLU"},
                {"type": "Linear", "params": "in_features=32,out_features=10", "activation": NO_ACTIVATION},
            ]
        )
        names = list(dict(model.named_children()).keys())
        self.assertIn("lag_1_Flatten", names)
        self.assertIn("lag_2_Linear", names)
        self.assertIn("akt_2_ReLU", names)

    def test_shape_validation_shows_flatten_hint(self):
        # Linear uden Flatten skal give en hjælpsom form-fejl.
        model = build_sequential_model(
            [{"type": "Linear", "params": "in_features=784,out_features=10", "activation": NO_ACTIVATION}]
        )
        with self.assertRaises(ValueError) as context:
            validate_model_shape(model)
        self.assertIn("Flatten", str(context.exception))

    def test_training_progress_and_completion(self):
        # Træning skal levere løbende fremdrift og ende med statusværdien "completed".
        train_loader, test_loader = tiny_loaders()
        updates = []

        result = UserAI().train(
            {
                "epochs": 2,
                "learning_rate": 0.001,
                "loss": "CrossEntropyLoss",
                "layers": [
                    {"type": "Flatten", "params": "", "activation": NO_ACTIVATION},
                    {"type": "Linear", "params": "in_features=784,out_features=10", "activation": NO_ACTIVATION},
                ],
                "train_loader": train_loader,
                "test_loader": test_loader,
            },
            progress_callback=updates.append,
            cancel_event=threading.Event(),
        )

        self.assertEqual(result["status"], "completed")
        self.assertGreater(len(updates), 0)
        self.assertGreaterEqual(updates[-1]["progress"], 1.0)

    def test_training_cancel(self):
        # Annulleringsevent skal stoppe træningen og returnere statusværdien "cancelled".
        train_loader, test_loader = tiny_loaders()
        cancel_event = threading.Event()

        def callback(_payload):
            cancel_event.set()

        result = UserAI().train(
            {
                "epochs": 5,
                "learning_rate": 0.001,
                "loss": "CrossEntropyLoss",
                "layers": [
                    {"type": "Flatten", "params": "", "activation": NO_ACTIVATION},
                    {"type": "Linear", "params": "in_features=784,out_features=10", "activation": NO_ACTIVATION},
                ],
                "train_loader": train_loader,
                "test_loader": test_loader,
            },
            progress_callback=callback,
            cancel_event=cancel_event,
        )

        self.assertEqual(result["status"], "cancelled")


if __name__ == "__main__":
    unittest.main()
