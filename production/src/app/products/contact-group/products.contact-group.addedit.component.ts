import { Component, OnInit, OnDestroy } from '@angular/core';

import { Router,ActivatedRoute } from '@angular/router';
import { ContactGroupService } from './products.contact-group.service';
import { GlobalService } from '../../global/service/app.global.service';
import { AddEditTransition } from '../.././addedit.animation';
@Component({
  templateUrl: './templates/add_contactgroup.html',
  providers: [ContactGroupService],
  animations: [ AddEditTransition ],
  host: {
    '[@AddEditTransition]': ''
  },

})
export class ContactGroupAddEditComponent implements OnInit,OnDestroy { 

	public response: any;
	public errorMsg: string;
	public successMsg: string;

	public country_list: any;
	public formModel: any = {};

	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public ipaddress: any;


	constructor(
		public _globalService:GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _contactGroupService: ContactGroupService
	) {

	this.ipaddress = _globalService.getCookie('ipaddress');

	}
	
	ngOnInit(){

		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.sub = this._route.params.subscribe(params => {
	       this.formModel.contactId = +params['id']; // (+) converts string 'id' to a number
		});
		
		this._contactGroupService.contactGroupLoad(this.formModel.contactId).subscribe(
	       	data => {

	       		let that = this;
	       		this.response = data;
	       		if(this.formModel.contactId>0){
	       			this.formModel.contactId = this.response.api_status.id;
		            this.formModel.listName = this.response.api_status.name;
		            this.formModel.fromName = this.response.api_status.fromname;
		            this.formModel.ownerName = this.response.api_status.owner_name;
		            this.formModel.replyToEmail = this.response.api_status.reply_email;
		            this.formModel.defaultSubject = this.response.api_status.default_subject;
		            this.formModel.companyName = this.response.api_status.company;
		            this.formModel.myEmail = this.response.api_status.owner_email;
		            this.formModel.subscribed = this.response.api_status.people_subscribe;
		            this.formModel.unsubscribed = this.response.api_status.people_unsubscribe;
		            this.formModel.address = this.response.api_status.address;
		            this.formModel.city = this.response.api_status.city;
		            this.formModel.zip = this.response.api_status.zipcode;
		            this.formModel.country = this.response.api_status.country_id;
		            this.formModel.phone = this.response.api_status.phone;
		            this.formModel.type = this.response.api_status.usertype;
		            this.country_list = this.response.countries;
		            

		            if(this.formModel.subscribed == 'y'){
			      		this.formModel.subscribed = true;	
			      	}else{
			      		this.formModel.subscribed = false;
			      	}

			      	if(this.formModel.unsubscribed == 'y'){
			      		this.formModel.unsubscribed = true;
			      	}else{
			      		this.formModel.unsubscribed = false;
			      	}
	       		}else{
	       			this.country_list = this.response;
	       			this.formModel.contactId = 0;
	       			this.formModel.type="customer";

	       			this.country_list.forEach(function (item: any) {
		              if(item.id==99){
		                that.formModel.country = item.id;         
		              }
		            });
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

	ngOnDestroy(){
		this.sub.unsubscribe();
	}

    addEditContactGroup(form: any){

    	this.errorMsg = '';

    	var data: any = {};
	    data.company_website_id = 1;
      	data.name = this.formModel.listName;
      	data.fromname = this.formModel.fromName;
      	data.owner_name = this.formModel.ownerName;
      	data.reply_email = this.formModel.replyToEmail;
      	data.default_subject = this.formModel.defaultSubject;
      	data.company = this.formModel.companyName;
      	data.address = this.formModel.address;
      	data.city = this.formModel.city;
      	data.zipcode = this.formModel.zip;
      	data.country_id = this.formModel.country;
      	data.phone = this.formModel.phone;
      	data.usertype = this.formModel.type;
      	data.owner_email = this.formModel.myEmail;
      	if(this.formModel.subscribed){
      		data.people_subscribe = 'y';	
      	}else{
      		data.people_subscribe = 'n';
      	}

      	if(this.formModel.unsubscribed){
      		data.people_unsubscribe = 'y';
      	}else{
      		data.people_unsubscribe = 'n';
      	}
      	
        data.ip_address=this.ipaddress;
      	if(this.formModel.contactId<1){
          data.createdby = this._globalService.getUserId();
        }
        data.updatedby = this._globalService.getUserId();
      	
    	
        this._contactGroupService.contactGroupAddEdit(data,this.formModel.contactId).subscribe(
           	data => {
               	this.response = data;
              
               	if(this.response.status==1){
                   this._router.navigate(['/contactlists']);
                   this._globalService.deleteTab(this.tabIndex,this.parentId);
               	}else{
                   
                   this.errorMsg = this.response.message;
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
