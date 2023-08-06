import torch; torch.cuda.empty_cache()
from torchvision import transforms
from PIL import Image
from skimage.transform import resize
from .utils import cvt1to3channels, normalize_image
import os
def output_mask(img):

    skpath = os.path.dirname(__file__)+'/weights/dti.pth'
    model = torch.hub.load('mateuszbuda/brain-segmentation-pytorch', 'unet',
                        in_channels=3, out_channels=1, init_features=32,
                        pretrained=False)
    # load pretrained weights trianed on our data
    model.load_state_dict(torch.load(skpath, map_location=torch.device('cpu')))
    
    for p in model.parameters():
        p.requires_grad = False
    model.eval()

    trans = transforms.Compose([transforms.Resize((225,225)),transforms.CenterCrop(256), transforms.ToTensor()])

    img = normalize_image(img)
    tensor_stack = trans(Image.fromarray(cvt1to3channels(img.astype('uint8')))).unsqueeze(0)
    
    mask_tensor = model(tensor_stack)[0,0,:,:]

    out_trans = transforms.Compose([
                        transforms.CenterCrop((225,225)),
                    ])
    mask_orig = resize(out_trans(mask_tensor).numpy(),(img.shape[0],img.shape[1]))
    return mask_orig

