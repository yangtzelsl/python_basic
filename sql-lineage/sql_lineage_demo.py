from sqllineage.runner import LineageRunner

'''
数据血缘关系梳理工具：
1.开源工具sqllineage
    pip install sqllineage
    写代码
2.在线工具
https://sqlflow.gudusoft.com/#/
'''

sql = """
with invite as
        (
        --邀请人数，
        select user_id

        from amber_apollo_dwd.dwd_qs_user_sub
        where refer_code not in ('', 'null')
        ),

     register as
        (
        select distinct user_id, tags, a.created_time as register_time,
               setting_basecurrency,
               setting_autoconvertpnl,
               setting_enablequickorder,
               setting_enabletsmargin,
               setting_enablefixnegativebalance,
               setting_autocoverloanpledge,
               setting_autoredeemloanpledge    --加入setting相关字段

        from amber_apollo_dws.dws_qs_user_sub a
        left join amber_amp_dwd.dwd_amp_client b on a.user_id = b.client_id
        left join amber_amp_dwd.dwd_amp_client_master c     on c.master_id = b.master_id
        where b.is_delete = 0 and c.is_delete = 0
        ),

     price as   --全部价格按照当天凌晨一点的币价换算
        (
        select coin_name, cast(price as decimal(38,20)) as price, snap_date
        from amber_app_dws.dws_major_price_snap
        ),

     current_price as
        (
        select coin_name, cast(price as decimal(38,20)) as price
        from amber_app_dws.dws_major_price_snap
        where snap_date = to_date(now())
        )

select info.user_id,
       register.register_time,
       register.tags,
       setting_basecurrency,
       setting_autoconvertpnl,
       setting_enablequickorder,
       setting_enabletsmargin,
       setting_enablefixnegativebalance,
       setting_autocoverloanpledge,
       setting_autoredeemloanpledge,
       invite.user_id as invite,
       id,
       event,
       ctime,
       utime,
       exchange,
       algo,
       ratio,
       direction,
       ticker,
       order_size,
       deal_size,
       fee,
       price,
       current_price,
       amount

from register
left join
        (
        --login
        select user_id,
               null as id,
               'login' as event,
               `datetime` as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               null as ticker,
               null as eaas_coin,
               null as order_size,
               1 as deal_size,
               null as fee,
               null as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_login_log


        UNION ALL

        --register
        select a.user_id,
               null as id,
               'register' as event,
               created_time as ctime,
               null as utime,
               null as exchange,
               case when b.type = 1 then 'individual'
                when b.type = 2 then 'institution'
               end as algo,
               null as ratio,
               null as direction,
               null as ticker,
               null as eaas_coin,
               null as order_size,
               1 as deal_size,
               null as fee,
               null as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_user_sub a
        left join amber_apollo_dwd.dwd_qs_kyc_profile b on a.user_id = b.user_id


        UNION ALL

        --KYC_1
        select user_id,
               null as id,
               'KYC_advanced' as event,
               submit_time as ctime,
               null as utime,
               null as exchange,
               case when type = 1 then 'individual'
                when type = 2 then 'institution'
               end as algo,
               null as ratio,
               null as direction,
               null as ticker,
               null as eaas_coin,
               null as order_size,
               1 as deal_size,
               null as fee,
               null as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_kyc_profile
        where kyc1_status = 3


        UNION ALL

        --KYC_2
        select user_id,
               null as id,
               'KYC_fiat' as event,
               submit_time as ctime,
               null as utime,
               null as exchange,
               case when type = 1 then 'individual'
                when type = 2 then 'institution'
               end as algo,
               null as ratio,
               null as direction,
               null as ticker,
               null as eaas_coin,
               null as order_size,
               1 as deal_size,
               null as fee,
               null as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_kyc_profile
        where kyc2_status = 3


        UNION ALL

        --KYC_0
        select user_id,
               null as id,
               'KYC_basic' as event,
               submit_time as ctime,
               null as utime,
               null as exchange,
               case when type = 1 then 'individual'
                when type = 2 then 'institution'
               end as algo,
               null as ratio,
               null as direction,
               null as ticker,
               null as eaas_coin,
               null as order_size,
               1 as deal_size,
               null as fee,
               null as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_kyc_profile
        where kyc0_status = 3


        UNION ALL

        --deposit  待验证内部转账的取数逻辑
        select a.user_id,
               deposit_id as id,
               'deposit' as event,
               last_updated_time as ctime,
               null as utime,
               case when transfer_id is null then 'external'
                when transfer_id is not null and transfer_type in (1, 2) then 'App self'
                when transfer_id is not null and transfer_type in (3, 4) then 'App others'
                when transfer_id is not null and transfer_type = 0 then 'Pro'
               end as exchange,
               null as algo,
               null as ratio,
               null as direction,
               b.coin_name as ticker,
               null as eaas_coin,
               null as order_size,
               case when arrive_amount is null then amount
                when arrive_amount = 0 then amount
                else arrive_amount
               end as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_deposit a
        left join amber_apollo_dwd.dwd_qs_coin b      on a.coin_id = b.coin_id
        left join price                               on b.coin_name = price.coin_name and to_date(a.created_time) = snap_date
        left join current_price                       on b.coin_name = current_price.coin_name
        where a.status = 9


        UNION ALL

        --首次入金
        select a.user_id,
               null as id,
               'first_deposit' as event,
               min(last_updated_time) as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               null as ticker,
               null as eaas_coin,
               null as order_size,
               1 as deal_size,
               null as fee,
               null as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_deposit a
        where a.status = 9
        group by 1


        UNION ALL

        --withdraw
        select user_id,
               withdraw_id as id,
               'withdraw' as event,
               last_updated_time as ctime,
               null as utime,
               case when transfer_id is null then 'external'
                when transfer_id is not null and transfer_type in (1, 2) then 'App self'
                when transfer_id is not null and transfer_type in (3, 4) then 'App others'
                when transfer_id is not null and transfer_type = 0 then 'Pro'
               end as exchange,
               null as algo,
               null as ratio,
               null as direction,
               b.coin_name as ticker,
               null as eaas_coin,
               null as order_size,
               case when arrive_amount is null then amount
                when arrive_amount = 0 then amount
                else arrive_amount
               end as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_withdraw a
        left join amber_apollo_dwd.dwd_qs_coin b      on a.coin_id = b.coin_id
        left join price                               on b.coin_name = price.coin_name and to_date(a.created_time) = snap_date
        left join current_price                       on b.coin_name = current_price.coin_name
        where a.status = 9


        UNION ALL

        --EAAS  下单，取下单日期的frozen coin对应的价格
        select user_id,
               order_id as id,
              'EAAS_order' as event,
               created_time as ctime,
               updated_time as utime,
               split_part(request_exchanges,'"',2) as exchange,
               request_algorithm as algo,
               request_fill_ratio as ratio,
               direction as direction,
               `symbol` as ticker,
               frozen_coin as eaas_coin,
               frozen_amount as order_size,
               null as deal_size,
               null as fee,
               price.price as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_eaas_order_request_details
        left join price                               on frozen_coin = price.coin_name and to_date(created_time) = snap_date


        UNION ALL

        --EAAS成交，取成交日期的时间的quote价格计算成交量
        select user_id,
               order_id as id,
              'EAAS_complete' as event,
               created_time as ctime,
               updated_time as utime,
               split_part(request_exchanges,'"',2) as exchange,
               request_algorithm as algo,
               request_fill_ratio as ratio,
               direction as direction,
               `symbol` as ticker,
               null as eaas_coin,
               frozen_amount as order_size,
               deal_quote_size as deal_size,
               fee as fee,
               price.price as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_eaas_order_request_details
        left join price                               on split_part(`symbol`,'_',2) = upper(price.coin_name)
                                                        and to_date(updated_time) = snap_date
        where status = 4


        UNION ALL

        --EAAS fee，取成交日期的时间的quote价格计算成交量
        select user_id,
               order_id as id,
              'EAAS_fee' as event,
               updated_time as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               `symbol` as ticker,
               null as eaas_coin,
               null as order_size,
               deal_quote_size as deal_size,
               fee as fee,
               price.price as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_eaas_order_request_details
        left join price                               on split_part(`symbol`,'_',2) = upper(price.coin_name)
                                                        and to_date(updated_time) = snap_date
        where status = 4


        UNION ALL

        --treasury subscribe
        select user_id,
               order_id as id,
              'Treasury subscribe' as event,
               ts as ctime,
               arrive_ts as utime,
               null as exchange,
               case when a.product_type = 0 then 'float deposit'
                when a.product_type = 1 then 'fixed deposit'
                when a.product_type = 2 then 'custom deposit'
                when a.product_type = 3 then 'structured dual'
                when a.product_type = 4 then 'PDT fund'
               end as algo,
               null as ratio,
               null as direction,
               b.coin_name as ticker,
               null as eaas_coin,
               amount as order_size,
               amount as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_ts_pos_log a
        left join amber_apollo_dwd.dwd_qs_coin b      on a.coin_id = b.coin_id
        left join price                               on b.coin_name = price.coin_name and to_date(a.ts) = snap_date
        left join current_price                       on b.coin_name = current_price.coin_name
        where direction = 0


         UNION ALL

        --首次理财
        select user_id,
               null as id,
               'first_treasury' as event,
               min(ts) as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               null as ticker,
               null as eaas_coin,
               null as order_size,
               1 as deal_size,
               null as fee,
               null as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_ts_pos_log
        where direction = 0
        group by 1


        UNION ALL

        --treasury redeem
        select user_id,
               order_id as id,
              'Treasury redeem' as event,
               ts as ctime,
               arrive_ts as utime,
               null as exchange,
               case when a.product_type = 0 then 'float deposit'
                when a.product_type = 1 then 'fixed deposit'
                when a.product_type = 2 then 'custom deposit'
                when a.product_type = 3 then 'structured dual'
                when a.product_type = 4 then 'PDT fund'
               end as algo,
               null as ratio,
               null as direction,
               b.coin_name as ticker,
               null as eaas_coin,
               amount as order_size,
               amount as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_ts_pos_log a
        left join amber_apollo_dwd.dwd_qs_coin b      on a.coin_id = b.coin_id
        left join price                               on b.coin_name = price.coin_name and to_date(a.ts) = snap_date
        left join current_price                       on b.coin_name = current_price.coin_name
        where direction = 1


        UNION ALL

        --treasury snap
        select a.user_id,
               order_id as id,
              'Treasury snap' as event,
               c.create_ts as ctime,
               null as utime,
               null as exchange,
               case when a.product_type = 0 then 'float deposit'
                when a.product_type = 1 then 'fixed deposit'
                when a.product_type = 2 then 'custom deposit'
                when a.product_type = 3 then 'structured dual'
                when a.product_type = 4 then 'PDT fund'
               end as algo,
               null as ratio,
               null as direction,
               b.coin_name as ticker,
               null as eaas_coin,
               c.amount as order_size,
               c.amount as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_ts_pos_snapshot c
        left join amber_apollo_dwd.dwd_qs_ts_pos_log a   on c.pos_id = a.pos_id
        left join amber_apollo_dwd.dwd_qs_coin b      on a.coin_id = b.coin_id
        left join price                               on b.coin_name = price.coin_name and to_date(c.create_ts) = snap_date
        left join current_price                       on b.coin_name = current_price.coin_name
        where c.amount <> 0


        UNION ALL

        --treasury fee
        select c.user_id,
               a.id as id,
              'Treasury fee' as event,
               a.ts as ctime,
               null as utime,
               null as exchange,
               case when c.product_type = 0 then 'float deposit'
                when c.product_type = 1 then 'fixed deposit'
                when c.product_type = 2 then 'custom deposit'
                when c.product_type = 3 then 'structured dual'
                when c.product_type = 4 then 'PDT fund'
               end as algo,
               null as ratio,
               null as direction,
               b.coin_name as ticker,
               null as eaas_coin,
               a.amount as order_size,
               a.amount as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_ts_pos_fee_log a
        left join amber_apollo_dwd.dwd_qs_ts_position c on a.pos_id = c.id
        left join amber_apollo_dwd.dwd_qs_coin b      on cast(a.coin_id as integer) = b.coin_id
        left join price                               on b.coin_name = price.coin_name and to_date(a.ts) = snap_date
        left join current_price                       on b.coin_name = current_price.coin_name



UNION ALL

        --treasury pnl
        select c.user_id,
               a.id as id,
              'Treasury pnl' as event,
               a.ts as ctime,
               null as utime,
               null as exchange,
               case when c.product_type = 0 then 'float deposit'
                when c.product_type = 1 then 'fixed deposit'
                when c.product_type = 2 then 'custom deposit'
                when c.product_type = 3 then 'structured dual'
                when c.product_type = 4 then 'PDT fund'
               end as algo,
               null as ratio,
               null as direction,
               b.coin_name as ticker,
               null as eaas_coin,
               a.amount as order_size,
               a.amount as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_ts_pos_pnl_log a
        left join amber_apollo_dwd.dwd_qs_ts_position c on a.pos_id = c.id
        left join amber_apollo_dwd.dwd_qs_coin b      on cast(a.coin_id as integer) = b.coin_id
        left join price                               on b.coin_name = price.coin_name and to_date(a.ts) = snap_date
        left join current_price                       on b.coin_name = current_price.coin_name

        where a.status = 1 and c.product_type in (0,1,2,4)


        UNION ALL

        --借贷
        select user_id,
               id as id,
               'borrow' as event,
               begin_ts as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               ccy as ticker,
               null as eaas_coin,
               null as order_size,
               total_amount as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_bl_position a
        left join price                               on a.ccy = price.coin_name and to_date(a.begin_ts) = snap_date
        left join current_price                       on a.ccy = current_price.coin_name
        where status in (0, 1, 2)


        UNION ALL

        --还款
        select user_id,
               id as id,
               'repay' as event,
               ctime as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               ccy as ticker,
               null as eaas_coin,
               null as order_size,
               amount as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_bl_repay a
        left join price                               on a.ccy = price.coin_name and to_date(a.ctime) = snap_date
        left join current_price                       on a.ccy = current_price.coin_name


        UNION ALL

        --借款利息
        select user_id,
               id as id,
               'bl interest' as event,
               a.ts as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               b.ccy as ticker,
               null as eaas_coin,
               null as order_size,
               a.interest as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_bl_pos_snapshot a
        left join amber_apollo_dwd.dwd_qs_bl_position b    on a.pos_id = b.id
        left join price                               on b.ccy = price.coin_name and to_date(a.ts) = snap_date
        left join current_price                       on b.ccy = current_price.coin_name


        UNION ALL

        --借款仓位
        select user_id,
               id as id,
               'bl snapshot' as event,
               to_date(a.ts) as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               b.ccy as ticker,
               null as eaas_coin,
               null as order_size,
               a.principal as deal_size,
               null as fee,
               price.price as price,
               current_price.price as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_bl_pos_snapshot a
        left join amber_apollo_dwd.dwd_qs_bl_position b    on a.pos_id = b.id
        left join price                               on b.ccy = price.coin_name and to_date(a.ts) = snap_date
        left join current_price                       on b.ccy = current_price.coin_name

        where hour(a.ts) = 23


         UNION ALL

        --trade position
        select a.user_id,
               a.order_id as id,
               'trade' as event,
               a.created_time as ctime,
               null as utime,
               cast(a.status as string) as exchange,    --status = 4为cancelled
               case when a.open_close = '1' then 'open'
                when a.open_close = '2' then 'close'
               end as algo,
               null as ratio,
               null as direction,
               a.contract_name as ticker,
               null as eaas_coin,
               a.quantity as order_size,
               a.filled as deal_size,
               null as fee,
               price.price as price,
               null as current_price,
               filled * avg_price as amount

        from amber_apollo_dwd.dwd_qs_order a
        left join price                               on split_part(a.contract_name,'_',1) = price.coin_name
                                                        and to_date(a.created_time) = snap_date


        UNION ALL

        --trade settle
        select a.user_id,
               a.order_id as id,
               'trade' as event,
               a.created_time as ctime,
               null as utime,
               null as exchange,
               'settle' as algo,
               null as ratio,
               null as direction,
               a.contract_name as ticker,
               null as eaas_coin,
               null as order_size,
               a.quantity as deal_size,
               null as fee,
               null as price,
               null as current_price,
               quantity * price as amount

        from amber_apollo_dwd.dwd_qs_client_trade a
        where type = 3


        UNION ALL

        --funding cost
        select a.user_id,
               a.id as id,
               'funding' as event,
               a.create_time as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               coin_type as ticker,
               null as eaas_coin,
               null as order_size,
               a.venue_amount as deal_size,
               null as fee,
               price.price as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_funding_cost_details a
        left join price                               on lower(coin_type) = price.coin_name
                                                        and to_date(a.create_time) = snap_date
        where coin_type is not null




--         --trade
--         select user_id,
--                transaction_id as id,
--                'trade' as event,
--                created_time as ctime,
--                null as utime,
--                null as exchange,
--                null as algo,
--                null as ratio,
--                null as direction,
--                contract_name as ticker,
--                null as eaas_coin,
--                null as order_size,
--                quantity as deal_size,
--                null as fee,
--                null as price,
--                null as current_price,
--                case when a.quote in ('usd','usdt','pax','usdc') then cast(a.amount as decimal(38,15))
--                else cast(a.amount2 as decimal(38,15))
--                end as amount
--
--         from
--                (
--                select user_id,
--                       order_id,
--                       contract_name,
--                       quantity,
--                       split_part(contract_name,'_',2) as quote,
--                       quantity*a.price as amount,
--                       quantity*a.price*cast(b.price as decimal(20,8)) as amount2,
--                       created_time
--                from amber_apollo_dwd.dwd_qs_client_trade a
--                left join amber_app_dwd.dwd_major_price_snap b on split_part(a.contract_name,'_',2) = coin_name
--                                                                        and to_date(created_time) = date_sub(snap_date,1)
--                where type not in (11,3)
--                ) a


--         UNION ALL
--
--         --首次交易
--         select user_id,
--                null as id,
--                'first_trade' as event,
--                min(created_time) as ctime,
--                null as utime,
--                null as exchange,
--                null as algo,
--                null as ratio,
--                null as direction,
--                null as ticker,
--                null as eaas_coin,
--                null as order_size,
--                1 as deal_size,
--                null as fee,
--                null as price,
--                null as current_price,
--                null as amount
--
--         from amber_apollo_dwd.dwd_qs_client_trade
--         group by 1


        UNION ALL

        --首次交易
        select a.user_id,
               null as id,
               'first_trade' as event,
               min(ctime) as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               null as ticker,
               null as eaas_coin,
               null as order_size,
               1 as deal_size,
               null as fee,
               null as price,
               null as current_price,
               null as amount

        from
        (
        select user_id, ts as ctime from amber_apollo_dwd.dwd_qs_ts_pos_log
        UNION ALL
        select user_id, updated_time as ctime from amber_apollo_dwd.dwd_qs_eaas_order_request_details
        where deal_base_size > 0
        ) a
        group by 1


        UNION ALL

        --首次理财交易
        select a.user_id,
               null as id,
               'first_treasury_trade' as event,
               min(ctime) as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               null as ticker,
               null as eaas_coin,
               null as order_size,
               1 as deal_size,
               null as fee,
               null as price,
               null as current_price,
               null as amount

        from
        (select user_id, created_time as ctime from amber_apollo_dwd.dwd_qs_client_trade
        UNION ALL
        select user_id, ts as ctime from amber_apollo_dwd.dwd_qs_ts_pos_log
        UNION ALL
        select user_id, updated_time as ctime from amber_apollo_dwd.dwd_qs_eaas_order_request_details
        where deal_base_size > 0
        ) a
        group by 1


        UNION ALL

        -- API
        select user_id,
               null as id,
               'API' as event,
               created_time as ctime,
               null as utime,
               null as exchange,
               null as algo,
               null as ratio,
               null as direction,
               null as ticker,
               null as eaas_coin,
               null as order_size,
               1 as deal_size,
               null as fee,
               null as price,
               null as current_price,
               null as amount

        from amber_apollo_dwd.dwd_qs_access_key

        ) info  on register.user_id = info.user_id

left join

invite          on info.user_id = invite.user_id


"""
result = LineageRunner(sql)
print(result)
# 打印result，会产出下面的信息
# Statements(#): 2
# Source Tables:
#    db1.table12
#    db2.table21
#    db2.table22
# Target Tables:
#    db3.table3
# Intermediate Tables:
#    db1.table11

# 也可以直接获取各个源表
for tbl in result.source_tables:
    print(tbl)
# db1.table12
# db2.table21
# db2.table22

# 目标表当然也是可以的
for tbl in result.target_tables:
    print(tbl)
# db3.table13

# 甚至还可以调用matplotlib绘制血缘图
result.draw()
