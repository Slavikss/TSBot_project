# Оглавление:
Этот асинхронный [бот](https://t.me/St_srbot) предназначен для переноса стиля с помощью [CycleGAN](https://github.com/junyanz/CycleGAN), 
[медленного алгоритма](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html), а также повышения разрешения изображения 
с помощью [ESRGAN](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html). 

# Как это работает:
1.Изначально бот приветствует пользователя, затем тот выбирает одну из 7 возможных категорий для преобразования изображений: 
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
2. В папке venv создать файл token.env и вставить токен вашего бота(TOKEN = ____) 
3. Скачать [веса](https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY) модели `RDRB_ESRGAN_X4.pth` и поместить в `ESRGAN/models/`
4. Скачать [веса](https://drive.google.com/drive/folders/1KC7TWXIOqX1oEzp_ur74njAqJjL4753S?usp=sharing) для CycleGAN и поместить их в `CycleGAN/checkpoints/`
3. Выполнить "python3 main.py", 
 В случае успешной загрузки бота, он пропишет соответствующую строку в консоли.
---
2 способ: 
1. Загрузить папку с проектом на свой GoogleDrive.
2. Открыть TSBot_project.ipynb.
3. Примонтировать свой GoogleDrive к Colab.
4. Запустить все ячейки.

