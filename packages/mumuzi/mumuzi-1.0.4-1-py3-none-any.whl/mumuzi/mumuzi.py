import base64
import binascii
import re
import random
import os
from .taoshenyulu import taoshenyulu
from . import LSB
import hashlib
import time

layer_pattern = re.compile(b'^This_is_layer_.*?_of_Matryoshka:')




def enc_to_txt_file(input_file,output_file,method):
	print("enc_to_txt_file",input_file,output_file,method)
	#output_file_type=txt,1 base64 2 base85 3 文件hex 	
	with open(input_file,'rb')as f:
		input_data=f.read()
	with open(output_file,'w')as f:
		if method==1:
			#1 base64
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+base64.b64encode(input_data).decode())
		elif method==2:
			#3 base85
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+base64.a85encode(input_data).decode())
		elif method==3:
			# 文件hex
			f.write("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"+binascii.b2a_hex(input_data).decode())


def enc_to_zip_file(input_file,output_file,method):
	print('enc_to_zip_file',input_file,output_file,method)
	#output_file_type=zip,1 随机加密密码为可见3位随机字符 2 伪加密
	layer="This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"
	if method==1:
		password=random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
		cmd='zip -P '+password+' '+output_file+' '+input_file
		#print(cmd)
		os.system(cmd)
		with open(output_file,'rb')as f:
			old = f.read()
		with open(output_file,'wb')as f:
			f.write(layer.encode()+old)
	elif method==2:
		cmd='zip '+output_file+' '+input_file
		os.system(cmd)
		with open(output_file, 'rb') as f:
			r_all = f.read()
			r_all = bytearray(r_all)
			#  504B0304后的第3、4个byte改成0900
			index = r_all.find(b'PK\x03\x04')
			if not index:
				i = index + 4
				r_all[i + 2:i + 4] = b'\x09\x00'
			 #  504B0102后的第5、6个byte改成0900
			index1 = r_all.find(b'PK\x01\x02')
			if index1:
				print()
				i = index1 + 4
				r_all[i + 4:i + 6] = b'\x09\x00'
		with open(output_file, 'wb') as f1:
			f1.write(layer.encode()+r_all)

def enc_reverse_file(input_file,output_file):
	#全文件倒序
	print('enc_reverse_file',input_file,output_file)
	layer="This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"
	with open(input_file,'rb')as f:
		old = f.read()
	with open(output_file,'wb')as f:
		f.write(layer.encode()+old[::-1])

def enc_xor_file(input_file,output_file):
	#全文件xor
	print("enc_xor_file",input_file,output_file)
	layer="This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"
	key=ord(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))
	with open(input_file,'rb')as f:
		bindata=f.read()
	with open(output_file,'wb')as f:
		f.write(layer.encode())
		for i in bindata:
			f.write(int(i ^ key).to_bytes(1, 'big'))



def enc_to_png_file(input_file,output_file,method):
	png_base_file=b"""iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAhcSURBVHhe7dYxAQAgDMCwgX/PwIGLJk8tdJ1nAICU/QsAhBgAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAAEEGAACCDAAABBkAAAgyAAAQZAAAIMgAAECQAQCAIAMAADkzF445B/wqOZhLAAAAAElFTkSuQmCC"""
	png_base_file_b=base64.b64decode(png_base_file)
	png_base_file_small=b"""iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAANSURBVBhXY/j///9/AAn7A/0FQ0XKAAAAAElFTkSuQmCC"""
	print('enc_to_png_file',input_file,output_file,method)
	layer="This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka:"
	with open('temp.png','wb')as f:
		f.write(png_base_file_b)
	if method==1:
		with open(input_file,'rb')as f:
			old=f.read()
		with open(output_file,'wb')as f:
			f.write(layer.encode()+base64.b64decode(png_base_file_small)+old)
	elif method==2:
		with open(input_file,'rb')as f:
			input_file_data=f.read()
		LSB.LSB(path='',ori='temp.png',out=output_file+'.png',payload=input_file_data,bit=random.choice(["43670251","40325716","17206543","05621437","40357162","05312476","32746150","46572301","04351762"]),plane='RGBA')
		with open(output_file+'.png','rb')as f:
			old = f.read()
		with open(output_file,'wb')as f:
			f.write(layer.encode()+old)

def get_file_size(filename):
	with open(filename,'rb')as f:
		return(len(f.read()))


def waiting(cycle=20, delay=0.01):
	"""旋转式进度指示"""
	for i in range(cycle):
		for ch in ['-', '\\', '|', '/']:
			print('\b%s'%ch, end='', flush=True)
			time.sleep(delay)
		print('\b..',end='',flush=True)
	print('')
	print('')





class mumuzi:
	'大家最爱的mumuzi'
	tao_layer=0
	talk_count=0
	name="mumuzi"
	description="我是大家最爱的mumuzi，你可以叫我ctf全栈全自动解题姬哟~"
	def __init__(self):
		banner="IF9fICBfXyAgICAgICAgICAgICAgICAgICAgICAgICAgIF8gCnwgIFwvICB8XyAgIF8gXyBfXyBfX18gIF8gICBfIF9fXyhfKQp8IHxcL3wgfCB8IHwgfCAnXyBgIF8gXHwgfCB8IHxfICAvIHwKfCB8ICB8IHwgfF98IHwgfCB8IHwgfCB8IHxffCB8LyAvfCB8CnxffCAgfF98XF9fLF98X3wgfF98IHxffFxfXyxfL19fX3xffAogICAgICAgICAgICBGdWxsIFN0YWNrIEF1dG9tYXRpYyBDVEYgU29sdmluZyBIaW1lCj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09"
		print(base64.b64decode(banner).decode())
		print('Now Initiating..',end='')
		waiting(cycle=8)
		print('succeeded!')
		print('')
		time.sleep(0.1)
		print('Connecting mumuzi..',end='')
		waiting(cycle=6)
		time.sleep(0.1)
		print('mumuzi:\n\t没事叫我干嘛，爬!')

	def help(self):
		help_msg='''mumuzi:
	不帮，滚

一般路过群友:
	mumuzi目前可使用的函数列表如下：

	1.tao(input_filename,layer)
		自动套娃，输入文件名和层数，根据套神的心情好坏来帮你套娃，返回值为输出文件名。
	2.talk()
		和神说话。
	3.kou()
		表演口算md5。
	4.kua()
		套神夸人。

mumuzi:
	不要插嘴，你也给我爬'''
		print(help_msg)

	def talk(self):
		'跟神说话'
		print('='*100)
		print(random.choice(taoshenyulu))
		mumuzi.talk_count=mumuzi.talk_count+1


	def tao(self,input_file,layer):
		'套题'
		for i in range(layer):
			if mumuzi.tao_layer>mumuzi.talk_count:
				print('mumuzi:\n\t麻了\nmumuzi:\n\t还要冲一次\nmumuzi:\n\t腿已经软了')
				return
			print("This_is_layer_"+str(mumuzi.tao_layer)+"_of_Matryoshka")
			mumuzi.tao_layer=mumuzi.tao_layer+1
			output_file_type=random.choice(['zip','txt','reverse','png','xor'])
			#output_file_type='txt'
			output_file=input_file.split('.')[0]+'.tao'+str(mumuzi.tao_layer)
			file_size=get_file_size(input_file)
			if file_size<1024*1024:
				#文件大于1m，不适合png的method2、txt的method1和3 和xor
				mask=0
			elif file_size>5*1024*1024:
				#文件大于5m，不适合txt 和xor
				mask=2
			else:
				mask=1

			if output_file_type=='txt' and mask<2:
				enc_to_txt_file(input_file,output_file,random.randint(1+mask,3-mask))
			elif output_file_type=='zip':
				enc_to_zip_file(input_file,output_file,random.randint(1,2))
			elif output_file_type=='png':
				enc_to_png_file(input_file,output_file,random.randint(1,int(2-mask/2)))
			elif output_file_type=='xor' and mask==0:
				enc_xor_file(input_file,output_file)
			else:
				enc_reverse_file(input_file,output_file)

			input_file=output_file
		
		return(output_file)
	
	def kou(self):
		'口算md5'
		md5_dict={}
		for i in range(3):
			x=random.randint(0,1)
			m=''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',k=12))
			if x:
				md5_dict[hashlib.md5(m.encode()).hexdigest()]=m
			else:
				md5_dict[hashlib.md5(m.encode()).hexdigest()[8:-8]]=m
		print('mumuzi:\n\t你想要计算哪个哈希？')
		i=1
		k={}
		for key in md5_dict:
			print(i,key)
			k[str(i)]=key
			i=i+1
		a=input(':')
		if a not in '123':
			self.kua()
		else:
			x=random.randint(0,10)
			if x<9:
				print('口算完了，这是'+str(len(k[a]))+'位md5，明文是:'+md5_dict[k[a]])
			else:
				self.kua()

	def kua(self):
		'套神夸人'
		print('='*100)
		print(random.choice(taoshenyulu[:22]))
		mumuzi.talk_count=mumuzi.talk_count+1



		
