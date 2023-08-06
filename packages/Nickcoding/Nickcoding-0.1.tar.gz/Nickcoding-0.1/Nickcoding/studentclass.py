# studentclass.py

class Student:
	def __init__(self,name):
		self.name = name
		self.exp = 0
		self.lesson = 0
		# call Function
		# self.AddEXP(10)

	def Hello(self):
		print('Sawadee jaaa my name is {}'.format(self.name))

	def Coding(self):
		print('{}:กำลังเขียนโปรแกรม..'.format(self.name))
		self.exp += 5
		self.lesson += 1
	
	def ShowEXP(self):
		print('{} have {} exp '.format(self.name,self.exp))
		print('เรียนไป {} ครั้งแล้ว'.format(self.lesson))

	def AddEXP(self,score):
		self.exp += score # self.exp = student1.exp + 10
		self.lesson += 1


class SpecialStudent(Student):
 	
	def __init__(self, name,father):
		super().__init__(name)
		self.father = father
		mafia = ['Bill Gates','Thomas Edison']
		if father in mafia:
			self.exp += 100

	def AddEXP(self,score):
		self.exp += (score * 3)
		self.lesson += 1

	def Askexp (self,score = 10):
		print('ครู!! ขอคะแนนพิเศษให้ผมหน่อยสิสัก {} exp'.format(score))
		self.AddEXP(score)



if __name__ == '__main__':

	print('========1 jan======')

	student0 = SpecialStudent('Mark Zuckerberg','Bill Gates')
	student0.Askexp()
	student0.ShowEXP()


	student1 = Student('Albert')
	print(student1.name)
	student1.Hello()
	print('------------')
	student2 = Student('Steve')
	print(student2.name)
	student2.Hello()

	print('========2 Jan=======')
	print('------ใครอยากเรียนโค้ดดิ้ง? (10 exp)-------')
	# student1.exp += 10 # student1.exp = student1.exp + 10
	student1.AddEXP(10)

	print('========3 Jan=======')

	print('ตอนนี้ exp ของแต่ละคนได้เท่าไรกันแล้ว')
	print(student1.name, student1.exp)
	print(student2.name, student2.exp)
	print('========4 Jan=======')

	for i in range(5):
		student2.Coding()
	# print('{} have {} exp\n เรียนไป {} ครั้งแล้ว'.format(student2.name,student2.exp,student2.lesson))
	# print('{} have {} exp\n เรียนไป {} ครั้งแล้ว'.format(student1.name,student1.exp,student1.lesson))
	student1.ShowEXP()
	student2.ShowEXP()
