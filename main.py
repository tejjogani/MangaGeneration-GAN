
import os, time, sys
import matplotlib.pyplot as plt
import itertools
import pickle
import imageio
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torchvision.utils import save_image
from torch.autograd import Variable
from AnimeDataset import AnimeDataset


#setting hyperparameters
batch_size = 128
learning_rate = 0.0002
n_epoch = 20
img_size = 64
cuda = True if torch.cuda.is_available() else False

def main():
    #Setting the DataLoader
    directory = "images/"
    dataset = AnimeDataset(directory)
    training_data_loader = torch.utils.data.DataLoader(dataset, batch_size=128, shuffle=True)
    '''
    FOR TESTING
    temp = training_data_loader.dataset.__getitem__(1)
    print(temp.shape[1] == 64)
    ''' 
    #BUILDING NETWORK STRUCTURE
    generator = Generator(128)
    discriminator = Discriminator(128)
    generator.cuda()
    discriminator.cuda()
    
    generator.weight_init(mean=0.0, std=0.02)
    discriminator.weight_init(mean=0.0, std=0.02)
    
    criterion = nn.BCELoss()
    criterion.cuda()
    optimizer_dis = optim.Adam(discriminator.parameters(),lr=learning_rate, betas=(0.5, 0.999))
    optimizer_gen = optim.Adam(generator.parameters(), lr=learning_rate, betas=(0.5, 0.999))

    Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor

    #TRAINING
    for epoch in range(n_epoch):
        for i, (imgs, _) in enumerate(training_data_loader):
            real = Variable(Tensor(imgs.shape[0], 1).fill_(0.9), requires_grad=False)
            fake = Variable(Tensor(imgs.shape[0], 1).fill_(0.1), requires_grad=False)

            real_imgs = Variable(imgs.type(Tensor))
            z_vec = Variable(Tensor(np.random.normal(0, 1, (imgs.shape[0], opt.latent_dim))))
            optimizer_gen.zero_grad()
            generator_images = generator(z_vec)
            g_loss = criterion(discriminator(generator_images), real)
            g_loss.backward()
            optimizer_gen.step()

            #DISCRIMINATOR
            optimizer_disc.zero_grad()
            real_img_loss = criterion(discriminator(real_imgs), real)
            fake_img_loss = criterion(discriminator(generator_images.detach()), fake)
            disc_loss = (real_img_loss + fake_img_loss)/2
            disc_loss.backward()
            optimizer_disc.step()

            print(
                "[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f]"
                % (epoch, n_epoch, i, len(training_data_loader), disc_loss.item(), g_loss.item())
            )
            batches_done = epoch * len(training_data_loader) + i
            if batches_done % 32 == 0:
                save_image(gen_imgs.data[:25], "images_save/%d.png" % batches_done, nrow=5, normalize=True)

if __name__ == "__main__":
    main()





