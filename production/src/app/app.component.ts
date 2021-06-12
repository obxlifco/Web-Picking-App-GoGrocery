import { mergeMap, map, filter} from 'rxjs/operators';
import { Component, Injectable, OnInit, Inject, NgZone, AfterViewInit } from '@angular/core';
import { Headers, BaseRequestOptions, RequestOptions } from '@angular/http';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import { Title, DOCUMENT } from '@angular/platform-browser';
import { CookieService} from 'ngx-cookie';
import { GlobalService } from './global/service/app.global.service';
import { Global } from './global/service/global';
import { routerTransition } from './router.animations';
@Component({
  selector: 'my-app',
  templateUrl: './app.component.html',
  providers: [ Global ],
  animations: [ routerTransition ],
})
export class AppComponent implements OnInit, AfterViewInit {
	innerWidth: any;
	navLinks: any=[];
	tabs: any;
	isSidebarVisible: boolean;
	public showSpinnerLoaded: boolean = false;
	constructor(
		private router: Router,
		private activatedRoute: ActivatedRoute,
		private titleService: Title,
		@Inject(DOCUMENT) private document: any,
	  	private globalService: GlobalService,
	  	private global: Global,
	  	private zone:NgZone,
	  	private _cookieService:CookieService,
	) {
	  	this.innerWidth = (window.screen.width);
	  	// set user ip address in cookie
	  	this._cookieService.put('ipaddress', '192.168.0.125');
	  	/*
	  	this.global.Ipaddress().subscribe(
			data => {
			  this._cookieService.put('ipaddress', data.ip);
			}
	  	);
	  	*/
	}

  	ngAfterViewInit(){
		this.globalService.loadSpinnerChange$.subscribe(
			(value) => {
				this.showSpinnerLoaded = value;
			}
		);
  	} 

  // Initialization method
	ngOnInit() {
		// route state change event
		this.router.events.pipe(
			filter((event) => event instanceof NavigationEnd),
			map(() => this.activatedRoute),
			map((route) => {
				while (route.firstChild) route = route.firstChild;
				return route;
			}),
			filter((route) => route.outlet === 'primary'),
			mergeMap((route) => route.data),).subscribe((event) => {
				this.titleService.setTitle(event['title']+':GoGrocery'); //set title of the html page
				//this.titleService.setTitle(event['title']); //set title of the html page
				if(event['is_login']){ //check if current route is before logged in
				  //swap stylesheets according to route
						// if(this.document.getElementById('theme').getAttribute('href')=='assets/css/style.css'){
			  //       this.document.getElementById('theme').setAttribute('href','assets/css/login-style.css'); 
			  //     }
				  	this.isSidebarVisible = false; //hide sidebar from the page layout 
				} else { // current route is after logged in
				  	//swap stylesheets according to route
				  	// if(this.document.getElementById('theme').getAttribute('href')=='assets/css/login-style.css'){
				  	//   this.document.getElementById('theme').setAttribute('href','assets/css/style.css');
				  	// }
					this.isSidebarVisible = true; //show sidebar on the page layout if route is after logged in
				  	this.zone.run(() => { // <== added
					   this.isSidebarVisible = true;
			   		});
				}
			});
	}
	// Get the current or activated route state
	getState(outlet: any) {
	  return outlet.activatedRouteData.state;
	}
}
