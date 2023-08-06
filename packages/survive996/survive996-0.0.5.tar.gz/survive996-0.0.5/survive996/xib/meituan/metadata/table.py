import copy

__common__ = {
    "bank_loan_create": "借据ID,账户ID,借据编号,银行卡号,银行名称,放款业务流水号,借据类型,利率,利息周期,罚息率,罚息周期,贷款总本金,贷款期限,还款方式,还款间隔,总期数,贷款起息日,借款日,贷款到期日,借据状态,结清日期,借据余额,已计划本金,未计划本金,本金桶余额,利息桶余额,罚息桶余额,费用桶余额,应还本金,应还利息,应还罚息,应还费用,已还本金,已还利息,已还罚息,已还费用,逾期天数,逾期等级,版本,数据生成时间,数据更新时间,债权方比例,申请授信件编号,借款用途,放款渠道".split(","),
    "bank_period_create": "期数单ID,借据ID,期数单状态,计划项还款日,实际还款日,逾期等级,逾期天数,期数单余额,本金桶余额,利息桶余额,罚息桶余额,费用桶余额,应还本金,应还利息,应还罚息,应还费用,已还本金,已还利息,已还罚息,已还费用,数据生成时间,数据更新时间,版本".split(","),
    "bank_repay_loan": "业务流水号,借款编号,借款ID,还款银行卡号,还款银行卡银行名称,还款业务流水号,还款类型,还款日期,总金额（单位分）,本次实还本金金额（单位分）,本次实还利息金额（单位分）,本次实还逾期本金罚息金额（单位分）,本次实还费用金额（单位分）,交易发生时间,入账状态".split(","),
    "bank_repay_period": "业务流水号,借款编号,借款ID,期数单ID,还款类型,还款日期,总金额（单位分）,本次实还本金金额（单位分）,本次实还利息金额（单位分）,本次实还逾期本金罚息金额（单位分）,本次实还费用金额（单位分）,交易发生时间".split(","),
    "bank_loan_init": "借据ID,账户ID,借据编号,借据类型,利率,利息周期,罚息率,罚息周期,贷款总本金,贷款期限,还款方式,还款间隔,总期数,贷款起息日,借款日,贷款到期日,借据状态,结清日期,借据余额,已计划本金,未计划本金,本金桶余额,利息桶余额,罚息桶余额,费用桶余额,应还本金,应还利息,应还罚息,应还费用,已还本金,已还利息,已还罚息,已还费用,逾期等级,逾期天数,版本,数据生成时间,数据更新时间,债权方比例,正常本金余额,逾期本金余额,正常利息余额,逾期利息余额,逾期本金罚息余额,停息停费状态,核销标识".split(","),
    "bank_instmnt_init": "期数单ID,借据ID,借据编号,期数单状态,计划项还款日,实际还款日,逾期等级,逾期天数,期数单余额,本金桶余额,利息桶余额,罚息桶余额,费用桶余额,应还本金,应还利息,应还罚息,应还费用,已还本金,已还利息,已还罚息,已还费用,数据生成时间,数据更新时间,版本".split(","),
    "subject_detail": "entry_id,fiscal_date,account_no,account_name,loan_id,debit_no,subject_code,subject_name,direct,amount,balance_direct,balance,tran_jrnl_id,remark,id,trade_type".split(","),
    "zx_detail": "type,bank_id,loan_type1,loan_type2,loan_no,loan_place,issue_date,due_date,loan_acct,loan_amount1,loan_amount2,max_debt,gty_main_method,return_freq,return_term,resi_term,curr_return_date,lately_return_date,curr_return_amount,fact_return_amount,loan_balance,passed_terms,passed_amount,passed_31_60due,passed_61_90due,passed_91_180due,passed_180due,accum_default,max_passed_terms,loan_form5,loan_status,return_status_24m,passed_180due2,cus_status,per_name,id_type,id_no,yuliu,typ2,sex,dob,marriage_status,education,degree,family_phone,mobile_phone,com_tel,email,address,zip_code,household_place,mate_name,mate_id_type,mate_id_no,mate_com_name,mate_phone,type3,occupation,com_name,com_field,com_address,com_zip_code,start_date,job_title,certification,income,sal_acc_id,sal_bank_id,type4,cur_address,cur_zip_code,abode_status".split(
        ",")
}
metadata = {
    "mtf": __common__,
    "mtl": __common__,
    "mtm": {
        "bank_loan_init": "借据号,客户号,借据类型,借据状态,核销状态,贷款起息日,贷款到期日,结清日期,贷款期限,贷款总本金,正常本金余额,逾期本金余额,正常利息余额,逾期利息余额,逾期罚息余额,逾期等级,逾期天数".split(","),
        "bank_instmnt_init": "借据号,期数单编号,借据状态,计划项账单日,计划项还款日,结清日期,应收本金,应收利息,应收罚息,已还本金,已还利息,已还罚息,本金余额,利息余额,罚息余额,逾期等级,逾期天数".split(","),
        "bank_loan_create": "客户号,借据号,交易流水号,放款金额,借据类型,贷款用途,内部结转标识,分期手续费率,罚息率,还款方式,贷款期限,放款入账时间,贷款到期日,授信编号,出资比例".split(","),
        "bank_repay_period": "客户号,借据号,交易流水号,期数单号,还款类型,还款日期,总金额（单位分）,本次实还正常本金（单位分）,本次实还正常利息金额（单位分）,本次实还逾期罚息金额（单位分）,本次实还逾期本金（单位分）".split(","),
        "bank_repay_loan": "客户号,借据号,交易流水号,还款银行卡号,还款银行卡银行名称,还款类型,还款日期,总金额（单位分）,本次实还正常本金（单位分）,本次实还正常利息金额（单位分）,本次实还逾期罚息金额（单位分）,本次实还逾期本金（单位分）,交易发生时间,内部结转标识,入账状态".split(","),
        "bank_accounting": "放款总本金,还款本金-正常,还款利息-正常,还款本金-逾期,还款利息-逾期,还款罚息-逾期,还款已核销本金,还款已核销利息,还款已核销罚息,结计本金-正常,结计利息-正常,结计罚息-正常,结计本金-M4以上,结计利息-M4以上,结计罚息-M4以上,本金应计转非应计,利息应计转非应计,罚息应计转非应计,本金非应计转应计,利息本金非应计转应计,罚息本金非应计转应计,减免利息-正常,减免利息-逾期,减免罚息-正常,正常本金转逾期本金,正常利息转逾期利息,核销本金,核销利息,核销罚息".split(","),
        "fund_fee": "借据号,本金余额,贴息费率,贴息发生额".split(","),
        "subject_detail": "entry_id,fiscal_date,account_no,account_name,loan_id,debit_no,subject_code,subject_name,direct,amount,balance_direct,balance,tran_jrnl_id,remark,id,trade_type".split(",")
    },
    "dtype": {
        "loan_id": str,
        "借据ID": str,
        "debit_no": str,
        "借据号": str,
        "借据编号": str,
        "期数单ID": str,
        "期数单号": str,
        "期数单编号": str,
        "客户号": str,
        "账户ID": str,
        "交易流水号": str,
        "银行卡号": str,
        "还款银行卡号": str,
        "授信编号": str,
        "subject_code": str
    }
}
