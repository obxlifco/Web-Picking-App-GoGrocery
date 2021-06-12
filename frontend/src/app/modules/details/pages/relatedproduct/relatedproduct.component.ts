import { Component, OnInit,Input,EventEmitter,Output} from '@angular/core';
import {ProductService} from '../../../../global/service/product.service';
import {CartService} from '../../../../global/service/cart.service';
import {MatSelectModule} from '@angular/material/select';
import {Router} from '@angular/router';
import { WarehouseService } from '../../../../global/service/warehouse.service';

@Component({
  selector: 'app-relatedproduct',
  templateUrl: './relatedproduct.component.html',
  styleUrls: ['./relatedproduct.component.css']
})
export class RelatedproductComponent implements OnInit {

  private _productId;
 // @Input() productId;
  @Output() onChangeNavigation = new EventEmitter();

  public relatedProductDetails;

  constructor(private _ps:ProductService,private _router:Router,public cartService:CartService,private _warehouseservice:WarehouseService) { }

  get productId(): string {
    // transform value for display
    return this._productId;

  }
  
  @Input()
  set productId(productId: string) {
   /* console.log('prev value: ', this._productId);
    console.log('got name: ', productId);*/
    this._productId = productId;
    this.getSimilarProductByProductId();


  }


  ngOnInit() {
   
  	//this.getSimilarProductByProductId();
  }
  /**
   * Method for getting similar product details by product id
   * @access public

  */
  getSimilarProductByProductId() {
    this._warehouseservice.warehouseData$.subscribe(res=>{
      this._ps.getSimilarProductByProductId(this._productId).subscribe(response => {
        if(response && response['status'] == 200) {
 
          this.relatedProductDetails = this.formatProductData(response['data']);
          console.log("****************** Similar product data *****************");
          console.log(this.relatedProductDetails);
 
        }
       //this.relatedProductDetails = this.formatProductData()
     });
    })
  	


  }
  /**
    * Method for formatting deals or sales data
    * @access public
    * @return array
   */
   formatProductData(similarProductData = []) {
   	

     if(similarProductData.length > 0) {

       let i = 0;
       similarProductData.forEach(productData => {
         let tempProductData = [];
         let cloneProductData = Object.assign({},productData);
         delete cloneProductData.variant_product;
         similarProductData[i]['selected_product'] = cloneProductData['product'];
         cloneProductData['is_parent'] = true;
         tempProductData.push(cloneProductData['product']);
         if(productData['product']['variant_product'].length > 0) {
           tempProductData = tempProductData.concat(productData['product']['variant_product']);

         }
         if(productData['stock_details'].length > 0) {  
           similarProductData[i]['selected_product']['stock_details'] = productData['stock_details'];
         }
         similarProductData[i]['variant_product'] = tempProductData;
         i++;

       });
     }
     return similarProductData;
   }
   /**
    * Method for navigating to another url
   */
   navigateToUrl(productSlug) {
   	/*alert(productSlug);
   	this._router.navigate(['details/'+productSlug]);*/
   	this.onChangeNavigation.emit(productSlug);
   }


}
