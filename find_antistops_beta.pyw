#coding=utf-8
import sys
import pymysql
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow,QWidget,QAction,QApplication,

	QComboBox,QLineEdit,QTextEdit,QLabel,QPushButton,QMessageBox)

#最好不要有关闭快捷键
#多窗口矛盾

#-> 怎么写逻辑？

class Button2(QPushButton):	#Button to show results
	def __init__(self,window):
		super().__init__(window)
		self.setStyleSheet(	"""QPushButton{
								background-color:white;
								border:none;
								text-align:left;
								font-size:14px;
								}"""
							"""QPushButton:hover{
								background-color:#f4f4f4;
								}""")
		self.setText(" ")


class QMainWindow2(QMainWindow):
	
	def mousePressEvent(self, event):
		if event.button()==Qt.LeftButton:
			self.m_drag=True
			self.m_DragPosition=event.globalPos()-self.pos()
			event.accept()

	def mouseMoveEvent(self, QMouseEvent):
		if QMouseEvent.buttons() and Qt.LeftButton:
			try:
				self.move(QMouseEvent.globalPos()-self.m_DragPosition)
				QMouseEvent.accept()
			except:
				#I don't know what it is
				pass

	def mouseReleaseEvent(self, QMouseEvent):
		self.m_drag=False


class Window1(QMainWindow2):	#Main window

	def __init__(self):
		super().__init__()
		#var
		self.table = "Python"
		self.model = "关键词"

		self.word_list = [1]
		#(word,show content)

		config = {
		  'host':'localhost',
		  'user':'root',
		  'password':'',
		  'db':'example',
		  'charset':'utf8'
		  }
		self.db = pymysql.connect(**config)
		self.cursor = self.db.cursor()

		#screen
		self.initUI()


	def initUI(self):
		m1,m2 = (0,10)
		a,h = (600,385+20)

		self.setWindowTitle('Search')					#Window set
		self.setFixedSize(a,h)
		self.move(300,300)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setStyleSheet("""Window1{background-color:#E6E6F5;
								border:1px solid #D7D7F0;}""")

		self.label1 = QLabel("模式："+self.model,self)	#widget: label1
		self.label1.move(150,28)
		self.label1.resize(self.label1.sizeHint())

		self.label2 = QLabel("语言：",self)				#widget: label2
		self.label2.move(7,28)
		self.label2.resize(self.label2.sizeHint())

		self.label3 = QLabel("",self)					#widget: label3
		self.label3.move(1,44)							#(a space)
		self.label3.resize(11,30)
		self.label3.setStyleSheet("""QLabel{background-color:white;}""")

		self.choose1 = QComboBox(self)					#widget: choose
		self.choose1.move(50,23)
		self.choose1.addItem("Python")
		self.choose1.addItem("Ruby")
		self.choose1.addItem("Java")
		self.choose1.resize(self.choose1.sizeHint())
		self.choose1.activated[str].connect(self.l_change)

		self.input1 = QLineEdit(self)     				#widget: lineedit
		self.input1.move(6,44)
		self.input1.setMinimumWidth(a-7)
		self.input1.setStyleSheet("""QLineEdit{
										text-indent:2;
										height:18px;
										background-color:white;
										border:none;
										font-size:14px;
										}""")
		self.input1.textChanged[str].connect(self.update)

		for i in range(12):								#widget: results
			self.create_button(i+1,a,m1,m2)
			self.create_f(i+1)
			exec("self.button%d.clicked.connect(f%d)"%(i+1,i+1))


		self.next_p = QPushButton("下一页",self)			#widget: p_move
		self.next_p.resize(self.next_p.sizeHint())
		self.next_p.move(a-77,h-20-9)
		self.next_p.clicked.connect(self.next_page)
		self.next_p.hide()

		self.last_p = QPushButton("上一页",self)
		self.last_p.resize(self.next_p.sizeHint())
		self.last_p.move(a-77-74,h-20-9)
		self.last_p.clicked.connect(self.last_page)
		self.last_p.hide()


		menubar = self.menuBar()						#widget: menu
		fileMenu = menubar.addMenu('&File')

		exitAction = QAction(QIcon('exit.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(quit)
		fileMenu.addAction(exitAction)

		changeAction = QAction(QIcon('change.png'), '&Change', self)
		changeAction.setShortcut('Ctrl+Return')
		changeAction.triggered.connect(self.m_change)
		fileMenu.addAction(changeAction)

		cleanAction = QAction(QIcon('clean.png'), '&Clean', self)
		cleanAction.setShortcut('Ctrl+L')
		cleanAction.triggered.connect(self.clean)
		fileMenu.addAction(cleanAction)

		addAction = QAction(QIcon('add.png'), '&Add', self)
		addAction.setShortcut('Ctrl+D')
		addAction.triggered.connect(self.add_word)
		fileMenu.addAction(addAction)					
		
		add2Action = QAction(QIcon('add_tag.png'), '&Add Tag', self)
		add2Action.setShortcut('Ctrl+T')
		add2Action.triggered.connect(self.add_tag)
		fileMenu.addAction(add2Action)					#menu end


		self.input1.setFocus()							#start
		self.show()


	def search_only(self,text):
		#进行搜索
		if self.model == "关键词":
			sql ="""select 关键词,说明
					from %s
					where 关键词 like '%s%%';"""%(self.table,text)
		else:
			assert self.model == "标签"
			sql ="""select 关键词,说明
					from %s
					where 标签 like '%%%s%%';"""%(self.table,text)
		self.cursor.execute(sql)

	def sto_12(self):
		temp_list = [0,6,6,6,6,6,6,6,6,6,6,6,6]	#空位标记，有对应try
		for i in range(12):
			txt = " "	#行首空格
			data = self.cursor.fetchone()
			if data:#结果必然只有两列
				txt = ' '+data[0]+'\t'+str(data[1])
				temp_list[i+1] = (data[0],txt)
			else:#all recorded
				self.word_list.append(temp_list)
				break
			if i == 11:	#满了
				temp_list[0] = 1	#页满标记
				self.word_list.append(temp_list)

	def show_result(self):
		l = self.word_list
		page = l[0]
		for i in range(12):
			try:
				txt = l[page][i+1][1]
			except:
				break
			exec("self.button%d.setText('%s')"%(i+1,txt))
		if page != 1:
			self.last_p.show()	#唯一显示入口
		if l[page][0] == 1:
			self.next_p.show()

	def update(self, text):
		self.clean2()
		if text == "":
			return
		else:
			self.word_list = [1]
			self.search_only(text)
			self.sto_12()
			self.show_result()


	def next_page(self):
		if len(self.word_list) == self.word_list[0] + 1:	#最后一页
			self.sto_12()
		self.clean2()
		self.word_list[0] += 1
		self.show_result()

	def last_page(self):
		self.clean2()
		self.word_list[0] -= 1
		self.show_result()


	def m_change(self):
		if self.model == "关键词":
			self.model = "标签"		#等号！
		else:
			self.model = "关键词"
		self.label1.setText("模式："+self.model)

	def l_change(self, text):
		self.table = text
		self.clean()


	def clean(self):
		self.input1.setFocus()
		self.input1.setText("")

		self.clean2()

	def clean2(self):
		for i in range(12):
			exec("self.button%d.setText('')"%(i+1))
		self.next_p.hide()
		self.last_p.hide()


	def create_button(self,n,a,m1,m2):
		exec("self.button%d = Button2(self)"%n)
		exec("self.button%d.move(%d,%d)"%(n,1,m2+40+25*n))
		exec("self.button%d.resize(%d,25)"%(n,a-2))

	def create_f(self,n):#这里的函数遇6跳过（空白按钮）		
		exec("""def f%d():
		try:
			l = window1.word_list
			window1.true_f(l[l[0]][%d][0])
		except:
			print("Maybe empty (error in f_d)")"""%(n,n),globals())
	

	def true_f(self,word):
		print(word)
		window3.find(word)		
		window3.show()

	def add_word(self):
		window4.show()		

	def add_tag(self):
		window5.show()		


class Window3(QMainWindow2):	#detail screen
	def __init__(self):
		super().__init__()
		
		self.cursor = window1.db.cursor()	#另一指针？
						
		self.initUI()
		
	def initUI(self):
		m1,m2 = (0,10)
		a,h = (600,385+20)

		self.setWindowTitle('Details')					#Window set
		self.setFixedSize(a,h)
		self.move(900-1,300)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setStyleSheet("""Window3{background-color:white;
								border:1px solid #D7D7F0;}""")
								
		menubar = self.menuBar()						#widget: menu
		fileMenu = menubar.addMenu('&File')

		exitAction = QAction(QIcon('exit.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(self.close)
		fileMenu.addAction(exitAction)					#menu end
		
		
		self.label1 = QLabel("",self)					#widget: word
		self.label1.move(30,40)	
		self.label1.setStyleSheet("""QLabel{background-color:white;
										font-family:Microsoft YaHei;
										font-size:30px;}""")
		
		self.label2 = QLabel("",self)					#widget: tag
		self.label2.move(30,100)	
		self.label2.setStyleSheet("""QLabel{font-size:14px;}""")
		
		self.label3 = QLabel("",self)					#widget: detail
		self.label3.move(30,140)
		self.label3.setStyleSheet("""QLabel{font-size:14px;}""")
		
	def find(self,word):	#find and set
		sql ="""select *
				from %s
				where 关键词 = '%s';"""%(window1.table,word)
		self.cursor.execute(sql)
		record = self.cursor.fetchone()
		self.label1.setText(self.reline(record[0]))
		self.label1.adjustSize()
		self.label2.setText(self.reline(record[1]))
		self.label2.adjustSize()
		self.label3.setText(self.reline(record[2]))
		self.label3.adjustSize()

	def reline(self,txt,k=80):
		return '\n'.join(txt[i:i+k] for i in range(0,len(txt),k))	
	

class Window4(QMainWindow2):	#add antistop
	def __init__(self):
		super().__init__()
		
		self.cursor = window1.db.cursor()
		
		self.initUI()
		
	def initUI(self):
		m1,m2 = (0,10)
		a,h = (600,385+20)

		self.setWindowTitle('Add antistop')			#Window set
		self.setFixedSize(a,h)
		self.move(900-1,300)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setStyleSheet("""Window4{background-color:white;
								border:1px solid #D7D7F0;}""")
								
								
		self.edit1 = QLineEdit("",self)				#widget: word
		self.edit1.move(60,40)	
		self.edit1.setMinimumWidth(600-60-30)
		self.edit1.setStyleSheet("""QLineEdit{background-color:white;
										font-family:Microsoft YaHei;
										font-size:16px;}""")
		
		self.label1 = QLabel("关键词：",self)			#widget: label1
		self.label1.move(10,49)
		self.label1.resize(self.label1.sizeHint())
		
		self.edit2 = QLineEdit("",self)				#widget: tag
		self.edit2.move(60,100)	
		self.edit2.setMinimumWidth(600-60-30)
		self.edit2.setStyleSheet("""QLineEdit{font-size:14px;}""")
		
		self.label2 = QLabel("标签：",self)			#widget: label2
		self.label2.move(15,109)
		self.label2.resize(self.label1.sizeHint())
		
		self.edit3 = QTextEdit("",self)				#widget: detail
		self.edit3.move(60,160)
		self.edit3.resize(600-60-30,205)
		self.edit3.setStyleSheet("""QTextEdit{font-size:14px;}""")
		
		self.label3 = QLabel("内容：",self)			#widget: label3
		self.label3.move(15,169)
		self.label3.resize(self.label1.sizeHint())
		
		self.button1 = QPushButton("确定",self)		#widget: button
		self.button1.move(600-30*2-49,370)
		self.button1.resize(80,24)
		self.button1.clicked.connect(self.yes)
		
		self.button2 = QPushButton("取消",self)		#widget: button
		self.button2.move(600-30*2-130,370)
		self.button2.resize(80,24)
		self.button2.clicked.connect(self.close2)
		
	def close2(self):
		self.edit1.setText("")
		self.edit2.setText("")
		self.edit3.setText("")
		
		window1.db.commit()	#...
		self.close()
		
	def yes(self):
		antistop = self.edit1.text().strip()
		tag = self.edit2.text().strip()
		detail = self.edit3.toPlainText().strip()
		sql ="""insert into %s
			values ('%s','%s','%s');
			"""%(window1.table,antistop,detail,tag)
		try:
			self.cursor.execute(sql)
		except:
			print("failed in add_all",antistop)
			QMessageBox.about(self,'Error',
						"failed in add_all "+antistop)
			return
			
		self.edit1.setText("")
		self.edit2.setText("")
		self.edit3.setText("")


class Window5(QMainWindow2):	#add tag
	def __init__(self):
		super().__init__()
		
		self.cursor = window1.db.cursor()
		
		self.initUI()
		
	def initUI(self):
		m1,m2 = (0,10)
		a,h = (600,200)

		self.setWindowTitle('Add tag')					#Window set
		self.setFixedSize(a,h)
		self.move(900-1,300)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setStyleSheet("""Window5{background-color:white;
								border:1px solid #D7D7F0;}""")
								
								
		self.edit1 = QLineEdit("",self)				#widget: word
		self.edit1.move(60,40)	
		self.edit1.setMinimumWidth(600-60-30)
		self.edit1.setStyleSheet("""QLineEdit{background-color:white;
										font-family:Microsoft YaHei;
										font-size:16px;}""")
										
		self.label1 = QLabel("关键词：",self)			#widget: label1
		self.label1.move(10,49)
		self.label1.resize(self.label1.sizeHint())
		
		self.edit2 = QLineEdit("",self)				#widget: tag
		self.edit2.move(60,100)	
		self.edit2.setMinimumWidth(600-60-30)
		self.edit2.setStyleSheet("""QLineEdit{font-size:14px;}""")
		
		self.label2 = QLabel("新标签：",self)			#widget: label2
		self.label2.move(10,109)
		self.label2.resize(self.label1.sizeHint())
		
		
		
		self.button1 = QPushButton("确定",self)		#widget: button
		self.button1.move(600-30*2-49,165)
		self.button1.resize(80,24)
		self.button1.clicked.connect(self.yes)
		
		self.button2 = QPushButton("取消",self)		#widget: button
		self.button2.move(600-30*2-130,165)
		self.button2.resize(80,24)
		self.button2.clicked.connect(self.close2)
		
	def close2(self):
		self.edit1.setText("")
		self.edit2.setText("")
		
		window1.db.commit()	#...
		self.close()
		
	def yes(self):
		antistop = self.edit1.text().strip()
		tag = self.edit2.text().strip()
		table = window1.table
		
		if tag == "":
			print("failed in add_tag: add nothing")
			QMessageBox.about(self,'Error',
						"failed in add_tag: add nothing")
			return
		sql ="""select 标签
				from %s
				where 关键词='%s';"""%(table,antistop)
		self.cursor.execute(sql)
		record = self.cursor.fetchone()
		if record == None:
			print("failed in add_tag: can't find:",antistop)
			QMessageBox.about(self,'Error',
						"failed in add_tag: can't find: "+antistop)
			return
		else:
			tag0 = record[0]
			if tag0 != "":
				tag = tag0 + ' ' + tag
			else:
				pass	#首个tag				
		sql ="""update %s
				set 标签 = '%s'
				where 关键词='%s';"""%(table,tag,antistop)
		
		try:
			self.cursor.execute(sql)
			
			
		except:
			print("failed in add_tag: can't update:",antistop)
			QMessageBox.about(self,'Error',
						"failed in add_tag: can't update: "+antistop)
			return
			
		self.edit1.setText("")
		self.edit2.setText("")	
				
########################################################################		

########################################################################
if __name__ == '__main__':

	app = QApplication(sys.argv)
	window1 = Window1()
	#button2
	window3 = Window3()
	window4 = Window4()
	window5 = Window5()

	sys.exit(app.exec_())




