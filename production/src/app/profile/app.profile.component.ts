import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material';
import { UserService } from '../employee/user/employee.user.service';
import { HeaderService } from '../partial-component/app.header.service';
import { GlobalService } from '../global/service/app.global.service';
@Component({
  templateUrl: './templates/edit_profile.html',
  providers: [UserService]
})
export class AccountDetailsComponent implements OnInit { 
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public rolelist: any;
	public formModel: any = {};
	constructor(
		private dialogRef: MatDialogRef<AccountDetailsComponent>,
		private _userService:UserService,
		private _globalService:GlobalService,
	) {}
	ngOnInit(){
		this.formModel.userId = this._globalService.getUserId();
		this._userService.userLoad(this.formModel.userId).subscribe(
	       	data => {
	       		this.response = data;
	       		if(this.formModel.userId>0){
	       			this.formModel.userId = this.response.api_status.id;
		            this.formModel.empName = this.response.api_status.employee_name;
		            this.formModel.empDesignation = this.response.api_status.designation;
		            this.formModel.empEmail = this.response.api_status.email;
		            this.formModel.empPhone = this.response.api_status.phone;
		            this.formModel.empUsername = this.response.api_status.username;
		            this.formModel.status = this.response.api_status.isblocked;
		            if(this.response.api_status.reset_password=='n'){
		            	this.formModel.empPasswordReset = false;
		            }else{
		            	this.formModel.empPasswordReset = true;
		            }
		            
		            this.rolelist = this.response.role;
		            this.formModel.role = this.response.api_status.role.id;
	       		}else{
	       			this.rolelist = this.response;
	       			this.formModel.userId = 0;
	       		}
	       	},
	       	err => console.log(err),
	       	function(){
	       		//completed callback
	       	}
	    );
	}

    addEditUser(form: any){
    	this.errorMsg = '';
    	var data: any = {};
        var employee: string = this.formModel.empName.split(" ");
      	data.first_name = employee[0];
     	data.last_name = employee[1];
     	if(employee[1]){
     		data.last_name = employee[1];
     	}else{
     		data.last_name = '';
     	}
      	data.employee_name = this.formModel.empName;
      	data.designation = this.formModel.empDesignation;
      	data.password = '';  
      	data.email = this.formModel.empEmail;
      	data.role_id = this.formModel.role;
      	data.phone = this.formModel.empPhone;
      	data.username = this.formModel.empUsername;

        this._userService.userAddEdit(data,this.formModel.userId).subscribe(
           	resData => {
               	this.response = resData;
              
               	if(this.response.status==1){
               		this._globalService.updateUserCookie(data);
					this.closeDialog();
					this._globalService.showToast(this.response.message);
               	}else{
                   
                   this.errorMsg = this.response.message;
               	}
            },
           	err => console.log(err),
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
  templateUrl: './templates/edit_profile_password.html',
  providers: [HeaderService]
})
export class PasswordUpdateComponent implements OnInit { 
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	constructor(
		private dialogRef: MatDialogRef<PasswordUpdateComponent>,
		private _headerService:HeaderService,
		private _globalService:GlobalService,
	) {}

	ngOnInit(){
		this.formModel.userId = this._globalService.getUserId();	
	}

    UpdatePassword(form: any){
    	this.errorMsg = '';
    	var data: any = {};
	    data.old_password = this.formModel.currentPassword;
     	data.new_password = this.formModel.newPassword;
        this._headerService.updatePassword(data,this.formModel.userId).subscribe(
           	resData => {
               	this.response = resData;
               	if(this.response.status==1){
               		this.closeDialog();
               		this._globalService.showToast(this.response.message);
               	} else {
                   this.errorMsg = this.response.message;
               	}
            },
           	err => console.log(err),
           	function(){
                //completed callback
           	}
        );
	}

	closeDialog(){
		this.dialogRef.close();
	}
}
