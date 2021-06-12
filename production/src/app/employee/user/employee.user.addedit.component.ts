import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { UserService } from './employee.user.service';
import { GlobalService } from '../../global/service/app.global.service';
import { Global } from '../../global/service/global';
import { AddEditTransition } from '../.././addedit.animation';

@Component({
	templateUrl: './templates/add_users.html',
	providers: [UserService, Global],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class UserAddEditComponent implements OnInit, OnDestroy {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public rolelist: any;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public ip_address: any;
	public warehouse_list:any = [];
	constructor(
		private _userService: UserService, 
		public _globalService: GlobalService, 
		private _router: Router,
		private global : Global,
		private _route: ActivatedRoute
	) {
		this.ip_address = (this._globalService.getCookie('ipaddress'))?this._globalService.getCookie('ipaddress'):'';
	}
	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.sub = this._route.params.subscribe(params => {
			this.formModel.userId = +params['id']; // (+) converts string 'id' to a number
		});

		let websiteId = this._globalService.getWebsiteId();
        this.global.warehouseLoad(websiteId, this._globalService.getUserId()).subscribe(
            data => {
                this.warehouse_list = data.warehouse;
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );

		this._userService.userLoad(this.formModel.userId).subscribe(data => {
			this.response = data;
			if (this.formModel.userId > 0) {
				this.formModel.userId = this.response.api_status.id;
				this.formModel.empName = this.response.api_status.employee_name;
				this.formModel.empDesignation = this.response.api_status.designation;
				this.formModel.empEmail = this.response.api_status.email;
				this.formModel.empPhone = this.response.api_status.phone;
				this.formModel.empUsername = this.response.api_status.username;
				this.formModel.warehouse_id = this.response.api_status.warehouse_id;
				this.formModel.status = this.response.api_status.isblocked;
				if (this.response.api_status.reset_password == 'n') {
					this.formModel.empPasswordReset = false;
				} else {
					this.formModel.empPasswordReset = true;
				}
				this.rolelist = this.response.role;
				this.formModel.role = this.response.api_status.role.id;
			} else {
				this.rolelist = this.response;
				this.formModel.userId = 0;
				this.formModel.status = 'n';
			}
		}, err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		}, function() {
			//completed callback
		});
	}
	ngOnDestroy() {
		this.sub.unsubscribe();
	}
	addEditUser(form: any) {
		this.errorMsg = '';
		var data: any = {};
		var employee: string = this.formModel.empName.split(" ");
		data.first_name = employee[0];
		if (employee[1]) {
			data.last_name = employee[1];
		} else {
			data.last_name = '';
		}
		data.ip_address = this.ip_address;
		data.employee_name = this.formModel.empName;
		data.designation = this.formModel.empDesignation;
		if (this.formModel.empPassword != '' && this.formModel.empPassword != undefined) {
			data.password = this.formModel.empPassword;
		} else {
			data.password = '';
		}
		data.email = this.formModel.empEmail;
		data.phone = this.formModel.empPhone;
		data.username = this.formModel.empUsername;
		data.warehouse_id = this.formModel.warehouse_id;
		if (this.formModel.empPasswordReset) {
			data.reset_password = 'y';
		} else {
			data.reset_password = 'n';
		}
		if (this.formModel.empPasswordSend) {
			data.send_password = 1;
		} else {
			data.send_password = 0;
		}
		data.role_id = this.formModel.role;
		data.isblocked = this.formModel.status;
		if (this.formModel.userId < 1) {
			data.createdby_id = this._globalService.getUserId();
		}
		data.modifiedby_id = this._globalService.getUserId();
		data.website_id = this._globalService.getWebsiteId();
		this._userService.userAddEdit(data, this.formModel.userId).subscribe(data => {
			this.response = data;
			if (this.response.status == 1) {
				this._router.navigate(['/users']);
				this._globalService.deleteTab(this.tabIndex, this.parentId);
			} else {
				this.errorMsg = this.response.message;
			}
		}, err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		}, function() {
			//completed callback
		});
	}
}