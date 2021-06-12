import { Component, OnInit, OnDestroy, AfterViewInit, Input, ViewChild, ComponentFactoryResolver, ViewContainerRef, ElementRef, Inject } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';
import { Router, ActivatedRoute } from '@angular/router';
import { GlobalService } from '../../global/service/app.global.service';
import { Global } from '../../global/service/global';
import { PageService } from '../../global/service/app.page.service';

import { WidgetDirective } from '../cms/widgets/widget.directive';
import { WidgetComponent } from '../cms/widgets/widget.component';
import { Widget } from '../cms/widget';

import { WidgetsService } from '../cms/widgets.service';
import { CookieService } from 'ngx-cookie';
import { LOCAL_STORAGE } from '@ng-toolkit/universal';

@Component({
	templateUrl: './templates/page.html',
	providers: [PageService,WidgetsService],
	host: {
		'(document:click)': 'onClick($event)',
	},
})
export class PageComponent implements OnInit {
	public sub: any;
	public page_slug: string;
	public cms_widgets: any = [];
	public lang_code: string;
	public response: any;
	public page_details: any = {};
	public company_name: string = '';
	public agCode: string = '';
	public currentUrl: string = '';

	@Input() widgets: Widget[];
	@ViewChild(WidgetDirective) widgetHost: WidgetDirective;
	subscription: any;
	constructor(@Inject(LOCAL_STORAGE) private localStorage: any, 
		private _pageService: PageService,
		public _globalService: GlobalService,
		private componentFactoryResolver: ComponentFactoryResolver,
		private _widgetsService: WidgetsService,
		private _route: ActivatedRoute,
		private _router: Router,
		public viewContainerRef: ViewContainerRef,
		private meta: Meta,
		private titleService: Title,
		private _cookieService: CookieService,
		public _global: Global,
		private elRef: ElementRef
	) {
		let globalData = this._cookieService.getObject('globalData');
		if (globalData['lang_code']) {
			this.lang_code = globalData['lang_code'];
		}
		this._globalService.langChange$.subscribe(value => {
			if (this.lang_code != value) {
				this.lang_code = value;
				this.ngOnInit();
			}
		});

		this.company_name = this._globalService.getFrontedCompanyName();
	}

	ngOnInit() {
		if (this.sub != undefined)
			this.sub.unsubscribe();

		this.sub = this._route.params.subscribe(params => {
			if (params['slug'] && params['slug'] != '') {
				this.page_slug = params['slug'];

			} else {
				this.page_slug = 'home';

			}
			this.loadCMS();

		});

		// Agent code....
		this.currentUrl = this._router.url;
		//console.log(this.currentUrl.search("reffer/"));
		if (this.currentUrl.search("reffer/")) {
			if (this._route.snapshot.params.id && this._route.snapshot.params.id != '') {
				this.agCode = atob(this._route.snapshot.params.id);
			}
			if (this.agCode != '') {
				this._cookieService.put('agentCode', this.agCode);
			}
		}
		//console.log(this.agCode + '>>' + this.page_slug);
	}


	loadCMS() {
		
		let data: any = { url: this.page_slug, template_id: 1, company_website_id: this._globalService.getFrontedWebsiteId(), lang: this.lang_code }
		this._pageService.pageLoad(data).subscribe(
			data => {
				console.log("*************** Page data ****************");
				console.log(data);
				if (data.status) {
					this.response = Object.assign({}, data);
					if (this.lang_code && this.lang_code == 'th') {
						this.titleService.setTitle('GoGrocery: ' + ((data.page_title_th != null && data.page_title_th != '') ? data.page_title_th : data.page_title)); //set title of the page
					} else {
						this.titleService.setTitle('GoGrocery:'+data.page_title); //set title of the page
					}
					this.meta.updateTag({ name: 'description', content: data.page_meta_description });
					this.meta.updateTag({ name: 'keywords', content: data.page_meta_keywords });
					this.page_details['page_title'] = data.page_title;
					this.page_details['page_type'] = data.page_type;
					this.page_details['page_data'] = data.page_data;
					this.page_details['page_id'] = data.page_id;
					//alert(data.page_id)
					//if(data.page_type==0){
					this.cms_widgets = data.cms_widgets;
					this.loadComponent();
					//}

					if (data.funnel_data.length) {
						let stored_funnel_data: any = [];
						if (this.localStorage.getItem('funnel_data') && this.localStorage.getItem('funnel_data') != null) {
							stored_funnel_data = JSON.parse(this.localStorage.getItem('funnel_data'));
						}

						data.funnel_data.forEach((item) => {
							if (item.landing_or_thankyou == 1) { // landing page
								let single_record: any = {};
								single_record.funnel_id = item.funnel_id;
								single_record.funnel_target = item.funnel_target;
								single_record.funnel_type = item.funnel_type;
								single_record.products = item.products;

								let already_exist: any = stored_funnel_data.filter(funnel => funnel.funnel_id == item.funnel_id);
								if (already_exist.length == 0) {
									stored_funnel_data.push(single_record);
									this.funnelTrack(item.funnel_id);
								}
							} else { // Thankyou page
								if (stored_funnel_data.length) {
									stored_funnel_data.forEach((inner_item, index) => {
										if (item.funnel_id == inner_item.funnel_id) {
											this.funnelTrack(item.funnel_id);
											stored_funnel_data.splice(index, 1);
										}
									});
								}
							}
						});
						this.localStorage.setItem('funnel_data', JSON.stringify(stored_funnel_data));
					}
				}
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}


	ngOnDestroy() {
		this.sub.unsubscribe();
	}

	loadComponent() {
		let page_details: any = { page_id: this.page_details.page_id, page_name: this.page_details.page_title };
		this.widgetHost.viewContainerRef.clear();
		this.cms_widgets.forEach(item => {
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

	funnelTrack(funnel_id: number) {
		let req_data: any = {};
		req_data.funnel_id = funnel_id;
		req_data.website_id = this._globalService.getWebsiteId();
		req_data.page_id = this.page_details.page_id;
		req_data.page_url = '/page/' + this.page_slug;
		req_data.user_id = this._globalService.getCustomerId();
		req_data.ip_address = (this._globalService.getCookie('ipaddress')) ? this._globalService.getCookie('ipaddress') : '';
		this._global.funnelTrack(req_data).subscribe(
			data => {

			},
			err => {
			},
			() => {
				//completed callback
			}
		);
	}

	onClick(event: any) {

		if (event.target.id == 'form_save') {
			event.preventDefault();
			var myForm = this.elRef.nativeElement.querySelector('#funnelForm');
			let form_data: any = {};
			for (var i = 0; i < myForm.elements.length; i++) {
				if (myForm.elements[i].type != 'button' && myForm.elements[i].type != 'submit') {
					form_data[myForm.elements[i].name] = myForm.elements[i].value;
				}
			}

			let data: any = {};
			data['company_website_id'] = this._globalService.getFrontedWebsiteId();
			data['page_name'] = this.page_details.page_title;
			data['page_id'] = this.page_details.page_id;
			data['form_data'] = JSON.stringify(form_data);
			this._global.cmsFormSubmit(data).subscribe(
				data => {
					if (this.response.funnel_data[0].thankyou_slug != '') {
						this._router.navigate(['/page/' + this.response.funnel_data[0].thankyou_slug]);
					} else {
						this._router.navigate(['/']);
					}

				},
				err => {

				},
				function () {
					//completed callback
				}
			);
		}
	}

}