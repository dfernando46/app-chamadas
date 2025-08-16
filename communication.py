import threading
import socket
import json
import time
from kivy.clock import Clock

class CommunicationManager:
    def __init__(self, app):
        self.app = app
        self.server_socket = None
        self.running = False
        self.port = 12345
        
    def start_server(self):
        """Iniciar servidor para receber chamadas"""
        def server_thread():
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server_socket.bind(('0.0.0.0', self.port))
                self.server_socket.listen(5)
                self.running = True
                
                print("Servidor iniciado, aguardando conexões...")
                
                while self.running:
                    try:
                        client_socket, address = self.server_socket.accept()
                        print(f"Conexão recebida de {address}")
                        
                        # Receber dados em thread separada
                        threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
                        
                    except Exception as e:
                        if self.running:
                            print(f"Erro no servidor: {e}")
                        break
                        
            except Exception as e:
                print(f"Erro ao iniciar servidor: {e}")
        
        threading.Thread(target=server_thread, daemon=True).start()
    
    def handle_client(self, client_socket):
        """Processar dados recebidos"""
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                message = json.loads(data)
                if message['type'] == 'call':
                    # Receber chamada
                    Clock.schedule_once(lambda dt, msg=message: self.show_incoming_call(msg))
                elif message['type'] == 'response':
                    # Receber resposta
                    Clock.schedule_once(lambda dt, msg=message: self.show_response(msg))
                    
        except Exception as e:
            print(f"Erro ao processar cliente: {e}")
        finally:
            client_socket.close()
    
    def show_incoming_call(self, message):
        """Mostrar chamada recebida na tela"""
        app = self.app
        app.caller_name = message['caller']
        app.called_name = message['called']
        app.root.current = 'tela_recebida'
        app.reset_inactivity_timer()
        print(f"Chamada recebida de {message['caller']}")
    
    def show_response(self, message):
        """Mostrar resposta recebida"""
        app = self.app
        response = message['response']
        caller = message['caller']
        
        # Mostrar popup com a resposta
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        
        popup = Popup(
            title='Resposta Recebida',
            content=Label(text=f'{caller} respondeu: {response}', color=(0, 0, 0, 1)),
            size_hint=(0.8, 0.4)
        )
        popup.open()
        
        # Retornar para tela principal após mostrar resposta
        Clock.schedule_once(lambda dt: self.return_to_main(), 3)
    
    def return_to_main(self):
        """Retornar para tela principal"""
        app = self.app
        app.root.current = 'tela_nome'
        app.reset_inactivity_timer()
    
    def send_call(self, caller, called, target_ip):
        """Enviar chamada para outro dispositivo"""
        def send_thread():
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((target_ip, self.port))
                
                message = {
                    'type': 'call',
                    'caller': caller,
                    'called': called,
                    'timestamp': time.time()
                }
                
                client_socket.send(json.dumps(message).encode('utf-8'))
                client_socket.close()
                
                print(f"Chamada enviada para {target_ip}")
                
            except Exception as e:
                print(f"Erro ao enviar chamada: {e}")
                Clock.schedule_once(lambda dt: self.handle_call_error())
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def send_response(self, caller, response, target_ip):
        """Enviar resposta para o chamador"""
        def send_thread():
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((target_ip, self.port))
                
                message = {
                    'type': 'response',
                    'caller': caller,
                    'response': response,
                    'timestamp': time.time()
                }
                
                client_socket.send(json.dumps(message).encode('utf-8'))
                client_socket.close()
                
                print(f"Resposta enviada para {target_ip}: {response}")
                
            except Exception as e:
                print(f"Erro ao enviar resposta: {e}")
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def handle_call_error(self):
        """Tratar erro de chamada"""
        print("Não foi possível conectar ao dispositivo")
    
    def stop(self):
        """Parar o servidor"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()