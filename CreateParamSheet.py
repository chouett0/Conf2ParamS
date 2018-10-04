#encoding: utf-8

# ライブラリのインポート
import csv
import os
import sys
import re
import openpyxl

# 使用方法を表示する際のテンプレート
_USAGE = """
Usage: python CreateParamSheet.py [Target Directories]

"""

# コンフィグを解析するための関数を定義したクラス
class ParseConfig:
  # 初期化を行うインストラクタ
  # self         : クラス内で同クラスの要素へアクセスするための要素(おまじない)
  # BasePath     : コンフィグファイルの格納されているディレクトリ名
  # CommandValue : 出力するコマンドのList
  # SubCommValue : 出力する詳細コマンドのList
  def __init__(self, BasePath, CommandValue, SubCommValue):
    self.BasePath         = BasePath
    self.CommandValue     = CommandValue
    self.SubCommValue     = SubCommValue
    self.ConfCommandDict  = {}
    self.ConfSubCommDict  = {}
  
  # 指定したディレクトリ内のファイルをListで返す関数
  # dirname: ファイルを走査するディレクトリ名,デフォルトはBasePathディレクトリ内
  #
  # return: ディレクトリ内のファイル一覧をListで返却
  def getDir(self, dirname=""):
    # 「path=」に対して与えている値からディレクトリ内のファイル名をListで取得
    # dirnameに任意のフォルダ名を与えるとそのディレクトリが,与えなければデフォルトはBasePathディレクトリのみ走査
    dir = os.listdir(path=self.BasePath + dirname)
    return dir

  # CommandValueで指定されたコマンドをKeyとした空の連想配列を生成
  def createDict(self ):
        for row in self.CommandValue:
              self.ConfCommandDict[row] = []

  # コンフィグファイルの読み込みを行う関数
  # filename: コンフィグファイルのファイル名
  #
  # return: コンフィグファイルを読み込んだ内容をListとして返却
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
    try:
      # 出力を行う要素をKeyとした連想配列の生成
      self.createDict()

      # 読み込んだファイルのListのサイズ
      eof = len(config)

      # コマンド内容を一時保存する変数
      command = ""
      
      # 詳細コマンドを一時保存する変数
      sub_comm = ""

      # 一行ずつ読み込み
      for i in range(0, eof):
        # '!' である場合は除外
        if (not ('!' in config[i])):
              # 先頭が空白ではない場合はコマンド、空白である場合は詳細コマンド
              if (not ( ' ' in config[i][0])):
                # Command
                # 一度コマンドを空白区切りでList化
                c = config[i].split(" ")

                # 先頭がipの場合はその次の要素もDictのKeyとして利用、異なる場合はそのままKeyに利用
                if ( "ip" in c[0]):
                      # Keyとして格納
                      command = c[0] + " " + c[1]

                      # 必要がないのでListから除外
                      c.pop(0)
                      c.pop(0)

                else:
                      # Keyとして格納
                      command = c[0]
                      # Listから除外
                      c.pop(0)

                # Keyに利用した情報を省いたものから更に末尾2文字(改行文字と空白)を消去して文字列に戻す
                sub_comm = ' '.join(c)[:-2]

                # 取得したいコマンドであれば情報をDictに格納し、それ以外は無視
                if (command in self.CommandValue):
                      self.ConfCommandDict[command].append(sub_comm)

                else:
                      continue

              else:
                # Sub
                # コマンド名のKeyを持ったDictが存在しない場合は新たに生成する
                if (not (sub_comm in self.ConfSubCommDict.keys())):
                      self.ConfSubCommDict[sub_comm] = []

                # コマンドと詳細コマンドの紐づけを行う(コマンド名をKeyとして詳細コマンドをvalueとする)
                self.ConfSubCommDict[sub_comm].append(config[i][2:-2])
     
     # デバッグ用 ##################################################################
      """      
      for key, value in self.ConfOrderDict.items():
            print("Key: ", key)
            for row in value:
              print("\tValue: ", row)
              if (not (row in self.ConfSubDict.keys())):
                    continue
              for r in self.ConfSubDict[str(row)]:
                    print("\t\t", r)
      """
      #############################################################################

    except Exception as e:
      print("[!] Read Config Error:", e)
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

    return self.ConfCommandDict, self.ConfSubCommDict

# main関数
def main():
  # 引数を与えて実行しているかの確認,適切に実行してない場合は使用方法を表示して終了
  if (len(sys.argv) < 2):
    print(_USAGE)
    exit(1)

#  CommandValue = ["hostname", "interface", "ip route", "ip access-list", "ntp"]
  CommandValue = ["hostname", "interface"]
  SubCommValue = ["address", "switchport", "shutdown", "mdi"]


  # 引数に初期化用の情報を与えてParseConfigのインスタンス作成
  filepath = sys.argv[1]
  pc = ParseConfig(filepath, CommandValue, SubCommValue)

  # コンフィグファイルリストの取得
  files = pc.getDir()

  print("[*] Dumping config to Excel File...")
  # ファイルを一つずつ処理
  for file in files:
      print("Start dump config: %s" % file)

      # コンフィグ情報の連想配列の取得
      Command, SubComm = pc.getConfig(file)

      wb = openpyxl.Workbook()
      ws = wb.active

      wb.titile = "Parameter"

      for comm_key, comm_val in Command.items():
            print("comm_key: ", comm_key)

            if (comm_key is "hostname"):
                  hostname = ws["B1"]
                  hostname.font = openpyxl.styles.Font(size=20)
                  hostname.value = comm_val[0][1:-1]
                  ws.append([""])
                  continue

            if (comm_key is "interface"):
                  ws.append(["インターフェース情報"])
                  ws.append(["ポート", "speed", "duplex", "mdi", "shatdown", "モード", "vlanID"])

                  for row in comm_val:
                        print("port : ", row)
                        line = [row]
                        if (not (row in SubComm.keys()) or ("vlan" in row)):
                              ws.append(line)
                              continue

                        # speed
                        try:
                              line.extend([re.search('(auto|\d{2,4})', [value for value in SubComm[str(row)] if re.match('speed (\w+)$', value)][0]).group(0)])
                        except:
                              line.append("")

                        # duplex
                        try:
                              line.extend([re.search("(full|half|auto)", [value for value in SubComm[str(row)] if re.match("duplex (\w{4})", value)][0]).group(0)])
                        except:
                              line.append("")

                        # MDI/MDIX
                        line.append("mdi" if "no " in [value for value in SubComm[str(row)] if re.search(".*(mdix auto)", value)] else "mdix")

                        # shutdown
                        line.append("shutdown" if "shutdown" in SubComm[str(row)] else "")

                        # VLAN mode
                        line.extend([re.search("(access|trunk|stack)$", [value for value in SubComm[str(row)] if re.match('.*(access|trunk|stack)$', value)][0]).group(0)])

                        # VLANID
                        try:
                              line.extend([re.search("\d{1,3}([,]|[-])*(\d{1,3}([,]|[-])*)+", [value for value in SubComm[str(row)] if re.match("switchport (access vlan |trunk allowed vlan ).*", value)][0]).group(0)])
                        except:
                              line.append("")

#                        print(line)
                        ws.append(line)

      wb.save(".\\Result\\" + file[:-3] + "xlsx")

if __name__ == "__main__":
  main()