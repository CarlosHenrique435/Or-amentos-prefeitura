import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import threading
import math

class OrcamentoApp:
    def __init__(self, root):
        self.root = root
        root.title("Auto Center - Criar Orçamento")
        root.geometry("1000x700")
        root.configure(bg="#2e2e2e")

        self.linhas = []

        # Estilo visual
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#444", foreground="white")
        style.configure("Treeview", font=("Arial", 10), background="#3c3f41", foreground="white", fieldbackground="#3c3f41")
        style.map("Treeview", background=[("selected", "#555")])

        # Dados principais
        self.carro_var = tk.StringVar()
        self.placa_var = tk.StringVar()
        self.numero_var = tk.StringVar()
        self.email_destino_var = tk.StringVar(value="compras@beneditonovo.sc.gov.br")

        form_frame = tk.LabelFrame(root, text="Informações do Orçamento", bg="#2e2e2e", fg="white", padx=10, pady=10)
        form_frame.pack(pady=10, fill="x", padx=10)

        tk.Label(form_frame, text="Carro:", bg="#2e2e2e", fg="white").grid(row=0, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.carro_var, width=25, bg="#444", fg="white", insertbackground="white").grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Placa:", bg="#2e2e2e", fg="white").grid(row=0, column=2, sticky="e")
        tk.Entry(form_frame, textvariable=self.placa_var, width=15, bg="#444", fg="white", insertbackground="white").grid(row=0, column=3, padx=5)

        tk.Label(form_frame, text="Nº Do Carro:", bg="#2e2e2e", fg="white").grid(row=0, column=4, sticky="e")
        tk.Entry(form_frame, textvariable=self.numero_var, width=15, bg="#444", fg="white", insertbackground="white").grid(row=0, column=5, padx=5)

        tk.Label(form_frame, text="Email destino:", bg="#2e2e2e", fg="white").grid(row=1, column=0, sticky="e")
        tk.Entry(form_frame, width=50, textvariable=self.email_destino_var, bg="#444", fg="white", insertbackground="white").grid(row=1, column=1, columnspan=5, pady=5)

        # Tabela
        self.tree = ttk.Treeview(root, columns=("peca", "qnt", "valor", "desc", "total"), show='headings', height=18)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(pady=10, padx=10, fill="x")

        campos_frame = tk.LabelFrame(root, text="Adicionar Item", bg="#2e2e2e", fg="white", padx=10, pady=10)
        campos_frame.pack(fill="x", padx=10, pady=10)

        self.peca_var = tk.StringVar()

        self.qnt_var = tk.StringVar()
        self.qnt_unidade_var = tk.StringVar(value="Un")  # unidade padrão



        self.valor_var = tk.StringVar(value="")  # valor padrão
        self.desc_var = tk.StringVar(value="35,5")
        self.desc_tipo_var = tk.StringVar(value="%")  # tipo de desconto padrão

        input_width = 18

        tk.Label(campos_frame, text="Peça/Serviço:", bg="#2e2e2e", fg="white").grid(row=0, column=0)
        tk.Entry(campos_frame, textvariable=self.peca_var, width=input_width, bg="#444", fg="white", insertbackground="white").grid(row=0, column=1, padx=5)

        tk.Label(campos_frame, text="Quantidade:", bg="#2e2e2e", fg="white").grid(row=0, column=2)

        tk.Entry(campos_frame, textvariable=self.qnt_var, width=8, bg="#444", fg="white", insertbackground="white").grid(row=0, column=3, padx=1)
        tk.OptionMenu(campos_frame, self.qnt_unidade_var, "Un", "L", "H").grid(row=0, column=4, padx=2)


        tk.Label(campos_frame, text="Valor Unitário:", bg="#2e2e2e", fg="white").grid(row=0, column=5)
        tk.Entry(campos_frame, textvariable=self.valor_var, width=input_width, bg="#444", fg="white", insertbackground="white").grid(row=0, column=6, padx=5)

        tk.Label(campos_frame, text="Desconto:", bg="#2e2e2e", fg="white").grid(row=0, column=7)
        tk.Entry(campos_frame, textvariable=self.desc_var, width=10, bg="#444", fg="white", insertbackground="white").grid(row=0, column=8, padx=5)

        tk.OptionMenu(campos_frame, self.desc_tipo_var, "%", "R$").grid(row=0, column=9, padx=5)

        tk.Button(campos_frame, text="Adicionar", command=self.adicionar_item, borderwidth=0, bg="#007acc", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5)

        tk.Button(campos_frame, text="Remover", command=self.remover_item, borderwidth=0, bg="#dc3545", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=1, padx=5)

        #remover todos os itens
        tk.Button(campos_frame, text="Remover Todos", command=self.remover_todos_itens,
         borderwidth=0, bg="#ff8c00", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=2, padx=5)

        tk.Button(campos_frame, text="Pré-visualizar PDF", command=self.visualizar_pdf, borderwidth=0, bg="#ff0000", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=3, padx=5)



        # Botão enviar
        bot_enviar = tk.Button(root, text="Enviar Orçamento por Email", bg="#159b34", fg="white", font=("Arial", 12, "bold"), borderwidth=0, command=self.enviar_email)
        bot_enviar.pack(pady=10)
        bot_enviar.bind("<Enter>", self.mudar_cursor)
        bot_enviar.bind("<Leave>", self.restaurar_cursor)
    
    def mudar_cursor(self, event):
        event.widget['cursor'] = 'hand2'
    
    def restaurar_cursor(self, event):
        event.widget['cursor'] = ''

    def remover_todos_itens(self):
        confirmar = messagebox.askyesno("Confirmação", "Deseja realmente remover todos os itens?")
        if confirmar:
            for item in self.tree.get_children():
                self.tree.delete(item)

    def adicionar_item(self):
        peca = self.peca_var.get().strip()

        if peca.lower() == "total":
            total_geral = 0.0
            for row in self.tree.get_children():
                valores = self.tree.item(row)["values"]
                if len(valores) >= 5:
                    try:
                        total_geral += float(str(valores[4]).replace(",", "."))
                    except ValueError:
                        continue
            messagebox.showinfo("Total peças", f"Soma total: R$ {total_geral:.2f}")
            self.tree.insert("", "end", values=("SOMA DAS PEÇAS", "-", "-", "-", f"R$ {total_geral:.2f}"), tags=("bold", "soma"))
            self.tree.tag_configure("bold", background="#444", foreground="#0FA824", font=("Arial", 10, "bold"))
            self.peca_var.set("")
            return

        if peca == "" or peca == "\\n":
            # Inserir linha em branco (todas as colunas vazias)
            self.tree.insert("", "end", values=("", "", "", "", ""))
            
            # Limpa os campos
            self.peca_var.set("")
            self.qnt_var.set(0)
            self.valor_var.set("")
            self.desc_var.set("")
            self.desc_tipo_var.set("R$")
            return

        try:
            qnt_raw = self.qnt_var.get().replace(",", ".")
            qnt = float(qnt_raw)
            qnt_unidade = self.qnt_unidade_var.get()
            qnt_display = f"{qnt:.2f} {qnt_unidade}"
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade deve ser um número válido.")
            return

        try:
            valor = float(self.valor_var.get().replace(",", "."))
            desconto_input = float(self.desc_var.get().replace(",", "."))
            if self.desc_tipo_var.get() == "%":
                desconto_str = f"{desconto_input:.1f}%"
                desconto_calc = (valor * qnt * desconto_input / 100)
            else:
                desconto_str = f"R$ {desconto_input:.2f}"
                desconto_calc = desconto_input
        except ValueError:
            messagebox.showwarning("Erro", "Valor e desconto devem ser números válidos.")
            return

        total = (qnt * valor) - desconto_calc

        if not peca or qnt <= 0 or valor <= 0:
            messagebox.showwarning("Erro", "Preencha os campos corretamente.")
            return

        self.tree.insert("", "end", values=(peca, qnt_display, f"{valor:.2f}", desconto_str, f"{total:.2f}"))


        self.peca_var.set("")
        self.qnt_var.set(0)
        self.valor_var.set("")
        self.desc_var.set("35,5")
        self.desc_tipo_var.set("%")

    def remover_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
        else:
            messagebox.showwarning("Atenção", "Selecione um item para remover.")

    def gerar_pdf(self, caminho):
        pdf = FPDF()
        pdf.add_page()
        # Adiciona a imagem no topo
        pdf.image("midia/midia-logo.jpg", x=10, y=8, w=100)  # ajuste w conforme necessário

        pdf.set_font("Arial", "B", 14)
        pdf.ln(25)  # Espaço após a imagem
        pdf.cell(0, 10, "Orçamento Auto Center", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.ln(5)

        pdf.cell(0, 10, f"Carro: {self.carro_var.get()}   Placa: {self.placa_var.get()}   Nº: {self.numero_var.get()}", ln=True)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(70, 10, "Peça/Serviço", 1, 0, "C")
        pdf.cell(20, 10, "Qtd", 1, 0, "C")
        pdf.cell(30, 10, "Valor", 1, 0, "C")
        pdf.cell(30, 10, "Desconto", 1, 0, "C")
        pdf.cell(40, 10, "Total", 1, 1, "C")

        pdf.set_font("Arial", size=12)
        for row in self.tree.get_children():
            vals = self.tree.item(row)["values"]
            # Checa se é a linha de soma
            if vals[0] == "SOMA DAS PEÇAS":
                pdf.set_fill_color(220, 220, 220)  # cinza claro
                fill = True
            elif vals[0].lower() == "mao de obra" or vals[0].lower() == "mão de obra":
                pdf.set_fill_color(173, 216, 230)  # azul claro
                fill = True
            else:
                fill = False
            pdf.cell(70, 10, str(vals[0]), 1, 0, "L", fill)
            pdf.cell(20, 10, str(vals[1]), 1, 0, "C", fill)
            pdf.cell(30, 10, str(vals[2]), 1, 0, "R", fill)
            pdf.cell(30, 10, str(vals[3]), 1, 0, "R", fill)
            pdf.cell(40, 10, str(vals[4]), 1, 1, "R", fill)

        pdf.output(caminho)

    def visualizar_pdf(self):
        from os import getcwd
        import subprocess

        carro = self.carro_var.get()
        placa = self.placa_var.get()
        numero = self.numero_var.get()

        if not carro or not placa or not numero:
            messagebox.showwarning("Erro", "Preencha os dados principais para gerar o PDF.")
            return

        nome_arquivo = f"{getcwd()}\\preview\\orcamento_preview_{placa.replace('-', '')}.pdf"
        self.gerar_pdf(nome_arquivo)

        try:
            subprocess.Popen([nome_arquivo], shell=True)  # abre no leitor padrão
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o PDF:\n{e}")


    def mostrar_loading(self, texto="Enviando email..."):
        loading = tk.Toplevel(self.root)
        loading.title("Aguarde")
        loading_width = 320
        loading_height = 180

        # Centraliza na tela
        screen_width = loading.winfo_screenwidth()
        screen_height = loading.winfo_screenheight()
        x = int((screen_width / 2) - (loading_width / 2))
        y = int((screen_height / 2) - (loading_height / 2))
        loading.geometry(f"{loading_width}x{loading_height}+{x}+{y}")

        loading.configure(bg="#f73939")
        loading.transient(self.root)
        loading.grab_set()
        loading.resizable(False, False)
        loading.protocol("WM_DELETE_WINDOW", lambda: None)  # Desabilita fechar

        tk.Label(loading, text=texto, font=("Arial", 14, "bold"), bg="#f73939", fg="#fff").pack(pady=(30,10))

        canvas = tk.Canvas(loading, width=60, height=60, bg="#f73939", highlightthickness=0)
        canvas.pack()
        angle = [0]

        def animate():
            canvas.delete("all")
            x, y, r = 30, 30, 25
            for i in range(12):
                a = math.radians(angle[0] + i*30)
                x0 = x + r * math.cos(a)
                y0 = y + r * math.sin(a)
                color = "#159b34" if i == 0 else "#fff"
                canvas.create_oval(x0-5, y0-5, x0+5, y0+5, fill=color, outline=color)
            angle[0] = (angle[0] + 30) % 360
            canvas.after(80, animate)
        animate()
        return loading

    def enviar_email(self):
        from os import getcwd

        confirmar = messagebox.askyesno("Confirmação", "Deseja realmente enviar o orçamento por e-mail?")
        if not confirmar:
            return

        carro = self.carro_var.get()
        placa = self.placa_var.get()
        numero = self.numero_var.get()
        destino = self.email_destino_var.get()

        if not carro or not placa or not numero or not destino:
            messagebox.showwarning("Erro", "Preencha todos os dados principais.")
            return

        nome_arquivo = f"{getcwd()}\\orcamento_{placa.replace('-', '').replace(' ', '').replace('\n', '').strip()}.pdf"
        self.gerar_pdf(nome_arquivo)

        assunto = f"Orçamento do carro {carro} - Placa {placa} N°{numero}"
        corpo = f"""Boa tarde,\nSegue o orçamento do carro {carro} placa {placa} N° {numero}.\n\nItens do orçamento:\n\n"""
        for row in self.tree.get_children():
            vals = self.tree.item(row)["values"]
            if vals[0] == "" or vals[0] == "\\n":
                linha = ""
            else:
                if vals[0] == "SOMA DAS PEÇAS":
                    linha = f"\nTotal peças: R$ {vals[4]}\n\n"
                else:
                    linha = f"- {vals[0]} | Qtd: {vals[1]} | Unitário: R$ {vals[2]} | Desconto: R$ {vals[3]} | Total: R$ {vals[4]}\n"
                corpo += linha + "\n"

        EMAIL_REMITENTE = "contatocentralautocenter@gmail.com"
        SENHA = "vhgm mwkb qljx buxq"

        loading = self.mostrar_loading("Enviando email...")

        def tarefa_envio():
            try:
                msg = EmailMessage()
                msg["Subject"] = assunto
                msg["From"] = EMAIL_REMITENTE
                msg["To"] = ", ".join([email.strip() for email in destino.split(";") if email.strip()])
                msg.set_content(corpo)

                with open(nome_arquivo, "rb") as f:
                    file_data = f.read()
                    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=nome_arquivo)

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(EMAIL_REMITENTE, SENHA)
                    smtp.send_message(msg)

                loading.destroy()
                messagebox.showinfo("Sucesso", "Orçamento enviado com sucesso!")
                self.email_destino_var.set("")
            except Exception as e:
                loading.destroy()
                messagebox.showerror("Erro", f"Falha ao enviar email:\n{e}")

        threading.Thread(target=tarefa_envio, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrcamentoApp(root)
    root.mainloop()
