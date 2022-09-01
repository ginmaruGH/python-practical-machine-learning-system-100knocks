import pandas as pd

class Calc:
    @staticmethod
    def get_rank_df(target_data, m_store) -> pd.DataFrame:
        """
        本部用レポートデータ
        店舗データの作成
        売上総額の集計
        ランキングデータフレームの返却
        """
        tmp = target_data.loc[target_data["status"].isin([1, 2])]
        rank = tmp.groupby(["store_id"])[
            "total_amount"].sum().sort_values(ascending=False)
        rank = pd.merge(rank, m_store, on="store_id", how="left")

        return rank

    @staticmethod
    def get_cancel_rank_df(target_data, m_store):
        """
        本部用レポートデータ
        店舗データの作成
        キャンセル率の計算
        ランキングデータフレームの返却
        """
        cancel_df = pd.DataFrame()
        cancel_cnt = target_data.loc[target_data["status"] == 9]\
            .groupby(["store_id"])["store_id"].count()
        order_cnt = target_data.loc[target_data["status"]\
                                    .isin([1, 2, 9])].groupby(["store_id"])["store_id"].count()
        cancel_rate = (cancel_cnt / order_cnt) * 100
        cancel_df["cancel_rate"] = cancel_rate
        cancel_df = pd.merge(cancel_df, m_store, on="store_id", how="left")
        cancel_df = cancel_df.sort_values("cancel_rate", ascending=True)

        return cancel_df

    def get_store_rank(target_id, target_df, m_store):
        """
        店舗用レポートデータ
        該当の店舗の売上ランクの返却
        """
        rank = Calc.get_rank_df(target_df, m_store)
        store_rank = rank.loc[rank["store_id"] == target_id].index + 1

        return store_rank[0]

    def get_store_sale(target_id, target_df, m_store):
        """
        該当店舗の売上データの返却
        """
        rank = Calc.get_rank_df(target_df, m_store)
        store_sale = rank.loc[rank["store_id"] == target_id]["total_amount"]

        return store_sale

    def get_store_cancel_rank(target_id, target_df, m_store):
        """
        店舗用レポートデータ
        該当の店舗のキャンセル率ランクの返却
        """
        cancel_df = Calc.get_cancel_rank_df(target_df, m_store)
        cancel_df = cancel_df.reset_index()
        store_cancel_rank = cancel_df.loc[cancel_df["store_id"] == target_id].index + 1

        return store_cancel_rank[0]

    def get_store_cancel_count(target_id, target_df):
        """
        該当店舗のキャンセル数の返却
        """
        store_cancel_count = target_df.loc[
            (target_df["status"] == 9) & (target_df["store_id"] == target_id)
        ].groupby("store_id")["store_id"].count()

        return store_cancel_count

    @staticmethod
    def get_delivery_rank_df(target_id, target_df, m_store):
        """
        該当店舗の「配達完了までの時間」の平均
        """
        delivery = target_df.loc[target_df["status"] == 2]
        delivery_delta = delivery.groupby(["store_id"])["delta"].mean().sort_values()
        delivery_delta = pd.merge(delivery_delta, m_store, on="store_id", how="left")

        return delivery_delta

    def get_store_delivery_rank(target_id, target_df, m_store):
        """
        該当の店舗の配達完了までの時間」ランクの返却
        """
        delivery_rank = Calc.get_delivery_rank_df(target_id, target_df, m_store)
        store_delivery_rank = delivery_rank.loc[
            delivery_rank["store_id"] == target_id].index + 1

        return store_delivery_rank[0]
