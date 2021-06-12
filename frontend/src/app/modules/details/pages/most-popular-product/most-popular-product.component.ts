import { Component, OnInit,Input,OnChanges,EventEmitter,Output, Inject, PLATFORM_ID} from '@angular/core';
import {ProductService} from '../../../../global/service/product.service';
import {CartService} from '../../../../global/service/cart.service';
import {MatSelectModule} from '@angular/material/select';
import { WarehouseService } from '../../../../global/service/warehouse.service';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-most-popular-product',
  templateUrl: './most-popular-product.component.html',
  styleUrls: ['./most-popular-product.component.css']
})
export class MostPopularProductComponent implements OnChanges {
  public mostPopularProduct;
  public updatedProductId;
  private _productId;
  @Output() onChangeNavigation = new EventEmitter();
  constructor(
    private _ps:ProductService,
    public cartService:CartService,
    private _warehouseservice:WarehouseService,
    @Inject(PLATFORM_ID) private platformId: Object

  ) { }
  /*@Input() get productId() {
    alert(this.productId);
    return this.productId;

  }*/
  get productId(): string {
    // transform value for display
    return this._productId;
  }
  
  @Input()
  set productId(productId: string) {
   /* console.log('prev value: ', this._productId);
    console.log('got name: ', productId);*/
    this._productId = productId;
    this.getMostPopularProductByProductId();
  }
  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this._warehouseservice.warehouseData$.subscribe(res=>{
        //this.getMostPopularProductByProductId();
         this.getMostPopularProductByProductId();
        })
    }


  }
  ngOnChanges() {
    //this.ngOnInit();
  }
   /**
   * Method for getting similar product details by product id
   * @access public

  */
  getMostPopularProductByProductId() {
    this._ps.getPopularProductByProductId(this._productId).subscribe(response => {
       if(response && response['status'] == 200) {
         this.mostPopularProduct = [];
         this.mostPopularProduct = this.formatProductData(response['data']);
         console.log("*************** Most popular product ***************");
         console.log(this.mostPopularProduct);
       }
      //this.relatedProductDetails = this.formatProductData()
    });
  }
  /**
    * Method for formatting deals or sales data
    * @access public
    * @return array
   */
   formatProductData(popularProductData = []) {
     if(popularProductData.length > 0) {
       let i = 0;
       popularProductData.forEach(productData => {
         let tempProductData = [];
         let cloneProductData = Object.assign({},productData);
         delete cloneProductData.variant_product;
         popularProductData[i]['selected_product'] = cloneProductData['product'];
         cloneProductData['is_parent'] = true;
         tempProductData.push(cloneProductData['product']);
         if(productData['product']['variant_product'].length > 0) {
           tempProductData = tempProductData.concat(productData['product']['variant_product']);
         }
        
         if(productData['stock_details'].length > 0) {
            
           popularProductData[i]['selected_product']['stock_details'] = productData['stock_details'];

         }
         popularProductData[i]['variant_product'] = tempProductData;
         i++;
       });
     }
     
     return popularProductData;
   }
   /**
    * Method for navigating to another url
   */
   navigateToUrl(productSlug) {
     /*alert(productSlug);
     this._router.navigate(['details/'+productSlug]);*/
     this.onChangeNavigation.emit(productSlug);
     window.scroll(0,0);
   }
}
