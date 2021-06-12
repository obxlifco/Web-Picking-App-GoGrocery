import { Component, OnInit,Inject,ViewChild, PLATFORM_ID } from '@angular/core';
import { Router } from '@angular/router';
import { MatDialog,MatDialogRef,MAT_DIALOG_DATA,MatMenuTrigger } from '@angular/material';
import { GlobalService } from '../../../global/service/app.global.service';
import { Global } from '../../../global/service/global';
import {DialogsService} from '../../../global/dialog/confirm-dialog.service';
import { PageSetupService } from './page.setup.service';
import { isPlatformBrowser } from '@angular/common';

@Component({
  templateUrl: './templates/add-edit-page.html',
  providers: [PageSetupService]
})
export class AddEditPageComponent implements OnInit {


	public formModel: any = {};
	public successMsg: string;
	public errorMsg: string;
	public ipaddress:string;

	constructor(
				public _globalService: GlobalService,
                public _pageSetupService: PageSetupService,
                public dialogRef: MatDialogRef<AddEditPageComponent> ,
                public dialog: MatDialog,
                @Inject(MAT_DIALOG_DATA) public data: any
    ){
        dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
        this.ipaddress = _globalService.getCookie('ipaddress');
    } 


	ngOnInit(){
		this.formModel.id = this.data.page_id;
		if(this.formModel.id){
			this._pageSetupService.pageLoad(this.formModel.id).subscribe(
		        data => {
		            if(data.status){
		            	this.formModel = Object.assign({},data.api_status);
		            }
		        },
		        err => {
		         this._globalService.showToast('Something went wrong. Please try again.');
		        },
		        function(){
		            //completed callback
		        }
		    );
		}
	}

  	createUrl(val:string){

	    var slug = '';
	    if(val && val!=''){
	    	slug = val.toLowerCase().replace(/[^\w ]+/g,'-').replace(/ +/g,'-');
			this.formModel.url = slug;	
	    }
	}

  	addEditPage(form:any){

        //console.log("************** Form data **************",form);
	    this.errorMsg = '';
	    var data: any = {};
	    data = Object.assign({},this.formModel);
	    data.ip_address=this.ipaddress;
	    data.createdby_id = this._globalService.getUserId();
	    data.modifiedby_id = this._globalService.getUserId();

	    data.company_website_id = this._globalService.getWebsiteId();
	    data.layout = 1;
	    data.device = 'web';
	    data.saved_page = data.url;

	    
	    this._pageSetupService.pageAddEdit(data,this.formModel.id).subscribe(
	        data => {
	            if(data.status==1){
	              this.dialogRef.close(true);
	            }else{
	              this.errorMsg = data.message;
	            }
	        },
	        err => {
	         this._globalService.showToast('Something went wrong. Please try again.');
	        },
	        function(){
	            //completed callback
	        }
	    );

	}		

	closeDialog(){

		this.dialogRef.close();
	}
}	


@Component({
  templateUrl: './templates/manage-page.html',
  providers: [PageSetupService,Global]
})
export class ManagePageComponent implements OnInit {


	public page_list: any = [];
	public successMsg: string;
	public errorMsg: string;
	public ipaddress:string;

	constructor(
				public _global: Global,
				public _dialogsService: DialogsService,
                public _globalService: GlobalService,
                public _pageSetupService: PageSetupService,
                private _router: Router,
                public dialogRef: MatDialogRef<AddEditPageComponent> ,
                public dialog: MatDialog,
				@Inject(MAT_DIALOG_DATA) public data: any,
				@Inject(PLATFORM_ID) private platformId: Object

    ) {
        dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
        this.ipaddress = _globalService.getCookie('ipaddress');
    } 


	ngOnInit(){
		if (isPlatformBrowser(this.platformId)) {
			this.pageLoad();
		}
	}

	pageLoad(){
		this._pageSetupService.getAllPages().subscribe(
	        data => {
	            if(data.status){
	            	this.page_list = data.api_status;
	            }
	        },
	        err => {
	         this._globalService.showToast('Something went wrong. Please try again.');
	        },
	        function(){
	            //completed callback
	        }
	    );
	}

	dialogRefEditPage: MatDialogRef<AddEditPageComponent> | null;
	editPage(page_id:number){

		this.dialogRef.close();

	    let data:any = { page_id: page_id};
	    this.dialogRefEditPage = this.dialog.open(AddEditPageComponent,{data: data,maxHeight:500,maxWidth:500});
	    this.dialogRefEditPage.afterClosed().subscribe(result => {

	    });
	}

	deletePage(page_id: number){
		this._dialogsService.confirm('Warning', 'Do you really want to delete selected record?').subscribe(res => {
	    	if(res){
		    	this._global.doStatusUpdate('EngageboostPages',[page_id],2).subscribe(
		           	data => {
		           		//this._globalService.showToast(data.Message);
		           		this.pageLoad();
		           	},
		           	err => console.log(err),
		           	function(){
		           	}
		        );
	    	}
	    });
	}
	

	closeDialog(){

		this.dialogRef.close();
	}

	redirectPage(slug:string){

		if(slug && slug!=''){
			this.dialogRef.close();
			this._router.navigate(['/editor/page/'+slug]);
		}
	}
}

@Component({
  templateUrl: './templates/add-edit-navigation.html',
  providers: [PageSetupService,Global]
})
export class AddEditNavigationComponent implements OnInit {

	public page_list: any = [];
	public category_list: any = [];
	public enable_parent_menu:boolean = false;
	public enable_label_menu:boolean = true;
	public parent_menu: any = [];
	public formModel:any = {};
	public successMsg: string;
	public errorMsg: string;
	public ipaddress:string;

	@ViewChild(MatMenuTrigger) trigger: MatMenuTrigger;
	constructor(
				public _global: Global,
				public _dialogsService: DialogsService,
                public _globalService: GlobalService,
                public _pageSetupService: PageSetupService,
                public dialogRef: MatDialogRef<AddEditPageComponent> ,
                public dialog: MatDialog,
                @Inject(MAT_DIALOG_DATA) public data: any
    ){
        dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
        this.ipaddress = _globalService.getCookie('ipaddress');
    }


	ngOnInit(){
		this.formModel.id = this.data.nav_id;
		
		if(this.formModel.id){
			this._pageSetupService.navigationLoad(this.formModel.id,this.data.header_footer).subscribe(
		        data => {
		            if(data.status){
		            	this.parent_menu = data.header_menu;
		            	this.formModel = data.api_status[0];
		            	if(this.data.header_footer==1 && this.formModel.parent_id){
		            		this.enable_label_menu = false;
		            	}else if(this.data.header_footer==0 && this.formModel.parent_id){
		            		this.enable_parent_menu = true;
		            	}
		            }
		        },
		        err => {
		         this._globalService.showToast('Something went wrong. Please try again.');
		        },
		        function(){
		            //completed callback
		        }
		    );	
		}else{
			this._pageSetupService.getAllPages().subscribe(
		        data => {
		            if(data.status){
		            	this.page_list = data.api_status;
		            }
		        },
		        err => {
		         this._globalService.showToast('Something went wrong. Please try again.');
		        },
		        function(){
		            //completed callback
		        }
		    );	
		}
		
	}

	changeMenuPage(){

		if(this.formModel.page_id=='cat'){

			this._pageSetupService.getAllCategories().subscribe(
		        data => {
		            this.category_list = data.parent_child;
		        },
		        err => {
		         this._globalService.showToast('Something went wrong. Please try again.');
		        },
		        function(){
		            //completed callback
		        }
		    );
		}
		
	}

	showSubMenu(event:any){

		if(event.checked){
			this.enable_parent_menu = true;
			this._pageSetupService.getAllParents(this.data.header_footer).subscribe(
		        data => {
		            this.parent_menu = data.header_menu;
		        },
		        err => {
		         this._globalService.showToast('Something went wrong. Please try again.');
		        },
		        function(){
		            //completed callback
		        }
		    );

		}else{
			this.enable_parent_menu = false;
			this.parent_menu = [];
		}
	}

	setCategory(category:any){
		this.formModel.category_id = category.id;
		this.formModel.category_name = category.name;


		this.trigger.closeMenu();
	}

	addEditNavigation(form:any){

		this.errorMsg = '';
	    var data: any = {};
	    data = Object.assign({},this.formModel);
	    data.ip_address=this.ipaddress;
	    data.createdby_id = this._globalService.getUserId();
	    data.modifiedby_id = this._globalService.getUserId();
	    data.company_website_id = this._globalService.getWebsiteId();
	    data.device = 'web';
	    if(this.formModel.page_id=='cat'){
	    	delete data["page_id"];
	    }else{
	    	delete data["category_id"];
	    }

	    if(!this.formModel['parent_id']){
	    	data.parent_id = 0;
	    }

	    data.flag = this.data.header_footer;
	    // for footer menu
	    if(this.data.header_footer){
	    	data.label = this.formModel.label;
	    }
	   
	    this._pageSetupService.navigationAddEdit(data,this.formModel.id,this.data.header_footer).subscribe(
	        data => {
	            if(data.status==1){
	              this.dialogRef.close(true);
	              this._globalService.showToast(data.message);
	            }else{
	              this.errorMsg = data.message;
	            }
	        },
	        err => {
	         this._globalService.showToast('Something went wrong. Please try again.');
	        },
	        function(){
	            //completed callback
	        }
	    );
	}

	closeDialog(){

		this.dialogRef.close();
	}	

	showFooterLabel(event:any){
		if(event.checked){
			this.enable_label_menu = true;
			
		}else{
			this.enable_label_menu = false;
			this._pageSetupService.getAllParents(this.data.header_footer).subscribe(
		        data => {
		            this.parent_menu = data.header_menu;
		        },
		        err => {
		         this._globalService.showToast('Something went wrong. Please try again.');
		        },
		        function(){
		            //completed callback
		        }
		    );
		}
	}	

}	


@Component({
  templateUrl: './templates/manage-page-navigation.html',
  providers: [PageSetupService,Global]
})
export class ManageNavigationComponent implements OnInit {

	public menu_list: any = [];
	public successMsg: string;
	public errorMsg: string;
	public ipaddress:string;
	constructor(
				public _global: Global,
				public _dialogsService: DialogsService,
                public _globalService: GlobalService,
                public _pageSetupService: PageSetupService,
                public dialogRef: MatDialogRef<AddEditNavigationComponent> ,
                public dialog: MatDialog,
				@Inject(MAT_DIALOG_DATA) public data: any,
				@Inject(PLATFORM_ID) private platformId: Object

    ){
        dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
        this.ipaddress = _globalService.getCookie('ipaddress');
    }

	ngOnInit(){
		if (isPlatformBrowser(this.platformId)) {

		this.navigationLoad();
		}
	}

	navigationLoad(){
		this._pageSetupService.getHeaderMenus(this.data.header_footer).subscribe(
	        data => {
	            
	            this.menu_list = Object.assign([],data.header_menu);
	            this.menu_list.forEach(parent=>{

	            	parent['child'] = [];
	            	data.child.forEach(child=>{
	            		if(parent.id==child.parent_id){
	            			parent.child.push(child);
	            		}
	            	});
	            });

	        },
	        err => {
	         this._globalService.showToast('Something went wrong. Please try again.');
	        },
	        function(){
	            //completed callback
	        }
	    );
	}

	dialogRefAddEditNav: MatDialogRef<AddEditNavigationComponent> | null;
	addEditNavigation(nav_id:number = 0){

		this.dialogRef.close();

	    let data:any = { nav_id: nav_id, header_footer: this.data.header_footer};
	    this.dialogRefAddEditNav = this.dialog.open(AddEditNavigationComponent,{data: data,minHeight:'400px',minWidth:'500px'});
	    this.dialogRefAddEditNav.afterClosed().subscribe(result => {

	    });
	}

	closeDialog(){

		this.dialogRef.close();
	}	

	deleteNavigation(nav_id:number){

		this._dialogsService.confirm('Warning', 'Do you really want to delete selected record?').subscribe(res => {
	    	if(res){
		    	this._global.doStatusUpdate('EngageboostCmsMenus',[nav_id],2).subscribe(
		           	data => {
		           		//this._globalService.showToast(data.Message);
		           		this.navigationLoad();
		           	},
		           	err => console.log(err),
		           	function(){
		           	}
		        );
	    	}
	    });
	}

}	