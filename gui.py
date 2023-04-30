import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
import torch
from diffusers import StableDiffusionPipeline
from PIL import ImageQt


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        self.inference_path = 'mount/inf_model'
        self.alt_models = 'mount/models'
        
        if not os.path.exists(self.alt_models):
            os.makedirs(self.alt_models)
        
        if not os.path.exists(self.inference_path):
            print ('Downloading Base Model')
            pipe_name ="CompVis/stable-diffusion-v1-4"

            self.pipe = StableDiffusionPipeline.from_pretrained(pipe_name, torch_dtype=torch.float16)
            self.pipe.to("cuda")
            self.pipe.save_pretrained(self.inference_path)
        
        shutil.copy(self.inference_path+'/unet/diffusion_pytorch_model.bin',
                    self.alt_models+'/original.bin')
        
        self.load_model()
        self.init_ui()

    def load_model(self):
        print ('Loading Pretrained Model')
        self.pipe = StableDiffusionPipeline.from_pretrained(self.inference_path, torch_dtype=torch.float16)
        self.pipe.to("cuda")   
        
    def text_to_pil(self,text):
        image = self.pipe(prompt=text).images[0]
        return image

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.text_prompt = QLineEdit()
        self.layout.addWidget(self.text_prompt)

        self.pixmap = QPixmap(512, 512)
        self.pixmap.fill(QColor("black"))
        self.pixmap_label = QLabel(self)
        self.pixmap_label.setPixmap(self.pixmap)
        self.pixmap_label.setAlignment(Qt.AlignCenter)  # Set the alignment of the pixmap_label to center
        self.layout.addWidget(self.pixmap_label)

        self.button = QPushButton("Execute Prompt")
        self.button.clicked.connect(self.execute_prompt)  # Connect the button to the execute_prompt method
        self.layout.addWidget(self.button)
        
        self.model_selector = QComboBox()
        self.populate_model_selector()
        self.model_selector.currentIndexChanged.connect(self.update_model_symlink)
        self.layout.addWidget(self.model_selector)
        
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)  # Set the QVBoxLayout alignment to center alignment

        self.setWindowTitle("Stable Diffusion GUI")
        self.setGeometry(100, 100, 600, 600)
        
    def populate_model_selector(self):
        for file in os.listdir(self.alt_models):
            if os.path.isfile(os.path.join(self.alt_models, file)):
                self.model_selector.addItem(file)

    def update_model_symlink(self, index):
        selected_model = self.model_selector.itemText(index)
        source = os.path.join(self.alt_models, selected_model)
        target = os.path.join(self.inference_path, 'unet', 'diffusion_pytorch_model.bin')
        if os.path.exists(target):
            os.remove(target)
        os.link(source, target)
        self.load_model()

    def execute_prompt(self):
        text = self.text_prompt.text()
        pil_image = self.text_to_pil(text)
        qt_image = ImageQt.ImageQt(pil_image)  # Convert PIL image to QImage
        self.pixmap = QPixmap.fromImage(qt_image)  # Convert QImage to QPixmap
        self.pixmap = self.pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.pixmap_label.setPixmap(self.pixmap)

def main():
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
