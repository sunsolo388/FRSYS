USE testdemo;

CREATE TEMPORARY TABLE t1 AS(
    SELECT SUM(price*count) AS order_price, order_id FROM df_order_orderdetailinfo GROUP BY order_id);
        
INSERT INTO order_order (order_id, order_price, order_time,customer_id_id,deliver_id,order_status_id)
SELECT oid AS order_id, 
order_price,
odate AS order_time, 
user_id AS customer_id_id,
order_id AS deliver_id,
1
FROM df_order_orderinfo, t1
WHERE oid = t1.order_id;

select * from df_order_orderinfo;
select * from order_order; 

CREATE TEMPORARY TABLE t2 AS(
    SELECT df_goods_goodsinfo.id, gtitle, gtype_id,ttitle, gprice FROM df_goods_goodsinfo,df_goods_typeinfo
    WHERE df_goods_goodsinfo.gtype_id = df_goods_typeinfo.id);
     
INSERT INTO product_product (product_id, product_name, product_type,product_price)
SELECT id AS product_id, 
gtitle AS product_name, 
ttitle AS product_type,
gprice AS product_price
FROM t2 where id not in (select product_id from product_product);

CREATE TEMPORARY TABLE t3 AS(
    SELECT id, count,price, goods_id,order_id FROM df_order_orderdetailinfo);

select * from t3;
INSERT INTO order_orderdetail (order_detail_id, detail_num,order_id_id,product_id_id)
SELECT id, 
count, 
order_id,
goods_id
FROM t3;
