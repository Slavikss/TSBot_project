# Content:
This asynchronous [bot](https://t.me/St_srbot) designed for transfer style with [CycleGAN](https://github.com/junyanz/CycleGAN), 
[slow algorithm](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html) and also to increase the resolution of the image using [ESRGAN](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html). 

# How it works:
Initially, the bot welcomes the user, then he chooses one of 7 possible categories for image conversion:
1. Summer⇄winter,
2. Photo⇄Monet(Claude Monet style)
3. Photo⇄Cezanne(style of Paul Cezanne)
4. Photo⇄Ukiyoe(image style arts of Japan)
5. Kyoto⇄Vangogh(Vincent Van Gogh style)
6. Image resolution improvement
7. Custom image for style transfer

2. After that, the bot accepts images of the selected style from the user, processes and sends them back to him.
<strong>All operations are asynchronous, it is not allowed to process more than one image for one user at the same time. When attempting to upload photo, or choose another category while image processe, bot raises warning. </strong>

# Examples of work:
1.
![Screenshot_20220701-130256_Telegram](https://user-images.githubusercontent.com/62743692/176903471-eee61e4a-c2cd-4ef3-8284-89a7f55b476c.jpg)→→→→→→→
![Screenshot_20220701-130321_Telegram](https://user-images.githubusercontent.com/62743692/176903482-0d401b0b-0dd0-4ece-95e9-6e54797f239a.jpg)

2.
![Screenshot_20220701-130146_Telegram](https://user-images.githubusercontent.com/62743692/176903680-dd1388ec-c1e1-4305-a373-96b599927d38.jpg)→→→→→→→
![Screenshot_20220701-130153_Telegram](https://user-images.githubusercontent.com/62743692/176903687-d8875627-46fb-48d1-b55d-c189c79b8d00.jpg)

3.
![Screenshot_20220701-130124_Telegram](https://user-images.githubusercontent.com/62743692/176903788-d4d4e3eb-b0d0-4c4a-ad88-5be819be1e20.jpg)→→→→→→→→
![Screenshot_20220701-130135_Telegram](https://user-images.githubusercontent.com/62743692/176903782-fa20e1b2-a46c-4de1-8c83-a737a6f2d921.jpg)

4.
https://user-images.githubusercontent.com/62743692/176929922-7a23df1f-3195-470d-b8bf-24fd7a45ac2b.mp4

5.
https://user-images.githubusercontent.com/62743692/176930667-d829009f-9613-43eb-92f5-fa83a16a0d28.mp4



# Installation:





1-st way:
1. Sequentially write this commands:
```
git clone https://github.com/Slavikss/TSBot_project.git

cd TSBot_project

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```
2.  Create file `token.env` in `venv` dir and insert your bot's token(`TOKEN` = ____) 
3. Download ESRGAN's [weights](https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY)(`RDRB_ESRGAN_X4.pth`) and put in `ESRGAN/models/`
4. Download CycleGAN's [weights](https://drive.google.com/drive/folders/1KC7TWXIOqX1oEzp_ur74njAqJjL4753S?usp=sharing) and put in `CycleGAN/checkpoints/`
3. Run `python3 main.py`, 
 If the bot is successfully loaded, it will write the corresponding line in the console.
---
2 way: 
1. Download folder with project to your `GoogleDrive`.
2. Open `TSBot_project.ipynb`.
3. Mount your `GoogleDrive` к `Colab`.
4. Download ESRGAN's [weights](https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY)(`RDRB_ESRGAN_X4.pth`) and put in `ESRGAN/models/`
5. Download CycleGAN's [weights](https://drive.google.com/drive/folders/1KC7TWXIOqX1oEzp_ur74njAqJjL4753S?usp=sharing) and put in `CycleGAN/checkpoints/`
6. Insert bot's token in `TOKEN`.
7. Run all cells.

