def list_split(items, n):
    """
    将输入的列表按照指定数量分割生成二维数组
    :param items: 待分割的列表
    :param n: 每个字列表元素数量
    :return: 分割后的二维数组
    """
    return [items[i:i+n] for i in range(0, len(items), n)]