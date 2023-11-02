import numpy as np
import torch as th
import cv2
from PIL import Image
import time
import copy
import numpy as np
import open_clip
import torchvision.transforms as T

def calculate_l2_distances(query, gallery):
    return np.linalg.norm(gallery - query, axis=1)

def get_k_nearest_neighbors(distances, k):
    indices = np.argsort(distances)[:k]
    return indices

def get_similarity_l2(embeddings_gallery, embeddings_query, k):
    print('Processing indices...')

    s = time.time()

    scores = []
    indices = []

    for query in embeddings_query:
        distances = calculate_l2_distances(query, embeddings_gallery)
        nearest_indices = get_k_nearest_neighbors(distances, k)
        scores.append(distances[nearest_indices])
        indices.append(nearest_indices)

    e = time.time()

    print(f'Finished processing indices, took {e - s}s')
    return np.array(scores), np.array(indices)

def get_transform():  
    transform = T.Compose([
            T.Resize(
                size=(224, 224), 
                interpolation=T.InterpolationMode.BICUBIC,
                antialias=True),
            T.ToTensor(), 
            T.Normalize(
                mean=(0.48145466, 0.4578275, 0.40821073), 
                std=(0.26862954, 0.26130258, 0.27577711)
            )
        ])
    return transform

def convert_indices_to_labels(indices, labels):
    indices_copy = copy.deepcopy(indices)
    for row in indices_copy:
        for j in range(len(row)):
            row[j] = labels[row[j]]
    return indices_copy

def read_image(image_file):
    img = cv2.imread(
        image_file, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION
    )
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if img is None:
        raise ValueError('Failed to read {}'.format(image_file))
    return img


def transform_img(image):
    img = image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    if isinstance(img, np.ndarray):
        img =  Image.fromarray(img)

    transform = get_transform()
        
    img = transform(img)

    return img

@th.no_grad()
def get_feature_vector_img(model, imgs, epoch=10, use_cuda=False):
    features = []
    if use_cuda:
        imgs = imgs.cuda()
    x = (model(imgs)).detach().cpu().numpy().astype(np.float32)  # .half()
    features.append(x)

    return np.concatenate(features, axis=0)

def Model():
    backbone = open_clip.create_model_and_transforms('ViT-H-14', None)[0].visual
    backbone.load_state_dict(th.load('./model1.pt'))
    backbone.eval()   # Dropping unecessary layers
    return backbone

def find(img_path):

    image = read_image(img_path)

    image = transform_img(image)

    image = image.unsqueeze(dim=0)

    feature_vectors_gallery = np.load('./VPR image similarity search/gallary_embedding/feature_vectors_gallery.npy')

    model = Model()

    feature_vectors_query = get_feature_vector_img(model, image, 1)

    _, indices = get_similarity_l2(feature_vectors_gallery, feature_vectors_query, 1000)

    indices = indices.tolist()

    return indices