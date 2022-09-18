import os
import datetime

class MakeFolder:
    def make_active_folder(output_dir, target_year_month):
        """
        フォルダ名とフォルダパスの作成
        output_dir = "data/10_output"
        target_year_month = YYYYMM
        年月_更新日時でフォルダ名を作る
        ex: 202007_20220901_1200
        """
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        target_output_dir_name = target_year_month + "_" + now
        target_output_dir = os.path.join(output_dir, target_output_dir_name)
        os.makedirs(target_output_dir)
        print(target_output_dir)

        return target_output_dir
