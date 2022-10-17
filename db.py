"""
topic = "地下空间"
driver.find_element(By.ID,'btnSearch').click()
driver.find_element(By.ID,'keyword_ordinary').send_keys(topic)
driver.find_element(By.CLASS_NAME,'btn-search').click()
time.sleep(0.3)

# 筛选文献
driver.find_element(By.ID,"articletype_a").click()
time.sleep(0.3)
driver.find_element(By.CSS_SELECTOR,"a[data-value=\"14\"]").click()

# 筛选学科
# driver.find_element_by_id("menu-toggle").click()
# driver.find_element(By.CLASS_NAME,'c-filter-title').click()

# 获取文献数量
num = driver.find_element(By.CLASS_NAME,'search-number').text
num = int(num[:-1])

# 加载所有页面
for i in range(int(num/10)):
    driver.find_element(By.CLASS_NAME,'c-company__body-item-more').click()
    time.sleep(0.3)

#  加载3页
# for i in range(3):
#     driver.find_element(By.CLASS_NAME,'c-company__body-item-more').click()
#     time.sleep(0.3)  
    
# 把网页拉到最下面，确保网页加载完成
# driver.find_element(By.CLASS_NAME,"c-footer__copyright").click()
# time.sleep(0.3)

# 获取文献信息
title = driver.find_elements(By.CLASS_NAME,'c-company__body-title')
author = driver.find_elements(By.CLASS_NAME,'c-company__body-author')
link = driver.find_elements(By.CLASS_NAME,'c-company-top-link')
content = driver.find_elements(By.CLASS_NAME,'c-company__body-content')
company = driver.find_elements(By.CLASS_NAME,'color-green')
info = driver.find_elements(By.CLASS_NAME,'c-company__body-info')

# 保存到Excel
# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet(topic)  #添加sheet
head = ['标题', '作者', '摘要', '来源', '引用', '链接']    #表头
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去
i = 1  #定义Excel表格的行数，从第二行开始写入，第一行已经写了表头    
for n in range(len(title)): 
    sheet.write(i, 0, title[n].text)
    sheet.write(i, 1, author[n].text)
    sheet.write(i, 2, content[n].text)
    sheet.write(i, 3, company[n].text)
    sheet.write(i, 4, info[n].text)
    sheet.write(i, 5, link[n].get_attribute('href'))    
    i += 1
workbook.save('知网文献汇总.xls')
"""