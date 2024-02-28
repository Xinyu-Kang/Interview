import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 货币代号对照表
CURRENCY_SYMBOL_DICT = {
    "AED": "阿联酋迪拉姆",
    "AUD": "澳大利亚元",
    "BRL": "巴西里亚尔",
    "CAD": "加拿大元",
    "CHF": "瑞士法郎",
    "DKK": "丹麦克朗",
    "EUR": "欧元",
    "GBP": "英镑",
    "HKD": "港币",
    "IDR": "印尼卢比",
    "INR": "印度卢比",
    "JPY": "日元",
    "KRW": "韩国元",
    "MOP": "澳门元",
    "MYR": "林吉特",
    "NOK": "挪威克朗",
    "NZD": "新西兰元",
    "PHP": "菲律宾比索",
    "RUB": "卢布",
    "SAR": "沙特里亚尔",
    "SEK": "瑞典克朗",
    "SGD": "新加坡元",
    "THB": "泰国铢",
    "TRY": "土耳其里拉",
    "TWD": "新台币",
    "USD": "美元",
    "ZAR": "南非兰特"
}

def output_text(currency, rate, datetime):
    """
    打印查询结果至output和result.txt
    """
    result_text = "货币名称：{}\n现汇卖出价：{}\n发布时间：{}".format(currency, rate, datetime)
    f = open("result.txt", "w")
    f.write(result_text)
    f.close()
    print(result_text)
    print("(数据已存入result.txt)")

def main(date, currency):
    """
    查询该货币<currency>在该日期<date>的现货出卖价格
    """
    # 通过WebDriver打开中国银行外汇牌价网站
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.boc.cn/sourcedb/whpj/")

    # 查找页面中日期输入、货币选择和搜索键元素
    date_input = driver.find_element(by=By.XPATH, value='//*[@id="historysearchform"]/div/table/tbody/tr/td[4]/div/input')
    currency_dropdown = driver.find_elements(by=By.TAG_NAME, value='option')
    search_button = driver.find_element(by=By.XPATH, value='//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input')
    
    # 输入日期，选择货币
    date_input.send_keys(date)  
    i = 0
    while i < len(currency_dropdown):
        if currency_dropdown[i].text == currency:
            currency_dropdown[i].click()
        i += 1
    
    # 按搜索键
    search_button.click()

    # 等待搜索完成并取表格第一行的结果
    try:
        first_row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[4]/table/tbody/tr[2]'))
        )
        td_list = first_row.find_elements(by=By.TAG_NAME, value='td')
        rate = td_list[3].text # 现货出卖价格
        datetime = td_list[6].text # 发布时间
        output_text(currency, rate, datetime)
    except:
        print("查询失败")
    driver.quit()
    
            
if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("请输入：日期、货币代号")
    elif (not args[1].isdigit()) or (len(args[1]) != 8):
        print("日期格式错误（正确格式如：20240109）")
    elif args[2] not in CURRENCY_SYMBOL_DICT:
        print("货币<{}>不存在".format(args[2]))
    else:
        date = args[1]
        currency = CURRENCY_SYMBOL_DICT[args[2]]
        main(date, currency)