import { Subject }    from 'rxjs';
import { Router,NavigationEnd } from '@angular/router';
import { CookieService } from 'ngx-cookie';
import {MatSnackBar} from '@angular/material';
import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable, Inject} from '@angular/core';
import { GlobalService } from './app.global.service';
import { GlobalVariable } from './global';
import { LOCAL_STORAGE } from '@ng-toolkit/universal';
const CART_KEY = "cart";
@Injectable()
export class ShoppingCartService {
  private cart_key = CART_KEY+'_'+this._globalService.getFrontedWebsiteId();
  private baseApiUrl = GlobalVariable.BASE_API_URL;
  private products: any = [];
  public S3_URL_PRODUCT = GlobalVariable.S3_URL+'product/200x200/';
  // Observable
  public cartChangeSource = new Subject<any>();
  public cartChange$ = this.cartChangeSource.asObservable();
   
  public constructor(@Inject(LOCAL_STORAGE) private localStorage: any, 
          private _http: Http,
          private _router:Router,
          private _globalService: GlobalService,
          private CookieService: CookieService,
          public snackBar: MatSnackBar
        ) {
    
  }

  public addProductToCart(product: any, qty:number=1,index:number = 0): void {
      //alert("hiii");
      this.addItem(product, qty, true, true,index);
  }

  public removeProductFromCart(product: any, qty:number=-1, index:number): void {
    if(qty>-1){
          qty = -qty;
    }
    this.addItem(product, qty, false, true, index);
  }

  public productInCart(product: any) {
      let cart = this.retrieve();
      return cart.items.some((i) => i.id === product.id);
  }

  public addItem(product: any, quantity: number, is_add: boolean = true, is_check: boolean = true, index: number=0, cart_table_exist = 0): void {
    let cart:any = this.retrieve();
    let item:any;
    let flag_add: boolean = false;
    //console.log('art Sevice');
    //console.log(product);
    if(product.is_preorder=='y' && product.stock == 0 && this._globalService.getFrontedWebsiteId() == 1) {
      is_check = false;
    }
    
    if(is_add) {
      if(product.hasOwnProperty('mapping_product') && product.mapping_product[index].merchant_id>1){ // addto cart from details page
        item = cart.items.find((p) => p.id === product.id && p.merchant_product_id === product.mapping_product[index].market_place_product_id);
      } else if(product.hasOwnProperty('merchant_id') && product.merchant_id>1){ //add to cart from listing page
        item = cart.items.find((p) => p.id === product.id && p.merchant_product_id === product.market_place_product_id);
      } else {
        item = cart.items.find((p) =>  p.id === product.id);  
      }  
    } else {
      item = cart.items[index];
    }
    if (item === undefined) {
      flag_add = true;
      item = {};  
      item.id = product.id;
      item.product_id = product.id;
      item.name = product.name;
      item.name_th = product.name_th;
      item.sku = product.sku;
      item.slug = product.slug;
      item.cover_img = product.cover_img;
      item.quantity = quantity;
      item.coupon_discount_price_base = 0;
      item.product_discount_price_base = 0;
      item.product_discount_price = 0;
      //console.log(product);
      if(product.hasOwnProperty('mapping_product') && product.mapping_product[index].merchant_id>1) { // add to cart from details page merchant product
        item.product_price = parseFloat(product.mapping_product[index].mapping_price);
        if(product.mapping_product[index].discount_percentage>0){
          item.product_discount_rate = product.mapping_product[index].discount_percentage;
          item.product_disc_type = 1;  
          item.discounted_price = this._globalService.calculateProductDiscount(1,product.mapping_product[index].discount_percentage,product.mapping_product[index].mapping_price);
        } else {
          item.product_discount_rate = 0;
          item.product_disc_type = null;  
        }
        item.shipping_price = 0;
        item.shipping_price_base = product.mapping_product[index].merchant_shipping_price;
        item.merchant_product_id = product.id;
        item.merchant_website_id = this._globalService.getFrontedWebsiteId();
        item.merchant_name = product.mapping_product[index].merchant_websitename;
        item.stock = product.mapping_product[index].merchant_stock;
      } else if(product.hasOwnProperty('merchant_id') && product.merchant_id>1) { // add to cart from listing page merchant product
        item.product_price = parseFloat(product.default_price);
        if(product.discount_percentage>0) {
          item.product_discount_rate = product.discount_percentage;
          item.product_disc_type = 1;  
          item.discounted_price = this._globalService.calculateProductDiscount(1,product.discount_percentage,product.default_price);
        } else {
          item.product_discount_rate = 0;
          item.product_disc_type = null;  
        }
        item.shipping_price = 0;
        item.shipping_price_base = product.merchant_shipping_price;
        item.merchant_product_id = product.id;
        item.merchant_website_id = this._globalService.getFrontedWebsiteId();
        item.merchant_name = product.merchant_websitename;
        item.stock = product.stock;
      } else {
        item.product_price = parseFloat(product.default_price);
        if( product.hasOwnProperty('discount') && JSON.stringify(product.discount)!='{}'){
          item.product_discount_rate = product.discount.amount;
          item.product_disc_type = product.discount.disc_type;  
          item.discounted_price = this._globalService.calculateProductDiscount(product.discount.disc_type,product.discount.amount,product.default_price);
        } else {
          item.product_discount_rate = 0;
          item.product_disc_type = null;  
        }
        item.shipping_price = 0;
        item.shipping_price_base = 0;
        item.merchant_product_id = product.id;
        item.merchant_website_id = this._globalService.getFrontedWebsiteId();
        item.merchant_name = '';
        item.stock = product.stock;
      }

      item.price_marketplace = product.price_marketplace;
      item.variants = [];
      if(product.custom_fields){
        product.custom_fields.forEach(field=>{
          let variation:any = {};
          variation.field_id = field.fields.id;
          variation.field_name = field.fields.field_name;
          if(field.value.length>1){
            field.value.forEach(value=>{
              if(value.flag){
                variation.value = value.value;
              }
            });  
          } else {
            variation.value = field.value[0].value;
          }
          item.variants.push(variation);
        });
      }
    } else {
        if(cart_table_exist == 0) {
            item.quantity += quantity;  
        }
    }

    item.is_preorder = (product.is_preorder)?product.is_preorder:'n';
    if(is_check) {
      let data:any = {};
      data["quantity"] = item.quantity;
      data["product_id"] = item.merchant_product_id;
      data["website_id"] = item.merchant_website_id;
      this.checkProductStock(data).subscribe(
        data => {            
            if(data.status==0){
              this._globalService.showToast('Only '+data.real_stock+' quantity available for the product - '+ item.name);
              item.quantity = data.real_stock;  
            } else if (flag_add) {
              cart.items.push(item);
            }
            cart.items = cart.items.filter((cartItem) => cartItem.quantity > 0);
            this.calculateCart(cart);
            this.save(cart);
            this.dispatch(cart);
            if(this._globalService.isLoggedInFrontend() && cart_table_exist == 0){
              if(is_add){
                this.addTempCart(item.product_id,item.quantity);  
              }else{
                this.removeTempCart(item.product_id);
              }
            }
            let itemCount:number = cart.items.map((x) => x.quantity).reduce((p, n) => p + n, 0);
            if(is_add && data.status){
              this.snackBar.open('Added product to cart, You got '+itemCount+' products in cart', 'Ok', {
                duration: 3000,
                verticalPosition: 'top'
              });  
            }
        },
        err => {},
        function(){
           //completed callback
        }
      );
    } else {
      //cart.items.push(item);
      //console.log(flag_add);
      if (flag_add) {
        cart.items.push(item);
      }
      cart.items = cart.items.filter((cartItem) => cartItem.quantity > 0);
      this.calculateCart(cart);
      this.save(cart);
      this.dispatch(cart);
      if(this._globalService.isLoggedInFrontend() && cart_table_exist == 0){
        if(is_add) {
            this.addTempCart(item.product_id,item.quantity);  
        } else {
            this.removeTempCart(item.product_id);
        }
      }
      let itemCount:number = cart.items.map((x) => x.quantity).reduce((p, n) => p + n, 0);
      if(is_add && cart_table_exist == 0){
        this.snackBar.open('Added product to cart, You got '+itemCount+' products in cart', 'Ok', {
          duration: 3000,
          verticalPosition: 'top'
        });  
      }
    }
  }

  public empty(): void  {
    //remove from temp table
    let cart:any = this.retrieve();
    if(this._globalService.isLoggedInFrontend()) {
        let product_ids:any = [];
        cart.items.forEach(item=>{
            product_ids.push(item.id);
        });
        this.removeTempCart(product_ids,true);  
    }
    if(this.CookieService.get('temp_order_id')) {
        this.CookieService.remove('temp_order_id');
    }
    cart = {};
    cart.items = [];
    this.save(cart);
    this.dispatch(cart);
  }


 public local_storage_empty(): void  {
      //remove from temp table
      let cart:any = this.retrieve();
      cart = {};
      cart.items = [];
      this.save(cart);
      this.dispatch(cart);
  }


  public calculateCart(cart: any) {
    cart.gross_amount = cart.items.map((item) => {
      if(item.discounted_price>=0){
          return item.quantity * item.discounted_price;
      } else {
          return item.quantity * item.product_price;
      }
      
    }).reduce((previous, current) => previous + current, 0);
    cart.cart_discount = (cart.cart_discount)?cart.cart_discount:0;
    cart.shipping_cost = (cart.shipping_cost)?cart.shipping_cost:0;
    cart.tax_amount = (cart.tax_amount)?cart.tax_amount:0;
    //cart.net_amount = (cart.gross_amount + cart.shipping_cost + cart.tax_amount) - cart.cart_discount;
    cart.net_amount = (cart.gross_amount + cart.shipping_cost) - cart.cart_discount;
    //console.log('net_amount'+ cart.net_amount + '/tax_amount'+ cart.tax_amount + '/shipping_cost' + cart.shipping_cost + '/gross_amount'+ cart.gross_amount);
  }

  public retrieve() {
    let cart:any = {};
    cart.items = [];
    let storedCart:any = this.localStorage.getItem(this.cart_key);
    if (storedCart) {
      cart = JSON.parse(storedCart);
    }
    return cart;
  }

  public save(cart: any) { 
    this.localStorage.setItem(this.cart_key, JSON.stringify(cart));
  }

  public dispatch(cart: any) {
    this.cartChangeSource.next(cart);
  }


  public addToWishlist(product:any, page:string='') {
    if(this._globalService.isLoggedInFrontend()){
      let data: any = {};
      data.products = product.id;
      data.user_id = this._globalService.getClientId();
      data.website_id = 1;
      this.addWishlist(data).subscribe(
          data => {
            if(data.status){
              let product_data: any = { name: product.name, cover_img: this.S3_URL_PRODUCT+product.cover_img, action: 'add' };
              this._globalService.showProductSnakbar(product_data);
            }else{
              this._globalService.showToast(data.message);
            }
           
        },
        err => {
            this._globalService.showToast('Something went wrong. Please try again.');
        },
        function(){
           //completed callback
        }
      );
    } else {       
      if(page == 'details') {
        this.CookieService.put('after_login_redirect','/product/'+ product.slug);  
      } else {
        this.CookieService.put('after_login_redirect',this._router.url);
      }
      this._router.navigate(['/login']);
    }
  }

  public addTempCart(product_id:number, quantity:number) {
      let customer_id = this._globalService.getCustomerId();
      let website_id: number = this._globalService.getFrontedWebsiteId();
      let data:any = {"website_id": website_id, "company_id":1,"device_id":"", "customer_id": customer_id,"product_id":product_id, quantity: quantity};
      this.addUserCart(data).subscribe(
        data => {},
        err => {},
        function(){
           //completed callback
        }
      );
  }

  public removeTempCart(product_id:any,is_arr:boolean=false) {
    let data:any = {"website_id":1,"customer_id": this._globalService.getCustomerId()};
    if(is_arr){
      data.product_id = product_id;
    } else {
      data.product_id = [product_id];  
    } 
    this.removeUserCart(data).subscribe(
      data => {},
      err => {},
      function(){
         //completed callback
      }
    );
  }  

  public getCartProducts(data:any){
      return this._http.post(this.baseApiUrl+'cartlist/', data).pipe(map(res =>  res.json()),catchError(this.handleError));   
  } 
  // After login cart data inserted to database
  public addTempCartAfterLogin(data:any){
      return this._http.post(this.baseApiUrl+'cart_product_add_login/', data, this._globalService.getHttpOptionClient()).pipe(map(res =>  res.json()),catchError(this.handleError));   
  }
    
  public checkProductStock(data:any){
      return this._http.post(this.baseApiUrl+'product-stock-check/', data).pipe(map(res =>  res.json()),catchError(this.handleError));   
  }  

  private addUserCart(data:any){
      return this._http.post(this.baseApiUrl+'cart_product_add/', data, this._globalService.getHttpOptionClient()).pipe(map(res =>  res.json()),catchError(this.handleError));   
  }

  private removeUserCart(data:any){
      return this._http.post(this.baseApiUrl+'cart-product-delete/', data, this._globalService.getHttpOptionClient()).pipe(map(res =>  res.json()),catchError(this.handleError));   
  }  

    private addWishlist(data:any){
        return this._http.post(this.baseApiUrl+'wishlist/', data, this._globalService.getHttpOptionClient()).pipe(map(res =>  res.json()),catchError(this.handleError));   
    }

    public currecnyExchange(currency_id:number) {
        let website_id: number = this._globalService.getFrontedWebsiteId();
        return this._http.get(this.baseApiUrl+'currency-change/'+currency_id+'/'+website_id+'/').pipe(map(res =>  res.json()),catchError(this.handleError));   
    }

    public addItemGuest(product: any, quantity: number, is_add: boolean = true, is_check: boolean = true, index: number=0): void {
        let cart:any = this.retrieve();
        let item:any;
        let flag_add: boolean = false;
        if(is_add) {
            item = cart.items.find((p) =>  p.id === product.id);  
        } else {
           item = cart.items[index];
        }        
        if (item === undefined) {
            flag_add = true;
            item = {};  
            item.id = product.id;
            item.product_id = product.id;
            item.name = product.name;
            item.name_th = product.name_th;
            item.sku = product.sku;
            item.slug = product.slug;
            item.cover_img = product.cover_img;

            item.quantity = quantity;
            item.coupon_discount_price_base = 0;
            item.product_discount_price_base = 0;
            item.product_discount_price = 0;

            item.product_price = parseFloat(product.default_price);
            
            if(JSON.stringify(product.discount)!='{}' && JSON.stringify(product.discount) != undefined){
              item.product_discount_rate = product.discount.amount;
              item.product_disc_type = product.discount.disc_type;  
              item.discounted_price = this._globalService.calculateProductDiscount(product.discount.disc_type,product.discount.amount,product.default_price);
            }else{
              item.product_discount_rate = 0;
              item.product_disc_type = null;  
            }

            item.shipping_price = 0;
            item.shipping_price_base = 0;
            item.merchant_product_id = product.id;
            item.merchant_website_id = this._globalService.getFrontedWebsiteId();
            item.merchant_name = '';
            item.stock = product.stock;
      
            item.price_marketplace = product.price_marketplace;
            item.variants = [];
            if(product.custom_fields){
                product.custom_fields.forEach(field=>{
                    let variation:any = {};
                    variation.field_id = field.fields.id;
                    variation.field_name = field.fields.field_name;
                    if(field.value.length>1){
                        field.value.forEach(value=>{
                          if(value.flag){
                            variation.value = value.value;
                          }
                        });  
                    }else{
                        variation.value = field.value[0].value;
                      }
                item.variants.push(variation);
                });
            }
        } else {
              item.quantity += quantity;
        }
        item.is_preorder = (product.is_preorder)?product.is_preorder:'n';

        if(is_check){
          let data:any = {};
          data["quantity"] = item.quantity;
          data["product_id"] = item.merchant_product_id;
          data["website_id"] = item.merchant_website_id;

          this.checkProductStock(data).subscribe(
            data => {
                if(data.status==0){
                  this._globalService.showToast('Only '+data.real_stock+' quantity available for the product - '+ item.name);
                  item.quantity = data.real_stock;
                } else if (flag_add) {
                  cart.items.push(item);
                }
                cart.items = cart.items.filter((cartItem) => cartItem.quantity > 0);
                this.calculateCart(cart);
                this.save(cart);
                this.dispatch(cart);

                let itemCount:number = cart.items.map((x) => x.quantity).reduce((p, n) => p + n, 0);
                if(is_add && data.status){
                  this.snackBar.open('Added product to cart, You got '+itemCount+' products in cart', 'Ok', {
                    duration: 3000,
                    verticalPosition: 'top'
                  });  
                }
            },
            err => {},
            function(){
               //completed callback
            }
          );
        } else {
          //cart.items.push(item);
            if (flag_add) {
                cart.items.push(item);
            }
            cart.items = cart.items.filter((cartItem) => cartItem.quantity > 0);
            this.calculateCart(cart);
            this.save(cart);
            this.dispatch(cart);
            let itemCount:number = cart.items.map((x) => x.quantity).reduce((p, n) => p + n, 0);
        } 
    }


    private handleError(error: Response) { 
        return Observable.throw(error || "Server err"); 
    }
    
}
