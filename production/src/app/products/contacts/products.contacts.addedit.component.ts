import { Component, OnInit, OnDestroy } from '@angular/core';

import { Router,ActivatedRoute } from '@angular/router';
import { ContactService } from './products.contacts.service';
import { GlobalService } from '../../global/service/app.global.service';
import { AddEditTransition } from '../.././addedit.animation';

@Component({
  templateUrl: './templates/add_contacts.html',
  providers: [ContactService],
  animations: [ AddEditTransition ],
  host: {
    '[@AddEditTransition]': ''
  },

})
export class ContactsAddEditComponent implements OnInit,OnDestroy { 

	public response: any;
	public errorMsg: string;
	public successMsg: string;

	public contact_list: any;
	public country_list: any;
	public formModel: any = {};

	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public ipaddress: any;
	public maxDate: any;


	constructor(
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _contactService: ContactService
	) {

	this.ipaddress = _globalService.getCookie('ipaddress');

	}
	
	ngOnInit(){

		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.sub = this._route.params.subscribe(params => {
	       this.formModel.contactId = +params['id']; // (+) converts string 'id' to a number
		});
		
		this._contactService.contactLoad(this.formModel.contactId).subscribe(
	       	data => {

	       		let that = this;
	       		this.response = data;
	       		if(this.formModel.contactId>0){
	       			this.formModel.contactId = this.response.api_status.id;
		            this.formModel.firstName = this.response.api_status.first_name;
		            this.formModel.lastName = this.response.api_status.last_name;
		            this.formModel.title = this.response.api_status.title;
		            this.formModel.email = this.response.api_status.email;
		            this.formModel.emailFormat = this.response.api_status.email_format;
		            this.formModel.activityStatus = this.response.api_status.activity_status;
		            this.formModel.confirmStatus = this.response.api_status.confirmation_status;
		            this.formModel.zip = this.response.api_status.zipcode;
		            this.formModel.country = this.response.api_status.country.id;
		            this.formModel.phone = this.response.api_status.phone;
		            this.formModel.mobile = this.response.api_status.mobile;
		            this.formModel.fax = this.response.api_status.fax;
		            this.formModel.dob = new Date(this.response.api_status.date_of_birth);
		            this.formModel.anniDate = new Date(this.response.api_status.anniversary_date);
		            this.formModel.contactGroup = this.response.api_status.contact_list.id;
		            this.contact_list = this.response.ContactsList;
		            this.country_list = this.response.Countries;
		            
	       		}else{
	       			this.contact_list = this.response.ContactsList;
	       			this.country_list = this.response.Countries;
	       			this.formModel.contactId = 0;

		            this.country_list.forEach(function (item: any) {
		              if(item.id==99){
		                that.formModel.country = item.id;         
		              }
		            });

		        }
		        this.maxDate = new Date();
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

    addEditContacts(form: any){

    	this.errorMsg = '';

    	var data: any = {};
	    data.ip_address=this.ipaddress;
      	data.company_website_id = 1;	
      	data.customer_id = this._globalService.getUserId();
      	data.user_name = this.formModel.firstName+" "+this.formModel.lastName;	
      	data.first_name = this.formModel.firstName;
      	data.last_name = this.formModel.lastName;
      	data.title = this.formModel.title;
      	data.email = this.formModel.email;
      	data.email_format = this.formModel.emailFormat;
      	data.activity_status = this.formModel.activityStatus;
      	data.confirmation_status = this.formModel.confirmStatus;
      	if(this.formModel.dob!=undefined){
        	data.date_of_birth = this.formModel.dob;  
      	}
      
      	if(this.formModel.anniDate!=undefined){
        	data.anniversary_date = this.formModel.anniDate;  
      	}
      
      	data.zipcode = this.formModel.zip;
      	data.country_id = this.formModel.country;
      	data.fax = this.formModel.fax;
      	data.mobile = this.formModel.mobile;
      	data.phone = this.formModel.phone;
      	data.contact_list_id = this.formModel.contactGroup;
      	if(this.formModel.userId<1){
          data.createdby = this._globalService.getUserId();
        }
        data.updatedby = this._globalService.getUserId();
      	
        this._contactService.contactAddEdit(data,this.formModel.contactId).subscribe(
           	data => {
               	this.response = data;
              
               	if(this.response.status==1){
                   this._router.navigate(['/contacts']);
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
