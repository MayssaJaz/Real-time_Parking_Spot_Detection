import torch
import os


# Function to load a pre-trained model


def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_path = os.getenv('MODEL_PATH')
    state_dict = torch.load(model_path, map_location=device)
    model = torch.hub.load('pytorch/vision:v0.10.0',
                           os.getenv('MODEL_ID'), pretrained=True)
    for params in model.parameters():
        params.requires_grad_ = False
    # add a new final layer
    nr_filters = model.fc.in_features  # number of input features of last layer
    model.fc = torch.nn.Linear(nr_filters, 1)

    # Load the model
    model.load_state_dict(state_dict)
    model = model.to(device)
    # Set the model to evaluation mode
    model.eval()
    return model, device