import { Component, OnInit, AfterViewInit, Input, ViewChild, ComponentFactoryResolver, Inject, PLATFORM_ID} from '@angular/core';
import { Meta,Title } from '@angular/platform-browser';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import { GlobalService } from '../../global/service/app.global.service';
import { LoaderService } from '../../global/service/loader.service';
import { HomeService } from './app.home.service';
import { WidgetDirective } from '../cms/widgets/widget.directive';
import { WidgetComponent } from '../cms/widgets/widget.component';
import { Widget }      from '../cms/widget';
import { WidgetsService } from '../cms/widgets.service';
import {CookieService} from 'ngx-cookie';
import {DialogsService} from '../../global/dialog/confirm-dialog.service';
import { isPlatformBrowser } from '@angular/common';


@Component({
  // templateUrl: './templates/home.html',
  template: `<ng-template widget-host></ng-template>`,
  providers: [HomeService]
})
export class HomeComponent implements OnInit,AfterViewInit{  
	public cms_widgets: any = [];
	public lang_code:string;
	public page_details:any={};
	public company_name:string = '';
	public currentUrl:string= '';
	@Input() widgets: Widget[];
  	@ViewChild(WidgetDirective) widgetHost: WidgetDirective;
  	subscription: any;
	constructor(
		private _homeService: HomeService, 
		public _globalService: GlobalService,
		private componentFactoryResolver: ComponentFactoryResolver, 
		private _widgetsService: WidgetsService,
		private _cookieService:CookieService,
		private meta: Meta,
		private titleService: Title,
		private activatedRoute: ActivatedRoute,
		private _dialogsService: DialogsService,
		private _router: Router,
		private _loader:LoaderService,
		@Inject(PLATFORM_ID) private platformId: Object
	){

		let globalData = this._cookieService.getObject('globalData');
		this.lang_code = 'en';
      	if(globalData['lang_code']){
        	this.lang_code = globalData['lang_code'];
      	}
      	this._globalService.langChange$.subscribe(value=>{
        	this.lang_code = value;
        	this.ngOnInit();
      	});
      	
      	this.company_name = this._globalService.getFrontedCompanyName();
	}

	ngOnInit() {
		this.currentUrl = this._router.url; 
		let data:any = {url: 'home',template_id:1,company_website_id:this._globalService.getFrontedWebsiteId(),lang: this.lang_code}
		this._loader.show();
		
		if (isPlatformBrowser(this.platformId)) {
			this._homeService.pageLoad(data).subscribe(
				data => {
				  if(data.status) {
					  if(this.lang_code && this.lang_code=='th'){
						  this.titleService.setTitle('GoGrocery: '+((data.page_title_th!=null && data.page_title_th!='')?data.page_title_th:data.page_title)); //set title of the page
					  } else {
						  this.titleService.setTitle('GoGrocery: '+data.page_title); //set title of the page
					  }
					  this.page_details['page_title'] = data.page_title;
					  this.page_details['page_id'] = data.page_id;
					  this.meta.updateTag({ name: 'description', content: data.page_meta_description });
					  this.meta.updateTag({ name: 'keywords', content: data.page_meta_keywords });
						this.cms_widgets = data.cms_widgets;
						this.loadComponent();
				  }
				},
				err => {
				  this._globalService.showToast('Something went wrong. Please try again.');
				},
				() => this._loader.hide()
		  );
		}
		

	}
	ngAfterViewInit() {

	}
	
  	loadComponent() {
  		let page_details: any = {page_id: this.page_details.page_id, page_name: this.page_details.page_title};
  			/*console.log("************ Widget factory  data ********************");
	    	console.log(this.cms_widgets);*/
	    this.cms_widgets.forEach(item =>{
	    	let widget_data = JSON.parse(item.property_value);
	    
	      	let componentFactory = this.componentFactoryResolver.resolveComponentFactory(this._widgetsService.components[widget_data.component]);
	      	let viewContainerRef = this.widgetHost.viewContainerRef;
	      	viewContainerRef.clear();
	      	setTimeout(() => {
	        	let componentRef = viewContainerRef.createComponent(componentFactory);
	        	(<WidgetComponent>componentRef.instance).data = widget_data.insertables;
	        	(<WidgetComponent>componentRef.instance).page_data = page_details;
	      	}); 
	    });
    }
}