import { Component, OnInit, ElementRef, Renderer } from '@angular/core';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import { MenuService } from './app.menu.service';
import { GlobalService } from '../global/service/app.global.service';
@Component({
	selector: '<left-menu></left-menu>',
	templateUrl: './templates/left.html',
	providers: [MenuService]
})

export class LeftMenuComponent implements OnInit {
	constructor(
		private _menuService: MenuService,
		private globalService: GlobalService,
		private elRef: ElementRef,
		private router: Router,
		private activatedRoute: ActivatedRoute,
		public renderer: Renderer
	) {
		this.innerWidth = (window.screen.width);
	}
	public menu_list = {
		Frontend: [],
		Admin: []
	};
	public admin_menu: boolean = false;
	public user_menu: boolean = true;
	public menu_text: string = 'Admin';
	public current_url: any;
	public innerWidth: any;
	public selected: number;
	ngOnInit() {
		this.current_url = this.router.url;
		this.current_url = this.current_url.replace('/', '')
        /*this.router.events
    		.filter((event) => event instanceof NavigationEnd)
    		.map(() => this.activatedRoute)
    		.map((route) => {
      		while (route.firstChild) route = route.firstChild;
      		return route;
    		})
    		.filter((route) => route.outlet === 'primary')
    		.mergeMap((route) => route.data)
    		.subscribe((event) => {
    			this.current_url=this.router.url;
    			this.current_url=this.current_url.replace('/','')
    		});	*/
		this._menuService.menuInit().subscribe(
			data => {
				this.menu_list = data;
			},
			err => console.log(err),
			function () {
				//completed callback
			}
		);
	}

	toggleMenu() {
		this.admin_menu = !this.admin_menu;
		this.user_menu = !this.user_menu;
		if (this.admin_menu) {
			this.menu_text = 'Back to BMS';
		} else {
			this.menu_text = 'Admin';
		}
	}

	setActive(select_id: number, is_parent: number) {
		if (is_parent > 0 || select_id == 1) {
			this.selected = select_id;
		}
		if (this.innerWidth < 1000 && is_parent == 0) {
			document.querySelector('.maincontainer').classList.add('full');
		}
		setTimeout(() => {
			if (this.innerWidth > 700 && is_parent > 0) {
				var all_ele = document.querySelectorAll('.sub-li');
				for (var i = 0, len = all_ele.length; i < len; i++) {
					this.renderer.setElementClass(all_ele[i], 'show', false);
				}
				document.querySelector('.parent').classList.add('show');
			} else if (this.innerWidth > 700 && is_parent == 0) {
				if (document.querySelector('.show').classList) {
					//document.querySelector('.show').classList.remove('show');
				}
			}
		}, 500);
	}

	changeClass() {
		if (document.querySelector('.maincontainer').classList.contains('full')) {
			document.querySelector('.maincontainer').classList.remove('full');
		} else {
			document.querySelector('.maincontainer').classList.add('full');
		}

		// if (document.querySelector('.innertab_sec').classList.contains('full_intab')) {
		// 	document.querySelector('.innertab_sec').classList.remove('full_intab');
		// } else {
		// 	document.querySelector('.innertab_sec').classList.add('full_intab');
		// }

		if (document.querySelector('.bottom_fixedpart').classList.contains('back_expand')) {
			document.querySelector('.bottom_fixedpart').classList.remove('back_expand');
		} else {
			document.querySelector('.bottom_fixedpart').classList.add('back_expand');
		}
	}
}