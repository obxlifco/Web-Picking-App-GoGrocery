from django.shortcuts import render

from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# Import Model And Serializer
from webservices.models import *
from coremodule.coremodule_serializers import *
from coremodule.views.product import discount
# from coremodule.comm
# from coremodule.views import common_function


import json
import base64

class place_order(generics.ListAPIView):

    def post(self, request, *args, **kwargs):

		$website_id = $this->get_company_website_id_by_url();
		$company_id = $this->get_company_id_by_url();
		$CartTotal=0;
		$return_data = array();
		if($this->request->is('post')) {
			$device_id 				= isset($this->request->data['device_id'])?$this->request->data['device_id']:'';
			$user_id 				= isset($this->request->data['user_id'])?$this->request->data['user_id']:'';
			$address_book_id 		= isset($this->request->data['address_book_id'])?$this->request->data['address_book_id']:'';
			$time_slot_date 		= isset($this->request->data['time_slot_date'])?$this->request->data['time_slot_date']:'';
			$time_slot_time 		= isset($this->request->data['time_slot_time'])?$this->request->data['time_slot_time']:'';
			$special_instruction 	= isset($this->request->data['special_instruction'])?$this->request->data['special_instruction']:'';
			$coupon_code 			= isset($this->request->data['coupon_code'])?$this->request->data['coupon_code']:'';
			$time_slot_id 			= isset($this->request->data['time_slot_id'])?$this->request->data['time_slot_id']:'';
			$referal_code 			= isset($this->request->data['referal_code'])?$this->request->data['referal_code']:'';
			$otp_type 				= isset($this->request->data['otp_type'])?$this->request->data['otp_type']:'';
		} else {
			$device_id 				= isset($this->params['url']['device_id'])?$this->params['url']['device_id']:'';
			$user_id 				= isset($this->params['url']['user_id'])?$this->params['url']['user_id']:'';
			$address_book_id 		= isset($this->params['url']['address_book_id'])?$this->params['url']['address_book_id']:'';
			$time_slot_date 		= isset($this->params['url']['time_slot_date'])?$this->params['url']['time_slot_date']:'';
			$time_slot_time 		= isset($this->params['url']['time_slot_time'])?$this->params['url']['time_slot_time']:'';
			$special_instruction 	= isset($this->params['url']['special_instruction'])?$this->params['url']['special_instruction']:'';
			$coupon_code 			= isset($this->params['url']['coupon_code'])?$this->params['url']['coupon_code']:'';
			$time_slot_id 			= isset($this->params['url']['time_slot_id'])?$this->params['url']['time_slot_id']:'';
			$referal_code 			= isset($this->params['url']['referal_code'])?$this->params['url']['referal_code']:'';
			$otp_type 				= isset($this->params['url']['otp_type'])?$this->params['url']['otp_type']:'';
		}
		$warehouse_id = '';
		// otp_type = // COD => Cash on delivery // CROD => Card on delivery // CRDC = > Credit Card // DBCRD = > Debit Card // NBK => Net Banking
		$fulfillment_id 		= $this->get_fullfilment_id($referal_code);
		$applied_coupon_code 	= '';
		$cart_discount 			= 0;
		$discount_amount 		= 0;
		$net_promotion_discount = 0;
		$address_cond 			= "CustomersAddressBook.id = {$address_book_id} ";
		$address_data 			= $this->CustomersAddressBook->find('first',array('conditions'=>$address_cond));
		$product_data 			= $this->preview_cart_checkout($device_id,$user_id);

		$CartTotal 				= $product_data['Shipping']['order_amount'];
		$minimum_order_amount 	= $product_data['Shipping']['min_order_amount'];
		$gross_discount_amount_base = $product_data['Shipping']['saved_amount'];
		$minimum_order_amount 		= $product_data['Shipping']['min_order_amount'];
		$new_discount_amount 		= $product_data['Shipping']['saved_amount'];
		$arr 						= array();
		// Check max order limit
		$this->Customer->unBindModel(array('belongsTo' => array('Country','CustomerGroup'),'hasOne'=>array('CustomersAddressBook')));
		$customer_data 	= $this->Customer->find('first', array('conditions'=>array('id'=>$user_id),'fields'=>array('id','max_order_limit')));
		$to_day 		= date('Y-m-d');
		$max_cond 				= "OrderList.customer_id= ".$user_id." AND OrderList.buy_status ='1' AND OrderList.order_status NOT IN (2,5,7) AND DATE(created_date) ='".$to_day."'";
		$customer_order_count 	= $this->OrderList->find('count',array('conditions' => $max_cond));
		if(!empty($customer_data['Customer']['max_order_limit']) && ($customer_data['Customer']['max_order_limit'] <= $customer_order_count)) {
			$ack 		= 'fail';
			$msg 		= "Your max order limit {$customer_data['customer_id']['max_order_limit']} for today .";
		} else {
			if(!empty($product_data['Shipping']['order_amount']) && !empty($product_data['total_cart_count'])) {
				if($product_data['Shipping']['order_amount']>=$product_data['Shipping']['min_order_amount']) {
					$net_tax=0;
					$total_count_product = 0;
					foreach ($product_data as $product_datavalue) {
						$product_quantity = isset($product_datavalue['quantity'])?$product_datavalue['quantity']:0;
						$total_count_product = $total_count_product +$product_quantity;
						$product_tax = isset($product_datavalue['tax_price'])?$product_datavalue['tax_price']:0;
						$net_tax += $product_tax*$product_quantity;
					}
					$shipping_method_id = isset($product_data['Shipping']['shipping_method']) ? $product_data['Shipping']['shipping_method']:0;
					$arr['shipping_method_id']=$shipping_method_id;
					$shipping_cost = isset($product_data['Shipping']['shipping_price']) ? $product_data['Shipping']['shipping_price']:0;
					if(!empty($shipping_cost)) {
						$arr['shipping_cost'] = $shipping_cost;
					} else {
						$arr['shipping_cost'] = 0.00;
					}
					//apply coupon code
					if(!empty($coupon_code)) {
						$couponCodeStatus= $this->check_coupon_code_status($coupon_code,$user_id);
						if($couponCodeStatus==0) {
							$return_data= $this->apply_coupon_code($device_id,$coupon_code,$user_id);
							$product_data=$return_data['Cartdetails'];
							if(isset($return_data['discount_amount_order_total']) && $return_data['discount_amount_order_total']!=0) {
								$cart_discount=$return_data['discount_amount_order_total'];
							}
							if(isset($return_data['discount_amount']) && $return_data['discount_amount']!=0) {
								$new_discount_amount=$return_data['discount_amount'];
							}
							if(isset($return_data['applied_coupon_code']) && $return_data['applied_coupon_code']!='') {
								$applied_coupon_code=$return_data['applied_coupon_code'];
							}
							$CartTotal = $return_data['CartTotal'];
						}
					}
					// min order checking after apply coupon
					//if($CartTotal>$minimum_order_amount)
					//{
						$arr['website_id'] 		= $website_id;
						$arr['company_id'] 		= $company_id;
						$arr['customer_id'] 	= $user_id;
						$arr['address_book_id'] = $address_book_id;
						$arr['webshop_id'] 		= 101;
						$arr['tracking_no'] 	= 'Mobile';
						$arr['order_status'] 	= 0;
						$arr['buy_status'] 		= 1;
						$arr['ip_address']   	= getenv('REMOTE_ADDR');
						$arr['created_date'] 	= date('Y-m-d H:i:s');
						$arr['currency_code']	= 'INR';
						$arr['refferal_code']	= $referal_code;
						$arr['order_status'] 		= 0;
						$arr['buy_status'] 			= 1;
						$arr['ip_address']   		= getenv('REMOTE_ADDR');
						$arr['created_date'] 		= date('Y-m-d H:i:s');
						$arr['currency_code']		= 'INR';
						$arr['refferal_code']		= $referal_code;
						$arr['channel_orderlineitem_id']	= $fulfillment_id;
						$arr['payment_method_id']     	= 16;
						$arr['payment_type_id']      	= 4;
						$arr['payment_method_name']   	= 'Cash On Delivery';
						if(!empty($otp_type )){
							$otp_type = strtolower($otp_type);
							if( $otp_type == 'crod'){
								$arr['payment_method_id']     	= 59;
								$arr['payment_type_id']      	= 4;
								$arr['payment_method_name']   	= 'Card On Delivery';
							}
						}
						// customer addres billing/shipping
						$subarea = $address_data['CustomersAddressBook']['delivary_street_address1'];
						$arr['billing_name']          	=  ucwords($address_data['CustomersAddressBook']['delivery_name']);
						$arr['billing_company']       	=  $address_data['CustomersAddressBook']['delivery_company'];
						$arr['billing_email_address'] 	=  $address_data['CustomersAddressBook']['delivery_email_address'];
						$arr['billing_street_address'] 	=  $address_data['CustomersAddressBook']['delivery_street_address'];
						$arr['billing_street_address1'] =  $address_data['CustomersAddressBook']['delivary_street_address1'];
						$arr['billing_city']          	=  $address_data['CustomersAddressBook']['delivery_city'];
						$arr['billing_postcode']      	=  $address_data['CustomersAddressBook']['delivery_postcode'];
						$arr['billing_state']         	=  $address_data['CustomersAddressBook']['delivery_state'];
						$arr['billing_country']       	=  $address_data['CustomersAddressBook']['delivery_country'];
						$arr['billing_country_name']  	=  'India';
						$arr['billing_phone']         	=  $address_data['CustomersAddressBook']['delivery_phone'];
						$arr['billing_fax']           	=  $address_data['CustomersAddressBook']['delivery_fax'];
						$arr['delivery_name']          	=  ucwords($address_data['CustomersAddressBook']['delivery_name']);
						$arr['delivery_email_address'] 	=  $address_data['CustomersAddressBook']['delivery_email_address'];
						$arr['delivery_street_address'] =  $address_data['CustomersAddressBook']['delivery_street_address'];
						$arr['delivery_street_address1']=  $address_data['CustomersAddressBook']['delivary_street_address1'];
						$arr['delivery_city']          	=  $address_data['CustomersAddressBook']['delivery_city'];
						$arr['delivery_postcode']      	=  $address_data['CustomersAddressBook']['delivery_postcode'];
						$arr['delivery_state']         	=  $address_data['CustomersAddressBook']['delivery_state'];
						$arr['delivery_country']       	=  $address_data['CustomersAddressBook']['delivery_country'];
						$arr['delivery_country_name']   =  'India';
						$arr['delivery_phone']         	=  $address_data['CustomersAddressBook']['delivery_phone'];
						$arr['delivery_fax']           	=  $address_data['CustomersAddressBook']['delivery_fax'];
						$arr['area_id'] = $this->get_area_id_by_subarea($subarea);
						// end of customer address
						$arr['custom_msg']  = $special_instruction;
						//$gross_discount_amount = 0;
						$tax_amount = 0;
						$net_amount = 0;
						$net_shipping = $shipping_cost;
						$net_excise_duty=0;
						// calculating net amount
						 foreach ($product_data as $product_datavalue) {
						 	$quantity_purchased=isset($product_datavalue['quantity'])?$product_datavalue['quantity']:0;
						 	$new_default_price=isset($product_datavalue['new_default_price'])?$product_datavalue['new_default_price']:0;
						 	$amount = $new_default_price*$quantity_purchased;
						 	//$net_amount=$net_amount+($new_default_price*$quantity_purchased);
							$net_amount = $net_amount+$amount;
						 }
						// calculating amounts
						$gross_amount = $net_amount+$net_tax+$net_shipping+$net_excise_duty-$cart_discount;
						$paid_amount = $gross_amount;
						$arr['net_amount'] 			= $net_amount;
						$arr['net_amount_base'] 	= $net_amount;
						$arr['gross_amount'] 		= $gross_amount;
						$arr['gross_amount_base'] 	= $gross_amount;
						$arr['shipping_cost_base'] 	= $net_shipping;
						$arr['order_amount'] 	= $paid_amount;
						$arr['gross_discount_amount_base'] 	= $new_discount_amount;
						$arr['gross_discount_amount'] 		= $new_discount_amount;
						$arr['cart_discount'] 				= $cart_discount;
						$arr['applied_coupon'] 				= $applied_coupon_code;
						// getting delivery slot data
						$time_slot_arr  			= explode('-',$time_slot_time);
						$arr['time_slot_id'] 		= $time_slot_time;
						$arr['time_slot_date'] 		= date('Y-m-d',strtotime($time_slot_date));
						$arr['slot_start_time'] 	= date('H:i:s',strtotime($time_slot_arr[0]));
						$arr['slot_end_time'] 		= date('H:i:s',strtotime($time_slot_arr[1]));
						$zone_id 					= $this->get_zone_id($arr['delivery_postcode']);
						$arr['zone_id'] 			= $zone_id;
						$warehouse_id = $this->get_warehouse_id_from_zone_id($zone_id);
						$arr['warehouse_id'] 		= $warehouse_id;
						/*if($this->Session->check('used_shopongo_points')) {
							$arr['mobiquest_point_discount'] = $this->Session->read('shopongo_points_amount');
						}*/
						//End: For coupon code save in order master table
						$custom_order_id = $this->getcustomorderid($website_id);
						$chk_order_id = $this->OrderList->find('count',array('fields'=>'id', 'conditions'=>array('custom_order_id' => $custom_order_id)));

						// checking duplicate entry...
						$duplicate_cond = "customer_id='".$user_id."' AND buy_status='1' AND created_date >= (now() - INTERVAL 45 SECOND)";
						$duplicate_order = $this->OrderList->find('count',array('fields'=>'id', 'conditions' => $duplicate_cond));
						if(!empty($chk_order_id) && $chk_order_id > 0){
							$custom_order_id = $this->getcustomorderid($website_id);
						}
						if(!empty($custom_order_id) && $user_id > 0 && empty($duplicate_order)) {
							$arr['custom_order_id'] = $custom_order_id;
							$this->OrderList->create();
							$this->OrderList->save($arr);
							$order_id = $this->OrderList->id;
						} else {
							$order_id 	= 0;
							$ack 		= 'fail';
							$msg 		= 'Your cart is empty.';
						}
						if($order_id > 0) {
							if(!empty($applied_coupon_code) && $couponCodeStatus == 0) {
								$discount_array = $this->generate_discount_conditions_coupon($website_id,$applied_coupon_code);
								if(!empty($discount_array)) {
									if($discount_array[0]['DiscountMaster']['coupon_type'] ==1) {
										if($discount_array[0]['DiscountMaster']['has_multiplecoupons'] == 'y') {
											//multiple discount coupon single user scenario ...
											if(!empty($discount_array[0]['DiscountMasterCoupon']) && $discount_array[0]['DiscountMasterCoupon'][0]['is_used'] == 'n') {
												$new_discount_array = array();
												$new_discount_array['is_used'] 	= 'y';
												$new_discount_array['id'] 		= $discount_array[0]['DiscountMasterCoupon'][0]['id'];
												//echo "<br/>saved discountmastercoupon array<pre>"; print_r($$new_discount_array); echo "</pre>"; //exit;
												$this->DiscountMasterCoupon->save($new_discount_array);
											}
										} else {
											/*$new_discount_array = array();
											$new_discount_array['DiscountMaster']['id'] 	   		= $discount_array[0]['DiscountMaster']['id'];
											$new_discount_array['DiscountMaster']['used_coupon'] 	= 1;
											$this->DiscountMaster->save($new_discount_array['DiscountMaster']);*/
										}
									}
								}
							}
							$seqno =  $this->get_order_seqno($user_id, $order_id);
							$seqno_arr['id'] = $order_id;
							$seqno_arr['customer_order_seq'] = ((int)$seqno + 1);
							$this->OrderList->save($seqno_arr);

							$order_activities_str = '';
							if(!empty($applied_coupon_code) && $cart_discount > 0){
								$order_activities_str = 'Order is created by customers using coupon code ' . $applied_coupon_code;
								$this->save_order_activity($order_id,NULL,7,$order_activities_str,1,$user_id);
							} else {
								$this->save_order_activity($order_id,NULL,0,$order_activities_str,1,$user_id);
							}

							if(isset($user_id)) {
								$cnd1 = "Customer.id='".$user_id."'";
								$findCustInfo = $this->Customer->find('first',	array(
										'fields' => array('Customer.orders','Customer.avgorder','Customer.totalorder'),
										'conditions' => $cnd1));
								$orderStatId 				= $findCustInfo['Customer']['orders'];
								$ordcount 					= $findCustInfo['Customer']['orders']+1;
								$totalOrderAmount 			= $findCustInfo['Customer']['totalorder']+$net_amount;
								$ordinfoCustomers['id'] 	= $user_id;
								$ordinfoCustomers['orders'] = $ordcount;
								$ordinfoCustomers['totalorder'] = $findCustInfo['Customer']['totalorder']+$net_amount;
								$ordinfoCustomers['avgorder'] 	= $totalOrderAmount / $ordcount;
								$this->Customer->save($ordinfoCustomers);
							}
							//increase orders count @jp
							$cnd = "DbWebsitestat.company_website_id='".$website_id."'";
							$findOrderstat = $this->DbWebsitestat->find('first',	array(
									'fields' => array('DbWebsitestat.id','DbWebsitestat.orders','DbWebsitestat.revenue'),
									'conditions' => $cnd));
							$orderStatId 		= $findOrderstat['DbWebsitestat']['id'];
							$orderStatOrders 	= $findOrderstat['DbWebsitestat']['orders'];
							$orderStatRevenue 	= $findOrderstat['DbWebsitestat']['revenue'];
							if($orderStatId > 0) {
								$arr2['id'] 		= $orderStatId;
								$arr2['orders'] 	= $orderStatOrders+1;
								$arr2['revenue'] 	= $orderStatRevenue+$gross_amount;
								$this->DbWebsitestat->save($arr2);
							}
							//Table websitehits count
							$curDate 		= date('Y-m-d');
							$cndns1 		= array('DbWebsitehit.company_website_id' => $website_id, 'DbWebsitehit.date' => $curDate);
							$findhits = $this->DbWebsitehit->find('first',	array(
										'fields' => array('DbWebsitehit.id','DbWebsitehit.company_website_id','DbWebsitehit.date','DbWebsitehit.visits'),
										'conditions' => $cndns1));
							if(!empty($findhits)) {
								//update
								$hits['id'] 		= $findhits['DbWebsitehit']['id'];
								$hits['visits'] 	= $findhits['DbWebsitehit']['visits']+1;
								$this->DbWebsitehit->save($hits);
							} else {
								//insert
								$this->DbWebsitehit->create();
								$curDate 					= date('Y-m-d');
								$hits['company_website_id'] = $website_id;
								$hits['date'] 				= $curDate;
								$hits['visits'] 			= 1;
								$this->DbWebsitehit->save($hits);
							}
							$all_product_ids = array();
							foreach($product_data as $key => $val) {
								$product_disc_type = 0;
								$product_discount_rate = 0;
								$discount_price = 0;
								$quantity 				= isset($val['quantity'])?$val['quantity']:0;
								$product_id 			= isset($val['product_id'])?$val['product_id']:0;
								$all_product_ids[] 		= $product_id;
								$new_default_price 		= isset($val['new_default_price'])?$val['new_default_price']:0;
								$tax_price 				= isset($val['tax_price'])?$val['tax_price']:0;
								$tax_name 				= isset($val['tax_name'])?$val['tax_name']:'';
								$excise_duty 			= isset($val['excise_duty'])?$val['excise_duty']:0;
								$excise_duty_per 		= isset($val['excise_duty_per'])?$val['excise_duty_per']:0;

								if(isset($val['product_discount_rate']) && $val['product_discount_rate'] >0){
									$product_discount_rate = $val['product_discount_rate'] ;
								} else if(isset($val['discount_amount']) && $val['discount_amount'] >0) {
									$product_discount_rate = $val['discount_amount'] ;
								}
								if(isset($val['product_disc_type']) && $val['product_disc_type'] >0){
									$product_disc_type = $val['product_disc_type'] ;
								} else if(isset($val['disc_type']) && $val['disc_type'] >0) {
									$product_disc_type = $val['disc_type'] ;
								}
								$discount_price 		= isset($val['discount_price'])?$val['discount_price']:0;
								if(empty($discount_price)){
									if($val['default_price'] > $new_default_price){
										$discount_price 		= $val['default_price'] - $new_default_price ;
									}
								}
								$product_discount_name 	= isset($val['product_discount_name'])?$val['product_discount_name']:'NA';
								//$product_discount_rate 	= isset($val['product_discount_rate'])?$val['product_discount_rate']:0;
								//$product_disc_type 		= isset($val['product_disc_type'])?$val['product_disc_type']:'';
								$is_kvi 				= $val['is_kvi'];
								if($discount_price =='') {
									$discountprice=0;
								} else {
									$discountprice=$discount_price;
								}
								if(!empty($product_id) && !empty($quantity) && $new_default_price >0) {
									$this->OrderProduct->create();
									$orderProductarr['order_id'] 			= $this->OrderList->id;
									$orderProductarr['product_id'] 			= $product_id;
									$orderProductarr['quantity'] 			= $quantity;
									$orderProductarr['product_price'] 		= $new_default_price;
									$orderProductarr['product_excise_duty'] = $excise_duty; // added by cds for excise_duty
									$orderProductarr['product_tax_price'] 	= $tax_price;
									$orderProductarr['tax_name'] 			= $tax_name;
									$orderProductarr['excise_duty_per'] 	= $excise_duty_per;
									$orderProductarr['product_discount_price'] 	= $discount_price;
									$orderProductarr['product_price_base'] 		= $new_default_price;
									$orderProductarr['product_discount_price_base'] 	= $discountprice;
									$orderProductarr['product_discount_name'] 	= $product_discount_name;
									$orderProductarr['product_disc_type'] 		= $product_disc_type;
									$orderProductarr['product_discount_rate'] 	= $product_discount_rate;
									$orderProductarr['is_kvi'] 	= $is_kvi;
									$offer_desc = $this->is_special_offer($product_id);
									$orderProductarr['product_offer_desc']      = $offer_desc;
									$orderProductarr['status'] = 0;
									$this->OrderProduct->save($orderProductarr);
									// Start  Stock update
					 				$product_id = $product_id;
									$product_qty = $quantity;
									$product_status = 'Decrease';
									$stock_minus_type = 'virtual';
								    $this->update_stock_all_move_order_status($product_id, $warehouse_id, $product_qty, $product_status, $stock_minus_type,'','','',$website_id);
									// End Stock update
									if($warehouse_id > 0) {
										$this->update_autoassign_data($order_id, $product_id, $warehouse_id);
									}
								}
							}
							$ack='success';
							$msg='success';
							$cartAvailabilitycondition = "TemporaryShoppingCart.company_id = {$company_id} AND TemporaryShoppingCart.website_id = {$website_id} AND TemporaryShoppingCart.customer_id = '{$user_id}'";
							$this->TemporaryShoppingCart->deleteAll($cartAvailabilitycondition);
							$this->sendmail_order($order_id, 'No');
							$arr['custom_order_id'] = $arr4g['custom_order_id'];
							$this->send_sms($arr,2, $arr['delivery_phone'],1,$user_id);
							//$this->send_sms($order_id);
							$ack='success';
							$msg='success';
						}
					//}
					// else
					// {
					// 	$order_id=0;
					// 	$ack='fail';
					// 	$msg= 'Sorry minimum order amount is'.$minimum_order_amount;
					// }
				} else {
					$order_id=0;
					$ack='fail';
					$msg= 'Sorry minimum order amount is'.$minimum_order_amount;
				}
			} else {
				$order_id 	= 0;
				$ack 		= 'fail';
				$msg 		= 'Your cart is empty.';
			}
		}
		$arr['customer_order_seq'] 		= $seqno_arr['customer_order_seq'];
		$data['arr'] 					= $arr;
		$data['custom_order_id'] 		= $arr['custom_order_id'];
		$data['payment_method_name'] 	= $arr['payment_method_name'];
		$data['shipping_cost'] 			= $arr['shipping_cost'];
		$data['delivery_name'] 				= $arr['delivery_name'];
		$data['delivery_street_address'] 	= $arr['delivery_street_address'];
		$data['delivery_street_address1'] 	= $arr['delivery_street_address1'];

		$data['order_id'] 				= $order_id;
		$data['user_id'] 				= $user_id;
		$data['ack'] 					= $ack;
		$data['msg'] 					= $msg;
		echo json_encode($data);