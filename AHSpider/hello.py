# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import cookielib
import SQLTool
from datetime import datetime, timedelta

def html2table(htmlData):

	pattern = re.compile(r'<title>anhui \| CMS \|(.*?)</title>',re.S)
	tt = re.findall(pattern, htmlData)[0].encode('utf-8').strip()

	pattern = re.compile(r'<table class="table table-striped table-bordered table-hover" id="datatable">.*?</table>',re.S)
	content = re.findall(pattern, htmlData)

	pattern = re.compile(r'<th class="text-center">(.*?)</th>',re.S)
	titleList = re.findall(pattern, content[0].encode('utf-8'))
	newlist = []
	for title in titleList:
		s = title.replace('(', '').replace(')', '').replace('（', '').replace('）', '').replace('/', '')
		title = s
		newlist.append(s)
	titleList = newlist

	if titleList[0] == '':
		titleList.pop(0)

	if tt == '订单工时分类明细':
		titleList[2] = '日期'

	sql = SQLTool.Mysql()
	sql.createTable(tt, titleList)

	# reobj = re.compile(r'<!--  <td>.*?</td> -->',re.S)  
	result = re.sub(r'<!--.*?<td>.*?</td>.*?-->', '', content[0].encode('utf-8')) 

	# print(titleList)
	# print(result)
	pattern = re.compile(r'<tr class="text-center">(.*?)</tr>',re.S)
	tableContent = re.findall(pattern, result)
	contentList = []
	for oneList in tableContent:
		pattern = re.compile(r'<td.*?>(.*?)</td>',re.S)
		record = re.findall(pattern, oneList)

		tp = record
		for i,t in enumerate(tp):
			if 'fa-search' in record[i]:
				record.pop(i)
			if '<a href="#" data-toggle="dropdown"' in record[i]:
				pattern = re.compile(r'(.*?)<a href=\"#\" data-toggle=\"dropdown\"' ,re.S)
				r = re.findall(pattern, record[i])[0].replace('/n', '')
				record[i] = r

		contentList.append(record)
	
	pattern = re.compile(r'<option value=.*? selected="selected">(.*?)</option>',re.S)
	name = re.findall(pattern, htmlData)

	print('要插入的数据数量为 %d' % len(contentList))

	insert2DB = []
	titleList.append("店铺的名称")

	for r in contentList:
		tempList = []
		for i,value in enumerate(r):
			# print(type(value))
			tempList.append(value)
		tempList.append(name[0].encode('utf-8'))
		insert2DB.append(tempList)
	if len(insert2DB) > 0:
		sql.insertData(tt, titleList, insert2DB)

	# print(contentDicList)

def findContent(opener, request):
	try:
		response = opener.open(request).read().decode('utf-8')
		html2table(response)
	except urllib2.URLError, e:
		if hasattr(e,"code"):
			print e.code
		if hasattr(e,"reason"):
			print e.reason

page = 1
url = 'http://cms.anhui-tech.com/user/home?_url=%2Fuser%2Fhome'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
try:
	login_url = 'http://cms.anhui-tech.com/login'
	values = {'userid':'test-mao', 'password':'maodongliang'}
	data = urllib.urlencode(values)
	request = urllib2.Request(login_url, data)

	cookie = cookielib.CookieJar()
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	response = opener.open(request)

	result = opener.open(url).read().decode('utf-8')
	pattern = re.compile(r'<ul class="treeview-menu">.*?</ul>',re.S)
	content = re.findall(pattern,result)[0]

	pattern = re.compile(r'<a href=\"(.*?)\">')
	items = re.findall(pattern, content)
	# findContent(opener, "http://cms.anhui-tech.com/report/mcs/get_export_detail")

	# for i in [1,2,3,4,5,6,7,8,9]:
	# data = 'date=2015-02-12+-+2017-02-14&supplier_name=&name=&code=&shop_id=1&export=0'
	# request = urllib2.Request(items[0].encode("utf-8"), data)
	# print('请求URL：%s' % items[0].encode("utf-8"))
	# print(request)
	# findContent(opener, request)

		# if 'get_check_inventory_supply' in item.encode("utf-8"):
		# 	print('跳过这个表格')
		# 	pass
		# else:
	# item = 'http://cms.anhui-tech.com/report/mcs/get_storage_detail'    完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_supply_peijian_detail_new'   完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_check_inventory_supply'  完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_out_detail'   完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_supply_peijian_total_new'  完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_export_detail'    完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_enterprice_order_detail' 完成
	# item = 'http://cms.anhui-tech.com/report/mcs/temp_get_work_hour_report'  完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_product_byst'  完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_order_income' 完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_supply_byst'   完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_order_parts'  完成  
	# item = 'http://cms.anhui-tech.com/report/mcs/get_return_order_detail'  完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_engineer_supply_detail' 完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_engineer_work_detail' 完成
	# item = 'http://cms.anhui-tech.com/report/mcs/temp_get_export_detail' 完成
	#item = 'http://cms.anhui-tech.com/report/mcs/get_work_hour_report' 完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_order_derate_detail' 完成
	# item = 'http://cms.anhui-tech.com/report/mcs/get_company_credit_detail' 完成


	# item = 'http://cms.anhui-tech.com/report/mcs/get_profit_report'  抓成功了，但是表格没有建立
	# item = 'http://cms.anhui-tech.com/report/mcs/temp_get_order_detail'  

	# item = 'http://cms.anhui-tech.com/report/mcs/get_engineer_work_total' 表格异常
	# item = 'http://cms.anhui-tech.com/report/mcs/get_engineer_supply_total' 失败
	# item = 'http://cms.anhui-tech.com/report/mcs/get_company_credit_sum' 失败
  # item = 'http://cms.anhui-tech.com/report/mcs/get_business_analysis' 失败
	# item = 'http://cms.anhui-tech.com/report/mcs/total_operating_data' 失败
	# for j,item in enumerate(items):
	item = item.encode('utf-8')
	for i in [1,2,3,4,5,6,7,8,9]:
	
		date = datetime(2016, 5, 1)
		dn = datetime(2017, 2, 15)
		while date  < dn:
			dateStr = date.strftime("%Y-%m-%d") 
			print(dateStr)
			data = 'date=%s+-+%s&shop_id=%d' % (dateStr, dateStr, i)
			request = urllib2.Request(item.encode("utf-8"), data)
			print('正在爬去第%d个url， 正在爬去第%s天  %d店铺的数据请求URL：%s' % (1, dateStr, i, item.encode("utf-8")))
			print(request)
			findContent(opener, request)
			date = date + timedelta(1)	
		

except urllib2.URLError, e:
	if hasattr(e,"code"):
		print e.code
	if hasattr(e,"reason"):
		print e.reason


