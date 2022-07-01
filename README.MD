# Оглавление:
Этот асинхронный [бот](https://t.me/St_srbot) предназначен для переноса стиля с помощью [CycleGAN](https://github.com/junyanz/CycleGAN), 
[медленного алгоритма](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html), а также повышения разрешения изображения 
с помощью [ESRGAN](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html). 

# Как это работает:
1.Изначально бот приветствует пользователя, затем тот выбирает одну из 7 возможных категорий для преобразования изображений: \
1)Summer⇄winter,  
2)Photo⇄Monet(стиль Клода Моне), \
3)Photo⇄Cezanne(стиль Поля Сезанна), \
4)Photo⇄Ukiyoe(стиль изобр. искусства Японии), \
5)oto⇄Vangogh(стиль Винсента Ван Гога), \
6)вышение разрешения изображения, \
7)Собственное изображение для переноса стиля.

2. После этого бот принимает изображения выбранного стиля от пользователя, обрабатывает и отправляет ему обратно.

<strong>Все операции асинхронны, одному пользователю нельзя одновременно обрабатывать больше чем одно изображение. При попытке загрузить фото, или выбрать другую категорию во время процессинга выйдет соответствующее предупреждение.</strong>

# Примеры работы:
![Screenshot_20220701-130256_Telegram](https://user-images.githubusercontent.com/62743692/176903471-eee61e4a-c2cd-4ef3-8284-89a7f55b476c.jpg)---->>>
![Screenshot_20220701-130321_Telegram](https://user-images.githubusercontent.com/62743692/176903482-0d401b0b-0dd0-4ece-95e9-6e54797f239a.jpg)

![Screenshot_20220701-130146_Telegram](https://user-images.githubusercontent.com/62743692/176903680-dd1388ec-c1e1-4305-a373-96b599927d38.jpg)---->>>
![Screenshot_20220701-130153_Telegram](https://user-images.githubusercontent.com/62743692/176903687-d8875627-46fb-48d1-b55d-c189c79b8d00.jpg)

![Screenshot_20220701-130124_Telegram](https://user-images.githubusercontent.com/62743692/176903788-d4d4e3eb-b0d0-4c4a-ad88-5be819be1e20.jpg)---->>>
![Screenshot_20220701-130135_Telegram](https://user-images.githubusercontent.com/62743692/176903782-fa20e1b2-a46c-4de1-8c83-a737a6f2d921.jpg)


https://user-images.githubusercontent.com/62743692/176929922-7a23df1f-3195-470d-b8bf-24fd7a45ac2b.mp4

https://user-images.githubusercontent.com/62743692/176930667-d829009f-9613-43eb-92f5-fa83a16a0d28.mp4



# Установка:





1 способ:
1. Последовательно прописать команды:
```
git clone https://github.com/Slavikss/TSBot_project.git

cd TSBot_project

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```
2. В папке `venv` создать файл `token.env` и вставить токен вашего бота(`TOKEN` = ____) 
3. Скачать [веса](https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY) модели `RDRB_ESRGAN_X4.pth` и поместить в `ESRGAN/models/`
4. Скачать [веса](https://drive.google.com/drive/folders/1KC7TWXIOqX1oEzp_ur74njAqJjL4753S?usp=sharing) для CycleGAN и поместить их в `CycleGAN/checkpoints/`
3. Выполнить `python3 main.py`, 
 В случае успешной загрузки бота, он пропишет соответствующую строку в консоли.
---
2 способ: 
1. Загрузить папку с проектом на свой `GoogleDrive`.
2. Открыть `TSBot_project.ipynb`.
3. Примонтировать свой `GoogleDrive` к `Colab`.
4. Скачать [веса](https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY) модели `RDRB_ESRGAN_X4.pth` и поместить в `ESRGAN/models/`
5. Скачать [веса](https://drive.google.com/drive/folders/1KC7TWXIOqX1oEzp_ur74njAqJjL4753S?usp=sharing) для CycleGAN и поместить их в `CycleGAN/checkpoints/`
6. Вставить токен в `TOKEN`.
7. Запустить все ячейки.

