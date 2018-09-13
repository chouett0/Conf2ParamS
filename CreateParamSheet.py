#encoding: utf-8

# ライブラリのインポート
import csv
import os
import sys

# 使用方法を表示する際のテンプレート
_USAGE = """
Usage: python CreateParamSheet.py [Target Directories]

"""

# コンフィグを解析するための関数を定義したクラス
class ParseConfig:
  # 初期化を行うインストラクタ
  # self        : クラス内で同クラスの要素へアクセスするための要素(おまじない)
  # BasePath    : コンフィグファイルの格納されているディレクトリ名
  # OutputValue : 出力する要素のList
  def __init__(self, BasePath, OutputValue):
    self.BasePath     = BasePath
    self.OutputValue  = OutputValue
  
  # 指定したディレクトリ内のファイルをListで返す関数
  # dirname: ファイルを走査するディレクトリ名,デフォルトはBasePathディレクトリ内
  def getDir(self, dirname=""):
    # 「path=」に対して与えている値からディレクトリ内のファイル名をListで取得
    # dirnameに任意のフォルダ名を与えるとそのディレクトリが,与えなければデフォルトはBasePathディレクトリのみ走査
    dir = os.listdir(path=self.BasePath + dirname)
    return dir

  # コンフィグファイルの読み込みを行う関数
  # filename: コンフィグファイルのファイル名
  def readConfig(self, filename):
    # ファイルの読み込み
    f = open(self.BasePath + filename, "r")
    # ファイル全体を行単位で読み込んでList化
    config = f.readlines()
    # 後処理
    f.close()
    return config

  # コンフィグをブロック単位の連想配列に変換する関数
  # config: コンフィグファイルのList化済みデータ
  def conf2block(self, config):
    Blocks = {}
    for BlocksIndex in self.OutputValue:
      Blocks[BlocksIndex] = []

    try:

      # データを一行ずつ読み込んで処理を行う
      for i in range(0, len(config)):
        if (config[i][:1] is not "  " and !("!" in config[i]):
          if (config[i+1][0] is not "  "):
            conf = config.split(" ")
            if (conf[0] in Blocks.keys()):
              del conf[0]
              value = " ".join(conf)
              if (len(value) > 1):
                
              else:
                Block[]

    except Exception as e:
      print"[!] Read Config Error:", e
      exit(1)

  # コンフィグをインターフェースやACL単位の連想配列として取得
  def getConfig(self, filename):
    # コンフィグファイルの読み込み
    config = self.readConfig(filename)

    # コンフィグファイルの先頭の余分な情報を削除
    while ( (config[0].find("hostname") )):
      del config[0]

    # 取得したコンフィグ情報を連想配列に変換
    ConfBlock = self.conf2block(config)

#    return ConfBlock

# main関数
def main():
  # 引数を与えて実行しているかの確認,適切に実行してない場合は使用方法を表示して終了
  if (len(sys.argv) < 2):
    print(_USAGE)
    exit(1)

  OutputValue = ["hostname", "vlan", "interface", "route", "access-list", "snmp-server", "logging", "ntp"]

  # 引数に初期化用の情報を与えてParseConfigのインスタンス作成
  pc = ParseConfig(sys.argv[1], OutputValue)

  # コンフィグファイルリストの取得
  files = pc.getDir()

  print("[*] Dumping config to CSV...")
  # ファイルを一つずつ処理
  for file in files:
      print("Start dump config: %s" % file)

      output = []
      # コンフィグ情報の連想配列の取得
      ConfBlock = pc.getConfig(file)
      """
      with open("ParamSheet.csv", "r") as f:
        writer = csv.writer()
        
        for i in range(0, len(OutputValue)):
          level = 0
          writer.writerow(OutputValue[i])

          for node in ConfBlock:
            op = [""]
            for ()

          writer.writerow()
      """

if __name__ == "__main__":
  main()