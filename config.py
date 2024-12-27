import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QGridLayout, QScrollArea, QPushButton, QSizePolicy, QVBoxLayout, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
import os
import subprocess

# Variável da home do usuário
home_dir = os.path.expanduser("~")

# Caminho para arquivos de configurações
colors_conf = f"{home_dir}/.config/hypr/config.d/colors.conf"
borders_conf = f"{home_dir}/.config/hypr/config.d/borders.conf"
waybar_style = f"{home_dir}/.config/waybar/accent-color.css"
waybar_conf = f"{home_dir}/.config/waybar/config.jsonc"


class SystemInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informações do Sistema")
        self.setFixedSize(500, 500)  

        layout = QVBoxLayout(self)

        # Coletar informações do sistema
        distro = subprocess.getoutput("uname -a | awk '{print $2}'")
        kernel = subprocess.getoutput("uname -r")
        uptime = subprocess.getoutput("uptime -p | sed 's/up //g'")
        packages = subprocess.getoutput("pacman -Q | wc -l")
        flatpak = subprocess.getoutput("flatpak list --app | wc -l")
        aur = subprocess.getoutput("pacman -Qm | wc -l")
        de = subprocess.getoutput("echo $XDG_CURRENT_DESKTOP")
        session = subprocess.getoutput("echo $XDG_SESSION_TYPE")
        cpu = subprocess.getoutput("lscpu | grep '^Nome do modelo:' | awk '{print $5, $6, $7}'")
        used_mem = subprocess.getoutput("free -m | grep '^[Mem.:]' | awk '{print $3}'")
        total_mem = subprocess.getoutput("free -m | grep '^[Mem.:]' | awk '{print $2}'")
        total_disk = subprocess.getoutput("df -Th / | tail -1 | awk '{print $3}'")
        used_disk = subprocess.getoutput("df -Th / | tail -1 | awk '{print $4}'")
        graphics = subprocess.getoutput(
            """if [[ $(nvidia-smi) ]]; then
                nvidia-smi -q | grep "Product Name" | sed 's/.*: //;s/\\(.*\\)/[\\1]/'
            else
                lspci | grep VGA | awk '{print $11, $12, $13}'
            fi"""
        )
        temp_radeon = subprocess.getoutput(
            """if [[ $(nvidia-smi) ]]; then
                nvidia-smi -q | grep "GPU Current Temp" | sed 's/.*: //;s/ C/ºC/'
            else
                sensors | grep -A 0 'edge' | cut -c16-17
            fi"""
        )
        temp_cpu = subprocess.getoutput(
            """if [[ $(cat /proc/cpuinfo | grep "vendor_id" | head -n 1 | sed 's/.*: //') == 'GenuineIntel' ]]; then
                sensors | grep "Package" | sed 's/\..*//;s/.*+//'
            else
                sensors | grep -A 0 'temp1' | cut -c16-17
            fi"""
        )

        # Adicionar informações ao layout
        layout.addWidget(QLabel(f"<b>Distribuição:</b> {distro}"))
        layout.addWidget(QLabel(f"<b>Kernel:</b> {kernel}"))
        layout.addWidget(QLabel(f"<b>Ambiente de Desktop:</b> {de} ({session})"))
        layout.addWidget(QLabel(f"<b>Tempo de Atividade:</b> {uptime}"))
        layout.addWidget(QLabel(f"<b>Pacotes Instalados:</b><br>Pacman {packages}<br> Flatpak {flatpak}<br> AUR {aur}"))
        layout.addWidget(QLabel(f"<b>Memória:</b> {used_mem} / {total_mem} MB"))
        layout.addWidget(QLabel(f"<b>Disco:</b> {used_disk} / {total_disk}"))        
        layout.addWidget(QLabel(f"<b>CPU:</b> {cpu} ({temp_cpu}°C)"))
        layout.addWidget(QLabel(f"<b>Placa de Vídeo:</b> {graphics}] ({temp_radeon}°C)"))

        # Botão para fechar
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #383c4a;
            }
            QPushButton:hover {
                background: #556077;
            }        
        """)
        layout.addWidget(close_button)


class MainUi(QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        
        # Carregando arquivo UI e definindo o título do app
        loadUi(f"{home_dir}/.scripts/hypr/config.ui", self)
        self.setWindowTitle("Configurações")

        #Botões do app
        
        # Botão para abrir arquivo de configuração dos atalhos do hyprland
        self.btn_atalhos.clicked.connect(self.keybinds)
        #Estilo css
        self.btn_atalhos.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #383c4a;
            }
            QPushButton:hover {
                background: #556077;
            }
        """)

        # Botão para abrir arquivo de configuração dos módulos da waybar
        self.btn_regras.clicked.connect(self.window_rules)
        #Estilo css
        self.btn_regras.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #383c4a;
            }
            QPushButton:hover {
                background: #556077;
            }
        """)

        # Botão para abrir informações do systema (info.py)
        self.btn_sobre.clicked.connect(self.show_system_info)
        #Estilo css
        self.btn_sobre.setStyleSheet("""
            QToolButton {
                border: 1px solid #505567;
                background: #383c4a;
            }
            QToolButton:hover {
                background: #556077;
            }
        """)

        # Botão para definir a resolução 1280x720
        self.btn_720p.clicked.connect(self.set_720p)
        #Estilo css
        self.btn_720p.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #383c4a;
            }
            QPushButton:hover {
                background: #556077;
            }
        """)

        # Botão para definir a resolução 1920x1080
        self.btn_1080p.clicked.connect(self.set_1080p)
        #Estilo css
        self.btn_1080p.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #383c4a;
            }
            QPushButton:hover {
                background: #556077;
            }
        """)

        # Botão para definir cor de destaque vermelho
        self.btn_red.clicked.connect(self.make_red)
        #Estilo css
        self.btn_red.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #c91622;
            }
            QPushButton:hover {
                background: #e92621;
            }
        """)

        # Botão para definir a cor de destaque laranja
        self.btn_orange.clicked.connect(self.make_orange)
        #Estilo css
        self.btn_orange.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #fa7544;
            }
            QPushButton:hover {
                background: #ff8544;
            }
        """)

        # Botão para definir a cor de destaque amarelo
        self.btn_yellow.clicked.connect(self.make_yellow)
        #Estilo css
        self.btn_yellow.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #FABC3F;
            }
            QPushButton:hover {
                background: #fbcd4f;
            }
        """)

        # Botão para definir a cor de destaque verde
        self.btn_green.clicked.connect(self.make_green)
        #Estilo css
        self.btn_green.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #9ade44;
            }
            QPushButton:hover {
                background: #aafe55;
            }
        """)

        # Botão para definir a cor de destaque ciano
        self.btn_cian.clicked.connect(self.make_cian)
        #Estilo css
        self.btn_cian.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #44cdee;
            }
            QPushButton:hover {
                background: #65edfe;
            }
        """)

        # Botão para definir a cor de destaque rosa
        self.btn_pink.clicked.connect(self.make_pink)
        #Estilo css
        self.btn_pink.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #f766ab;
            }
            QPushButton:hover {
                background: #fa76bb;
            }
        """)

        # Botão para definir a cor de destaque roxo
        self.btn_purple.clicked.connect(self.make_purple)
        #Estilo css
        self.btn_purple.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #b75cfb;
            }
            QPushButton:hover {
                background: #c76cfd;
            }
        """)

        # Botão para criar thumbnails das imagens
        self.btn_recarregar.clicked.connect(self.make_thumbnails)
        #Estilo css
        self.btn_recarregar.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #383c4a;
            }
            QPushButton:hover {
                background: #556077;
            }
        """)

        # Botão para abrir diretório de imagens
        self.btn_imagens.clicked.connect(self.open_folder_walls)
        #Estilo css
        self.btn_imagens.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #383c4a;
            }
            QPushButton:hover {
                background: #556077;
            }
        """)

        # Conectando os sliders e botões
        self.bordersize_slider.valueChanged.connect(self.update_bordersize_label)
        self.borderradius_slider.valueChanged.connect(self.update_borderradius_label)
        self.btn_border.clicked.connect(self.apply_changes)
        self.btn_border.setStyleSheet("""
            QPushButton {
                border: 1px solid #505567;
                background: #383c4a;
            }
            QPushButton:hover {
                background: #556077;
            }
        """)
        
        # Carregar os valores iniciais do arquivo de configuração
        self.load_initial_values()
    
        self.load_wallpapers(f'{home_dir}/.scripts/hypr/wallpapers')
    

	# ------------------------- Exibir Informações do Sistema ---------------------------------#

    def show_system_info(self):
        dialog = SystemInfoDialog(self)
        dialog.exec_()


    # ------------------- Editar Atalhos e Regras das Janelas ---------------------------------#


    def keybinds(self):
        subprocess.Popen(["xdg-open", f"{home_dir}/.config/hypr/config.d/keybinds.conf"])
        self.close()


    def window_rules(self):
        subprocess.Popen(["xdg-open", f"{home_dir}/.config/hypr/config.d/rules.conf"])
        self.close()

    #----------------------------------------------------------------------------------------#
    # ------------------------------------ Resolução ----------------------------------------#
    #----------------------------------------------------------------------------------------#
    def set_720p(self):
        subprocess.run(['hyprctl', 'keyword', 'monitor', 'HDMI-A-1,1280x720@60,auto,auto'])
        
        # Mudar a largura da waybar
        try:
            # Comando sed para substituir a linha específica
            comando = f"sed -i '/\"width\":/s/\"width\": [0-9]*,/\"width\": 1260,/' {waybar_conf}"
            subprocess.run(comando, shell=True, check=True)
            print(f"Width atualizado com sucesso para 1280x720 no arquivo {waybar_conf}")
            # Reiniciar a Waybar
            subprocess.run(["killall", "waybar"], check=True)
            subprocess.Popen(["waybar"])
            print("Waybar reiniciada com sucesso!")      
        
        except subprocess.CalledProcessError as e:
            print(f"Erro ao alterar o width: {e}")


    def set_1080p(self):
        subprocess.run(['hyprctl', 'keyword', 'monitor', 'HDMI-A-1,1920x1080@60,auto,auto'])
        
        # Mudar a largura da waybar
        try:
            # Comando sed para substituir a linha específica
            comando = f"sed -i '/\"width\":/s/\"width\": [0-9]*,/\"width\": 1900,/' {waybar_conf}"
            subprocess.run(comando, shell=True, check=True)
            print(f"Width atualizado com sucesso para 1920x1080 no arquivo {waybar_conf}")
            # Reiniciar a Waybar
            subprocess.run(["killall", "waybar"], check=True)
            subprocess.Popen(["waybar"])
            print("Waybar reiniciada com sucesso!")      
        
        except subprocess.CalledProcessError as e:
            print(f"Erro ao alterar o width: {e}")

    #----------------------------------------------------------------------------------------#
    # ------------------------------------ Cor de Destaque ----------------------------------#
    #----------------------------------------------------------------------------------------#

    def make_red(self):
        try:
            # Substituindo a linha correspondente a $COR1
            comando_cor1 = f"sed -i 's/^\\$COR1=.*/$COR1=FE4444FF/' {colors_conf}"
            subprocess.run(comando_cor1, shell=True, check=True)

            # Substituindo a linha correspondente a $COR2
            comando_cor2 = f"sed -i 's/^\\$COR2=.*/$COR2=ED5555EE/' {colors_conf}"
            subprocess.run(comando_cor2, shell=True, check=True)

            print(f"As cores foram atualizadas com sucesso no arquivo: {colors_conf}")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao atualizar as cores: {e}")

        #Waybar
        try:
            # Alterar a linha com 'color:'
            comando_alterar = f"sed -i '/^\\s*color:/c\\    color: #FE4444;' {waybar_style}"
            subprocess.run(comando_alterar, shell=True, check=True)
            print("Linha com 'color:' atualizada com sucesso!")

            # Reiniciar a Waybar
            subprocess.run(["killall", "waybar"], check=True)
            subprocess.Popen(["waybar"])
            print("Waybar reiniciada com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar os comandos: {e}")


    def make_orange(self):
        try:
            # Substituindo a linha correspondente a $COR1
            comando_cor1 = f"sed -i 's/^\\$COR1=.*/$COR1=FA7544FF/' {colors_conf}"
            subprocess.run(comando_cor1, shell=True, check=True)

            # Substituindo a linha correspondente a $COR2
            comando_cor2 = f"sed -i 's/^\\$COR2=.*/$COR2=FF8544EE/' {colors_conf}"
            subprocess.run(comando_cor2, shell=True, check=True)

            print(f"As cores foram atualizadas com sucesso no arquivo: {colors_conf}")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao atualizar as cores: {e}")

        #Waybar
        try:
            # Alterar a linha com 'color:'
            comando_alterar = f"sed -i '/^\\s*color:/c\\    color: #FF8544;' {waybar_style}"
            subprocess.run(comando_alterar, shell=True, check=True)
            print("Linha com 'color:' atualizada com sucesso!")

            # Reiniciar a Waybar
            subprocess.run(["killall", "waybar"], check=True)
            subprocess.Popen(["waybar"])
            print("Waybar reiniciada com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar os comandos: {e}")


    def make_yellow(self):
        try:
            # Substituindo a linha correspondente a $COR1
            comando_cor1 = f"sed -i 's/^\\$COR1=.*/$COR1=FABC3FFF/' {colors_conf}"
            subprocess.run(comando_cor1, shell=True, check=True)

            # Substituindo a linha correspondente a $COR2
            comando_cor2 = f"sed -i 's/^\\$COR2=.*/$COR2=FBCD4FEE/' {colors_conf}"
            subprocess.run(comando_cor2, shell=True, check=True)

            print(f"As cores foram atualizadas com sucesso no arquivo: {colors_conf}")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao atualizar as cores: {e}")

        #Waybar
        try:
            # Alterar a linha com 'color:'
            comando_alterar = f"sed -i '/^\\s*color:/c\\    color: #FABC3F;' {waybar_style}"
            subprocess.run(comando_alterar, shell=True, check=True)
            print("Linha com 'color:' atualizada com sucesso!")

            # Reiniciar a Waybar
            subprocess.run(["killall", "waybar"], check=True)
            subprocess.Popen(["waybar"])
            print("Waybar reiniciada com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar os comandos: {e}")


    def make_green(self):
        try:
            # Substituindo a linha correspondente a $COR1
            comando_cor1 = f"sed -i 's/^\\$COR1=.*/$COR1=9ADE44FF/' {colors_conf}"
            subprocess.run(comando_cor1, shell=True, check=True)

            # Substituindo a linha correspondente a $COR2
            comando_cor2 = f"sed -i 's/^\\$COR2=.*/$COR2=AAFE55EE/' {colors_conf}"
            subprocess.run(comando_cor2, shell=True, check=True)

            print(f"As cores foram atualizadas com sucesso no arquivo: {colors_conf}")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao atualizar as cores: {e}")

        #Waybar
        try:
            # Alterar a linha com 'color:'
            comando_alterar = f"sed -i '/^\\s*color:/c\\    color: #9ADE44;' {waybar_style}"
            subprocess.run(comando_alterar, shell=True, check=True)
            print("Linha com 'color:' atualizada com sucesso!")

            # Reiniciar a Waybar
            subprocess.run(["killall", "waybar"], check=True)
            subprocess.Popen(["waybar"])
            print("Waybar reiniciada com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar os comandos: {e}")


    def make_cian(self):
        try:
            # Substituindo a linha correspondente a $COR1
            comando_cor1 = f"sed -i 's/^\\$COR1=.*/$COR1=44CDEEFF/' {colors_conf}"
            subprocess.run(comando_cor1, shell=True, check=True)

            # Substituindo a linha correspondente a $COR2
            comando_cor2 = f"sed -i 's/^\\$COR2=.*/$COR2=65EDFEEE/' {colors_conf}"
            subprocess.run(comando_cor2, shell=True, check=True)

            print(f"As cores foram atualizadas com sucesso no arquivo: {colors_conf}")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao atualizar as cores: {e}")

        #Waybar
        try:
            # Alterar a linha com 'color:'
            comando_alterar = f"sed -i '/^\\s*color:/c\\    color: #44CDEE;' {waybar_style}"
            subprocess.run(comando_alterar, shell=True, check=True)
            print("Linha com 'color:' atualizada com sucesso!")

            # Reiniciar a Waybar
            subprocess.run(["killall", "waybar"], check=True)
            subprocess.Popen(["waybar"])
            print("Waybar reiniciada com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar os comandos: {e}")


    def make_pink(self):
        try:
            # Substituindo a linha correspondente a $COR1
            comando_cor1 = f"sed -i 's/^\\$COR1=.*/$COR1=F766ABFF/' {colors_conf}"
            subprocess.run(comando_cor1, shell=True, check=True)

            # Substituindo a linha correspondente a $COR2
            comando_cor2 = f"sed -i 's/^\\$COR2=.*/$COR2=FA76BBEE/' {colors_conf}"
            subprocess.run(comando_cor2, shell=True, check=True)

            print(f"As cores foram atualizadas com sucesso no arquivo: {colors_conf}")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao atualizar as cores: {e}")

        #Waybar
        try:
            # Alterar a linha com 'color:'
            comando_alterar = f"sed -i '/^\\s*color:/c\\    color: #F766AB;' {waybar_style}"
            subprocess.run(comando_alterar, shell=True, check=True)
            print("Linha com 'color:' atualizada com sucesso!")

            # Reiniciar a Waybar
            subprocess.run(["killall", "waybar"], check=True)
            subprocess.Popen(["waybar"])
            print("Waybar reiniciada com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar os comandos: {e}")


    def make_purple(self):
        try:
            # Substituindo a linha correspondente a $COR1
            comando_cor1 = f"sed -i 's/^\\$COR1=.*/$COR1=B75CFBFF/' {colors_conf}"
            subprocess.run(comando_cor1, shell=True, check=True)

            # Substituindo a linha correspondente a $COR2
            comando_cor2 = f"sed -i 's/^\\$COR2=.*/$COR2=C76CFDEE/' {colors_conf}"
            subprocess.run(comando_cor2, shell=True, check=True)

            print(f"As cores foram atualizadas com sucesso no arquivo: {colors_conf}")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao atualizar as cores: {e}")

        #Waybar
        try:
            # Alterar a linha com 'color:'
            comando_alterar = f"sed -i '/^\\s*color:/c\\    color: #B75CFB;' {waybar_style}"
            subprocess.run(comando_alterar, shell=True, check=True)
            print("Linha com 'color:' atualizada com sucesso!")

            # Reiniciar a Waybar
            subprocess.run(["killall", "waybar"], check=True)
            subprocess.Popen(["waybar"])
            print("Waybar reiniciada com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar os comandos: {e}")
            
    #----------------------------------------------------------------------------------------#
    #------------------------------------ Funções: Bordas -----------------------------------#
    #----------------------------------------------------------------------------------------#
    def load_initial_values(self):
        try:
            with open(borders_conf, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if "$SIZE" in line:
                        size_value = int(line.split('=')[1].strip())
                        self.bordersize_slider.setValue(size_value)
                        self.numsize_label.setText(str(size_value))
                    elif "$RADIUS" in line:
                        radius_value = int(line.split('=')[1].strip())
                        self.borderradius_slider.setValue(radius_value)
                        self.numradius_label.setText(str(radius_value))
        except FileNotFoundError:
            print(f"Arquivo {borders_conf} não encontrado.")


    def update_bordersize_label(self):
        value = self.bordersize_slider.value()
        self.numsize_label.setText(str(value))
 
    
    def update_borderradius_label(self):
        value = self.borderradius_slider.value()
        self.numradius_label.setText(str(value))
 
    
    def apply_changes(self):
        size_value = self.bordersize_slider.value()
        radius_value = self.borderradius_slider.value()
        
        try:
            # Usando sed para atualizar os valores no arquivo
            subprocess.run(
                [f"sed -i 's/\\$SIZE=.*/\\$SIZE={size_value}/' {borders_conf}"], 
                shell=True, check=True
            )
            subprocess.run(
                [f"sed -i 's/\\$RADIUS=.*/\\$RADIUS={radius_value}/' {borders_conf}"], 
                shell=True, check=True
            )
            print("Configurações aplicadas com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao aplicar configurações: {e}")
    
    #----------------------------------------------------------------------------------------#
    #------------------------------------ Funções: Wallpapers -------------------------------#
    #----------------------------------------------------------------------------------------#
    
    def open_folder_walls(self):
        subprocess.Popen(['dolphin', f'{home_dir}/.scripts/hypr/wallpapers'])

        
    def make_thumbnails(self):
        subprocess.run([f"{home_dir}/.scripts/hypr/makethumbs.sh"])


    def load_wallpapers(self, folder):
        thumb_folder = os.path.join(folder, '.thumb')  # Caminho da pasta de miniaturas
        valid_extensions = ('.jpeg', '.jpg', '.png')
        files = [f for f in os.listdir(folder) if f.lower().endswith(valid_extensions)]
        layout = QGridLayout()
        self.scrollArea.setWidgetResizable(True)
        scroll_widget = self.scrollArea.widget()
        scroll_widget.setLayout(layout)

        row = 0
        col = 0
        for file in files:
            file_path = os.path.join(folder, file)
            thumb_path = os.path.join(thumb_folder, file)  # Caminho para a miniatura

            # Verifique se a miniatura existe antes de tentar carregar
            if os.path.exists(thumb_path):
                button = QPushButton()
                button.setIcon(QIcon(QPixmap(thumb_path)))  # Carregar a miniatura sem redimensionar
                button.setIconSize(QSize(260, 152))  # Tamanho do ícone
                button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #2a2a2a;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #5d5d5d;
                    }
                """)
                button.clicked.connect(lambda _, f=file_path: self.change_wallpaper(f))
                layout.addWidget(button, row, col)

                col += 1
                if col >= 2:  # Limitar a 2 colunas
                    col = 0
                    row += 1


    def change_wallpaper(self, file_path):
        script_path = f'{home_dir}/.scripts/hypr/change-wallpaper.sh'
        subprocess.run([script_path, file_path])

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    app.exec_()
