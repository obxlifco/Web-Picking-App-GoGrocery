from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
# Import Model And Serializer
from webservices.models import *
from frontapp.frontapp_serializers import *

from django.db.models import F, Func, FloatField
from django.db.models.functions import Cast

import json
import base64
import sys,os
import traceback
import datetime
    
class ViewProductDetails(APIView):
    permission_classes = []
    def get(self, request, format=None):
		
        website_id 	= get_company_website_id_by_url()
		max_order_unit = get_max_order_unit()
		
        return_array 	= array();
		variationFieldArray 	= array();
		customFieldsArray 		= array();
		arrayRelated 			= array();
		if($this->request->is('post')) {
			$product_id = isset($this->request->data['product_id'])?$this->request->data['product_id']:'';
			$user_id 	= isset($this->request->data['user_id'])?$this->request->data['user_id']:'';
			$device_id 	= isset($this->request->data['device_id'])?$this->request->data['device_id']:'';
			$zone_id 	= isset($this->request->data['zone_id'])?$this->request->data['zone_id']:'';
		} else {
			$product_id = isset($this->params['url']['product_id'])?$this->params['url']['product_id']:'';
			$user_id 	= isset($this->params['url']['user_id'])?$this->params['url']['user_id']:'';
			$device_id 	= isset($this->params['url']['device_id'])?$this->params['url']['device_id']:'';
			$zone_id 	= isset($this->params['url']['zone_id'])?$this->params['url']['zone_id']:'';
		}
		### PRODUCT DETAILS ################################################################################
		if(!empty($product_id)) {
			$product_quantity 	= 0;
			$conditions 		= "Product.id = '{$product_id}'";
			$ContentManagements = new ContentManagementsController();
			$product 			= $this->show_frontend_products($website_id, 'single', $conditions, '1',$product_id,'','','',$user_id,$device_id);
			$primary_category_id = $ContentManagements->category_ids_from_product_ids($product_id);
			$fields 			= "Category.id, Category.slug, Category.parent_id, Category.name, Category.isblocked, Category.isdeleted";
			$order 				= "Category.id ASC";
			$category_tree 		= $this->Category->getPath($primary_category_id, $fields);

			if(empty($product)) {
				$ack ='fail';
				$msg ='Product not available.';
			} else {
				$arrayRelated 			= array();
				$related_product_ids 	= $this->get_related_product_ids($product_id);
				$related_products 		= explode(",",$related_product_ids);
				$variationFieldArray 	= array();
				$newarraycrossProducts 	= array();
				$arryCrossProduct = $this->get_cross_products($product_id);
				$variant_count = 0;
				if(!empty($arryCrossProduct)){
					foreach ($arryCrossProduct as $key => $value){
						if(!empty($value['MarketplaceFieldValue']['product_id'])){
							// variant start
							array_splice($related_products, array_search($value['MarketplaceFieldValue']['product_id'], $related_products ), 1);
							$conditionsCross = "Product.id=".$value['MarketplaceFieldValue']['product_id'];
							$all_cross_products = $this->show_frontend_products($website_id, 'single', $conditionsCross, '1',$value['MarketplaceFieldValue']['product_id'],'','','',$user_id,$device_id);
							// cross product
							if(!empty($all_cross_products[0]['Product']['id'])) {
								$crossimage_path = '';
								$arraycrossProducts = array();
								$crossimage_path = $ContentManagements->product_image_resize_amazon_aws($all_cross_products[0]['ProductImage'][0]['img'], 100, 100, $website_id);
								if($all_cross_products[0]['Product']['id'] == $product_id){
									$cross_product_mrp = $product[0]['Product']['original_price'];
									$cross_product_offer = $product[0]['Product']['offer_price'];
									$cross_product_selling_price = $product[0]['Product']['effective_price'];
								} else {
									$cross_product_mrp = $all_cross_products[0]['Product']['original_price'];
									$cross_product_offer = $all_cross_products[0]['Product']['offer_price'];
									$cross_product_selling_price = $all_cross_products[0]['Product']['effective_price'];
								}
								$cross_product_quantity = isset($all_cross_products[0]['TemporaryShoppingCart']['quantity'])?$all_cross_products[0]['TemporaryShoppingCart']['quantity']:'0';
								$cross_product_real_stock = 0;
								if(isset($all_cross_products[0]['StockData']['real_stock']) && !empty($all_cross_products[0]['StockData']['real_stock'])){
									$cross_product_real_stock = $all_cross_products[0]['StockData']['real_stock'];
								}
								$cross_productreal_stock_msg = '';
								if($cross_product_real_stock<=0) {
									$cross_productreal_stock_msg = 'Out of stock';
								}
								$cross_product_max_order_unit = $max_order_unit;
								if(isset($all_cross_products[0]['Product']['max_order_unit']) && !empty($all_cross_products[0]['Product']['max_order_unit'])){
									$cross_product_max_order_unit = $all_cross_products[0]['Product']['max_order_unit'];
								}
								$is_out_of_stock_notified_cross_product = 'no';
								if(isset($all_cross_products[0]['OutofstockNotification']['product_id']) && !empty($all_cross_products[0]['OutofstockNotification']['product_id'])) {
									$is_out_of_stock_notified_cross_product = 'yes';
								}
								$variant_product_thumb_images = $this->update_product_images($all_cross_products, '80', '80',$website_id);
								$variant_product_big_images = $this->update_product_images($all_cross_products, '400', '400',$website_id);
								$variant_product_large_images = $this->update_product_images($all_cross_products, '800', '800',$website_id);
								$offer_desc = '';
								$is_offer 		= $this->check_special_offer($all_cross_products);
								if($is_offer) {
									$offer_desc = $all_cross_products[0]['Product']['product_offer_desc'];
								}
								$newarraycrossProducts=array(
									'parent_id'=>$product_id,
									'id'=>$all_cross_products[0]['Product']['id'],
									'sku'=>$all_cross_products[0]['Product']['sku'],
									'field_name'=>$value['MarketplaceFieldValue']['field_name'],
									'field_value'=>$value['MarketplaceFieldValue']['value'],
									'name'=>$all_cross_products[0]['Product']['name'],
									'mrp'=>number_format($cross_product_mrp,2),
									'offer'=>$cross_product_offer,
									'selling_price'=>number_format($cross_product_selling_price,2),
									'quantity'=>$cross_product_quantity,
									'real_stock'=>$cross_product_real_stock,
									'real_stock_msg'=>$cross_productreal_stock_msg,
									'max_order_unit'=>$cross_product_max_order_unit,
									'images'=>$crossimage_path,
									'veg_nonveg_type'=>$all_cross_products[0]['Product']['veg_nonveg_type'],
									'is_notified'=>$is_out_of_stock_notified_cross_product,
									'brand'=> $all_cross_products[0]['Brand']['name'],
									'product_offer_desc'=> $offer_desc,
								);
								$variationFieldArray[$variant_count] = $newarraycrossProducts;
								// images
								$variationFieldArray[$variant_count]['Images']['thumb_images'] 	= $variant_product_thumb_images[0]['ProductImage'];
								$variationFieldArray[$variant_count]['Images']['big_images'] 	= $variant_product_big_images[0]['ProductImage'];
								$variationFieldArray[$variant_count]['Images']['large_images'] 	= $variant_product_large_images[0]['ProductImage'];
								$variant_count++;
							}
						}
					}
				}
				### PRODUCT IMAGES #################################################################################
				$product_thumb_images 	= $this->update_product_images($product, '80', '80',$website_id);
				$product_big_images 	= $this->update_product_images($product, '400', '400',$website_id);
				$product_large_images 	= $this->update_product_images($product, '800', '800',$website_id);
				### RELATED PRODUCTS #######################################################################################
				//$related_products = $this->show_frontend_products($website_id, 'related', '', '5',$product_id,'','','',$user_id);
				//$related_products = $this->update_product_images($related_products, '100', '100',$website_id);
				### CUSTOM FIELDS #######################################################################################
				$primary_category_id = $ContentManagements->category_ids_from_product_ids($product_id);
				//$customfield= $this->get_custom_fields($primary_category_id, $product_id, $channel_id='6', $website_id=1, $type='values', $is_variant=0, $field_id=0);
				$field_name="'About product'";
				$customfield=$this->get_custom_fields_var($primary_category_id, $product_id,6,1,'','', $field_name);
				### PUSHING DATA INTO ARRAY #######################################################################################
				$description='';
				if($product[0]['Product']['description']!='') {
					$description=$product[0]['Product']['description'];
				}
				$features='';
				if($product[0]['Product']['features']!='') {
					$features=$product[0]['Product']['features'];
				}
				$all_product_real_stock=0;
				if(isset($product[0]['StockData']['real_stock']) && !empty($product[0]['StockData']['real_stock'])) {
					$all_product_real_stock=$product[0]['StockData']['real_stock'];
				}
				$all_productreal_stock_msg='';
				if($all_product_real_stock<=0) {
					$all_productreal_stock_msg='Out of stock';
				}
				$product_max_order_unit=$max_order_unit;
				if(isset($product[0]['Product']['max_order_unit']) && !empty($product[0]['Product']['max_order_unit'])) {
					$product_max_order_unit=$product[0]['Product']['max_order_unit'];
				}
				$is_out_of_stock_notified='no';
				if(isset($product[0]['OutofstockNotification']['product_id']) && !empty($product[0]['OutofstockNotification']['product_id'])) {
					$is_out_of_stock_notified='yes';
				}
				$product_quantity=isset($product[0]['TemporaryShoppingCart']['quantity'])?$product[0]['TemporaryShoppingCart']['quantity']:0;
				$return_array['Product']['id'] 				= $product[0]['Product']['id'];
				$return_array['Product']['sku'] 			= $product[0]['Product']['sku'];
				$return_array['Product']['name'] 			= $product[0]['Product']['name'];
				$return_array['Product']['description'] 	= $description;
				$return_array['Product']['features'] 		= $features;
				$return_array['Product']['mrp'] 			= number_format($product[0]['Product']['original_price'],2);
				$return_array['Product']['selling_price'] 	= number_format($product[0]['Product']['effective_price'],2);
				$return_array['Product']['offer'] 			= $product[0]['Product']['offer_price'];
				$return_array['Product']['quantity'] 		= $product_quantity;
				$return_array['Product']['real_stock'] 		= $all_product_real_stock;
				$return_array['Product']['real_stock_msg'] 	= $all_productreal_stock_msg;
				$return_array['Product']['max_order_unit'] 	= $product_max_order_unit;
				$return_array['Product']['veg_nonveg_type'] = $product[0]['Product']['veg_nonveg_type'];
				$return_array['Product']['is_notified'] 	= $is_out_of_stock_notified;
				$return_array['Product']['brand']			= $product[0]['Brand']['name'];

				$offer_desc = '';
				$is_offer 		= $this->check_special_offer($product);
				if($is_offer) {
					$offer_desc = $all_cross_products[0]['Product']['product_offer_desc'];
				}
				$return_array['Product']['product_offer_desc']			= $offer_desc;
				// images
				$return_array['Images']['thumb_images'] 	= $product_thumb_images[0]['ProductImage'];
				$return_array['Images']['big_images'] 		= $product_big_images[0]['ProductImage'];
				$return_array['Images']['large_images'] 	= $product_large_images[0]['ProductImage'];
				$return_array['Product']['Category'] 		= isset($category_tree[0]['Category']['name'])?$category_tree[0]['Category']['name']:'';
				$return_array['Product']['Sub Category'] 	= isset($category_tree[1]['Category']['name'])?$category_tree[1]['Category']['name']:'';
				$return_array['Product']['Product Type'] 	= isset($category_tree[2]['Category']['name'])?$category_tree[2]['Category']['name']:'';

				// creating related Product view
				$exclude=array();
				if(!empty($related_products)) {
					foreach($related_products as $related_product_val) {
						$arryRelatedCrossProduct=$this->get_cross_products($related_product_val);

						foreach($arryRelatedCrossProduct as $relatedkey => $relatedvalue) {
							if($related_product_val!=$relatedvalue['MarketplaceFieldValue']['product_id'] && !in_array($relatedvalue['MarketplaceFieldValue']['product_id'], $exclude)) {
								array_splice($related_products, array_search($relatedvalue['MarketplaceFieldValue']['product_id'], $related_products ), 1);
							}
							$exclude[]=$relatedvalue['MarketplaceFieldValue']['product_id'];
						}
					}
				}
				if(!empty($related_products)) {
					$counter=1;
					foreach($related_products as $related_product_val) {
						$relatedarraycrossProducts=array();
						$relatedvariationFieldArray=array();
						### PRODUCT With More DETAILS ################################################################################
						$conditions = "Product.id=".$related_product_val;
						$all_related_products = $this->show_frontend_products($website_id, 'single', $conditions, '1',$related_product_val,'','','',$user_id,$device_id);
						if(!empty($all_related_products[0]['Product']['id'])) {
							$related_image_path='';
							$related_image_path = $ContentManagements->product_image_resize_amazon_aws($all_related_products[0]['ProductImage'][0]['img'], 100, 100, $website_id);
							$arryRelatedCrossProduct=$this->get_cross_products($related_product_val);
							foreach($arryRelatedCrossProduct as $relatedkey => $relatedvalue) {
								$conditionsCross = "Product.id=".$relatedvalue['MarketplaceFieldValue']['product_id'];
								$all_related_cross_products = $this->show_frontend_products($website_id, 'single', $conditionsCross, '1',$relatedvalue['MarketplaceFieldValue']['product_id'],'','','',$user_id,$device_id);
								if(!empty($all_related_cross_products[0]['Product']['id'])) {
									$relatedCrossimage_path = '';
									$relatedarraycrossProducts = array();
									$relatedCrossimage_path = $ContentManagements->product_image_resize_amazon_aws($all_related_cross_products[0]['ProductImage'][0]['img'], 100, 100, $website_id);
									$related_product_quantity=isset($all_related_products[0]['TemporaryShoppingCart']['quantity'])?$all_related_products[0]['TemporaryShoppingCart']['quantity']:0;
									$related_cross_product_quantity=isset($all_related_cross_products[0]['TemporaryShoppingCart']['quantity'])?$all_related_cross_products[0]['TemporaryShoppingCart']['quantity']:0;
									// to show product price same as cross product
									if($all_related_products[0]['Product']['id']==$all_related_cross_products[0]['Product']['id']) {
										$related_product_mrp=$all_related_products[0]['Product']['original_price'];
										$related_product_offer=$all_related_products[0]['Product']['offer_price'];
										$related_product_selling_price=$all_related_products[0]['Product']['effective_price'];
									} else {
										$related_product_mrp=$all_related_cross_products[0]['Product']['original_price'];
										$related_product_offer=$all_related_cross_products[0]['Product']['offer_price'];
										$related_product_selling_price=$all_related_cross_products[0]['Product']['effective_price'];
									}
									$related_cross_product_real_stock=0;
									if(isset($all_related_cross_products[0]['StockData']['real_stock']) && !empty($all_related_cross_products[0]['StockData']['real_stock']))
									{
										$related_cross_product_real_stock=$all_related_cross_products[0]['StockData']['real_stock'];
									}
									$related_cross_productreal_stock_msg='';
									if($related_cross_product_real_stock<=0) {
										$related_cross_productreal_stock_msg='Out of stock';
									}
									$related_cross_product_max_order_unit=$max_order_unit;
									if(isset($all_related_cross_products[0]['Product']['max_order_unit']) && !empty($all_related_cross_products[0]['Product']['max_order_unit'])) {
										$related_cross_product_max_order_unit=$all_related_cross_products[0]['Product']['max_order_unit'];
									}
									$is_out_of_stock_notified_related_cross_product='no';
									if(isset($all_related_cross_products[0]['OutofstockNotification']['product_id']) && !empty($all_related_cross_products[0]['OutofstockNotification']['product_id'])) {
										$is_out_of_stock_notified_related_cross_product='yes';
									}
									$relatedarraycrossProducts=array(
										'parent_id'=>$all_related_products[0]['Product']['id'],
										'id'=>$all_related_cross_products[0]['Product']['id'],
										'sku'=>$all_related_cross_products[0]['Product']['sku'],
										'field_name'=>$relatedvalue['MarketplaceFieldValue']['field_name'],
										'field_value'=>$relatedvalue['MarketplaceFieldValue']['value'],
										'name'=>$all_related_cross_products[0]['Product']['name'],
										'mrp'=>number_format($related_product_mrp,2),
										'offer'=>$related_product_offer,
										'selling_price'=>number_format($related_product_selling_price,2),
										'quantity'=>$related_cross_product_quantity,
										'real_stock'=>$related_cross_product_real_stock,
										'real_stock_msg'=>$related_cross_productreal_stock_msg,
										'max_order_unit'=>$related_cross_product_max_order_unit,
										'images'=>$relatedCrossimage_path,
										'veg_nonveg_type'=>$all_related_cross_products[0]['Product']['veg_nonveg_type'],
										'is_notified'=>$is_out_of_stock_notified_related_cross_product,
									);
									$relatedvariationFieldArray[] = $relatedarraycrossProducts;
								}
							}
							$related_product_quantity=isset($all_related_products[0]['TemporaryShoppingCart']['quantity'])?$all_related_products[0]['TemporaryShoppingCart']['quantity']:0;
							$all_related_product_real_stock=0;
							if(isset($all_related_products[0]['StockData']['real_stock']) && !empty($all_related_products[0]['StockData']['real_stock']))
							{
								$all_related_product_real_stock=$all_related_products[0]['StockData']['real_stock'];
							}
							$all_related_productreal_stock_msg='';
							if($all_related_product_real_stock<=0) {
								$all_related_productreal_stock_msg='Out of stock';
							}
							$all_related_product_max_order_unit=$max_order_unit;
							if(isset($all_related_products[0]['Product']['max_order_unit']) && !empty($all_related_products[0]['Product']['max_order_unit']))
							{
								$all_related_product_max_order_unit=$all_related_products[0]['Product']['max_order_unit'];
							}
							$is_out_of_stock_notified_related_product='no';
							if(isset($all_related_products[0]['OutofstockNotification']['product_id']) && !empty($all_related_products[0]['OutofstockNotification']['product_id']))
							{
								$is_out_of_stock_notified_related_product='yes';
							}
							$rel_primary_category_id = $ContentManagements->category_ids_from_product_ids($all_related_products[0]['Product']['id']);
							$rel_fields 			= "Category.id, Category.slug, Category.parent_id, Category.name, Category.isblocked, Category.isdeleted";
							$rel_category_tree 		= $this->Category->getPath($rel_primary_category_id, $rel_fields);

							$arrayRelated[]=array(
								'id'=>$all_related_products[0]['Product']['id'],
								'sku'=>$all_related_products[0]['Product']['sku'],
								'name'=>$all_related_products[0]['Product']['name'],
								'mrp'=>number_format($all_related_products[0]['Product']['original_price'],2),
								'selling_price'=>number_format($all_related_products[0]['Product']['effective_price'],2),
								'offer'=>$all_related_products[0]['Product']['offer_price'],
								'quantity'=>$related_product_quantity,
								'real_stock'=>$all_related_product_real_stock,
								'real_stock_msg'=>$all_related_productreal_stock_msg,
								'max_order_unit'=>$all_related_product_max_order_unit,
								'images'=>$related_image_path,
								'veg_nonveg_type'=>$all_related_products[0]['Product']['veg_nonveg_type'],
								'is_notified'=>$is_out_of_stock_notified_related_product,
								'brand'=>$all_related_products[0]['Brand']['name'],
								'product_offer_desc'=>$all_related_products[0]['Product']['product_offer_desc'],
								'Category' 		=> isset($rel_category_tree[0]['Category']['name'])?$rel_category_tree[0]['Category']['name']:'',
								'Sub Category' 	=> isset($rel_category_tree[1]['Category']['name'])?$rel_category_tree[1]['Category']['name']:'',
								'Product Type' 	=> isset($rel_category_tree[2]['Category']['name'])?$rel_category_tree[2]['Category']['name']:'',

								'Variants'=>$relatedvariationFieldArray,
							);
							if($counter==6) {
								break;
							}
							$counter++;
						}
					}
				}
				$ack='success';
				$msg='success';
				$RecenyBuyproduct=array();
				if(!empty($user_id))
				{
					$RecenyBuyproduct=$this->get_recent_buy_product_list($user_id,$device_id);
				}
				$return_array['Variants']=$variationFieldArray;
				$return_array['CustomFields']=$customFieldsArray;
				$return_array['RelatedProduct']=$arrayRelated;
				$return_array['RecenyBuyproduct']=$RecenyBuyproduct;
			}
		}
		else
		{
			$ack='fail';
			$msg='Provide product id.';
		}
		$return_array['ack']=$ack;
		$return_array['msg']=$msg;

		$this->response->type('json');
	    $json = json_encode($return_array);
	    $this->response->body($json);
		// echo json_encode($return_array);
		// exit;


def get_company_website_id_by_url():
    return 1

def get_max_order_unit():
    return