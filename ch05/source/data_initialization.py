# データの初期化を行うファイル

import pandas as pd

class Initialize:

    @staticmethod
    def calc_delta(t):
        """
        配達完了時間までの時間を計算する
        返す値は単位（分）
        """
        t1, t2, = t
        delta = t2 - t1
        delta = delta.total_seconds() / 60
        return delta

    def init_tran_df(
            target_df: pd.DataFrame,
            m_store: pd.DataFrame,
            m_area: pd.DataFrame
        ) -> pd.DataFrame:
        """"""
        # 保守用店舗データの削除
        target_df = target_df.loc[target_df["store_id"] != 999]

        # データフレームの結合（ジョイン）
        target_df = pd.merge(target_df, m_store, on="store_id", how="left")
        target_df = pd.merge(target_df, m_area, on="area_cd", how="left")

        # マスタデータにないコードに対応した文字列の設定
        # ["takeout_name"]の追加
        target_df.loc[target_df["takeout_flag"] == 0, "takeout_name"] = "デリバリー"
        target_df.loc[target_df["takeout_flag"] == 1, "takeout_name"] = "お持ち帰り"
        # ["status_name"]の追加
        target_df.loc[target_df["status"] == 0, "status_name"] = "受付"
        target_df.loc[target_df["status"] == 1, "status_name"] = "お支払済"
        target_df.loc[target_df["status"] == 2, "status_name"] = "お渡し済"
        target_df.loc[target_df["status"] == 9, "status_name"] = "キャンセル"

        # ["order_date"]の追加
        target_df.loc[:, "order_date"] = pd.to_datetime(target_df["order_accept_date"]).dt.date

        # 配達完了までの時間を計算
        target_df.loc[:, "order_accept_datetime"] = pd.to_datetime(target_df["order_accept_date"])
        target_df.loc[:, "delivered_datetime"] = pd.to_datetime(target_df["delivered_date"])
        target_df.loc[:, "delta"] = target_df[["order_accept_datetime", "delivered_datetime"]]\
            .apply(Initialize.calc_delta, axis=1)

        return target_df
