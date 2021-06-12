import { Component, OnInit, AfterViewInit, Input, ViewChild, ComponentFactoryResolver ,Inject, PLATFORM_ID} from '@angular/core';
import { Global } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService} from 'ngx-cookie';
import { DialogsService} from '../../global/dialog/confirm-dialog.service';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { MatDialog,MatDialogRef,MAT_DIALOG_DATA } from '@angular/material';
import { isPlatformBrowser } from '@angular/common';

@Component({
	selector: 'footer-part',
	templateUrl: './footer.component.html',
	styleUrls: ['./footer.component.css'],
	providers: [Global]
})
export class FooterComponent {
	@Input() isCMS: boolean = false;
	@Input() pageType: number = 1;
	public menu_list:any = [];
	public today:any;
	public lang_code:string='en';
	public company_name:string = '';
	public is_dist:boolean = false;
	public page_uri:string;
	
	public formModel: any = {};
	public emailVal:string;
	public response:any;
	public errorMsg: string;
	public currentYear;
	constructor(
		private _global: Global,
		private _cookieService: CookieService,
		private _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _dialogsService: DialogsService,
		@Inject(PLATFORM_ID) private platformId: Object

	) {
    	this.today = Date.now();
    	let globalData = this._cookieService.getObject('globalData');
		if(globalData['lang_code']){
			this.lang_code = globalData['lang_code'];
		}

      	this._globalService.langChange$.subscribe(value=>{
        	this.lang_code = value;
      	});
      	
      	this.company_name = this._globalService.getFrontedCompanyName();
      	if(globalData['website_id']>1){
      		this.is_dist = true;
      	}else{
      		this.is_dist = false;
      	}
      	if (this._router.url.indexOf('/base') > -1) {
         	this.page_uri = '/base';
        }
  	}

  	ngOnInit() {
  		this.currentYear = (new Date()).getFullYear();
  		// this._global.getFooterMenus().subscribe(
	    //     data => {
	    //        	this.menu_list = Object.assign([],data.header_menu);
	    //         this.menu_list.forEach(parent=>{

	    //         	parent['child'] = [];
	    //         	data.child.forEach(child=>{
	    //         		if(parent.id==child.parent_id){
	    //         			parent.child.push(child);
	    //         		}
	    //         	});
	    //         });
	    //         console.log(this.menu_list)
	    //     },
	    //     err => {
	    //      //this._globalService.showToast('Something went wrong. Please try again.');
	    //     },
	    //     function(){
	    //         //completed callback
	    //     }
		// );
		if (isPlatformBrowser(this.platformId)) {
			this._global.getHeaderMenus().subscribe(
				data => {
					this.menu_list = Object.assign([], data.header_menu);
					this.menu_list.forEach(parent => {
	
						parent['child'] = [];
						data.child.forEach(child => {
							if (parent.id == child.parent_id) {
								parent.child.push(child);
							}
						});
					});
			  
				},
				err => {
					//this._globalService.showToast('Something went wrong. Please try again.');
				},
				function () {
					//completed callback
				}
			);
		}
  	}

  	vaidateNewletter() {
		if(this.formModel.emailVal && this.formModel.emailVal.trim()!='') {
   		} else {
   			this._dialogsService.alert('Error', 'Email is required!').subscribe(res => {});
   		}
	}

  	sendMail(form:any) {
		var userRegData ={};
		userRegData = this.formModel;
		userRegData['email'] = userRegData['emailVal'];
		userRegData['ip_address'] = this._globalService.getCookie('ipaddress');
		//this._globalService.showLoaderSpinner(true);
		this._global.newletter_mail(userRegData).subscribe(	           
           	data => {
           	  this.response = data;
           	  if(data.status) {
           	  	this._dialogsService.alert('Thankyou!', this.response.message).subscribe(res => {});  	
           	  } else {
           	  	this._globalService.showLoaderSpinner(false);
           	  	this.errorMsg = this.response.message;
	        	this._globalService.showToast(this.errorMsg);
           	  }
              //form.reset();
           },
           err => {
           	this._globalService.showLoaderSpinner(false);
           	this.errorMsg = this.response.message;
	        this._globalService.showToast(this.errorMsg);
           },
           ()=>{
               //completed callback
               this._globalService.showLoaderSpinner(false);
           }
        );
	}
	/**
	 * Method for navigating to url
	*/
	navigateToUrl(url) {
		this._router.navigate([url]);

	}
}
