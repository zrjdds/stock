# coding:utf-8

from Test.stockholm import Stockholm
from Test.option import *
import os


def checkFoldPermission(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            txt = open(path + os.sep + "test.txt", "w")
            txt.write("test")
            txt.close()
            os.remove(path + os.sep + "test.txt")

    except Exception as e:
        print(e)
        return False
    return True


def main():
    args = parser.parse_args()
    if not checkFoldPermission(args.store_path):  # 检测是否具有读写存储文件的权限
        print('\n没有文件读写权限: %s' % args.store_path)
    else:
        print('股票数据爬虫和预测启动...\n')
        stockh = Stockholm(args)  # 初始化参数
        stockh.run()  # 启动
        print('股票数据爬虫和预测完成...\n')


if __name__ == '__main__':
    main()