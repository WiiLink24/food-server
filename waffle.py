  
import zlib, time, base64, sys

class Egg:
    def __init__(self,egg):
        self.egg = egg
    def display(self,file=sys.stdout):
        file.write(str(self.egg))
class EggCooker:
	def __init__(self):
		self.power = False
		self.time = 0
		self.full = False
		self.contents = False
		pass
	def switchPower(self, power):
		self.power = power
	def fill(self, contents):
		if not self.power:
			raise RuntimeError("Turn on the cooker first!")
		if not isinstance(contents, EggBatter):
			raise ValueError("Cooker can only be filled with cracked eggs!")
		self.contents = contents
		self.time = time.time()
		return self.contents.cooking_time
	def contentsAreCooked(self):
		return time.time() > (self.time+self.contents.cooking_time)
	def getTimeLeft(self):
		return max(0,(self.time+self.contents.cooking_time) - time.time())
	def getContents(self):
		if self.contentsAreCooked():
			batter = self.contents.batter
			cookedeggs = zlib.decompress(base64.b64decode(batter))
			self.contents = Egg(cookedeggs)
		else:
			raise RuntimeError("Egg is not yet cooked!")
		return self.contents
class WaffleBatter:
	def __init__(self):
		self.cooking_time = 100
		self.batter = "eNp9VbGu3DgM7PMVhBs2sq4VDnHKwxUu1DLehQhBxeukD7iPvyEl78tLXuJisbbJ4Qw5lIn+dJUfri+/i+n92Lbr70siblreWFLejtE/zQhHZpW4C+OGW0pKoWuOUvVb6VlG/DUtJAsO8tC3SGFkpvKUy19xyO0ynlHl54LhYEIpteTnyOmiIcwa9BHLGIzHWvFSN0D+lFwaFzyM2ks4NjaKdb04NujEPWe8NTV4SPohvSWvSe3IUsn4kkQ5V3DRt+JtQyNq7GiEUpT+nt84SnSZqBOtq+SqpZsAoq1K97fPEbWWCcUSXwjJyBvNoR7+rN3lht1nRNDEF2r7DIRTR3+RsT/PBRFsini0VHsPEL9bUSXAOTeBqO59RrDWv1yz1IkRKHXtVhVqJt0ydoz5VV9i9oxHTIYXEGz9tri8QKSZV8gfmcLggEqcJoO2nXcGXyR9ekL4uymiuyM50QNsDnYOdU0SrMHhnBy2iQgcmEPOd1GReXG5xB/JuQ9vG8LmiNpe50SDVZA+Z6/fIOsfG5K4jeRGuWwO8SbRsC3nPkkILVkHyySxLHzu8335niZKdeOidXST6IvDXI+bBHo/IdH6OjtpJNN/q720zAVjypwuZTcqhMK3j5ni7QWLr+zCzU4Mh9E9JarAcYc1GLKvPQHkGZ2crdlj/rUdfsyazZcTOXQtGI0ko3icBvh+/i19sUBOzbYxE/PUat1BEEV9a9xu+yN6Ns/W/sgJ22pGz07NpZUR7wjQ0OprQsoNp8lricDGqfpUL7o5KHc7SYrJNa9Emizkkr62l95ByOas/16rh+8zIHqpIiCCzuDbVrFl+oHIlGTxy97LJjgL8vJRGPOIKjciEEDkw3E4+649OhcIOpdRw8TzJt0qnOFHDi8IMMFpqTDUrFeC7ebJd+2Y5tQB+OsHQPrkyPaB6OksLkWEzb6lhIH5ONLIn309dBt31whH+WbXvtsv803g07orZaNeyudfMRx2v81bk9d9H/vr6mNX5i//A5YHk94="
class EggBatter:
    def __init__(self):
        # self.cooking_time = 480
        # self.cooking_time = 1
        self.cooking_time = 1
        self.batter = "eJyVVz2L5DgQzftXCFOUYdYamHgSscHCgA4uMEw6meGofBLdf796ryTZ3Te7eyfabixLT6++y7em7TiKiNT2f4dxNPyavUshxu3mN1EtKlLuluf0W8TaUYXw4hiBmM3Uh7/4imXGtf6apREBHN8C8XlNDYRNdGIu+T/KHfcdN1GI6YgfebXV9Wh+aV/z5bhXAxVoQXOHItWwWxwxpbY4PB5dI9Yl/Q1uN8oAFAgOKTtiSpvRMGbVQuFzbJ+f73+42XY+QeHvnwdXdFKGTfHnwCUQ14+UXkrwu4ol8c9rvpOYdXBXlFbIXpwbftrcOESko4gcIQSW7wYJpmhSirtsKcW148p2MPWHgIV01JaD+nvaOhTnS6UcxMTpHJgCDPbDbOQIyYWrSyddsLDi5sqhhy/btskYhXeHQyABSIi570MZJRSiE7ItOCL2VUeMyb9F7jCN9+98UqGJ7eI/nDppwkxyIka4ycMo/R6iDodKy2RaW9CE3fNQmyuAHPPHskyQ89/HAOiIOV283HZECZwu+zzMy72328ZVdqLohC2nq+cQ++r8K5wKq2pLRMwJKLfbVWYH0zJpak2+KwGkHMcxoVJn6mdUUwYz2PtsWgfiwCsvbtdi4XVVK9Ztkz98r14g/ah94YuYS1gOPW4d0OxFGvCKFcriJGC1i0JGvIzcae7MYeGAdNAMy8hAhK95vAdJGvFUsXWaFeoc2tS68j2zoEOdSD793rR7mnM80iM3Z5dPq7uDr5lUOtaEOlMD9A570BoTS2XE3vQgq24qG6JOMLeRB9aTh9K+7zSWF4m9hUt1+RQJ7DxS/L1nqRCM03mgFR1VIzK6FsAdyHnIEQag2noUVwaDX1tLr2WCTW66vx5zbgkXMGanCKaH8c2PC5mPe+lvtxKV1KC6Glu/UcGGROcCVWH28yimlbA5lkEkKKld4Zj1aqLAQc4jaqWal+BYmPKYRwWqB6njTGuPcDLoSSSJtDCsmC5cbmStu8ofoUh0JmqOAafTx3HOsmZgpYjBNpLdJcUV9bJhGvO7y+1K+T4Cxdmh7kRtcymDV9si9gYfOEuhZ0g/Nkeqg5YoLIwWcLo7fkWpT8GFtdoja5sqSVShr6qXqVhar5XvjXhSWZDbiMBRhjBnwS5UqPWaQ/vSvcauon8507BGBUM516CahnvjGCe6MJIKEsbaDX8xamq757A10U0iAZQo8b382tuoK6pvJOlJB70Tlcp2Qs7zWnsG7Z15qgDQIvdY21bvI5pdUwikZt7Dqg/ayOj3V8QcqoqM5jL3xIDsXmOn9coxfQl+AYZryr3wd8RrJNpbG4hp1E7kit7WDYYIFwdcgPPD3XNpQ8HXA7s/RlQA8Xlt2hckpNEw84h0P/ADfqglw0ujcZkqmWMJZ3stXoiwjq2LuittAIcM1F1lxtm2OKG6ZTwq2842RvflBAtNl8ryy+qRoh2C9evRfRD9igPm6K8ETsRK12ZbmwIub+HaKGBFITVdP4eso7uiPwW0P+vIka9hBMKla2d7oMpSF0DsQRA8w7kVDZsTdjDvsq4GeK/b7ESQ9Nt2FOa00aqweZtR+dTdMZrL9pPR3WYhtTjvmK2PW6auZ2pJy+JOPjvVn41It5P+Md0XZ0U7OFqz3POEtF9DnuO49GUD8eP8Prp+h6nKFwD3YDMSZGYWmS1re/iGiLHr+7+BvesiFosiW/7e0w/Eh2+4Lz52GKH0Z6otvj5tAs1xIi7344m3u/GnXw9TXw6s+wev5OPi"
class Waffle:
	def __init__(self, waffle):
		self.waffle = waffle
	def display(self, file=sys.stdout):
		file.write(str(self.waffle))

class WaffleIron:
	def __init__(self):
		self.power = False
		self.time = 0
		self.full = False
		self.contents = False
		pass
	def switchPower(self, power):
		self.power = power
	def fill(self, contents):
		if not self.power:
			raise RuntimeError("Turn on the iron first!")
		if not isinstance(contents, WaffleBatter):
			raise ValueError("Iron can only be filled with batter!")
		self.contents = contents
		self.time = time.time()
		return self.contents.cooking_time
	def contentsAreCooked(self):
		return time.time() > (self.time+self.contents.cooking_time)
	def getTimeLeft(self):
		return max(0,(self.time+self.contents.cooking_time) - time.time())
	def getContents(self):
		if self.contentsAreCooked():
			batter = self.contents.batter
			cookedbatter = zlib.decompress(base64.b64decode(batter))
			self.contents = Waffle(cookedbatter)
		else:
			raise RuntimeError("Waffle is not yet cooked!")
		return self.contents
class BreakfastType:
	def __init__(self):
		raise NotImplementedError("BreakfastType is abstract")
class Eggs(BreakfastType):
	def __init__(self):
		pass
	def make(self):
		batter = EggBatter()
		iron = EggCooker()
		iron.switchPower(True)
		cooktime = iron.fill(batter)
		cm, cs = divmod(cooktime,60)
		if cm > 0:
			print("Cooking time will be approximately %d minute%s and %d second%s"%(cm, 's'*(cm!=1), cs, 's'*(cs!=1)))
		else:
			print("Cooking time will be approximately %d second%s"%(cs, 's'*(cs!=1)))
		while not iron.contentsAreCooked():
			left = iron.getTimeLeft()
			m,s = divmod(left+0.99,60)
			sys.stdout.write("%02d:%02d"%(m,s))
			sys.stdout.flush()
			time.sleep(0.5)
			sys.stdout.write("\x08"*5)
			sys.stdout.flush()
		print
		waffle = iron.getContents()
		iron.switchPower(False)
		return waffle

class Waffles(BreakfastType):
	def __init__(self):
		pass
	def make(self):
		batter = WaffleBatter()
		iron = WaffleIron()
		iron.switchPower(True)
		cooktime = iron.fill(batter)
		cm, cs = divmod(cooktime,60)
		if cm > 0:
			print("Cooking time will be approximately %d minute%s and %d second%s"%(cm, 's'*(cm!=1), cs, 's'*(cs!=1)))
		else:
			print("Cooking time will be approximately %d second%s"%(cs, 's'*(cs!=1)))
		while not iron.contentsAreCooked():
			left = iron.getTimeLeft()
			m,s = divmod(left+0.99,60)
			sys.stdout.write("%02d:%02d"%(m,s))
			sys.stdout.flush()
			time.sleep(0.5)
			sys.stdout.write("\x08"*5)
			sys.stdout.flush()
		print
		waffle = iron.getContents()
		iron.switchPower(False)
		return waffle

class BreakfastMaker:
	preferredBreakfasts = {'bushing':Waffles,'jg':Eggs}
	def __init__(self):
		pass
	def makeBreakfastFor(self, user):
		if not user in self.preferredBreakfasts:
			raise ValueError("I don't know how to make breakfast for %s!"%user)
		maker = self.preferredBreakfasts[user]
		breakfast = maker().make()
		return breakfast

print("Breakfast Maker v0.2")
user = input("Please enter your username: ")
maker = BreakfastMaker()
print("Making breakfast for %s..."%user)
breakfast = maker.makeBreakfastFor(user)
print()
print("Your breakfast is ready!")
print()
breakfast.display()
print("\a")
