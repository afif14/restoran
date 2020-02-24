from tkinter import *
import sqlite3
import tkinter.messagebox as tkMessageBox
import string

class FormSupplier(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        widthForm = 640
        heightForm = 250

        self.geometry("%dx%d+%d+%d" % (widthForm, heightForm, 
            parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
                    
        self.aturKomponen()
        self.aturKejadian()
        self.koneksiDatabase()
        
        self.resizable(width=False, height=False)
        self.title("Form Data Supplier")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onPass)
        self.parent = parent
        
        # setting awal
        self.isiDataList(self.sql)
        self.displayToEntry()
        self.formLoad()

        self.wait_window()
    
    def aturKomponen(self):
        # frame utama
        mainFrame = Frame(self)
        mainFrame.pack(fill=BOTH, expand=YES)
        
        # olah fr_list beserta komponennya
        fr_kiri = Frame(mainFrame)
        fr_kiri.pack(side=LEFT, fill=BOTH, expand=YES)
        
        fr_list = Frame(fr_kiri)
        fr_list.pack(fill=BOTH, expand=YES)
        
        self.list = Listbox(fr_list, width=30)
        self.list.pack(side=LEFT, fill=BOTH, expand=YES)
        
        scrollbar = Scrollbar(fr_list, orient=VERTICAL,
            command=self.list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list.config(yscrollcommand=scrollbar.set)
        
        # ---> atur fr_cari
        fr_cari = Frame(fr_kiri)
        fr_cari.pack(side=BOTTOM,fill=X, pady=5)
        
        self.statusCari = IntVar()
        self.checkCari = Checkbutton(fr_cari, text="Cari:",
            var=self.statusCari, command=self.onCekCari)
        self.checkCari.pack(side=LEFT)
        
        self.entryCari = Entry(fr_cari)
        self.entryCari.pack(side=LEFT, fill=X, expand=YES)
        
        # olah fr_kanan beserta komponennya
        fr_kanan = Frame(mainFrame, bd=5)
        fr_kanan.pack(fill=BOTH, expand=YES, side=LEFT)
        
        # ---> atur fr_data
        fr_data = Frame(fr_kanan)
        fr_data.pack()
        
        Label(fr_data, text="Kode Supplier").grid(row=0, 
            column=0, sticky=W)
        self.entryKdSup = Entry(fr_data, width=7)
        self.entryKdSup.grid(row=0, column=1, sticky=W, pady=5)
        kdFont = self.entryKdSup["font"]
        
        Label(fr_data, text="Nama Supplier").grid(row=1, 
            column=0, sticky=W)
        self.entryNmSup = Entry(fr_data, width=30)
        self.entryNmSup.grid(row=1, column=1, sticky=W, pady=5)
        
        Label(fr_data, text="No. Telepon").grid(row=2, 
            column=0, sticky=W)
        self.entryNoTelp = Entry(fr_data, width=15)
        self.entryNoTelp.grid(row=2, column=1, sticky=W, pady=5)
        
        Label(fr_data, text="Alamat").grid(row=3, 
            column=0, sticky=W)
        self.textAlamat = Text(fr_data, height=3, width=30,
            font=kdFont)
        self.textAlamat.grid(row=3, column=1, sticky=W, pady=5)
        
        # ---> fr_tombol
        fr_tombol = Frame(fr_kanan)
        fr_tombol.pack(side=BOTTOM, fill=X)
        
        self.buttonTambah = Button(fr_tombol, text='Tambah',
            command=self.onTambahKlik, underline=0, width=5)
        self.buttonTambah.pack(side=LEFT, fill=X, expand=YES)
        
        self.buttonSimpan = Button(fr_tombol, text='Simpan',
            command=self.onSimpanKlik, underline=0, width=5)
        self.buttonSimpan.pack(side=LEFT, fill=X, expand=YES)
        
        self.buttonHapus = Button(fr_tombol, text='Hapus',
            command=self.onHapusKlik, underline=0, width=5)
        self.buttonHapus.pack(side=LEFT, fill=X, expand=YES)
        
        self.buttonKeluar = Button(fr_tombol, text='Keluar',
            command=self.onKeluarKlik, underline=0, width=5)
        self.buttonKeluar.pack(side=LEFT, fill=X, expand=YES)
        
    def aturKejadian(self):
        self.entryCari.bind("<KeyRelease>", 
            self.onCariKeyRelease) 
        self.entryCari.bind("<Return>", 
            self.onCariReturn) 
        
        self.list.bind("<ButtonRelease-1>", self.onListKlik)
        self.list.bind("<Double-Button-1>", self.onListDblKlik)
        self.list.bind("<Down>", self.onUpDownPress) 
        self.list.bind("<Up>", self.onUpDownPress) 
        
        self.entryNmSup.bind("<Return>", self.onEntryNmSupEnter)
        self.entryNoTelp.bind("<Return>", self.onEntryNoTelpEnter)
        self.textAlamat.bind("<Return>", self.onTextAlamatEnter)
        
        self.buttonSimpan.bind("<Return>", self.onSimpanKlik)
        
    def onPass(self):
        pass 
        
    def onEntryNmSupEnter(self, event):
        self.entryNoTelp.focus_set()

    def onEntryNoTelpEnter(self, event):
        self.textAlamat.focus_set()

    def onTextAlamatEnter(self, event):
        self.buttonSimpan.focus_set()

    def onCariKeyRelease(self, event):
        strCari = self.entryCari.get()
        
        cariSQL = self.sql + " WHERE UPPER(nm_supplier) LIKE UPPER('%" + strCari + "%')"
        
        self.isiDataList(cariSQL)
        self.displayToEntry()
        
    def onCariReturn(self, event):
        self.list.focus_set()

    def onListKlik(self, event):
        self.displayToEntry()
        
    def onListDblKlik(self, event):
        self.buttonTambah.configure(state=DISABLED)
        self.buttonSimpan.configure(state=NORMAL)
        self.buttonHapus.configure(state=NORMAL)
        self.buttonSimpan.configure(text='Ubah')
        self.buttonKeluar.configure(text='Batal')
        
        self.list.configure(state=DISABLED)
        self.entryCari.configure(state=DISABLED)
        self.checkCari.configure(state=DISABLED)

        self.entryKdSup.configure(state=DISABLED)
        self.entryNmSup.focus_set()     
        self.displayToEntry()
        
    def onUpDownPress(self, event):
        self.list.bind("<KeyRelease>", self.onListKlik) 
                    
    def koneksiDatabase(self):
        self.db = sqlite3.connect("./data/datatoko.db")
        self.cur = self.db.cursor()     
        
        self.sql = "SELECT * FROM supplier"
                
    def formLoad(self):
        self.buttonSimpan.configure(state=DISABLED)
        self.buttonHapus.configure(state=DISABLED)
        
        if self.jumData == 0:
            self.list.configure(state=DISABLED)
            self.entryCari.configure(state=DISABLED)
            self.checkCari.configure(state=DISABLED)
        else:
            self.list.configure(state=NORMAL)
            self.entryCari.configure(state=DISABLED)
            self.checkCari.configure(state=NORMAL)
        
    def formKosong(self):
        self.entryKdSup.delete(0, END)
        self.entryNmSup.delete(0, END)
        self.entryNoTelp.delete(0, END)
        self.textAlamat.delete(1.0, END)
        
    def formNormal(self):
        self.formKosong()
        
        self.buttonTambah.configure(state=NORMAL)
        self.buttonSimpan.configure(state=DISABLED)
        self.buttonHapus.configure(state=DISABLED)
        self.buttonHapus["text"] = 'Hapus'
        self.buttonSimpan["text"] = 'Simpan'
        self.buttonKeluar["text"] = 'Keluar'
                        
        self.list.configure(state=NORMAL)
        self.entryCari.configure(state=DISABLED)
        self.checkCari.configure(state=NORMAL)
        
    def onClose(self, event=None):
        #self.parent.destroy()
        self.cur.close()
        self.db.close()
        self.destroy()

    def onCekCari(self):
        if self.statusCari.get() == 1:
            self.entryCari.configure(state=NORMAL)
            self.entryCari.focus_set()
        else:
            self.entryCari.delete(0, END)
            self.entryCari.configure(state=DISABLED)
            if self.jumData != 0:
                self.isiDataList(self.sql)
                self.displayToEntry()
        
    def onTambahKlik(self):
        self.formKosong()

        self.entryKdSup.insert(END, self.buatKode())
        self.entryKdSup.configure(state=DISABLED)
        self.entryNmSup.focus_set()

        self.buttonTambah.configure(state=DISABLED)
        self.buttonSimpan.configure(state=NORMAL)
        self.buttonSimpan.configure(text='Simpan')
        self.buttonKeluar.configure(text='Batal')
        
        self.list.configure(state=DISABLED)
        self.checkCari.configure(state=DISABLED)
                        
    def onSimpanKlik(self, event=None):
        kd_sup = self.entryKdSup.get()
        nm_sup = self.entryNmSup.get()
        no_tel = self.entryNoTelp.get()
        alamat = self.textAlamat.get(1.0, END).splitlines()
        #print alamat
        
        if nm_sup == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Nama supplier tidak boleh kosong!",
                parent=self)
            self.entryNmSup.focus_set()
        elif alamat == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Alamat supplier tidak boleh kosong!", 
                parent=self)
            self.textAlamat.focus_set()
        elif no_tel == "":
            tkMessageBox.showwarning("Perhatian!", 
                "No Telpon supplier tidak boleh kosong!",
                parent=self)
            self.entryNoTelp.focus_set()
        else:
            if self.buttonSimpan["text"]=='Ubah':
                str = "UPDATE supplier SET nm_supplier='%s', no_telp='%s', alamat='%s' WHERE kd_supplier='%s'"%(
                    nm_sup, no_tel, alamat[0], kd_sup)
                tkMessageBox.showinfo("Informasi", 
                    "Data telah diubah.", parent=self)
            else:
                str = "INSERT INTO supplier VALUES('%s','%s','%s','%s')" %(
                    kd_sup, nm_sup, no_tel, alamat[0])
                tkMessageBox.showinfo("Informasi", 
                    "Data telah disimpan.", parent=self)

            self.cur.execute(str)
            self.db.commit()
            
            self.entryKdSup.configure(state=NORMAL)
            self.list.configure(state=NORMAL)
            self.entryCari.configure(state=NORMAL)
            
            self.entryCari.delete(0, END)
            self.checkCari.deselect()

            self.formNormal()
                    
            self.isiDataList(self.sql)
            self.displayToEntry()
            self.list.focus_set()
                
    def onHapusKlik(self):
        if tkMessageBox.askyesno(
            "Hapus Data:", "Anda yakin akan menghapus record ini?",
            parent=self):
                sql = "DELETE FROM supplier WHERE kd_supplier='%s'"%(
                    self.entryKdSup.get())
                    
                self.cur.execute(sql)
                self.db.commit()
                
                self.entryKdSup.configure(state=NORMAL)
                self.entryCari.configure(state=NORMAL)
            
                self.entryCari.delete(0, END)
                self.checkCari.deselect()

                self.formNormal()
                self.formLoad()

                self.isiDataList(self.sql)
                self.displayToEntry()
                self.list.focus_set()
        else:
            self.entryKdSup.configure(state=NORMAL)
            self.formNormal()
            self.formLoad()

            self.isiDataList(self.sql)
            self.displayToEntry()
            self.list.focus_set()
        
    def onKeluarKlik(self):
        if self.buttonKeluar["text"] == 'Keluar':
            self.onClose()
        else:
            self.formNormal()
            self.buttonKeluar["text"] = 'Keluar'
            self.entryKdSup.configure(state=NORMAL)
            self.formKosong()
            self.displayToEntry()
            self.list.focus_set()
            self.entryCari.configure(state=NORMAL)          

    def eksekusi(self, sql):
        self.cur.execute(sql)
        lineData = self.cur.fetchall()
        totData = len(lineData)
        
        return lineData, totData
        
    def isiDataList(self, sql=None):
        self.list.delete(0, END)

        sql = sql + " ORDER BY nm_supplier"
        
        baris, jumData = self.eksekusi(sql)
        
        if jumData == 0:
            tkMessageBox.showwarning("Perhatian!",
                "Data Supplier masih kosong!", parent=self)
            self.buttonTambah.focus_set()
        else:       
            for data in range(jumData):
                teks = "%s" %(baris[data][1])
                self.list.insert(END, teks)
            self.list.selection_set(0)
        
        self.baris = baris
        self.jumData = jumData
                
    def displayToEntry(self):
        if self.jumData == 0:
            pass 
        else:
            index = self.list.curselection()
            strKlik = self.list.get(index)
        
            sql = "SELECT * FROM supplier WHERE nm_supplier='%s'"%strKlik
            
            baris, jumData = self.eksekusi(sql)

            self.formKosong()
            self.entryKdSup.insert(END, baris[0][0])
            self.entryNmSup.insert(END, baris[0][1])
            self.entryNoTelp.insert(END, baris[0][2])
            self.textAlamat.insert(END, baris[0][3])
            
    def buatKode(self):
        sql = "SELECT * FROM supplier"
        cek, jum = self.eksekusi(sql)
        
        if jum == 0:
            teks = "S001"
        else:
            kd = cek[jum-1][0]
            #print kd
            kode_sup = int(kd[-3:]) + 1
            #print kode_sup
            
            if kode_sup < 10:
                teks = "S00" + str(kode_sup)
            elif kode_sup < 100:
                teks = "S0" + str(kode_sup)
            elif kode_sup < 1000:
                teks = "S" + str(kode_sup)
            
        return teks
        
if __name__ == '__main__':
    root = Tk()
    
    def run():
        import formSupplier
        obj = formSupplier.FormSupplier(root)
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()
