import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
from colorama import init, Fore, Style

# Inicializa colorama
init()

class IntegratedLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Integrado de Aprendizado")
        self.root.geometry("800x600")
        
        # Configuração inicial
        self.setup_resources()
        self.create_learning_widgets()
        self.create_typing_widgets()
        self.hide_typing_widgets()
        
        # Variáveis de controle do teste de digitação
        self.typing_start_time = None
        self.typing_errors = 0
        self.current_typing_text = ""
    
    def setup_resources(self):
        """Define os recursos de aprendizado"""
        self.language_resources = {
            "Python": {
                "Iniciante": [
                    ("Variáveis e Tipos", "x = 10\ny = 3.14\nnome = \"Python\"", "https://docs.python.org/pt-br/3/tutorial/introduction.html"),
                    ("Condicionais", "if x > 5:\n    print(\"Maior que 5\")\nelif x == 5:\n    print(\"Igual a 5\")\nelse:\n    print(\"Menor que 5\")", "https://docs.python.org/pt-br/3/tutorial/controlflow.html#if-statements"),
                    ("Loops", "for i in range(5):\n    print(i)\n\nwhile x > 0:\n    print(x)\n    x -= 1", "https://docs.python.org/pt-br/3/tutorial/controlflow.html#for-statements")
                ],
                "Intermediário": [
                    ("Funções", "def soma(a, b):\n    return a + b\n\nresultado = soma(5, 3)", "https://docs.python.org/pt-br/3/tutorial/controlflow.html#defining-functions"),
                    ("Listas", "numeros = [1, 2, 3, 4, 5]\nfrutas = [\"maçã\", \"banana\"]", "https://docs.python.org/pt-br/3/tutorial/datastructures.html"),
                    ("Dicionários", "pessoa = {\"nome\": \"João\", \"idade\": 30}\nprint(pessoa[\"nome\"])", "https://docs.python.org/pt-br/3/tutorial/datastructures.html#dictionaries")
                ]
            },
            "JavaScript": {
                "Iniciante": [
                    ("Variáveis", "let x = 10;\nconst y = 3.14;\nvar nome = \"JavaScript\";", "https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Guide/Grammar_and_types"),
                    ("Condicionais", "if (x > 5) {\n  console.log(\"Maior que 5\");\n} else if (x === 5) {\n  console.log(\"Igual a 5\");\n} else {\n  console.log(\"Menor que 5\");\n}", "https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Statements/if...else"),
                    ("Loops", "for (let i = 0; i < 5; i++) {\n  console.log(i);\n}\n\nwhile (x > 0) {\n  console.log(x);\n  x--;\n}", "https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Guide/Loops_and_iteration")
                ]
            }
        }
    
    def create_learning_widgets(self):
        """Cria a interface de aprendizado"""
        self.learning_frame = ttk.Frame(self.root, padding="10")
        self.learning_frame.pack(fill=tk.BOTH, expand=True)
        
        # Controles de seleção
        control_frame = ttk.Frame(self.learning_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Linguagem:").pack(side=tk.LEFT, padx=5)
        self.language_var = tk.StringVar()
        self.language_cb = ttk.Combobox(
            control_frame,
            textvariable=self.language_var,
            values=list(self.language_resources.keys()),
            state="readonly"
        )
        self.language_cb.pack(side=tk.LEFT, padx=5)
        self.language_cb.current(0)
        
        ttk.Label(control_frame, text="Nível:").pack(side=tk.LEFT, padx=5)
        self.level_var = tk.StringVar()
        self.level_cb = ttk.Combobox(
            control_frame,
            textvariable=self.level_var,
            values=["Iniciante", "Intermediário"],
            state="readonly"
        )
        self.level_cb.pack(side=tk.LEFT, padx=5)
        self.level_cb.current(0)
        
        ttk.Button(
            control_frame,
            text="Carregar Tópicos",
            command=self.load_topics
        ).pack(side=tk.LEFT, padx=5)
        
        # Lista de tópicos
        self.topics_listbox = tk.Listbox(
            self.learning_frame,
            height=10,
            selectmode=tk.SINGLE
        )
        self.topics_listbox.pack(fill=tk.BOTH, pady=5, expand=True)
        
        # Área de informação
        info_frame = ttk.Frame(self.learning_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            info_frame,
            text="Ver Documentação",
            command=self.open_documentation
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            info_frame,
            text="Praticar Digitação",
            command=self.start_typing_practice
        ).pack(side=tk.LEFT, padx=5)
        
        # Área de código de exemplo
        self.code_display = scrolledtext.ScrolledText(
            self.learning_frame,
            height=10,
            wrap=tk.WORD,
            font=('Consolas', 10)
        )
        self.code_display.pack(fill=tk.BOTH, expand=True)
        self.code_display.config(state=tk.DISABLED)
    
    def create_typing_widgets(self):
        """Cria a interface de prática de digitação"""
        self.typing_frame = ttk.Frame(self.root, padding="10")
        
        # Texto de referência
        self.reference_text = tk.Text(
            self.typing_frame,
            height=10,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#f0f0f0'
        )
        self.reference_text.pack(fill=tk.BOTH, pady=5)
        self.reference_text.config(state=tk.DISABLED)
        
        # Área de digitação
        self.typing_area = tk.Text(
            self.typing_frame,
            height=10,
            wrap=tk.WORD,
            font=('Consolas', 10)
        )
        self.typing_area.pack(fill=tk.BOTH, pady=5)
        
        # Controles
        control_frame = ttk.Frame(self.typing_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            control_frame,
            text="Voltar ao Aprendizado",
            command=self.back_to_learning
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="Ver Resultados",
            command=self.show_typing_results
        ).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = ttk.Label(
            self.typing_frame,
            text="Digite o texto acima exatamente como aparece"
        )
        self.status_label.pack()
    
    def hide_typing_widgets(self):
        """Esconde os widgets de digitação"""
        self.typing_frame.pack_forget()
    
    def show_typing_widgets(self):
        """Mostra os widgets de digitação"""
        self.learning_frame.pack_forget()
        self.typing_frame.pack(fill=tk.BOTH, expand=True)
    
    def load_topics(self):
        """Carrega os tópicos disponíveis"""
        language = self.language_var.get()
        level = self.level_var.get()
        
        self.topics_listbox.delete(0, tk.END)
        
        if language in self.language_resources and level in self.language_resources[language]:
            for topic, *_ in self.language_resources[language][level]:
                self.topics_listbox.insert(tk.END, topic)
    
    def open_documentation(self):
        """Abre a documentação do tópico selecionado"""
        selected = self.topics_listbox.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um tópico primeiro")
            return
        
        language = self.language_var.get()
        level = self.level_var.get()
        topic_idx = selected[0]
        
        try:
            *_, url = self.language_resources[language][level][topic_idx]
            webbrowser.open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir: {str(e)}")
    
    def start_typing_practice(self):
        """Inicia o modo de prática de digitação"""
        selected = self.topics_listbox.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um tópico primeiro")
            return
        
        language = self.language_var.get()
        level = self.level_var.get()
        topic_idx = selected[0]
        
        try:
            _, code, _ = self.language_resources[language][level][topic_idx]
            self.current_typing_text = code
            self.show_typing_widgets()
            
            # Configura o texto de referência
            self.reference_text.config(state=tk.NORMAL)
            self.reference_text.delete(1.0, tk.END)
            self.reference_text.insert(tk.END, code)
            self.reference_text.config(state=tk.DISABLED)
            
            # Limpa a área de digitação
            self.typing_area.delete(1.0, tk.END)
            
            # Inicia o cronômetro
            self.typing_start_time = time.time()
            self.typing_errors = 0
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível iniciar: {str(e)}")
    
    def back_to_learning(self):
        """Volta para o modo de aprendizado"""
        self.hide_typing_widgets()
        self.learning_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_typing_results(self):
        """Mostra os resultados da digitação"""
        if not self.typing_start_time:
            return
        
        typed_text = self.typing_area.get(1.0, tk.END).strip()
        original_text = self.current_typing_text.strip()
        
        # Calcula erros
        errors = 0
        for t_char, o_char in zip(typed_text, original_text):
            if t_char != o_char:
                errors += 1
        
        # Calcula tempo e velocidade
        elapsed = time.time() - self.typing_start_time
        words = len(original_text.split())
        wpm = (words / elapsed) * 60 if elapsed > 0 else 0
        
        # Mostra resultados
        messagebox.showinfo(
            "Resultados",
            f"Tempo: {elapsed:.1f} segundos\n"
            f"Velocidade: {wpm:.1f} PPM\n"
            f"Erros: {errors}\n"
            f"Precisão: {100 - (errors/len(original_text)*100):.1f}%"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = IntegratedLearningApp(root)
    root.mainloop()