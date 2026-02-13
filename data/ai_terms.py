SAFE_LAYER_TYPES = ["Flatten", "Linear", "Dropout"]
NO_ACTIVATION = "Ingen"

# Eksempeltekster brugt som hjælpehint i parameterfeltet pr. lag.
LAYER_PARAM_TEMPLATES = {
    "Flatten": "",
    "Linear": "in_features=784,out_features=128",
    "Dropout": "p=0.2",
    "Conv2d": "in_channels=1,out_channels=16,kernel_size=3,padding=1",
    "MaxPool2d": "kernel_size=2,stride=2",
    "RNN": "input_size=28,hidden_size=64,batch_first=True",
    "GRU": "input_size=28,hidden_size=64,batch_first=True",
    "LSTMCell": "input_size=28,hidden_size=64",
}

# Centralt ordlisteindhold til infopopups i opsætning/lag/resultatskærme.
AI_INFO = {
    "antal_lag": {
        "title": "Antal lag",
        "description": "Antal lag styrer hvor mange trin din model bestaar af.",
        "example": "Eksempel: 3",
    },
    "epoker": {
        "title": "Epoker",
        "description": "En epoke betyder at modellen ser hele traeningsdatasettet en gang.",
        "example": "Eksempel: 3",
    },
    "laeringsrate": {
        "title": "Laeringsrate",
        "description": "Laeringsraten bestemmer hvor store opdateringer modellen laver i hver iteration.",
        "example": "Eksempel: 0.001",
    },
    "lossfunktion": {
        "title": "Lossfunktion",
        "description": "Loss maaler hvor forkert modellen er, saa den kan forbedres under traening.",
        "example": "Eksempel: CrossEntropyLoss til klassifikation.",
    },
    "avanceret_tilstand": {
        "title": "Avanceret tilstand",
        "description": "Avanceret tilstand viser alle lagtyper. Standardtilstand viser sikre begynderlag.",
        "example": "Eksempel: Slukket = Flatten, Linear, Dropout.",
    },
    "lagtype": {
        "title": "Lagtype",
        "description": "Lagtype bestemmer hvilken operation der koeres i det valgte lag.",
        "example": "Eksempel: Linear, Dropout eller Conv2d.",
    },
    "parametre": {
        "title": "Parametre",
        "description": "Parametre konfigurerer lagets opfoersel. Brug formatet key=value adskilt med komma.",
        "example": "Eksempel: in_features=784,out_features=128",
    },
    "per_lag_aktivering": {
        "title": "Per-lag aktivering",
        "description": "Du kan vaelge en aktiveringsfunktion efter hvert lag eller Ingen.",
        "example": "Eksempel: ReLU efter et Linear-lag.",
    },
    "resultat_loss": {
        "title": "Loss i resultat",
        "description": "Viser den seneste tab-vaerdi fra traeningen. Lavere er typisk bedre.",
        "example": "Eksempel: 0.2451",
    },
    "resultat_accuracy": {
        "title": "Accuracy",
        "description": "Accuracy er andelen af korrekte forudsigelser paa testdata i procent.",
        "example": "Eksempel: 92.40%",
    },
    "layer_flatten": {
        "title": "Flatten",
        "description": "Flatten omdanner billed-tensorer til en flad vektor foer Dense/Linear lag.",
        "example": "Eksempel: brug Flatten foer Linear.",
    },
    "layer_linear": {
        "title": "Linear",
        "description": "Linear er et klassisk dense lag med vaegte og bias.",
        "example": "Eksempel: in_features=784,out_features=128",
    },
    "layer_dropout": {
        "title": "Dropout",
        "description": "Dropout slaar tilfaeldigt neuroner fra under traening for at reducere overfitting.",
        "example": "Eksempel: p=0.2",
    },
    "layer_conv2d": {
        "title": "Conv2d",
        "description": "Conv2d finder lokale moenstre i billeder via filtre.",
        "example": "Eksempel: in_channels=1,out_channels=16,kernel_size=3",
    },
    "layer_maxpool2d": {
        "title": "MaxPool2d",
        "description": "MaxPool2d nedskalerer feature maps ved at tage maksimum i hvert vindue.",
        "example": "Eksempel: kernel_size=2,stride=2",
    },
}


def get_layer_info_key(layer_type):
    # Mapper valgt lagtype til dedikeret ordlistepost, når den findes.
    if not layer_type:
        return "lagtype"
    candidate = f"layer_{layer_type.lower()}"
    if candidate in AI_INFO:
        return candidate
    return "lagtype"


def get_info_text(info_key):
    # Returnerer infovinduesklar titel/brødtekst med eksempel tilføjet, når tilgængelig.
    info = AI_INFO.get(info_key)
    if not info:
        info = {
            "title": "Info",
            "description": "Ingen forklaring fundet for dette emne endnu.",
            "example": "",
        }
    example = info.get("example", "").strip()
    body = info.get("description", "")
    if example:
        body = f"{body}\n\n{example}"
    return info.get("title", "Info"), body


def get_layer_param_placeholder(layer_type):
    # Reserveværdi holder parameterfeltet brugbart for ukendte/egne lagnavne.
    return LAYER_PARAM_TEMPLATES.get(layer_type, "key=value")


