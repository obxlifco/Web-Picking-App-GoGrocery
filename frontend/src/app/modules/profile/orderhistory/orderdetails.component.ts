import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { Global,GlobalVariable } from '../../../global/service/global';
import { GlobalService } from '../../../global/service/app.global.service';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';


@Component({
  selector: 'app-orderdetails',
  templateUrl: './orderdetails.component.html',
  styleUrls: ['./orderdetails.component.css']
})
export class OrderdetailsComponent implements OnInit {
  public orders:any=[];
  public orderId:number;
  private baseApiUrl = GlobalVariable.BASE_API_URL;
  public S3_URL_PRODUCT = GlobalVariable.S3_URL+'product/200x200/';
  public view_order:number=0;
  public slug;
  public page_name:any;
  public order_status:number = 100;
 
  constructor (
    public global: Global,
    public _globalService: GlobalService,
		private _router: Router,
    private _activeRoute:ActivatedRoute,
    @Inject(PLATFORM_ID) private platformId: Object

  ) {
    let data=this._activeRoute.snapshot.params;
    this.orderId = +data.slug;
    //alert(this.orderId);
    this._activeRoute.url.subscribe(() => {
        this.view_order = this._activeRoute.snapshot.data['view_order'];
        this.slug = this._router.url.split('/');
    });
     console.log(this.slug)
  }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.get_order_details(this.orderId);

    }

  }

  get_order_details(id:number){
    var url='';
    var order_id:any;
    if(this.slug[1]=='approved-order'){
      url='order-details-payment';
      order_id=this.slug[3];
      this.page_name='approved-order';
      //console.log(order_id)
      let orderArr = order_id.split("?");
      order_id = orderArr[0];
    }else{
      url='order-details';
      order_id=id;
      this.page_name='profile';

    }
    if(order_id) {
      this.global.getWebServiceData(url, 'GET', '', order_id).subscribe(data => {
      /*	console.log("**************** Order detaills ********************");
      	console.log(data);
        console.log(data);*/

        if (data.status == 200) {

          this.orders = data.data;
          this.order_status = this.orders['order_status'];
          this.orderId=data.data.id;
          
         /* console.log("*************** Burn loyalty data ***************");
          console.log(this.burnLoyaltyData);*/


        } else {
          // console.log(data);
          this._globalService.showToast('Something went wrong. Please try again.');
        }
      }, err => console.log(err), function() {});
    } else {
      this._globalService.showToast('Order details not available for this order');
    }
  }
 

  navigate_payment_option(page=''){
    if(page==''){

      this._router.navigate(['/profile/payment-options',this.orderId]);
    }else{

      this._router.navigate(['/approved-order/payment-options-approved/'+this.slug[3]]);
    }
  }
  navigateToDetailPage(productSlug) {
    this._router.navigate(['details/'+productSlug]);
    window.scroll(0,0);
  }
 
}
