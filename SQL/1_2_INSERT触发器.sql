USE testdemo;

/*
drop trigger get_deliver_records;

DELIMITER $$
CREATE TRIGGER get_deliver_records
BEFORE INSERT
ON df_order_orderinfo
FOR EACH ROW
BEGIN
SElect uaddress FROM df_user_userinfo WHERE id = NEW.user_id INTO @customer_add;
Insert into deliver_deliver(deliver_id, start_add, aim_add, apply_time,status)
VALUES(CONCAT('XS',NEW.oid),'',@customer_add,NEW.odate,0);
END $$
DELIMITER ;
*/

drop trigger get_neworder_records;
DELIMITER $$
CREATE TRIGGER get_neworder_records
AFTER INSERT
ON df_order_orderinfo
FOR EACH ROW
Insert into order_order(order_id, order_price, order_time,customer_id_id,order_status_id)
VALUES(NEW.oid,NEW.ototal,NEW.odate,NEW.user_id, 1)$$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER get_neworderdetail_records
AFTER INSERT
ON df_order_orderdetailinfo
FOR EACH ROW
INSERT INTO order_orderdetail (order_detail_id, detail_num,order_id_id,product_id_id)
VALUES(NEW.id,NEW.count,NEW.order_id,NEW.goods_id)$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER get_product_records
AFTER INSERT
ON df_goods_goodsinfo
FOR EACH ROW
INSERT INTO product_product (product_id, product_name, product_type,product_price)
VALUES(NEW.id,NEW.gtitle,(select ttitle from df_goods_typeinfo where id=NEW.gtype_id),NEW.gprice)$$
DELIMITER ;