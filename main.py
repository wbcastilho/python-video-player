import tkinter
import tkVideoPlayer
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk


def freeze_first_frame(video_path):
    cap = cv2.VideoCapture(video_path)

    # Verificar se o vídeo foi aberto corretamente
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    # Ler o primeiro quadro do vídeo
    ret, frame = cap.read()

    # Converter o quadro para o formato RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Criar uma imagem PIL a partir do quadro
    image = Image.fromarray(frame_rgb)

    # Definir as dimensões
    width = 275
    height = 140

    # # Calcular a altura proporcionalmente à largura desejada
    # aspect_ratio = image.width / image.height
    # height = int(width / aspect_ratio)

    # Redimensionar a imagem para o tamanho desejado
    image = image.resize((width, height))

    # Exibir a imagem no Tkinter
    image_tk = ImageTk.PhotoImage(image)
    label.configure(image=image_tk)
    label.image = image_tk
    label.place(x=1, y=46)

    # Liberar os recursos
    cap.release()


def play():
    video.play()
    label.place_forget()


def pause():
    video.pause()


def stop():
    video.stop()
    label.place(x=1, y=46)


def load_video():
    file_path = filedialog.askopenfile()
    if file_path:
        print(file_path)
        video.load(file_path.name)
        freeze_first_frame(file_path.name)


def seek(value):
    video.seek(int(value))


def update_scale(event):
    progress_value.set(int(video.current_duration()))


def update_duration(event):
    duration = video.video_info()["duration"]
    progress_slider["to"] = duration


def video_ended(event):
    progress_slider.set(progress_slider["to"])
    progress_slider.set(0)
    label.place(x=1, y=46)


if __name__ == '__main__':
    # Contruir Tela
    root = tkinter.Tk()
    root.title("Mini Vídeo Player")
    root.geometry("300x300")
    root.resizable(True, True)

    frame = tkinter.Frame(root)
    frame.grid(row=0, padx=10, pady=10)

    # Botão Load
    btLoad = tkinter.Button(frame, text="Browse", width=10, borderwidth=2, background="gray", command=load_video)
    btLoad.grid(row=0, column=0, padx=10, pady=10)
    # btLoad.pack(padx=10, pady=10, anchor=tkinter.NW)

    video_frame = tkinter.Frame(frame, background="gray", width=275, height=140)
    video_frame.grid(row=1)

    # Video
    video = tkVideoPlayer.TkinterVideo(video_frame, scaled=True, keep_aspect=True, background="black")
    video.place(x=0, y=0, width=275, height=140)
    video.bind("<<Duration>>", update_duration)
    video.bind("<<SecondChanged>>", update_scale)
    video.bind("<<Ended>>", video_ended)

    slider_frame = tkinter.Frame(frame)
    slider_frame.grid(row=2, pady=10)

    # Progress slider
    progress_value = tkinter.IntVar(slider_frame)
    progress_slider = tkinter.Scale(slider_frame, variable=progress_value, length=150, from_=0, to=0, showvalue=False,
                                    orient="horizontal", width=10, command=seek)
    progress_slider.grid(row=0, column=1)

    buttons_frame = tkinter.Frame(frame)
    buttons_frame.grid(row=3)

    # Botão Play
    btPlay = tkinter.Button(buttons_frame, text="Play", relief="flat", background="gray", width=10, borderwidth=2,
                            command=play)
    btPlay.grid(row=0, column=0, padx=10, pady=10)

    # Botão Pause
    btPause = tkinter.Button(buttons_frame, text="Pause", relief="flat", background="gray", width=10, borderwidth=2,
                             command=pause)
    btPause.grid(row=0, column=1)

    # Botão Stop
    btStop = tkinter.Button(buttons_frame, text="Stop", relief="flat", background="gray", width=10, borderwidth=2, command=stop)
    btStop.grid(row=0, column=2, padx=10, pady=10)

    label = tkinter.Label(frame, background="black")
    label.place(x=1, y=46)

    root.mainloop()
