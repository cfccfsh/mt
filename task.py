# {"item":(名称,单价,能否使用菜品半价,能否使用满减)}，满减默认30-6
import traceback

MEAL_BASE_INFO_DICT = {"ITEM0001":("黄焖鸡",18,True,True),"ITEM0013":("肉夹馍",6,False,True),"ITEM0022":("凉皮",8,True,True)}

def return_str(show_params_list,off_half_meal_list,off_full_meal_list,off_flag,amount_price,half_price,price_flag):
    head_str = """============= 订餐明细 =============\n"""
    meal_info_str = "\n".join(["{} x {} = {}元\n".format(show_params[0],show_params[1],show_params[1]*show_params[2]) for show_params in show_params_list])
    split_line = """-----------------------------------\n"""
    off_line = ""
    off_meal_str = ""
    split_line_v2 = ""
    if off_flag:
        off_line = """使用优惠："""

        if price_flag==1:
            off_meal_str = """使用优惠:\n满30减6元，省6元\n"""
        elif price_flag==2:
            off_meal_str = """使用优惠:\n指定菜品半价{}，省{}元\n""".format(tuple(off_half_meal_list) if
                                                               len(off_half_meal_list) > 1 else off_half_meal_list[0],half_price)
        split_line_v2 = split_line
    amount_price_line = "总计：{}元\n".format(amount_price)
    end_line = """==================================="""

    show_str = head_str+meal_info_str+split_line+off_line+off_meal_str+split_line_v2+amount_price_line+end_line
    return show_str



def get_params(item):
    base_info_tuple = MEAL_BASE_INFO_DICT[item]

    name = base_info_tuple[0]
    price = base_info_tuple[1]
    is_half = base_info_tuple[2]
    is_full = base_info_tuple[3]

    return name,price,is_half,is_full

def get_amount_price(amount_price,half_price,full_flag,full_price):
    # 是否使用优惠
    off_flag = False
    # 所有商品均满足满减需求
    amount_price_full = amount_price
    amount_price_half = amount_price - half_price

    if half_price:
        off_flag = True
    if full_flag:
        # 总价是否满足满减
        if amount_price >= 30:
            amount_price_full = amount_price - full_price
            off_flag = True

    if amount_price_full == amount_price_half:
        return off_flag,1,amount_price_full
    else:
        if amount_price_full > amount_price_half:
            return off_flag,2, amount_price_half
        else:
            return off_flag,1, amount_price_full


def bestCharge(target_list):
    meal_info_list = [item.split(" ") for item in target_list if item]

    amount_price = 0
    half_price = 0
    full_price = 6  # 满减默认30-6元
    off_full_meal_list = []
    off_half_meal_list = []

    show_params_list = []
    try:
        for meal_info in meal_info_list:
            try:
                item = meal_info[0]
                cnt = int(meal_info[2])
            except IndexError:
                return "服务出现未知错误，请联系管理员"

            name, price, is_half, is_full = get_params(item)

            show_params_list.append((name,cnt,price))

            if name and price:
                # 计算总价
                amount_price += (price*cnt)
                # 计算半价优惠
                if is_half:
                    half_price += (int(price/2)*cnt)
                    off_half_meal_list.append(name)

                # 是否所有商品可使用满减
                if is_full:
                    off_full_meal_list.append(name)

            else:
                return "部分商品不可用"

        # 1---半价菜品，2----满减
        off_flag,price_flag, amount_price_half = get_amount_price(amount_price,half_price,off_full_meal_list,full_price)

        show_str = return_str(show_params_list, off_half_meal_list, off_full_meal_list, off_flag, amount_price_half,half_price,price_flag)
        print(show_str)

    except Exception as e:
        traceback.print_exc()
        print("程序未知错误：{}".format(e))


if __name__ == '__main__':
    target_list = ["ITEM0001 x 1", "ITEM0013 x 2", "ITEM0022 x 1"]
    bestCharge(target_list)