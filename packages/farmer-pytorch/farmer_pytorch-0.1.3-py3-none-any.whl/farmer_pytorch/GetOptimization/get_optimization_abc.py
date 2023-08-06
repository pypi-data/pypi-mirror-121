import torch
from pathlib import Path
from .get_optimization_fn import get_prog_bar


class GetOptimizationABC:
    batch_size: int
    epochs: int
    lr: float
    gpu: int
    optim_obj: torch.optim.Optimizer

    def __init__(self, model, loss_func, metrics, train_dataset, val_dataset):
        self.model = model
        self.loss_func = loss_func
        self.metrics = metrics
        self.train_dataset = train_dataset
        self.val_dataset = val_dataset

    def __call__(self):

        train_loader = torch.utils.data.DataLoader(
            self.train_dataset, batch_size=self.batch_size, shuffle=True)
        valid_loader = torch.utils.data.DataLoader(
            self.val_dataset, batch_size=self.batch_size, shuffle=False)

        device = torch.device(
            f"cuda:{self.gpu}" if torch.cuda.is_available() else "cpu")
        print(device)
        self.model.to(device)

        self.optimizer = self.optim_obj(
            [dict(params=self.model.parameters(), lr=self.lr)])

        save_model_dir = Path("./models")
        save_model_dir.mkdir(exist_ok=True)

        for epoch in range(self.epochs):
            print(f"\ntrain step, epoch: {epoch + 1}/{self.epochs}")
            self.model.train()
            training_loss, training_dice = 0, 0
            nb_iters = len(train_loader.dataset) // self.batch_size + 1
            for i, data in enumerate(train_loader, 1):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data
                inputs, labels = inputs.to(device), labels.to(device)

                outputs = self.model(inputs)
                loss = self.loss_func(outputs, labels)

                # zero the parameter gradients
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                # print statistics
                training_loss += loss.item()
                training_dice += self.metrics(outputs, labels).item()
                cout = get_prog_bar(i, nb_iters)
                cout += f" loss: {(training_loss / i):.5g}"
                cout += f" dice: {(training_dice / i):.5g}"
                print("\r"+cout, end="")

            # validation step
            print("\nvalidation step")
            self.model.eval()
            total_loss, total_dice = 0, 0
            with torch.no_grad():
                nb_iters = len(valid_loader.dataset) // self.batch_size + 1
                for i, data in enumerate(valid_loader, 1):
                    inputs, labels = data
                    inputs, labels = inputs.to(device), labels.to(device)
                    outputs = self.model(inputs)
                    total_loss += self.loss_func(outputs, labels).item()
                    total_dice += self.metrics(outputs, labels).item()

                    cout = get_prog_bar(i, nb_iters)
                    val_loss, val_dice = total_loss / i, total_dice / i
                    cout += f" val_loss: {val_loss:.5g}"
                    cout += f" val_dice: {val_dice:.5g}"
                    print("\r"+cout, end="")

            model_path = f'{save_model_dir}/model_epoch{epoch}.pth'
            torch.save(self.model.state_dict(), model_path)

            self.on_epoch_end()  # custom callbacks

        print('\nFinished Training')
        return val_dice

    def on_epoch_end(self):
        pass
