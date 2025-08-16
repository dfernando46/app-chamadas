from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.app import App

class TelaNome(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Criar layout principal com tema azul
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.canvas.before.clear()
        
        # Título
        titulo = Label(
            text='App de Chamadas', 
            font_size='24sp',
            size_hint_y=0.3,
            color=(1, 1, 1, 1)  # Branco
        )
        
        # Input de nome
        self.nome_input = TextInput(
            hint_text='Digite seu nome',
            font_size='18sp',
            multiline=False,
            size_hint_y=0.2,
            background_color=(1, 1, 1, 1),  # Branco
            foreground_color=(0, 0, 0, 1)   # Preto
        )
        self.nome_input.bind(on_text_validate=self.prosseguir)
        self.nome_input.bind(text=self.on_text_change)  # Converter para maiúsculas
        
        # Botão continuar
        btn_continuar = Button(
            text='Continuar',
            font_size='18sp',
            size_hint_y=0.2,
            background_color=(0.2, 0.6, 1, 1),  # Azul
            color=(1, 1, 1, 1)  # Branco
        )
        btn_continuar.bind(on_press=self.prosseguir)
        
        layout.add_widget(titulo)
        layout.add_widget(self.nome_input)
        layout.add_widget(btn_continuar)
        
        # Aplicar cor de fundo azul
        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.5, 0.9, 1)  # Azul escuro
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)
        
        self.add_widget(layout)
    
    def on_text_change(self, instance, value):
        """Converter texto para maiúsculas"""
        if value != value.upper():
            instance.text = value.upper()
            # Posicionar cursor no final
            instance.cursor = (len(instance.text), 0)
    
    def _update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.5, 0.9, 1)  # Azul escuro
            Rectangle(size=instance.size, pos=instance.pos)
    
    def prosseguir(self, instance):
        if self.nome_input.text.strip():
            app = App.get_running_app()
            app.caller_name = self.nome_input.text.strip().upper()
            app.root.current = 'tela_contatos'
            app.reset_inactivity_timer()

class TelaContatos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal com tema azul
        main_layout = BoxLayout(orientation='vertical')
        main_layout.canvas.before.clear()
        
        # Cabeçalho com botão de manutenção
        header = BoxLayout(size_hint_y=0.1, padding=[10, 5, 10, 5])
        titulo = Label(text='Escolha um contato', font_size='18sp', color=(1, 1, 1, 1))
        
        # Botão de manutenção pequeno no canto superior direito
        btn_manutencao = Button(
            text='🔧',
            size_hint=(None, None),
            size=(40, 40),
            background_color=(0, 0, 0, 1),  # Preto
            color=(1, 1, 1, 1),  # Branco
            font_size='16sp'
        )
        btn_manutencao.bind(on_press=self.abrir_manutencao)
        
        header.add_widget(titulo)
        header.add_widget(btn_manutencao)
        
        # Área de contatos com scroll
        self.scroll = ScrollView()
        self.contatos_layout = GridLayout(cols=1, spacing=10, padding=20, size_hint_y=None)
        self.contatos_layout.bind(minimum_height=self.contatos_layout.setter('height'))
        self.scroll.add_widget(self.contatos_layout)
        
        main_layout.add_widget(header)
        main_layout.add_widget(self.scroll)
        
        # Aplicar cor de fundo azul
        with main_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.5, 0.9, 1)  # Azul escuro
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
            main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        self.add_widget(main_layout)
        
        # Contatos padrão
        self.contatos = ['MARIA', 'JOÃO', 'ANA', 'PEDRO']
        self.atualizar_contatos()
    
    def _update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.5, 0.9, 1)  # Azul escuro
            Rectangle(size=instance.size, pos=instance.pos)
    
    def atualizar_contatos(self):
        self.contatos_layout.clear_widgets()
        for contato in self.contatos:
            btn = Button(
                text=contato,
                font_size='16sp',
                size_hint_y=None,
                height=dp(50),
                background_color=(0.3, 0.7, 1, 1),  # Azul médio
                color=(1, 1, 1, 1)  # Branco
            )
            btn.bind(on_press=lambda x, c=contato: self.chamar_contato(c))
            self.contatos_layout.add_widget(btn)
    
    def chamar_contato(self, contato):
        app = App.get_running_app()
        app.called_name = contato
        
        # Popup para digitar IP do destino
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input IP
        self.ip_input = TextInput(
            hint_text='IP do dispositivo destino',
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        
        # Botões
        buttons_layout = BoxLayout(spacing=10, size_hint_y=0.3)
        btn_confirmar = Button(
            text='Confirmar',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_cancelar = Button(
            text='Cancelar',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        
        buttons_layout.add_widget(btn_confirmar)
        buttons_layout.add_widget(btn_cancelar)
        
        popup_layout.add_widget(Label(text='Digite o IP do dispositivo', color=(0, 0, 0, 1)))
        popup_layout.add_widget(self.ip_input)
        popup_layout.add_widget(buttons_layout)
        
        self.call_popup = Popup(
            title='IP do Destino',
            content=popup_layout,
            size_hint=(0.8, 0.6)
        )
        
        def confirmar_chamada(instance):
            if self.ip_input.text.strip():
                # Enviar chamada via comunicação
                if hasattr(app, 'comm_manager'):
                    app.comm_manager.send_call(app.caller_name, contato, self.ip_input.text.strip())
                app.root.current = 'tela_chamada'
                app.reset_inactivity_timer()
                self.call_popup.dismiss()
            else:
                # Se não tiver comunicação, seguir normalmente
                app.root.current = 'tela_chamada'
                app.reset_inactivity_timer()
                self.call_popup.dismiss()
        
        def cancelar(instance):
            self.call_popup.dismiss()
        
        btn_confirmar.bind(on_press=confirmar_chamada)
        btn_cancelar.bind(on_press=cancelar)
        
        self.call_popup.open()
    
    def abrir_manutencao(self, instance):
        """Abrir popup de senha para manutenção"""
        # Popup para senha
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input senha (password=True para ocultar)
        self.senha_input = TextInput(
            hint_text='Digite a senha',
            multiline=False,
            password=True,  # Oculta a senha
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        
        # Botões
        buttons_layout = BoxLayout(spacing=10, size_hint_y=0.3)
        btn_confirmar = Button(
            text='Confirmar',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_cancelar = Button(
            text='Cancelar',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        
        buttons_layout.add_widget(btn_confirmar)
        buttons_layout.add_widget(btn_cancelar)
        
        popup_layout.add_widget(Label(text='Acesso à Manutenção', color=(0, 0, 0, 1)))
        popup_layout.add_widget(self.senha_input)
        popup_layout.add_widget(buttons_layout)
        
        self.popup_senha = Popup(
            title='Senha de Acesso',
            content=popup_layout,
            size_hint=(0.8, 0.6)
        )
        
        def confirmar_senha(instance):
            if self.senha_input.text == '0606':
                self.popup_senha.dismiss()
                self.abrir_tela_manutencao()
            else:
                # Erro - senha incorreta
                error_popup = Popup(
                    title='Erro',
                    content=Label(text='Senha incorreta!', color=(0, 0, 0, 1)),
                    size_hint=(0.6, 0.3)
                )
                error_popup.open()
        
        def cancelar(instance):
            self.popup_senha.dismiss()
        
        btn_confirmar.bind(on_press=confirmar_senha)
        btn_cancelar.bind(on_press=cancelar)
        
        self.popup_senha.open()
    
    def abrir_tela_manutencao(self):
        """Abrir tela de manutenção"""
        # Popup de manutenção
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=15)
        
        titulo = Label(text='Manutenção de Contatos', color=(0, 0, 0, 1), font_size='18sp')
        
        # Botões de manutenção
        btn_adicionar = Button(
            text='➕ Adicionar Contato',
            size_hint_y=0.2,
            background_color=(0.2, 0.8, 0.2, 1),  # Verde
            color=(1, 1, 1, 1)
        )
        btn_remover = Button(
            text='➖ Remover Contato',
            size_hint_y=0.2,
            background_color=(0.8, 0.2, 0.2, 1),  # Vermelho
            color=(1, 1, 1, 1)
        )
        btn_fechar = Button(
            text='Fechar',
            size_hint_y=0.15,
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        
        btn_adicionar.bind(on_press=lambda x: self.adicionar_contato_manutencao())
        btn_remover.bind(on_press=lambda x: self.remover_contato_manutencao())
        btn_fechar.bind(on_press=lambda x: self.popup_manutencao.dismiss())
        
        popup_layout.add_widget(titulo)
        popup_layout.add_widget(btn_adicionar)
        popup_layout.add_widget(btn_remover)
        popup_layout.add_widget(Label())  # Espaço
        popup_layout.add_widget(btn_fechar)
        
        self.popup_manutencao = Popup(
            title='Manutenção',
            content=popup_layout,
            size_hint=(0.8, 0.7)
        )
        self.popup_manutencao.open()
    
    def adicionar_contato_manutencao(self):
        """Adicionar contato na manutenção"""
        # Fechar popup de manutenção
        self.popup_manutencao.dismiss()
        
        # Popup para adicionar contato
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input nome
        self.nome_contato_input = TextInput(
            hint_text='Nome do contato',
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        
        # Botões
        buttons_layout = BoxLayout(spacing=10, size_hint_y=0.3)
        btn_confirmar = Button(
            text='Confirmar',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_cancelar = Button(
            text='Cancelar',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        
        buttons_layout.add_widget(btn_confirmar)
        buttons_layout.add_widget(btn_cancelar)
        
        popup_layout.add_widget(Label(text='Adicionar Contato', color=(0, 0, 0, 1)))
        popup_layout.add_widget(self.nome_contato_input)
        popup_layout.add_widget(buttons_layout)
        
        self.popup_add = Popup(
            title='Adicionar Contato',
            content=popup_layout,
            size_hint=(0.8, 0.6)
        )
        
        def confirmar_adicao(instance):
            if self.nome_contato_input.text.strip():
                app = App.get_running_app()
                if hasattr(app, 'tela_contatos'):
                    contato_nome = self.nome_contato_input.text.strip().upper()
                    if contato_nome not in app.tela_contatos.contatos:
                        app.tela_contatos.contatos.append(contato_nome)
                        app.tela_contatos.atualizar_contatos()
                        self.popup_add.dismiss()
                    else:
                        # Erro - contato já existe
                        error_popup = Popup(
                            title='Erro',
                            content=Label(text='Contato já existe!', color=(0, 0, 0, 1)),
                            size_hint=(0.6, 0.3)
                        )
                        error_popup.open()
        
        def cancelar(instance):
            self.popup_add.dismiss()
        
        btn_confirmar.bind(on_press=confirmar_adicao)
        btn_cancelar.bind(on_press=cancelar)
        
        self.popup_add.open()
    
    def remover_contato_manutencao(self):
        """Remover contato na manutenção"""
        # Fechar popup de manutenção
        self.popup_manutencao.dismiss()
        
        # Popup para remover contato
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input nome
        self.contato_remove_input = TextInput(
            hint_text='Nome do contato a remover',
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        
        # Botões
        buttons_layout = BoxLayout(spacing=10, size_hint_y=0.3)
        btn_confirmar = Button(
            text='Confirmar',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_cancelar = Button(
            text='Cancelar',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        
        buttons_layout.add_widget(btn_confirmar)
        buttons_layout.add_widget(btn_cancelar)
        
        popup_layout.add_widget(Label(text='Remover Contato', color=(0, 0, 0, 1)))
        popup_layout.add_widget(self.contato_remove_input)
        popup_layout.add_widget(buttons_layout)
        
        self.popup_remove = Popup(
            title='Remover Contato',
            content=popup_layout,
            size_hint=(0.8, 0.6)
        )
        
        def confirmar_remocao(instance):
            if self.contato_remove_input.text.strip():
                app = App.get_running_app()
                if hasattr(app, 'tela_contatos'):
                    contato_remover = self.contato_remove_input.text.strip().upper()
                    if contato_remover in app.tela_contatos.contatos:
                        app.tela_contatos.contatos.remove(contato_remover)
                        app.tela_contatos.atualizar_contatos()
                        self.popup_remove.dismiss()
                    else:
                        # Erro - contato não encontrado
                        error_popup = Popup(
                            title='Erro',
                            content=Label(text='Contato não encontrado!', color=(0, 0, 0, 1)),
                            size_hint=(0.6, 0.3)
                        )
                        error_popup.open()
        
        def cancelar(instance):
            self.popup_remove.dismiss()
        
        btn_confirmar.bind(on_press=confirmar_remocao)
        btn_cancelar.bind(on_press=cancelar)
        
        self.popup_remove.open()

class TelaChamada(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal com tema azul
        layout = BoxLayout(orientation='vertical', padding=20, spacing=30)
        layout.canvas.before.clear()
        
        # Informações da chamada
        self.info_label = Label(
            text='Chamando...',
            font_size='20sp',
            color=(1, 1, 1, 1)  # Branco
        )
        
        # Timer
        self.timer_label = Label(
            text='00:30',
            font_size='18sp',
            color=(1, 1, 1, 1)  # Branco
        )
        
        # Botão cancelar
        btn_cancelar = Button(
            text='Cancelar Chamada',
            font_size='16sp',
            size_hint_y=0.2,
            background_color=(0.8, 0.2, 0.2, 1),  # Vermelho
            color=(1, 1, 1, 1)  # Branco
        )
        btn_cancelar.bind(on_press=self.cancelar_chamada)
        
        layout.add_widget(self.info_label)
        layout.add_widget(self.timer_label)
        layout.add_widget(btn_cancelar)
        
        # Aplicar cor de fundo azul
        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.5, 0.9, 1)  # Azul escuro
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)
        
        self.add_widget(layout)
        self.timer = None
        self.seconds_left = 30
    
    def _update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.5, 0.9, 1)  # Azul escuro
            Rectangle(size=instance.size, pos=instance.pos)
    
    def on_enter(self):
        app = App.get_running_app()
        if hasattr(app, 'caller_name') and hasattr(app, 'called_name'):
            self.info_label.text = f'{app.caller_name} -> {app.called_name}'
        
        self.seconds_left = 30
        self.timer_label.text = f'00:{self.seconds_left:02d}'
        self.timer = Clock.schedule_interval(self.update_timer, 1)
    
    def update_timer(self, dt):
        self.seconds_left -= 1
        self.timer_label.text = f'00:{self.seconds_left:02d}'
        
        if self.seconds_left <= 0:
            self.cancelar_chamada(None)
    
    def on_leave(self):
        # Cancelar timer quando sair da tela
        if self.timer:
            self.timer.cancel()
    
    def cancelar_chamada(self, instance):
        if self.timer:
            self.timer.cancel()
        app = App.get_running_app()
        app.root.current = 'tela_nome'
        app.reset_inactivity_timer()

class TelaRecebida(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal com tema azul
        layout = BoxLayout(orientation='vertical', padding=20, spacing=30)
        layout.canvas.before.clear()
        
        # Nome do chamador
        self.caller_label = Label(
            text='Chamada Recebida',
            font_size='24sp',
            bold=True,
            color=(1, 1, 1, 1)  # Branco
        )
        
        # Botões de resposta
        buttons_layout = BoxLayout(spacing=10, size_hint_y=0.3)
        
        btn_indo = Button(
            text='Indo',
            background_color=(0, 0.8, 0, 1),  # Verde
            color=(1, 1, 1, 1)  # Branco
        )
        btn_ocupado = Button(
            text='Ocupado',
            background_color=(1, 1, 0, 1),  # Amarelo
            color=(0, 0, 0, 1)  # Preto
        )
        btn_ausente = Button(
            text='Ausente',
            background_color=(0.8, 0, 0, 1),  # Vermelho
            color=(1, 1, 1, 1)  # Branco
        )
        
        btn_indo.bind(on_press=lambda x: self.responder('Indo'))
        btn_ocupado.bind(on_press=lambda x: self.responder('Ocupado'))
        btn_ausente.bind(on_press=lambda x: self.responder('Ausente'))
        
        buttons_layout.add_widget(btn_indo)
        buttons_layout.add_widget(btn_ocupado)
        buttons_layout.add_widget(btn_ausente)
        
        layout.add_widget(self.caller_label)
        layout.add_widget(Label())  # Espaço
        layout.add_widget(buttons_layout)
        
        # Aplicar cor de fundo azul
        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.5, 0.9, 1)  # Azul escuro
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.5, 0.9, 1)  # Azul escuro
            Rectangle(size=instance.size, pos=instance.pos)
    
    def on_enter(self):
        app = App.get_running_app()
        if hasattr(app, 'caller_name') and hasattr(app, 'called_name'):
            self.caller_label.text = f'{app.caller_name}\nEstá chamando você!'
    
    def responder(self, resposta):
        app = App.get_running_app()
        print(f"Resposta: {resposta}")
        
        # Enviar resposta se tiver comunicação
        if hasattr(app, 'comm_manager') and hasattr(app, 'called_name'):
            # Aqui você precisaria ter o IP do chamador
            # Por simplicidade, vamos mostrar a resposta localmente
            pass
        
        # Mostrar resposta
        popup = Popup(
            title='Resposta Enviada',
            content=Label(text=f'Resposta: {resposta}', color=(0, 0, 0, 1)),
            size_hint=(0.6, 0.3)
        )
        popup.open()
        
        # Retornar para tela principal após um momento
        Clock.schedule_once(lambda dt: self.voltar_principal(), 2)
    
    def voltar_principal(self):
        app = App.get_running_app()
        app.root.current = 'tela_nome'
        app.reset_inactivity_timer()