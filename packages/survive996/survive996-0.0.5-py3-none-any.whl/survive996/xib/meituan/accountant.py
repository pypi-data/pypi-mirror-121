# -*- coding: UTF-8 -*-
import pandas as pd
from functools import reduce
from spongebox.timebox import timeit
import spongebox.iobox
from abc import ABCMeta, abstractmethod
from survive996.xib.meituan.datareader import read_plaintext
from survive996.xib.meituan.metadata.trade import metadata

pd.set_option("display.float_format", lambda x: "%.2f" % x)


class Accountant(metaclass=ABCMeta):

    # def __init__(self, product: Product):
    def __init__(self, product, data_reader):
        """
        Parameters
        ----------
        product:mtf,mtl or mtf
        data_reader:DataFrame or TextFileReader
        """
        self.product = product
        self.data_reader = data_reader
        self.SUBJECT_COL = "subject_code"
        self.DIRECT_COL = "direct"
        self.TRADE_TYPE_COL = "trade_type"
        self.AMOUNT_COL = "amount"
        self.trades = metadata[self.product]

    @abstractmethod
    def check(self, chunk):
        pass

    @abstractmethod
    def merge(self, x, y):
        pass

    @abstractmethod
    def extend(self, rs):
        pass

    @abstractmethod
    def normalize(self, _):
        return _

    def display(func):
        def wrap(*args, **kwargs):
            _ = func(*args, **kwargs)
            print("output",_.shape)
            print(_)
            return _

        return wrap

    @timeit
    @display
    def accounting(self):
        _ = reduce(self.merge, map(self.check, self.data_reader))
        # print(_)
        _ = self.extend(_)
        # print(_)
        return self.normalize(_)


class AccountantV2(Accountant):

    def check(self, chunk):
        print("process chunk {}-{}".format(chunk.iloc[0].name, chunk.iloc[-1].name))
        chunk[self.AMOUNT_COL] = chunk[self.AMOUNT_COL] / 100
        return chunk.groupby([self.SUBJECT_COL, self.DIRECT_COL, self.TRADE_TYPE_COL]).sum().reset_index()

    def merge(self, x, y):
        return pd.concat([x, y], sort=False).groupby([self.TRADE_TYPE_COL, self.SUBJECT_COL, self.DIRECT_COL]).sum().reset_index()

    def extend(self, rs):
        self.trades = pd.DataFrame(metadata[self.product], columns=metadata["cols"])
        df_C = pd.merge(rs[rs[self.DIRECT_COL] == "C"], self.trades, left_on=[self.TRADE_TYPE_COL, self.SUBJECT_COL], right_on=["trade", "sub_C"])
        # print(rs[rs[self.DIRECT_COL] == "C"])
        df_D = pd.merge(rs[rs[self.DIRECT_COL] == "D"], self.trades, left_on=[self.TRADE_TYPE_COL, self.SUBJECT_COL], right_on=["trade", "sub_D"])
        # print(rs[rs[self.DIRECT_COL] == "D"])
        _ = pd.concat([df_C, df_D])
        print("group:", rs.shape, "extend:", _.shape)
        return _

    def normalize(self, _):
        _ = _.pivot("trade_full_text", self.DIRECT_COL, self.AMOUNT_COL)
        _["diff"] = _.iloc[:, 0] - _.iloc[:, 1]
        ifsp = pd.merge(_.reset_index(), self.trades)
        ifsp.sort_values(["acc_C", "acc_D", "C"], ascending=True, inplace=True)
        return ifsp["trade_full_text,acc_C,acc_D,C,D,diff".split(",")]


class AccountantV1(Accountant):

    def check(self, chunk):

        def check_single_subject(trade):
            trade_type, subject_code_D, subject_code_C, trade_full_text = trade[0], trade[1], trade[2], trade[-1]
            # 核算借方科目
            C_1 = chunk[(chunk.trade_type == trade_type) & (
                    chunk.subject_code == subject_code_D) & (chunk.direct == "C")]["amount"].sum()
            D_1 = chunk[(chunk.trade_type == trade_type) & (
                    chunk.subject_code == subject_code_D) & (chunk.direct == "D")]["amount"].sum()
            _D = D_1 - C_1
            # 核算贷方科目
            C_2 = chunk[(chunk.trade_type == trade_type) & (
                    chunk.subject_code == subject_code_C) & (chunk.direct == "C")]["amount"].sum()
            D_2 = chunk[(chunk.trade_type == trade_type) & (
                    chunk.subject_code == subject_code_C) & (chunk.direct == "D")]["amount"].sum()
            _C = D_2 - C_2
            return {trade_full_text: [_D / 100, _C / 100]}

        return reduce(self.merge, map(check_single_subject, self.trades))

    def merge(self, x, y):
        for y_key in y:
            if y_key in x:
                x[y_key] = [i + j for i, j in zip(x[y_key], y[y_key])]
            else:
                x[y_key] = y[y_key]
        return x

    def extend(self, rs):
        for key in rs:
            for trade in self.trades:
                if key == trade.trade_full_text:
                    rs[key].extend([trade.acc_D, trade.acc_C])
                    break
        return rs

    def normalize(self, _):
        def ext_and_return(l, l1):
            l.extend(l1)
            return l

        _ = [ext_and_return([key], _[key]) for key in _]
        _ = pd.DataFrame(_, columns="trade_full_text,D,C,acc_D,acc_C".split(","))
        _["diff"] = _["D"] + _["C"]
        _.sort_values(["acc_C", "acc_D", "D"], ascending=True, inplace=True)
        return _["trade_full_text,acc_C,acc_D,D,C,diff".split(",")][_.D != 0]


if __name__ == "__main__":
    prd, path = "mtf", "C:\\Users\\LuoJi\\Desktop\\2021-09-23\\subject_detail_20210923"
    _ = AccountantV1(prd, read_plaintext(path, prd, chunk_size=10000)).accounting()
    print("*"*500)
    _ = AccountantV2(prd, read_plaintext(path, prd, chunk_size=10000)).accounting()
