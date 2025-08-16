from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from screens import TelaNome, TelaContatos, TelaChamada, TelaRecebida
from communication import CommunicationManager

class ChamadasApp(App):
    def build(self):
        self.title = "App de Chamadas"
        
        # Criar gerenciador de telas
        sm = ScreenManager()
        
        # Criar instâncias das telas
        self.tela_nome = TelaNome(name='tela_nome')
        self.tela_contatos = TelaContatos(name='tela_contatos')
        self.tela_chamada = TelaChamada(name='tela_chamada')
        self.tela_recebida = TelaRecebida(name='tela_recebida')
        
        # Adicionar telas ao gerenciador
        sm.add_widget(self.tela_nome)
        sm.add_widget(self.tela_contatos)
        sm.add_widget(self.tela_chamada)
        sm.add_widget(self.tela_recebida)
        
        # Inicializar gerenciador de comunicação
        self.comm_manager = CommunicationManager(self)
        
        # Timer para retorno automático
        self.inactivity_timer = None
        self.reset_inactivity_timer()
        
        return sm
    
    def reset_inactivity_timer(self):
        """Resetar o timer de inatividade"""
        if self.inactivity_timer:
            self.inactivity_timer.cancel()
        self.inactivity_timer = Clock.schedule_once(self.return_to_main, 30)
    
    def return_to_main(self, dt):
        """Retornar para a tela principal"""
        self.root.current = 'tela_nome'
        # Resetar dados
        if hasattr(self, 'tela_nome') and hasattr(self.tela_nome, 'nome_input'):
            self.tela_nome.nome_input.text = ''
        if hasattr(self, 'caller_name'):
            delattr(self, 'caller_name')
    
    def on_start(self):
        # Iniciar servidor de comunicação
        self.comm_manager.start_server()
        print("Servidor de comunicação iniciado")

if __name__ == '__main__':
    ChamadasApp().run()